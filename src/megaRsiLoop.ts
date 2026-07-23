/**
 * OpenRSI generational loop on KernelBench-Mega: the outer loop evolves the megakernel
 * writer's SCAFFOLD (bounded SkillOpt-style edits by default) across OPENRSI_GENERATIONS
 * generations, keeping a rewrite only if mean geomean decode speedup improves. Same
 * propose -> critique -> eval survivors -> verify -> keep cycle as the other loops, with
 * a mega inner solve (real pi coding agent) and fitness = geomean speedup.
 *
 *   OPENRSI_MEGA_DIR=/workspace/mega/benchmarks/mega/problems/02_kimi_linear_decode \
 *   OPENRSI_MEGA_SOLVE_S=2400 OPENRSI_GENERATIONS=6 OPENRSI_SURVIVORS=2 \
 *     node --env-file=.env dist/megaRsiLoop.js
 */
import { appendFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { Board } from "./board.js";
import { loadScaffold, type Scaffold } from "./inner/scaffold.js";
import type { SolveResult } from "./inner/solve.js";
import { type AttemptRecord } from "./outer/improve.js";
import { critiquePanel, proposeVariants } from "./outer/critique.js";
import { assertKey, modelSlug, tierModel } from "./provider.js";
import { solveMega } from "./mega/solveMega.js";

const RUN_DIR = process.env.OPENRSI_RUN_DIR || fileURLToPath(new URL("../runs/mega_rsi", import.meta.url));
const SCAFFOLD = process.env.OPENRSI_MEGA_SCAFFOLD || fileURLToPath(new URL("../agent/mega/scaffold.json", import.meta.url));
const BASE_DIR = process.env.OPENRSI_MEGA_DIR || "/workspace/mega/benchmarks/mega/problems/02_kimi_linear_decode";

const MEGA_OUTER_SYSTEM = `You are an AI systems researcher running a recursive-self-improvement loop. You improve the CODE (SCAFFOLD: system prompt + domain-knowledge tips) of an inner GPU-kernel-engineer agent that writes a fused single-launch Kimi-Linear W4A16 decode megakernel. It is scored by geomean decode speedup over baseline.py, gated on numerical correctness (an incorrect or non-fused kernel scores 0).

Propose ONE bounded improvement to the scaffold that raises mean speedup while keeping kernels correct + single-launch. High-leverage directions: int4 dequant-GEMV fusion that never materializes bf16 weights, coalesced weight streaming, shared-memory staging of group scales/zeros, block-size/occupancy tuning, keeping the best passing snapshot, and profiling before guessing. You cannot game the harness (an authenticity judge + correctness gate reject exploits).

Think-first (required): mechanism, expected_delta, falsification.`;

const MEGA_ANGLES = [
  "int4 dequant-GEMV fusion: unpack + per-group dequant inside the GEMV, stream int4 weights once, never materialize bf16",
  "single-launch fusion: fuse KDA+MLA layers, conv, state update, MoE router+experts, RMSNorms into one kernel launch",
  "memory: coalesced global weight access, shared-memory staging of scales/zeros, register-tiling to cut spills",
  "launch config: block sizes (multiples of 32), occupancy, grid shape for the decode step",
  "correctness-first robustness: reach check.py PASS reliably before optimizing; keep the best passing snapshot",
  "profiling discipline: profile the bottleneck (ncu/nsys/torch.profiler) before changing the kernel",
];

function meanPerf(rs: SolveResult[]): number {
  return rs.length ? rs.reduce((a, r) => a + (r.performance ?? 0), 0) / rs.length : 0;
}
function toPerProblem(rs: SolveResult[]) {
  return rs.map((r) => ({ problemId: r.problemId, performance: r.performance, rank: r.rank, valid: r.bestValid, evalsUsed: r.evalsUsed }));
}
function readFeedback(dir: string): string {
  const p = join(dir, "FEEDBACK.md");
  try { return existsSync(p) ? readFileSync(p, "utf8") : ""; } catch { return ""; }
}
async function evalScaffold(scaffold: Scaffold, model: any): Promise<SolveResult[]> {
  const r = await solveMega({ baseDir: BASE_DIR, scaffold, model });
  console.error(`[mega-rsi] eval v${scaffold.version}: geomean=${(r.performance ?? 0).toFixed(3)}x PASS=${r.bestValid} $${r.cost.toFixed(2)}${r.error ? " ERR=" + r.error : ""}`);
  return [r];
}

async function main() {
  assertKey();
  const generations = Number(process.env.OPENRSI_GENERATIONS || 6);
  const stagnationLimit = Number(process.env.OPENRSI_STAGNATION || 9999);
  const numProposals = Number(process.env.OPENRSI_PROPOSALS || 4);
  const numCritics = Number(process.env.OPENRSI_CRITICS || 3);
  const numSurvivors = Number(process.env.OPENRSI_SURVIVORS || 2);

  const innerModel = tierModel("outer"); // strongest model writes the megakernel (hard task)
  const outerModel = tierModel("outer");
  const board = new Board(RUN_DIR);
  const variantsDir = join(RUN_DIR, "variants");
  mkdirSync(variantsDir, { recursive: true });
  console.error(`[mega-rsi] model=${modelSlug("outer")} gens=${generations} propose=${numProposals} survivors=${numSurvivors} editMode=${process.env.OPENRSI_EDIT_MODE ?? "bounded"} solveS=${process.env.OPENRSI_MEGA_SOLVE_S || 2400}`);

  let totalCost = 0;
  let champion = loadScaffold(SCAFFOLD);
  let t0 = Date.now();
  let championResults = await evalScaffold(champion, innerModel);
  let championFitness = meanPerf(championResults);
  const baselineFitness = championFitness;
  totalCost += championResults.reduce((a, r) => a + r.cost, 0);
  board.append({ gen: 0, scaffoldVersion: 0, fitness: championFitness, accepted: true, champion: true, rationale: "baseline mega scaffold (no RSI)", perProblem: toPerProblem(championResults), cost: championResults.reduce((a, r) => a + r.cost, 0), seconds: Math.round((Date.now() - t0) / 1000), metricLabel: "geomean speedup" });
  // Persist the gen-0 kernel to the run dir so a PASSing solve's solution.py is NOT lost
  // when its temp workdir is cleaned (also covers GENERATIONS=0 single-solve runs).
  if (championResults[0]?.bestCode) writeFileSync(join(RUN_DIR, "solution_v0.py"), championResults[0].bestCode);
  console.error(`[mega-rsi] gen0 baseline geomean=${championFitness.toFixed(3)}x`);

  const history: AttemptRecord[] = [];
  let stagnation = 0;

  for (let gen = 1; gen <= generations; gen++) {
    t0 = Date.now();
    const feedback = readFeedback(RUN_DIR);
    const proposals = await proposeVariants({
      model: outerModel, champion, championResults, championFitness, history, feedback,
      count: numProposals, genOffset: gen - 1, angles: MEGA_ANGLES,
      outerSystem: MEGA_OUTER_SYSTEM, metricLabel: "geomean speedup",
    });
    totalCost += proposals.reduce((a, p) => a + p.cost, 0);
    const survivors = await critiquePanel({ model: outerModel, proposals, championFitness, history, critics: numCritics, survivors: numSurvivors });
    console.error(`[mega-rsi] gen${gen}: proposed ${proposals.length}, ${survivors.length} survived critique`);

    proposals.forEach((p, i) => {
      const cr = survivors.find((s) => s.proposal === p);
      writeFileSync(join(variantsDir, `gen${gen}_v${i}.json`), JSON.stringify({ gen, variant: i, angle: p.hint.split(":")[0], mechanism: p.mechanism, expected_delta: p.expectedDelta, rationale: p.rationale, survived: !!cr, scaffold: p.candidate }, null, 2) + "\n");
      appendFileSync(join(RUN_DIR, "VARIANTS.md"), `- gen${gen} v${i} [${p.hint.split(":")[0]}] critique=${cr ? cr.meanQuality.toFixed(1) + " SURVIVED" : "pruned"}: ${p.rationale.slice(0, 100)}\n`);
    });

    const evals: { candidate: Scaffold; rationale: string; results: SolveResult[]; fitness: number }[] = [];
    for (const s of survivors) {
      const c = s.proposal.candidate!;
      const results = await evalScaffold(c, innerModel);
      totalCost += results.reduce((a, r) => a + r.cost, 0);
      evals.push({ candidate: c, rationale: s.proposal.rationale, results, fitness: meanPerf(results) });
    }
    if (!evals.length) { stagnation++; if (stagnation >= stagnationLimit) break; continue; }
    const best = evals.reduce((a, b) => (b.fitness > a.fitness ? b : a));

    let accepted = best.fitness > championFitness;
    let recorded = best.fitness;
    if (accepted) {
      const verify = await evalScaffold(best.candidate, innerModel);
      totalCost += verify.reduce((a, r) => a + r.cost, 0);
      recorded = (best.fitness + meanPerf(verify)) / 2;
      accepted = recorded > championFitness;
      console.error(`[mega-rsi] gen${gen}: verify avg=${recorded.toFixed(3)}x vs champ ${championFitness.toFixed(3)}x -> ${accepted ? "CONFIRMED" : "rejected"}`);
    }

    history.push({ gen, rationale: best.rationale, fitness: recorded, accepted });
    board.append({ gen, scaffoldVersion: best.candidate.version, fitness: recorded, accepted, champion: accepted, rationale: `[survived critique] ${best.rationale}`, perProblem: toPerProblem(best.results), cost: evals.reduce((a, e) => a + e.results.reduce((s, r) => s + r.cost, 0), 0), seconds: Math.round((Date.now() - t0) / 1000), metricLabel: "geomean speedup" });

    if (accepted) {
      const prev = championFitness;
      champion = best.candidate; championResults = best.results; championFitness = recorded;
      writeFileSync(join(RUN_DIR, "champion_scaffold.json"), JSON.stringify(champion, null, 2) + "\n");
      if (best.results[0]?.bestCode) writeFileSync(join(RUN_DIR, "champion_solution.py"), best.results[0].bestCode);
      stagnation = 0;
      console.error(`[mega-rsi] gen${gen}: ACCEPTED champion geomean=${recorded.toFixed(3)}x (was ${prev.toFixed(3)}x)`);
    } else {
      stagnation++;
      console.error(`[mega-rsi] gen${gen}: champion holds ${championFitness.toFixed(3)}x (best ${best.fitness.toFixed(3)}x)`);
      if (stagnation >= stagnationLimit) break;
    }
  }

  const lines = [
    "# OpenRSI KernelBench-Mega (scaffold-RSI) results", "",
    `Champion scaffold v${champion.version}, mean geomean speedup: **${championFitness.toFixed(3)}x**`,
    `Baseline (gen0): ${baselineFitness.toFixed(3)}x  |  RSI delta: ${(championFitness - baselineFitness >= 0 ? "+" : "")}${(championFitness - baselineFitness).toFixed(3)}x`, "",
    `Edit mode: ${process.env.OPENRSI_EDIT_MODE ?? "bounded"}  |  per-solve budget: ${Number(process.env.OPENRSI_MEGA_SOLVE_S || 2400) / 60}min`,
    `Total OpenRouter cost: $${totalCost.toFixed(2)}`, "",
    "## Champion domain knowledge", ...champion.domain_knowledge.map((d) => `- ${d}`),
  ];
  writeFileSync(join(RUN_DIR, "RESULTS.md"), lines.join("\n") + "\n");
  console.error(`[mega-rsi] DONE champion geomean=${championFitness.toFixed(3)}x (baseline ${baselineFitness.toFixed(3)}x) cost=$${totalCost.toFixed(2)}`);
  process.exit(0);
}

main().catch((e) => { console.error("[mega-rsi] FATAL:", e?.stack || e); process.exit(1); });
