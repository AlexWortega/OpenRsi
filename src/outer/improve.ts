/**
 * Outer RSI step: the self-improvement agent.
 *
 * A strong pi agent reads the current champion scaffold and its per-problem
 * results (including failures), then proposes ONE rewrite of the scaffold aimed at
 * raising mean PRIVATE performance. It returns a full candidate Scaffold via a
 * structured tool (no free-form file editing → the scaffold schema stays intact).
 *
 * Selection happens in the caller (rsiLoop): the candidate is evaluated on the
 * held-out private cases and kept only if it beats the champion — reproducing
 * AIDE²'s "select on a private score the inner agent cannot see".
 */
import { Type } from "typebox";
import { createAgentSession, defineTool, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";
import type { Scaffold } from "../inner/scaffold.js";
import type { SolveResult } from "../inner/solve.js";

export interface AttemptRecord {
  gen: number;
  rationale: string;
  fitness: number;
  accepted: boolean;
}

export interface ProposeResult {
  candidate: Scaffold | null;
  rationale: string;
  // Think-first protocol (from the autoresearch skill): every hypothesis must state its
  // causal mechanism, an expected numeric move, and a falsification condition.
  mechanism: string;
  expectedDelta: string;
  falsification: string;
  hint: string;
  cost: number;
}

function resultsDigest(results: SolveResult[]): string {
  return results
    .map(
      (r) =>
        `- ${r.problemId} (${r.scoreType}): performance=${r.performance ?? "FAIL"} rank=${r.rank ?? "-"} ` +
        `publicScore=${r.bestPublicScore ?? "-"} valid=${r.bestValid} evalsUsed=${r.evalsUsed}` +
        (r.error ? ` error=${r.error}` : ""),
    )
    .join("\n");
}

export async function proposeImprovement(opts: {
  model: Model<any>;
  champion: Scaffold;
  championResults: SolveResult[];
  championFitness: number;
  history: AttemptRecord[];
  maxEvalCap?: number;
  /** A distinct "angle" for this variant so a generation explores diverse rewrites. */
  variantHint?: string;
  /** Free-form human guidance (from FEEDBACK.md); the outer agent must honour it. */
  feedback?: string;
  /** Benchmark-specific outer system prompt (defaults to the ALE-Bench one). */
  outerSystem?: string;
  /** Metric label shown in prompts (default "private performance"). */
  metricLabel?: string;
}): Promise<ProposeResult> {
  const { model, champion, championResults, championFitness, history } = opts;
  const cap = opts.maxEvalCap ?? 10;
  const metricLabel = opts.metricLabel ?? "private performance";

  const captured: {
    scaffold: Scaffold | null;
    rationale: string;
    mechanism: string;
    expectedDelta: string;
    falsification: string;
  } = { scaffold: null, rationale: "", mechanism: "", expectedDelta: "", falsification: "" };

  // Preserve any existing per-genre knowledge unless the proposer overrides a bucket.
  const genreKeys = Object.keys(champion.domain_knowledge_by_genre ?? {});

  const proposeTool = defineTool({
    name: "propose_scaffold",
    label: "propose_scaffold",
    description:
      "Submit ONE improved scaffold for the inner solver. Provide the FULL new scaffold plus the think-first fields. It will be peer-critiqued, then (if it survives) evaluated on held-out private cases and kept only if mean performance improves.",
    parameters: Type.Object({
      mechanism: Type.String({ description: "Causal path A->B->C->metric: WHY this raises private performance." }),
      expected_delta: Type.String({ description: "Numeric estimate + direction, e.g. '+150 performance, ~12% relative'." }),
      falsification: Type.String({ description: "What result would disprove the mechanism." }),
      rationale: Type.String({ description: "One-paragraph summary of the change." }),
      system_prompt: Type.String({ description: "The full new solver system prompt." }),
      domain_knowledge: Type.Array(Type.String(), { description: "General bullet tips appended for EVERY problem. Grow/refine these." }),
      domain_knowledge_by_genre: Type.Optional(
        Type.Record(Type.String(), Type.Array(Type.String()), {
          description: `Optional per-genre tips (injected only for matching problems). Keys are genres${genreKeys.length ? " (existing: " + genreKeys.join(", ") + ")" : ""}. Omit to leave existing buckets unchanged.`,
        }),
      ),
      max_public_evals: Type.Integer({ description: `Public-eval budget per problem (1..${cap}).`, minimum: 1, maximum: cap }),
    }),
    async execute(_id, args) {
      // Merge: proposer-provided buckets override same-named ones; others are kept.
      const byGenre = { ...(champion.domain_knowledge_by_genre ?? {}), ...((args as any).domain_knowledge_by_genre ?? {}) };
      captured.scaffold = {
        version: champion.version + 1,
        language: champion.language,
        max_public_evals: args.max_public_evals,
        system_prompt: args.system_prompt,
        domain_knowledge: args.domain_knowledge,
        ...(Object.keys(byGenre).length ? { domain_knowledge_by_genre: byGenre } : {}),
      };
      captured.rationale = args.rationale;
      captured.mechanism = args.mechanism;
      captured.expectedDelta = args.expected_delta;
      captured.falsification = args.falsification;
      return {
        content: [{ type: "text" as const, text: "Scaffold proposal recorded. Reply DONE." }],
        details: undefined,
      };
    },
  });

  const histTxt = history.length
    ? history
        .map((h) => `- gen${h.gen}: fitness=${h.fitness.toFixed(0)} ${h.accepted ? "ACCEPTED" : "rejected"} — ${h.rationale}`)
        .join("\n")
    : "(none yet)";

  const sys = opts.outerSystem ?? `You are an expert AI systems researcher running a recursive-self-improvement loop. You improve the CODE of an inner "solver" agent that competes on AtCoder Heuristic Contest optimization problems. The solver's behaviour is fully determined by its SCAFFOLD: a system prompt, a list of domain-knowledge tips, and a public-eval budget.

Your job: propose ONE targeted rewrite of the scaffold that will raise the solver's mean PRIVATE performance (score on hidden test cases, 0..3500). You cannot see the private cases; overfitting to the public score will NOT survive selection, so propose changes that improve genuine solution quality and generalization.

High-leverage directions to consider (pick what the results motivate, don't do all):
- Search strategy: stronger local search / simulated annealing, better neighbourhoods, restarts.
- Time management: precise internal wall-clock timing to use the full time limit without TLE.
- Eval-budget usage: the solver often stops early — instruct it to use its whole budget to refine.
- Robustness: guarantee always-valid output (avoid WA/RE/TLE that zero a case).
- Domain knowledge: add concrete, correct AHC heuristics as tips.
Make a focused, mechanistically-justified change — not a vague rewrite.

Think-first protocol (required): before proposing, answer three questions and pass them in the tool —
(1) mechanism: the causal path from your change to higher performance; (2) expected_delta: a numeric
estimate + direction; (3) falsification: what result would prove the mechanism wrong. A proposal
without a concrete mechanism and expected size is a guess, not a hypothesis.`;

  const hintBlock = opts.variantHint
    ? `\n## Angle for THIS variant\nFocus your rewrite primarily on: **${opts.variantHint}**. Other variants this round cover other angles.\n`
    : "";
  const feedbackBlock = opts.feedback?.trim()
    ? `\n## Human feedback (HIGH PRIORITY — follow this)\n${opts.feedback.trim()}\n`
    : "";

  const user = `${feedbackBlock}${hintBlock}## Champion scaffold (v${champion.version}) — mean ${metricLabel} = ${championFitness.toFixed(0)}
max_public_evals=${champion.max_public_evals}
system_prompt:
"""
${champion.system_prompt}
"""
domain_knowledge:
${champion.domain_knowledge.map((d) => `- ${d}`).join("\n")}

## Champion's per-problem results
${resultsDigest(championResults)}

## History of attempts
${histTxt}

Propose ONE improved scaffold now via the propose_scaffold tool (include ALL fields), then reply DONE.`;

  const { session } = await createAgentSession({
    model,
    thinkingLevel: "medium",
    customTools: [proposeTool],
    noTools: "builtin",
    systemPrompt: sys,
    sessionManager: SessionManager.inMemory(process.cwd()),
  } as any);

  const timeoutMs = Number(process.env.OPENRSI_PROPOSE_TIMEOUT_S || 240) * 1000;
  try {
    const timer = new Promise<void>((resolve) =>
      setTimeout(() => {
        process.stderr.write(`[improve] WATCHDOG timeout after ${timeoutMs / 1000}s — aborting\n`);
        session.abort().catch(() => {});
        resolve();
      }, timeoutMs),
    );
    await Promise.race([(async () => { await session.prompt(user); await session.waitForIdle(); })(), timer]);
  } catch {
    /* fall through; captured may still be set */
  }
  const stats = session.getSessionStats() as any;
  return {
    candidate: captured.scaffold,
    rationale: captured.scaffold ? captured.rationale : "(no proposal captured)",
    mechanism: captured.mechanism,
    expectedDelta: captured.expectedDelta,
    falsification: captured.falsification,
    hint: opts.variantHint ?? "",
    cost: stats?.cost ?? 0,
  };
}
