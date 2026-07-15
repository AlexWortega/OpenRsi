/**
 * Peer-critique before compute (from the autoresearch skill).
 *
 * Each generation we PROPOSE many diverse variants cheaply (LLM only), a panel of
 * critic agents scores them on quality + novelty BEFORE any benchmark eval, and only
 * the top survivors are actually run on the benchmark. This spends GPU/eval budget on
 * the most promising, non-duplicate hypotheses instead of every guess.
 */
import { Type } from "typebox";
import { createAgentSession, defineTool, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";
import type { Scaffold } from "../inner/scaffold.js";
import type { SolveResult } from "../inner/solve.js";
import { proposeImprovement, type AttemptRecord, type ProposeResult } from "./improve.js";

const ANGLES = [
  "search strategy: stronger simulated annealing / local search, better neighbourhoods, restarts",
  "domain knowledge: concrete problem-specific AHC heuristics and construction ideas",
  "time & eval-budget management: use the full time limit and the full submit budget",
  "output robustness: guarantee always-valid output, avoid WA/RE/TLE that zero a case",
  "algorithmic reframe: a different high-level approach to the objective",
  "parameter tuning: temperature schedule, move-type mix, O(1) delta-eval data structures",
];

/** Propose P diverse variants concurrently (parallel proposer teams, distinct angles). */
export async function proposeVariants(opts: {
  model: Model<any>;
  champion: Scaffold;
  championResults: SolveResult[];
  championFitness: number;
  history: AttemptRecord[];
  feedback: string;
  count: number;
  genOffset: number;
}): Promise<ProposeResult[]> {
  const jobs = Array.from({ length: opts.count }, (_, k) =>
    proposeImprovement({
      model: opts.model,
      champion: opts.champion,
      championResults: opts.championResults,
      championFitness: opts.championFitness,
      history: opts.history,
      variantHint: ANGLES[(opts.genOffset + k) % ANGLES.length],
      feedback: opts.feedback,
    }).catch(() => null),
  );
  const res = await Promise.all(jobs);
  return res.filter((r): r is ProposeResult => !!r && !!r.candidate);
}

export interface Critique {
  proposal: ProposeResult;
  meanQuality: number;
  keepVotes: number;
  critics: number;
  reasons: string[];
}

/** A panel of C critics scores every proposal (0-10 quality + keep vote) before compute. */
export async function critiquePanel(opts: {
  model: Model<any>;
  proposals: ProposeResult[];
  championFitness: number;
  history: AttemptRecord[];
  critics: number;
  survivors: number;
}): Promise<Critique[]> {
  const { proposals } = opts;
  if (!proposals.length) return [];

  const listing = proposals
    .map(
      (p, i) =>
        `### Proposal ${i}\n- angle: ${p.hint.split(":")[0]}\n- mechanism: ${p.mechanism}\n- expected_delta: ${p.expectedDelta}\n- falsification: ${p.falsification}\n- rationale: ${p.rationale}`,
    )
    .join("\n\n");

  const triedTxt = opts.history.length
    ? opts.history.map((h) => `- ${h.rationale} (fitness ${h.fitness.toFixed(0)}, ${h.accepted ? "accepted" : "rejected"})`).join("\n")
    : "(none)";

  const runOneCritic = async (ci: number): Promise<Array<{ index: number; quality: number; keep: boolean; reason: string }>> => {
    const captured: { scores: any[] } = { scores: [] };
    const scoreTool = defineTool({
      name: "score_proposals",
      label: "score_proposals",
      description: "Score every proposal before any compute is spent.",
      parameters: Type.Object({
        scores: Type.Array(
          Type.Object({
            index: Type.Integer(),
            quality: Type.Integer({ description: "0-10: expected impact x plausibility of the mechanism", minimum: 0, maximum: 10 }),
            keep: Type.Boolean({ description: "true if worth spending eval budget on (novel + plausible)" }),
            reason: Type.String(),
          }),
        ),
      }),
      async execute(_id, args) {
        captured.scores = args.scores;
        return { content: [{ type: "text" as const, text: "recorded" }], details: undefined };
      },
    });
    const sys = `You are critic ${ci + 1} on a peer-review panel for a recursive-self-improvement loop. You judge proposed rewrites of a competitive-programming solver BEFORE any expensive benchmark eval is spent. Reward proposals with (a) a clear causal mechanism, (b) a realistic expected gain, and (c) novelty vs already-tried ideas. Penalise vague, duplicate, or overfit-to-public-score proposals. Be skeptical: most proposals should NOT all pass.`;
    const user = `Champion mean private performance: ${opts.championFitness.toFixed(0)}.

## Already tried\n${triedTxt}

## Proposals to score\n${listing}

Score EVERY proposal (index 0..${proposals.length - 1}) via score_proposals, then reply DONE.`;
    const { session } = await createAgentSession({
      model: opts.model,
      thinkingLevel: "low",
      customTools: [scoreTool],
      noTools: "builtin",
      systemPrompt: sys,
      sessionManager: SessionManager.inMemory(process.cwd()),
    } as any);
    try {
      await Promise.race([
        (async () => { await session.prompt(user); await session.waitForIdle(); })(),
        new Promise<void>((r) => setTimeout(() => { session.abort().catch(() => {}); r(); }, 120000)),
      ]);
    } catch { /* keep whatever was captured */ }
    return captured.scores;
  };

  const panels = await Promise.all(Array.from({ length: opts.critics }, (_, ci) => runOneCritic(ci)));

  const agg: Critique[] = proposals.map((p) => ({ proposal: p, meanQuality: 0, keepVotes: 0, critics: 0, reasons: [] }));
  for (const panel of panels) {
    for (const s of panel) {
      const a = agg[s.index];
      if (!a) continue;
      a.meanQuality += s.quality;
      a.keepVotes += s.keep ? 1 : 0;
      a.critics += 1;
      if (s.reason) a.reasons.push(s.reason);
    }
  }
  for (const a of agg) a.meanQuality = a.critics ? a.meanQuality / a.critics : 0;

  // Survivors: mean quality >= 6 AND majority keep vote; then top-K by quality.
  const survivors = agg
    .filter((a) => a.critics > 0 && a.meanQuality >= 6 && a.keepVotes * 2 >= a.critics)
    .sort((x, y) => y.meanQuality - x.meanQuality)
    .slice(0, opts.survivors);
  // Fallback: if the panel rejected everything, keep the single highest-scored so the gen isn't empty.
  if (!survivors.length) {
    const best = [...agg].sort((x, y) => y.meanQuality - x.meanQuality)[0];
    if (best && best.critics > 0) return [best];
  }
  return survivors;
}
