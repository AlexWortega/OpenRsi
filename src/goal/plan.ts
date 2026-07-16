/**
 * Goal plan + direction checker — adopted from xai-org/grok-build's
 * `goal_planner_prompt.md`.
 *
 * At gen-0 we convert the benchmark objective into a SMALL set (3-5) of gating
 * criteria: numbered, atomic, observable, anchored literally to the objective, no
 * invented scope. Each generation the outer loop then asks a checker whether the
 * champion (a) has ACHIEVED the goal (all criteria hold) and (b) is going in the
 * RIGHT DIRECTION (trajectory improving), returning a short `steer` note that is fed
 * back into the parallel-hypothesis proposer as auto-feedback.
 *
 * This complements the existing search (proposeVariants/critiquePanel): the panel
 * generates & prunes hypotheses; the goal plan says whether the whole loop is on
 * track and when it can stop.
 */
import { Type } from "typebox";
import { createAgentSession, defineTool, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";

export interface GoalCriterion {
  id: number;
  outcome: string; // the observable outcome the objective demands
  observe: string; // how to check it (what to run / measure)
}

export interface GoalPlan {
  objective: string;
  metric: string;
  criteria: GoalCriterion[];
}

export interface GoalVerdict {
  achieved: boolean; // all criteria hold
  onTrack: boolean; // trajectory is heading the right way
  holding: number[]; // criterion ids believed to hold
  failing: number[]; // criterion ids not yet met
  steer: string; // one-paragraph steer for the next generation
}

/** Goal Plan Writer: run ONCE at goal creation to define the gating criteria. */
export async function writeGoalPlan(opts: {
  model: Model<any>;
  objective: string; // e.g. "maximize mean AtCoder performance on ahc008,ahc011"
  metric: string; // e.g. "mean private performance (0..3500)"
  taskText: string; // representative problem statement / reference source
}): Promise<GoalPlan> {
  const captured: { plan: GoalPlan | null } = { plan: null };
  const writePlan = defineTool({
    name: "write_goal_plan",
    label: "write_goal_plan",
    description: "Record the gating criteria for this goal. Keep it SMALL (3-5) and satisficing: every criterion must hold to pass.",
    parameters: Type.Object({
      criteria: Type.Array(
        Type.Object({
          outcome: Type.String({ description: "One observable outcome the objective literally demands." }),
          observe: Type.String({ description: "How to observe/measure it (what to run or read)." }),
        }),
        { minItems: 3, maxItems: 5 },
      ),
    }),
    async execute(_id, args) {
      captured.plan = {
        objective: opts.objective,
        metric: opts.metric,
        criteria: args.criteria.map((c, i) => ({ id: i + 1, outcome: c.outcome, observe: c.observe })),
      };
      return { content: [{ type: "text" as const, text: "recorded" }], details: undefined };
    },
  });

  const sys = `You are the Goal Plan Writer for a recursive-self-improvement harness. You run ONCE at goal creation and convert the objective into the single source of truth for "what was supposed to happen".

Write 3-5 GATING criteria. Rules (from the grok-build goal planner):
- Numbered, concrete, ONE outcome each, anchored to the LITERAL objective. Do NOT invent scope.
- Each must be independently checkable (verifiable in isolation), observable from real evaluation output — never from a mock or re-implementation.
- Keep it SMALL and satisficing: every criterion must hold to pass, so do not pad.
- Preserve the objective's must-have terms verbatim; never swap a named metric for a proxy.
Call write_goal_plan once, then reply DONE.`;
  const user = `Objective: ${opts.objective}
Fitness metric: ${opts.metric}

Representative task (for grounding the criteria):
"""
${opts.taskText.slice(0, 4000)}
"""

Write the gating criteria now.`;

  try {
    const { session } = await createAgentSession({
      model: opts.model,
      thinkingLevel: "medium",
      customTools: [writePlan],
      noTools: "builtin",
      systemPrompt: sys,
      sessionManager: SessionManager.inMemory(process.cwd()),
    } as any);
    await Promise.race([
      (async () => { await session.prompt(user); await session.waitForIdle(); })(),
      new Promise<void>((r) => setTimeout(() => { session.abort().catch(() => {}); r(); }, 120000)),
    ]);
  } catch {
    /* fall through to fallback */
  }

  return (
    captured.plan ?? {
      objective: opts.objective,
      metric: opts.metric,
      criteria: [
        { id: 1, outcome: "Every problem produces a valid, correct submission (no zero-scoring failure).", observe: "eval reports valid/correct on all problems" },
        { id: 2, outcome: `${opts.metric} improves over the gen-0 baseline.`, observe: "champion fitness > baseline fitness" },
        { id: 3, outcome: "The improvement holds under a fresh re-evaluation (not variance).", observe: "adversarial verify confirms the gain" },
      ],
    }
  );
}

export interface ProgressPoint {
  problemId: string;
  fitness: number | null;
  valid: boolean;
}

/**
 * Direction checker: given the gating criteria, the champion's current per-problem
 * results and the fitness history, decide whether the goal is achieved and whether
 * the loop is trending the right way, plus a short steer for the next generation.
 */
export async function checkGoalProgress(opts: {
  model: Model<any>;
  plan: GoalPlan;
  baselineFitness: number;
  championFitness: number;
  fitnessHistory: number[]; // champion fitness per generation, oldest first
  perProblem: ProgressPoint[];
}): Promise<GoalVerdict> {
  // Cheap deterministic trend prior (no LLM needed for direction).
  const h = opts.fitnessHistory;
  const rising = h.length < 2 ? opts.championFitness >= opts.baselineFitness : h[h.length - 1] >= h[0];

  const captured: { v: GoalVerdict | null } = { v: null };
  const report = defineTool({
    name: "report_progress",
    label: "report_progress",
    description: "Report which gating criteria hold, whether the goal is achieved, whether the run is on track, and how to steer next.",
    parameters: Type.Object({
      holding: Type.Array(Type.Integer(), { description: "criterion ids that currently HOLD" }),
      failing: Type.Array(Type.Integer(), { description: "criterion ids NOT yet met" }),
      achieved: Type.Boolean({ description: "true iff ALL criteria hold" }),
      on_track: Type.Boolean({ description: "true if the trajectory is heading toward achieving the remaining criteria" }),
      steer: Type.String({ description: "One paragraph: the single highest-leverage focus for the next generation." }),
    }),
    async execute(_id, args) {
      captured.v = {
        achieved: args.achieved,
        onTrack: args.on_track,
        holding: args.holding,
        failing: args.failing,
        steer: args.steer,
      };
      return { content: [{ type: "text" as const, text: "recorded" }], details: undefined };
    },
  });

  const criteriaTxt = opts.plan.criteria.map((c) => `${c.id}. ${c.outcome}  [observe: ${c.observe}]`).join("\n");
  const ppTxt = opts.perProblem
    .map((p) => `- ${p.problemId}: fitness=${p.fitness ?? "FAIL"} valid=${p.valid}`)
    .join("\n");
  const trendTxt = h.length ? h.map((x) => x.toFixed(1)).join(" -> ") : "(no history yet)";

  const sys = `You are the direction verifier for a recursive-self-improvement loop. Judge ONLY from the observed evaluation results below — do not assume. Decide which gating criteria currently hold, whether the goal is fully achieved, whether the loop is on track, and give one concrete steer. Be strict: a criterion holds only if the results demonstrate it.`;
  const user = `Objective: ${opts.plan.objective}
Metric: ${opts.plan.metric}
Baseline fitness: ${opts.baselineFitness.toFixed(1)}   Champion fitness: ${opts.championFitness.toFixed(1)}
Fitness trajectory: ${trendTxt}

## Gating criteria
${criteriaTxt}

## Champion per-problem results
${ppTxt}

Call report_progress, then reply DONE.`;

  try {
    const { session } = await createAgentSession({
      model: opts.model,
      thinkingLevel: "low",
      customTools: [report],
      noTools: "builtin",
      systemPrompt: sys,
      sessionManager: SessionManager.inMemory(process.cwd()),
    } as any);
    await Promise.race([
      (async () => { await session.prompt(user); await session.waitForIdle(); })(),
      new Promise<void>((r) => setTimeout(() => { session.abort().catch(() => {}); r(); }, 90000)),
    ]);
  } catch {
    /* fall through */
  }

  if (captured.v) {
    // Blend the model's on_track with the deterministic trend prior (either can rescue).
    return { ...captured.v, onTrack: captured.v.onTrack || rising };
  }
  // Fallback: purely deterministic verdict.
  const allValid = opts.perProblem.every((p) => p.valid);
  return {
    achieved: false,
    onTrack: rising,
    holding: allValid ? [1] : [],
    failing: opts.plan.criteria.map((c) => c.id).filter((id) => !(allValid && id === 1)),
    steer: rising
      ? "Trajectory is positive; keep pushing the highest-leverage angle from the last accepted change."
      : "Fitness stalled — try a materially different angle (search strategy or algorithmic reframe), not a small tweak.",
  };
}

export function formatVerdict(v: GoalVerdict): string {
  return `achieved=${v.achieved} onTrack=${v.onTrack} holding=[${v.holding.join(",")}] failing=[${v.failing.join(",")}]`;
}
