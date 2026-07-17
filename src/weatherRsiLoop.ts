/**
 * OpenRSI generational loop on WeatherBench-2: the base agent builds the best 72h
 * z500/t850 forecast model it can under a FIXED COMPUTE BUDGET; the outer RSI loop
 * evolves the solver scaffold for OPENRSI_GENERATIONS generations, keeping a rewrite
 * only if mean persistence-skill improves. Same propose -> critique -> eval survivors
 * -> verify -> keep cycle as the ALE/Kernel loops.
 *
 *   OPENRSI_GENERATIONS=10 OPENRSI_WB_TRAIN_S=120 OPENRSI_WB_GPU=3 \
 *     node --env-file=.env dist/weatherRsiLoop.js
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
import { WeatherEvalServer } from "./weather/evalClient.js";
import { solveWeather } from "./weather/solve.js";
import { checkGoalProgress, formatVerdict, writeGoalPlan, type GoalPlan, type GoalVerdict } from "./goal/plan.js";

const RUN_DIR = process.env.OPENRSI_RUN_DIR || fileURLToPath(new URL("../runs/weather", import.meta.url));
const SCAFFOLD = process.env.OPENRSI_WB_SCAFFOLD || fileURLToPath(new URL("../agent/weather/scaffold.json", import.meta.url));

const WEATHER_OUTER_SYSTEM = `You are an AI systems researcher running a recursive-self-improvement loop. You improve the CODE (SCAFFOLD: system prompt + domain-knowledge tips + submit budget) of an inner ML-researcher agent that builds a data-driven WeatherBench-2 forecast model (64x32 ERA5, predicting z500 + t850 at 72h) under a FIXED per-model compute budget. The model is scored by cos(lat)-weighted RMSE; fitness = persistence skill = 1 - mean(rmse/persistence), so higher is better and >0 beats persistence.

Propose ONE scaffold rewrite that raises mean skill. The compute budget per model is FIXED, so the leverage is in helping the inner agent spend it better: architecture choices (conv depth/width, U-Net, residual blocks, dilation/receptive field), residual-target + per-channel normalization, area-weighted loss, LR schedule + batch size to fill the budget, longitude-roll augmentation, mixed precision. You cannot see the test set; propose changes that improve genuine forecast skill, not harness exploits.

Think-first (required): mechanism, expected_delta, falsification.`;

const WEATHER_ANGLES = [
  "architecture: deeper/wider CNN, U-Net, residual blocks, dilated convs for a larger receptive field",
  "target & normalization: residual (Y-X) target, per-channel std normalization, output scaling",
  "loss design: cos(lat)-weighted MSE, per-channel balancing, gradient/spectral regularizers",
  "training schedule: optimizer, LR warmup/decay, batch size and steps to fully use the compute budget",
  "augmentation & regularization: longitude-roll augmentation, weight decay, dropout, early patience",
  "compute-budget usage: model size vs budget, mixed precision (amp) to fit more steps in the fixed time",
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

async function evalScaffold(server: WeatherEvalServer, scaffold: Scaffold, model: any): Promise<SolveResult[]> {
  const r = await solveWeather({ server, scaffold, model });
  console.error(`[wb-rsi] eval v${scaffold.version}: skill=${(r.performance ?? 0).toFixed(4)} valid=${r.bestValid} evals=${r.evalsUsed} $${r.cost.toFixed(3)}${r.error ? " ERR=" + r.error : ""} judge=${r.privateJudge ?? ""}`);
  return [r];
}

async function main() {
  assertKey();
  const generations = Number(process.env.OPENRSI_GENERATIONS || 10);
  const stagnationLimit = Number(process.env.OPENRSI_STAGNATION || 9999);
  const numProposals = Number(process.env.OPENRSI_PROPOSALS || 5);
  const numCritics = Number(process.env.OPENRSI_CRITICS || 3);
  const numSurvivors = Number(process.env.OPENRSI_SURVIVORS || 2);
  const goalStop = (process.env.OPENRSI_GOAL_STOP ?? "off") === "on";

  const innerModel = tierModel("inner");
  const outerModel = tierModel("outer");
  const server = new WeatherEvalServer();
  console.error(`[wb-rsi] inner=${modelSlug("inner")} outer=${modelSlug("outer")} gens=${generations} propose=${numProposals} survivors=${numSurvivors} trainBudget=${server.trainBudgetS}s`);

  const board = new Board(RUN_DIR);
  const variantsDir = join(RUN_DIR, "variants");
  mkdirSync(variantsDir, { recursive: true });

  let totalCost = 0;
  let champion = loadScaffold(SCAFFOLD);

  // ---- goal plan (grok-build) ----
  let goalPlan: GoalPlan | null = null;
  try {
    goalPlan = await writeGoalPlan({
      model: outerModel,
      objective: "Maximize persistence skill of a 72h z500/t850 WeatherBench-2 forecast model built under a fixed compute budget",
      metric: "persistence skill score (1 - mean(rmse/persistence); >0 beats persistence)",
      taskText: champion.system_prompt,
    });
    writeFileSync(join(RUN_DIR, "goal_plan.json"), JSON.stringify(goalPlan, null, 2) + "\n");
    console.error(`[wb-rsi] goal plan: ${goalPlan.criteria.length} gating criteria`);
  } catch (e: any) {
    console.error(`[wb-rsi] goal plan skipped: ${e?.message || e}`);
  }
  const fitnessHistory: number[] = [];

  let t0 = Date.now();
  let championResults = await evalScaffold(server, champion, innerModel);
  let championFitness = meanPerf(championResults);
  const baselineFitness = championFitness;
  fitnessHistory.push(championFitness);
  totalCost += championResults.reduce((a, r) => a + r.cost, 0);
  board.append({ gen: 0, scaffoldVersion: 0, fitness: championFitness, accepted: true, champion: true, rationale: "baseline weather scaffold (no RSI)", perProblem: toPerProblem(championResults), cost: championResults.reduce((a, r) => a + r.cost, 0), seconds: Math.round((Date.now() - t0) / 1000), metricLabel: "persistence skill" });
  console.error(`[wb-rsi] gen0 baseline skill=${championFitness.toFixed(4)}`);

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
      console.error(`[wb-rsi] gen${gen}: goal ${formatVerdict(goalVerdict)} steer="${goalVerdict.steer.slice(0, 80)}"`);
    }
    const feedback = [humanFeedback.trim(), goalVerdict ? `Goal-checker steer: ${goalVerdict.steer}` : ""].filter(Boolean).join("\n\n");

    const proposals = await proposeVariants({
      model: outerModel, champion, championResults, championFitness, history, feedback,
      count: numProposals, genOffset: gen - 1, angles: WEATHER_ANGLES,
      outerSystem: WEATHER_OUTER_SYSTEM, metricLabel: "persistence skill",
    });
    totalCost += proposals.reduce((a, p) => a + p.cost, 0);
    const survivors = await critiquePanel({ model: outerModel, proposals, championFitness, history, critics: numCritics, survivors: numSurvivors });
    console.error(`[wb-rsi] gen${gen}: proposed ${proposals.length}, ${survivors.length} survived critique`);

    proposals.forEach((p, i) => {
      const cr = survivors.find((s) => s.proposal === p);
      writeFileSync(join(variantsDir, `gen${gen}_v${i}.json`), JSON.stringify({ gen, variant: i, angle: p.hint.split(":")[0], mechanism: p.mechanism, expected_delta: p.expectedDelta, rationale: p.rationale, survived: !!cr, scaffold: p.candidate }, null, 2) + "\n");
      appendFileSync(join(RUN_DIR, "VARIANTS.md"), `- gen${gen} v${i} [${p.hint.split(":")[0]}] critique=${cr ? cr.meanQuality.toFixed(1) + " SURVIVED" : "pruned"}: ${p.rationale.slice(0, 100)}\n`);
    });

    const evals: { candidate: Scaffold; rationale: string; results: SolveResult[]; fitness: number }[] = [];
    for (const s of survivors) {
      const c = s.proposal.candidate!;
      const results = await evalScaffold(server, c, innerModel);
      totalCost += results.reduce((a, r) => a + r.cost, 0);
      evals.push({ candidate: c, rationale: s.proposal.rationale, results, fitness: meanPerf(results) });
    }
    if (!evals.length) { stagnation++; if (stagnation >= stagnationLimit) break; continue; }
    const best = evals.reduce((a, b) => (b.fitness > a.fitness ? b : a));

    let accepted = best.fitness > championFitness;
    let recorded = best.fitness;
    if (accepted) {
      const verify = await evalScaffold(server, best.candidate, innerModel);
      totalCost += verify.reduce((a, r) => a + r.cost, 0);
      recorded = (best.fitness + meanPerf(verify)) / 2;
      accepted = recorded > championFitness;
      console.error(`[wb-rsi] gen${gen}: verify avg=${recorded.toFixed(4)} vs champ ${championFitness.toFixed(4)} -> ${accepted ? "CONFIRMED" : "rejected"}`);
    }

    history.push({ gen, rationale: best.rationale, fitness: recorded, accepted });
    board.append({ gen, scaffoldVersion: best.candidate.version, fitness: recorded, accepted, champion: accepted, rationale: `[survived critique] ${best.rationale}`, perProblem: toPerProblem(best.results), cost: evals.reduce((a, e) => a + e.results.reduce((s, r) => s + r.cost, 0), 0), seconds: Math.round((Date.now() - t0) / 1000), goal: goalVerdict, metricLabel: "persistence skill" });

    if (accepted) {
      const prev = championFitness;
      champion = best.candidate; championResults = best.results; championFitness = recorded;
      fitnessHistory.push(recorded);
      writeFileSync(join(RUN_DIR, "champion_scaffold.json"), JSON.stringify(champion, null, 2) + "\n");
      stagnation = 0;
      console.error(`[wb-rsi] gen${gen}: ACCEPTED champion skill=${recorded.toFixed(4)} (was ${prev.toFixed(4)})`);
    } else {
      stagnation++;
      console.error(`[wb-rsi] gen${gen}: champion holds ${championFitness.toFixed(4)} (best ${best.fitness.toFixed(4)})`);
      if (stagnation >= stagnationLimit) break;
    }
    if (goalStop && goalVerdict?.achieved) { console.error(`[wb-rsi] gen${gen}: goal ACHIEVED — stopping early.`); break; }
  }

  const lines = [
    "# OpenRSI WeatherBench-2 results", "",
    `Champion scaffold v${champion.version}, mean persistence skill: **${championFitness.toFixed(4)}**`,
    `Baseline (gen0) skill: ${baselineFitness.toFixed(4)}  |  RSI delta: ${(championFitness - baselineFitness >= 0 ? "+" : "")}${(championFitness - baselineFitness).toFixed(4)}`, "",
    `Fixed compute budget: ${server.trainBudgetS}s / model on one V100.`,
    `Total OpenRouter cost: $${totalCost.toFixed(2)}`, "",
    "## Champion domain knowledge", ...champion.domain_knowledge.map((d) => `- ${d}`),
  ];
  writeFileSync(join(RUN_DIR, "RESULTS.md"), lines.join("\n") + "\n");
  console.error(`[wb-rsi] DONE champion skill=${championFitness.toFixed(4)} (baseline ${baselineFitness.toFixed(4)}) cost=$${totalCost.toFixed(2)}`);
  process.exit(0);
}

main().catch((e) => { console.error("[wb-rsi] FATAL:", e?.stack || e); process.exit(1); });
