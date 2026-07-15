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
import { writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { AleEvalServer } from "./ale/evalServer.js";
import { Board, type GenRecord } from "./board.js";
import { loadScaffold, saveScaffold, type Scaffold } from "./inner/scaffold.js";
import { solveProblem, type SolveResult } from "./inner/solve.js";
import { proposeImprovement, type AttemptRecord } from "./outer/improve.js";
import { assertKey, modelSlug, tierModel } from "./provider.js";

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
  const generations = Number(process.env.OPENRSI_GENERATIONS || 6);
  const stagnationLimit = Number(process.env.OPENRSI_STAGNATION || 3);
  const numWorkers = Number(process.env.OPENRSI_NUM_WORKERS || 12);

  const innerModel = tierModel("inner");
  const outerModel = tierModel("outer");
  console.error(
    `[rsi] inner=${modelSlug("inner")} outer=${modelSlug("outer")} problems=${problems.join(",")} heldout=${heldout.join(",")} gens=${generations}`,
  );

  const board = new Board(RUN_DIR);
  const server = new AleEvalServer();
  await server.start();

  let totalCost = 0;
  try {
    // ---- gen 0: baseline (default scaffold) ----
    let champion = loadScaffold();
    let t0 = Date.now();
    let championResults = await evalScaffold(server, champion, problems, innerModel, numWorkers);
    let championFitness = meanPerformance(championResults);
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
      const prop = await proposeImprovement({
        model: outerModel,
        champion,
        championResults,
        championFitness,
        history,
      });
      totalCost += prop.cost;
      if (!prop.candidate) {
        console.error(`[rsi] gen${gen}: no candidate proposed; skipping`);
        stagnation++;
        if (stagnation >= stagnationLimit) break;
        continue;
      }
      const candidate = prop.candidate;
      const candResults = await evalScaffold(server, candidate, problems, innerModel, numWorkers);
      const candFitness = meanPerformance(candResults);
      const candCost = candResults.reduce((a, r) => a + r.cost, 0) + prop.cost;
      totalCost += candResults.reduce((a, r) => a + r.cost, 0);
      const accepted = candFitness > championFitness;

      history.push({ gen, rationale: prop.rationale, fitness: candFitness, accepted });
      board.append({
        gen,
        scaffoldVersion: candidate.version,
        fitness: candFitness,
        accepted,
        champion: accepted,
        rationale: prop.rationale,
        perProblem: toPerProblem(candResults),
        cost: candCost,
        seconds: Math.round((Date.now() - t0) / 1000),
      });

      if (accepted) {
        champion = candidate;
        championResults = candResults;
        championFitness = candFitness;
        saveScaffold(champion); // persist new champion as the active scaffold
        stagnation = 0;
        console.error(`[rsi] gen${gen}: ACCEPTED new champion fitness=${candFitness.toFixed(1)} (was ${championFitness.toFixed(1)})`);
        const NOTIFY = process.env.HOME + "/.claude/skills/ml-intern/scripts/notify.sh";
        try {
          const { execFileSync } = await import("node:child_process");
          execFileSync("bash", [NOTIFY, "experiment_kept", `OpenRSI gen${gen} champion fitness=${candFitness.toFixed(0)}`], { stdio: "ignore" });
        } catch { /* notify optional */ }
      } else {
        stagnation++;
        console.error(`[rsi] gen${gen}: rejected (fitness ${candFitness.toFixed(1)} <= champion ${championFitness.toFixed(1)}) stagnation=${stagnation}`);
        if (stagnation >= stagnationLimit) {
          console.error(`[rsi] stagnation limit reached at gen${gen}; stopping.`);
          break;
        }
      }
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
