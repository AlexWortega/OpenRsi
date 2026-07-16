/**
 * OpenRSI generational loop retargeted to KernelBench (fast_p / speedup).
 * Same propose -> critique -> eval survivors -> verify -> keep cycle as the ALE loop,
 * with a CUDA-kernel scaffold, kernel eval on the GPU, and fitness = mean speedup.
 *
 *   PYTHONPATH-less; run on the GPU pod:
 *   OPENRSI_KB_PROBLEMS="2:40,2:15" node --env-file=.env dist/kernelRsiLoop.js
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
import { KernelEvalServer } from "./kernel/evalClient.js";
import { solveKernel } from "./kernel/solve.js";
import { fastPSweep, formatSweep, kernelFitness } from "./kernel/fastp.js";
import { checkGoalProgress, formatVerdict, writeGoalPlan, type GoalPlan, type GoalVerdict } from "./goal/plan.js";

const RUN_DIR = process.env.OPENRSI_RUN_DIR || fileURLToPath(new URL("../runs/kernel", import.meta.url));
const SCAFFOLD = process.env.OPENRSI_KB_SCAFFOLD || fileURLToPath(new URL("../agent/kernel/scaffold.json", import.meta.url));

const KERNEL_OUTER_SYSTEM = `You are an AI systems researcher running a recursive-self-improvement loop. You improve the CODE (SCAFFOLD: system prompt + domain-knowledge tips + eval budget) of an inner solver agent that writes CUDA/GPU kernels for KernelBench. The solver writes a \`ModelNew\` that replaces the torch reference operators with a custom kernel; it is scored by SPEEDUP over the torch reference, gated on numerical correctness (an incorrect kernel scores 0).

Propose ONE scaffold rewrite that raises mean speedup while keeping kernels correct. You cannot see the held-out problems; propose changes that improve genuine kernel quality (not harness exploits — reward-hacked kernels are flagged and rejected). High-leverage directions: correctness-first robustness, operator fusion, memory coalescing / shared memory / register tiling, launch-config (block/grid) tuning, raw-CUDA vs Triton, fast-math flags where tolerance allows, and using the full eval budget to profile+optimize.

Think-first (required): mechanism, expected_delta, falsification.`;

const KERNEL_ANGLES = [
  "correctness & robustness: always compile and match the reference before optimizing",
  "operator fusion: fuse the reference ops into a single kernel to cut memory round-trips",
  "memory optimization: coalesced global access, shared memory, register tiling",
  "launch configuration: block/grid sizing, occupancy, fewer kernel launches",
  "kernel backend: raw CUDA vs Triton; fast-math / -O3 flags where tolerance allows",
  "eval-budget usage: iterate the full budget, profile and target the slowest op",
];

function parseProblem(s: string): { level: number; problemId: number } {
  const [l, p] = s.split(":").map((x) => parseInt(x.trim(), 10));
  return { level: l, problemId: p };
}
// Fitness = fast_p (fraction correct AND speedup >= p; default p=1.0) unless
// OPENRSI_KB_FITNESS=mean. See src/kernel/fastp.ts.
const meanPerf = kernelFitness;
const meanSpeedup = (rs: SolveResult[]): number => (rs.length ? rs.reduce((a, r) => a + (r.performance ?? 0), 0) / rs.length : 0);
function toPerProblem(rs: SolveResult[]) {
  return rs.map((r) => ({ problemId: r.problemId, performance: r.performance, rank: r.rank, valid: r.bestValid, evalsUsed: r.evalsUsed }));
}
function readFeedback(dir: string): string {
  const p = join(dir, "FEEDBACK.md");
  try { return existsSync(p) ? readFileSync(p, "utf8") : ""; } catch { return ""; }
}

async function evalScaffold(server: KernelEvalServer, scaffold: Scaffold, problems: string[], model: any): Promise<SolveResult[]> {
  const out: SolveResult[] = [];
  for (const ps of problems) {
    const { level, problemId } = parseProblem(ps);
    const r = await solveKernel({ server, level, problemId, scaffold, model });
    console.error(`[kb-rsi] ${r.problemId} v${scaffold.version}: speedup=${(r.performance ?? 0).toFixed(3)} correct=${r.bestValid} evals=${r.evalsUsed} $${r.cost.toFixed(3)}${r.error ? " ERR=" + r.error : ""}`);
    out.push(r);
  }
  return out;
}

async function main() {
  assertKey();
  const problems = (process.env.OPENRSI_KB_PROBLEMS || "2:40,2:15").split(",").map((s) => s.trim()).filter(Boolean);
  const heldRaw = process.env.OPENRSI_KB_HELDOUT ?? "2:33";
  const heldout = heldRaw.split(",").map((s) => s.trim()).filter(Boolean);
  const generations = Number(process.env.OPENRSI_GENERATIONS || 8);
  const stagnationLimit = Number(process.env.OPENRSI_STAGNATION || 9999);
  const numProposals = Number(process.env.OPENRSI_PROPOSALS || 5);
  const numCritics = Number(process.env.OPENRSI_CRITICS || 3);
  const numSurvivors = Number(process.env.OPENRSI_SURVIVORS || 2);

  const innerModel = tierModel("inner");
  const outerModel = tierModel("outer");
  console.error(`[kb-rsi] inner=${modelSlug("inner")} outer=${modelSlug("outer")} problems=${problems.join(",")} heldout=${heldout.join(",")} gens=${generations} propose=${numProposals} survivors=${numSurvivors}`);

  const board = new Board(RUN_DIR);
  const variantsDir = join(RUN_DIR, "variants");
  mkdirSync(variantsDir, { recursive: true });
  const server = new KernelEvalServer();
  await server.start();

  const metricLabel = (process.env.OPENRSI_KB_FITNESS ?? "fast_p").toLowerCase() === "mean" ? "mean speedup" : `fast_p@${process.env.OPENRSI_KB_FASTP_P || "1.0"}`;
  const goalStop = (process.env.OPENRSI_GOAL_STOP ?? "off") === "on";

  let totalCost = 0;
  try {
    let champion = loadScaffold(SCAFFOLD);

    // ---- goal plan (grok-build): gating criteria from the first reference kernel ----
    let goalPlan: GoalPlan | null = null;
    try {
      const first = parseProblem(problems[0]);
      const probe = await server.openSession(first.level, first.problemId);
      goalPlan = await writeGoalPlan({
        model: outerModel,
        objective: `Maximize ${metricLabel} across KernelBench problems [${problems.join(", ")}] (correct kernels only)`,
        metric: metricLabel,
        taskText: probe.ref_src,
      });
      writeFileSync(join(RUN_DIR, "goal_plan.json"), JSON.stringify(goalPlan, null, 2) + "\n");
      console.error(`[kb-rsi] goal plan: ${goalPlan.criteria.length} gating criteria`);
    } catch (e: any) {
      console.error(`[kb-rsi] goal plan skipped: ${e?.message || e}`);
    }
    const fitnessHistory: number[] = [];

    let t0 = Date.now();
    let championResults = await evalScaffold(server, champion, problems, innerModel);
    let championFitness = meanPerf(championResults);
    const baselineFitness = championFitness;
    fitnessHistory.push(championFitness);
    totalCost += championResults.reduce((a, r) => a + r.cost, 0);
    board.append({ gen: 0, scaffoldVersion: 0, fitness: championFitness, accepted: true, champion: true, rationale: "baseline CUDA scaffold (no RSI)", perProblem: toPerProblem(championResults), cost: championResults.reduce((a, r) => a + r.cost, 0), seconds: Math.round((Date.now() - t0) / 1000), fastP: fastPSweep(championResults), metricLabel });
    console.error(`[kb-rsi] gen0 baseline ${metricLabel}=${championFitness.toFixed(3)} (${formatSweep(championResults)}, meanSpeedup=${meanSpeedup(championResults).toFixed(3)}x)`);

    const history: AttemptRecord[] = [];
    let stagnation = 0;

    for (let gen = 1; gen <= generations; gen++) {
      t0 = Date.now();
      const humanFeedback = readFeedback(RUN_DIR);

      let goalVerdict: GoalVerdict | undefined;
      if (goalPlan) {
        goalVerdict = await checkGoalProgress({
          model: outerModel, plan: goalPlan, baselineFitness, championFitness, fitnessHistory,
          perProblem: championResults.map((r) => ({ problemId: r.problemId, fitness: r.performance, valid: r.bestValid })),
        });
        console.error(`[kb-rsi] gen${gen}: goal ${formatVerdict(goalVerdict)} steer="${goalVerdict.steer.slice(0, 80)}"`);
      }
      const feedback = [humanFeedback.trim(), goalVerdict ? `Goal-checker steer: ${goalVerdict.steer}` : ""].filter(Boolean).join("\n\n");

      const proposals = await proposeVariants({
        model: outerModel, champion, championResults, championFitness, history, feedback,
        count: numProposals, genOffset: gen - 1, angles: KERNEL_ANGLES,
        outerSystem: KERNEL_OUTER_SYSTEM, metricLabel,
      });
      totalCost += proposals.reduce((a, p) => a + p.cost, 0);
      const survivors = await critiquePanel({ model: outerModel, proposals, championFitness, history, critics: numCritics, survivors: numSurvivors });
      console.error(`[kb-rsi] gen${gen}: proposed ${proposals.length}, ${survivors.length} survived critique`);

      proposals.forEach((p, i) => {
        const cr = survivors.find((s) => s.proposal === p);
        writeFileSync(join(variantsDir, `gen${gen}_v${i}.json`), JSON.stringify({ gen, variant: i, angle: p.hint.split(":")[0], mechanism: p.mechanism, expected_delta: p.expectedDelta, rationale: p.rationale, survived: !!cr, scaffold: p.candidate }, null, 2) + "\n");
        appendFileSync(join(RUN_DIR, "VARIANTS.md"), `- gen${gen} v${i} [${p.hint.split(":")[0]}] critique=${cr ? cr.meanQuality.toFixed(1) + " SURVIVED" : "pruned"}: ${p.rationale.slice(0, 100)}\n`);
      });

      const evals = [];
      for (const s of survivors) {
        const c = s.proposal.candidate!;
        const results = await evalScaffold(server, c, problems, innerModel);
        totalCost += results.reduce((a, r) => a + r.cost, 0);
        evals.push({ candidate: c, rationale: s.proposal.rationale, results, fitness: meanPerf(results) });
      }
      if (!evals.length) { stagnation++; if (stagnation >= stagnationLimit) break; continue; }
      const best = evals.reduce((a, b) => (b.fitness > a.fitness ? b : a));

      let accepted = best.fitness > championFitness;
      let recorded = best.fitness;
      let recordedResults = best.results;
      if (accepted) {
        const verify = await evalScaffold(server, best.candidate, problems, innerModel);
        totalCost += verify.reduce((a, r) => a + r.cost, 0);
        recorded = (best.fitness + meanPerf(verify)) / 2;
        recordedResults = meanPerf(verify) >= best.fitness ? best.results : verify;
        accepted = recorded > championFitness;
        console.error(`[kb-rsi] gen${gen}: verify avg=${recorded.toFixed(3)} vs champ ${championFitness.toFixed(3)} -> ${accepted ? "CONFIRMED" : "rejected"}`);
      }

      history.push({ gen, rationale: best.rationale, fitness: recorded, accepted });
      board.append({ gen, scaffoldVersion: best.candidate.version, fitness: recorded, accepted, champion: accepted, rationale: `[survived critique] ${best.rationale}`, perProblem: toPerProblem(best.results), cost: evals.reduce((a, e) => a + e.results.reduce((s, r) => s + r.cost, 0), 0), seconds: Math.round((Date.now() - t0) / 1000), fastP: fastPSweep(recordedResults), goal: goalVerdict, metricLabel });

      if (accepted) {
        const prev = championFitness;
        champion = best.candidate; championResults = best.results; championFitness = recorded;
        fitnessHistory.push(recorded);
        writeFileSync(join(RUN_DIR, "champion_scaffold.json"), JSON.stringify(champion, null, 2) + "\n");
        stagnation = 0;
        console.error(`[kb-rsi] gen${gen}: ACCEPTED champion ${metricLabel}=${recorded.toFixed(3)} (was ${prev.toFixed(3)}; ${formatSweep(best.results)})`);
      } else {
        stagnation++;
        console.error(`[kb-rsi] gen${gen}: champion holds ${championFitness.toFixed(3)} (best ${best.fitness.toFixed(3)})`);
        if (stagnation >= stagnationLimit) break;
      }

      if (goalStop && goalVerdict?.achieved) { console.error(`[kb-rsi] gen${gen}: goal ACHIEVED — stopping early (OPENRSI_GOAL_STOP=on).`); break; }
    }

    let heldResults: SolveResult[] = [];
    if (heldout.length) heldResults = await evalScaffold(server, champion, heldout, innerModel);
    const lines = [
      "# OpenRSI KernelBench results", "",
      `Champion scaffold v${champion.version} on [${problems.join(", ")}]:`,
      `- **${metricLabel} = ${championFitness.toFixed(3)}** (fitness the loop selected on)`,
      `- fast_p sweep: ${formatSweep(championResults)}`,
      `- mean speedup: ${meanSpeedup(championResults).toFixed(3)}x`, "",
      "## Held-out verification",
      heldResults.length ? `fast_p sweep: ${formatSweep(heldResults)}` : "(none)",
      ...heldResults.map((r) => `- ${r.problemId}: speedup=${(r.performance ?? 0).toFixed(3)}x correct=${r.bestValid}`), "",
      `Total OpenRouter cost: $${totalCost.toFixed(2)}`, "",
      "## Champion domain knowledge", ...champion.domain_knowledge.map((d) => `- ${d}`),
    ];
    writeFileSync(join(RUN_DIR, "RESULTS.md"), lines.join("\n") + "\n");
    console.error(`[kb-rsi] DONE champion speedup=${championFitness.toFixed(3)}x cost=$${totalCost.toFixed(2)}`);
  } finally {
    await server.stop();
  }
  process.exit(0);
}

main().catch((e) => { console.error("[kb-rsi] FATAL:", e?.stack || e); process.exit(1); });
