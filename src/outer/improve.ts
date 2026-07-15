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
}): Promise<ProposeResult> {
  const { model, champion, championResults, championFitness, history } = opts;
  const cap = opts.maxEvalCap ?? 10;

  const captured: { scaffold: Scaffold | null; rationale: string } = { scaffold: null, rationale: "" };

  const proposeTool = defineTool({
    name: "propose_scaffold",
    label: "propose_scaffold",
    description:
      "Submit ONE improved scaffold for the inner solver. Provide the FULL new scaffold (all fields). It will be evaluated on held-out private cases and kept only if mean performance improves.",
    parameters: Type.Object({
      rationale: Type.String({ description: "One-paragraph causal mechanism: why this raises private performance." }),
      system_prompt: Type.String({ description: "The full new solver system prompt." }),
      domain_knowledge: Type.Array(Type.String(), { description: "Bullet tips appended to the prompt. Grow/refine these." }),
      max_public_evals: Type.Integer({ description: `Public-eval budget per problem (1..${cap}).`, minimum: 1, maximum: cap }),
    }),
    async execute(_id, args) {
      captured.scaffold = {
        version: champion.version + 1,
        language: champion.language,
        max_public_evals: args.max_public_evals,
        system_prompt: args.system_prompt,
        domain_knowledge: args.domain_knowledge,
      };
      captured.rationale = args.rationale;
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

  const sys = `You are an expert AI systems researcher running a recursive-self-improvement loop. You improve the CODE of an inner "solver" agent that competes on AtCoder Heuristic Contest optimization problems. The solver's behaviour is fully determined by its SCAFFOLD: a system prompt, a list of domain-knowledge tips, and a public-eval budget.

Your job: propose ONE targeted rewrite of the scaffold that will raise the solver's mean PRIVATE performance (score on hidden test cases, 0..3500). You cannot see the private cases; overfitting to the public score will NOT survive selection, so propose changes that improve genuine solution quality and generalization.

High-leverage directions to consider (pick what the results motivate, don't do all):
- Search strategy: stronger local search / simulated annealing, better neighbourhoods, restarts.
- Time management: precise internal wall-clock timing to use the full time limit without TLE.
- Eval-budget usage: the solver often stops early — instruct it to use its whole budget to refine.
- Robustness: guarantee always-valid output (avoid WA/RE/TLE that zero a case).
- Domain knowledge: add concrete, correct AHC heuristics as tips.
Make a focused, mechanistically-justified change — not a vague rewrite.`;

  const user = `## Champion scaffold (v${champion.version}) — mean private performance = ${championFitness.toFixed(0)}
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
    cost: stats?.cost ?? 0,
  };
}
