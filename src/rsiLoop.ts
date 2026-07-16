/**
 * OpenRSI generational loop (AIDE² core): propose → evaluate on held-out private
 * cases → keep-if-better → checkpoint. The champion scaffold is the best-by-mean-
 * private-performance solver found so far.
 *
 *   node --env-file=.env dist/rsiLoop.js
 *
 * Env:
 *   OPENRSI_PROBLEMS   comma list, default "ahc008,ahc011"   (RSI fitness set)
 *   OPENRSI_HELDOUT    comma list, default "ahc015"          (final verification only)
 *   OPENRSI_GENERATIONS default 6
 *   OPENRSI_STAGNATION  default 3
 *   OPENRSI_NUM_WORKERS default 12
 */
import { appendFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { AleEvalServer } from "./ale/evalServer.js";
import { Board, type GenRecord } from "./board.js";
import { loadScaffold, type Scaffold } from "./inner/scaffold.js";
import { solveProblem, type SolveResult } from "./inner/solve.js";
import { type AttemptRecord } from "./outer/improve.js";
import { critiquePanel, proposeVariants } from "./outer/critique.js";
import { assertKey, modelSlug, tierModel } from "./provider.js";
import { checkGoalProgress, formatVerdict, writeGoalPlan, type GoalPlan, type GoalVerdict } from "./goal/plan.js";

/** Human guidance: re-read each generation so the user can steer the run live. */
function readFeedback(runDir: string): string {
  const p = join(runDir, "FEEDBACK.md");
  try {
    return existsSync(p) ? readFileSync(p, "utf8") : "";
  } catch {
    return "";
  }
}

const RUN_DIR = process.env.OPENRSI_RUN_DIR || fileURLToPath(new URL("../runs/openrsi", import.meta.url));

function meanPerformance(rs: SolveResult[]): number {
  if (!rs.length) return 0;
  return rs.reduce((a, r) => a + (r.performance ?? 0), 0) / rs.length;
}

async function evalScaffold(
  server: AleEvalServer,
  scaffold: Scaffold,
  problems: string[],
  model: any,
  numWorkers: number,
): Promise<SolveResult[]> {
  const out: SolveResult[] = [];
  for (const problemId of problems) {
    const r = await solveProblem({ evalServer: server, problemId, scaffold, model, numWorkers, lite: true });
    console.error(
      `[rsi] eval ${problemId} v${scaffold.version}: perf=${r.performance} valid=${r.bestValid} evals=${r.evalsUsed} $${r.cost.toFixed(3)}${r.error ? " ERR=" + r.error : ""}`,
    );
    out.push(r);
  }
  return out;
}

function toPerProblem(rs: SolveResult[]) {
  return rs.map((r) => ({
    problemId: r.problemId,
    performance: r.performance,
    rank: r.rank,
    valid: r.bestValid,
    evalsUsed: r.evalsUsed,
  }));
}

async function main() {
  assertKey();
  const problems = (process.env.OPENRSI_PROBLEMS || "ahc008,ahc011").split(",").map((s) => s.trim()).filter(Boolean);
  // Distinguish "unset" (use default) from "set empty" (no held-out).
  const heldoutRaw = process.env.OPENRSI_HELDOUT ?? "ahc015";
  const heldout = heldoutRaw.split(",").map((s) => s.trim()).filter(Boolean);
  const generations = Number(process.env.OPENRSI_GENERATIONS || 12);
  // Default: run ALL generations (no early stop). Set OPENRSI_STAGNATION to enable early stop.
  const stagnationLimit = Number(process.env.OPENRSI_STAGNATION || 9999);
  const numProposals = Number(process.env.OPENRSI_PROPOSALS || 5); // proposed cheaply per gen
  const numCritics = Number(process.env.OPENRSI_CRITICS || 3); // peer-critic panel size
  const numSurvivors = Number(process.env.OPENRSI_SURVIVORS || 2); // survivors actually evaluated
  const numWorkers = Number(process.env.OPENRSI_NUM_WORKERS || 12);
  const variantsDir = join(RUN_DIR, "variants");
  mkdirSync(variantsDir, { recursive: true });

  const innerModel = tierModel("inner");
  const outerModel = tierModel("outer");
  console.error(
    `[rsi] inner=${modelSlug("inner")} outer=${modelSlug("outer")} problems=${problems.join(",")} heldout=${heldout.join(",")} gens=${generations} propose=${numProposals} critics=${numCritics} survivors=${numSurvivors}`,
  );

  const board = new Board(RUN_DIR);
  const server = new AleEvalServer();
  await server.start();

  const goalStop = (process.env.OPENRSI_GOAL_STOP ?? "off") === "on";

  let totalCost = 0;
  try {
    // ---- goal plan (grok-build): define gating criteria ONCE, from a real statement ----
    let goalPlan: GoalPlan | null = null;
    try {
      const probe = await server.openSession({ problemId: problems[0], lite: true });
      goalPlan = await writeGoalPlan({
        model: outerModel,
        objective: `Maximize mean AtCoder private performance across [${problems.join(", ")}]`,
        metric: "mean private performance (0..3500)",
        taskText: probe.problem.statement ?? problems.join(", "),
      });
      await server.closeSession(probe.sessionId);
      writeFileSync(join(RUN_DIR, "goal_plan.json"), JSON.stringify(goalPlan, null, 2) + "\n");
      console.error(`[rsi] goal plan: ${goalPlan.criteria.length} gating criteria written to goal_plan.json`);
    } catch (e: any) {
      console.error(`[rsi] goal plan skipped: ${e?.message || e}`);
    }
    const fitnessHistory: number[] = [];

    // ---- gen 0: baseline (default scaffold) ----
    let champion = loadScaffold();
    let t0 = Date.now();
    let championResults = await evalScaffold(server, champion, problems, innerModel, numWorkers);
    let championFitness = meanPerformance(championResults);
    const baselineFitness = championFitness;
    fitnessHistory.push(championFitness);
    totalCost += championResults.reduce((a, r) => a + r.cost, 0);
    board.append({
      gen: 0,
      scaffoldVersion: champion.version,
      fitness: championFitness,
      accepted: true,
      champion: true,
      rationale: "baseline (default scaffold, no RSI)",
      perProblem: toPerProblem(championResults),
      cost: championResults.reduce((a, r) => a + r.cost, 0),
      seconds: Math.round((Date.now() - t0) / 1000),
    });
    console.error(`[rsi] gen0 baseline fitness=${championFitness.toFixed(1)}`);

    const history: AttemptRecord[] = [];
    let stagnation = 0;

    for (let gen = 1; gen <= generations; gen++) {
      t0 = Date.now();
      const humanFeedback = readFeedback(RUN_DIR);
      if (humanFeedback.trim()) console.error(`[rsi] gen${gen}: applying human feedback (${humanFeedback.trim().length} chars)`);

      // 0) GOAL CHECK (grok-build): is the champion achieving the goal / going the right way?
      let goalVerdict: GoalVerdict | undefined;
      if (goalPlan) {
        goalVerdict = await checkGoalProgress({
          model: outerModel, plan: goalPlan, baselineFitness, championFitness, fitnessHistory,
          perProblem: championResults.map((r) => ({ problemId: r.problemId, fitness: r.performance, valid: r.bestValid })),
        });
        console.error(`[rsi] gen${gen}: goal ${formatVerdict(goalVerdict)} steer="${goalVerdict.steer.slice(0, 80)}"`);
      }
      // Steer feeds the parallel-hypothesis proposer as auto-feedback (alongside human feedback).
      const feedback = [humanFeedback.trim(), goalVerdict ? `Goal-checker steer: ${goalVerdict.steer}` : ""].filter(Boolean).join("\n\n");

      // 1) PROPOSE many diverse variants in parallel (LLM only, cheap).
      const proposals = await proposeVariants({
        model: outerModel, champion, championResults, championFitness, history,
        feedback, count: numProposals, genOffset: gen - 1,
      });
      totalCost += proposals.reduce((a, p) => a + p.cost, 0);
      console.error(`[rsi] gen${gen}: proposed ${proposals.length}/${numProposals} variants`);

      // 2) PEER-CRITIQUE before any compute — only survivors get evaluated.
      const survivors = await critiquePanel({
        model: outerModel, proposals, championFitness, history,
        critics: numCritics, survivors: numSurvivors,
      });
      console.error(`[rsi] gen${gen}: ${survivors.length} survivor(s) after critique [${survivors.map((s) => s.meanQuality.toFixed(1)).join(",")}]`);

      // Save EVERY proposal (with critique score + survivor flag) for the user to inspect.
      proposals.forEach((p, i) => {
        const cr = survivors.find((s) => s.proposal === p);
        writeFileSync(
          join(variantsDir, `gen${gen}_v${i}.json`),
          JSON.stringify({ gen, variant: i, angle: p.hint.split(":")[0], mechanism: p.mechanism, expected_delta: p.expectedDelta, falsification: p.falsification, rationale: p.rationale, survived_critique: !!cr, scaffold: p.candidate }, null, 2) + "\n",
        );
        appendFileSync(join(RUN_DIR, "VARIANTS.md"),
          `- gen${gen} v${i} [${p.hint.split(":")[0]}] critique=${cr ? cr.meanQuality.toFixed(1) + " SURVIVED" : "pruned"}: ${p.rationale.slice(0, 100)} (variants/gen${gen}_v${i}.json)\n`);
      });

      // 3) EVALUATE survivors on the benchmark (compute spent only here).
      type Ev = { candidate: Scaffold; rationale: string; results: SolveResult[]; fitness: number };
      const evals: Ev[] = [];
      for (const s of survivors) {
        const c = s.proposal.candidate!;
        const results = await evalScaffold(server, c, problems, innerModel, numWorkers);
        totalCost += results.reduce((a, r) => a + r.cost, 0);
        evals.push({ candidate: c, rationale: s.proposal.rationale, results, fitness: meanPerformance(results) });
      }
      if (!evals.length) { stagnation++; if (stagnation >= stagnationLimit) break; continue; }
      const best = evals.reduce((a, b) => (b.fitness > a.fitness ? b : a));

      // 4) ADVERSARIAL VERIFY: a candidate that beats the champion is re-evaluated
      // (fresh solve) to confirm the gain is real, not inner-agent variance.
      let accepted = best.fitness > championFitness;
      let recordedFitness = best.fitness;
      if (accepted) {
        const verify = await evalScaffold(server, best.candidate, problems, innerModel, numWorkers);
        totalCost += verify.reduce((a, r) => a + r.cost, 0);
        const verifyFitness = meanPerformance(verify);
        recordedFitness = (best.fitness + verifyFitness) / 2; // average of the two independent evals
        accepted = recordedFitness > championFitness;
        console.error(`[rsi] gen${gen}: verify best=${best.fitness.toFixed(1)} reeval=${verifyFitness.toFixed(1)} avg=${recordedFitness.toFixed(1)} vs champ ${championFitness.toFixed(1)} -> ${accepted ? "CONFIRMED" : "rejected (variance)"}`);
      }

      history.push({ gen, rationale: best.rationale, fitness: recordedFitness, accepted });
      board.append({
        gen, scaffoldVersion: best.candidate.version, fitness: recordedFitness, accepted, champion: accepted,
        rationale: `[survived critique, best of ${evals.length}] ${best.rationale}`,
        perProblem: toPerProblem(best.results),
        cost: evals.reduce((a, e) => a + e.results.reduce((s, r) => s + r.cost, 0), 0),
        seconds: Math.round((Date.now() - t0) / 1000),
        goal: goalVerdict,
        metricLabel: "mean private performance",
      });

      if (accepted) {
        const prevFitness = championFitness;
        champion = best.candidate; championResults = best.results; championFitness = recordedFitness;
        fitnessHistory.push(recordedFitness);
        writeFileSync(join(RUN_DIR, "champion_scaffold.json"), JSON.stringify(champion, null, 2) + "\n");
        stagnation = 0;
        console.error(`[rsi] gen${gen}: ACCEPTED champion fitness=${recordedFitness.toFixed(1)} (was ${prevFitness.toFixed(1)})`);
        const NOTIFY = process.env.HOME + "/.claude/skills/ml-intern/scripts/notify.sh";
        try {
          const { execFileSync } = await import("node:child_process");
          execFileSync("bash", [NOTIFY, "experiment_kept", `OpenRSI gen${gen} champion fitness=${recordedFitness.toFixed(0)}`], { stdio: "ignore" });
        } catch { /* notify optional */ }
      } else {
        stagnation++;
        console.error(`[rsi] gen${gen}: champion holds ${championFitness.toFixed(1)} (best ${best.fitness.toFixed(1)}); continuing`);
        if (stagnation >= stagnationLimit) { console.error(`[rsi] stagnation limit; stopping.`); break; }
      }

      if (goalStop && goalVerdict?.achieved) { console.error(`[rsi] gen${gen}: goal ACHIEVED — stopping early (OPENRSI_GOAL_STOP=on).`); break; }
    }

    // ---- final verification on held-out problems ----
    let heldoutResults: SolveResult[] = [];
    if (heldout.length) {
      console.error(`[rsi] verifying champion on held-out: ${heldout.join(",")}`);
      heldoutResults = await evalScaffold(server, champion, heldout, innerModel, numWorkers);
      totalCost += heldoutResults.reduce((a, r) => a + r.cost, 0);
    }

    writeResults(RUN_DIR, { champion, championFitness, heldoutResults, totalCost, problems, heldout });
    console.error(`[rsi] DONE. champion fitness=${championFitness.toFixed(1)} totalCost=$${totalCost.toFixed(2)}`);
  } finally {
    await server.stop();
  }
  process.exit(0);
}

function writeResults(
  runDir: string,
  s: {
    champion: Scaffold;
    championFitness: number;
    heldoutResults: SolveResult[];
    totalCost: number;
    problems: string[];
    heldout: string[];
  },
): void {
  const heldTxt = s.heldoutResults.length
    ? s.heldoutResults.map((r) => `- ${r.problemId}: performance=${r.performance ?? "FAIL"} rank=${r.rank ?? "-"} valid=${r.bestValid}`).join("\n")
    : "(none)";
  const lines = [
    "# OpenRSI results",
    "",
    `Champion scaffold: v${s.champion.version}, max_public_evals=${s.champion.max_public_evals}`,
    `Mean private performance on RSI set [${s.problems.join(", ")}]: **${s.championFitness.toFixed(1)}**`,
    "",
    "## Held-out verification (problems the loop never selected on)",
    heldTxt,
    "",
    `Total OpenRouter cost: $${s.totalCost.toFixed(2)}`,
    "",
    "## Champion domain knowledge",
    ...s.champion.domain_knowledge.map((d) => `- ${d}`),
    "",
    "See leaderboard.md + board.jsonl for the full generation-by-generation RSI curve.",
  ];
  writeFileSync(join(runDir, "RESULTS.md"), lines.join("\n") + "\n");
  writeFileSync(join(runDir, "champion_scaffold.json"), JSON.stringify(s.champion, null, 2) + "\n");
}

main().catch((e) => {
  console.error("[rsi] FATAL:", e?.stack || e);
  process.exit(1);
});
