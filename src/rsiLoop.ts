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
import { proposeImprovement, type AttemptRecord } from "./outer/improve.js";
import { assertKey, modelSlug, tierModel } from "./provider.js";

/** Distinct rewrite angles so each generation explores diverse variants. */
const VARIANT_ANGLES = [
  "search strategy: stronger simulated annealing / local search, better neighbourhoods, restarts",
  "domain knowledge: concrete problem-specific AHC heuristics and construction ideas",
  "time & eval-budget management: use the full time limit and the full submit budget",
  "output robustness: guarantee always-valid output, avoid WA/RE/TLE that zero a case",
  "algorithmic reframe: a different high-level approach to the objective",
  "parameter tuning: temperature schedule, move-type mix, data structures for O(1) delta eval",
];

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
  const numVariants = Number(process.env.OPENRSI_VARIANTS || 3);
  const numWorkers = Number(process.env.OPENRSI_NUM_WORKERS || 12);
  const variantsDir = join(RUN_DIR, "variants");
  mkdirSync(variantsDir, { recursive: true });

  const innerModel = tierModel("inner");
  const outerModel = tierModel("outer");
  console.error(
    `[rsi] inner=${modelSlug("inner")} outer=${modelSlug("outer")} problems=${problems.join(",")} heldout=${heldout.join(",")} gens=${generations} variants/gen=${numVariants}`,
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
      const feedback = readFeedback(RUN_DIR);
      if (feedback.trim()) console.error(`[rsi] gen${gen}: applying human feedback (${feedback.trim().length} chars)`);

      // Propose + evaluate several diverse variants this generation; keep the best.
      type Variant = { candidate: Scaffold; rationale: string; hint: string; results: SolveResult[]; fitness: number };
      const variants: Variant[] = [];
      for (let k = 0; k < numVariants; k++) {
        const hint = VARIANT_ANGLES[(gen - 1 + k) % VARIANT_ANGLES.length];
        const prop = await proposeImprovement({
          model: outerModel,
          champion,
          championResults,
          championFitness,
          history,
          variantHint: hint,
          feedback,
        });
        totalCost += prop.cost;
        if (!prop.candidate) {
          console.error(`[rsi] gen${gen} variant${k}: no candidate proposed`);
          continue;
        }
        const results = await evalScaffold(server, prop.candidate, problems, innerModel, numWorkers);
        const fitness = meanPerformance(results);
        totalCost += results.reduce((a, r) => a + r.cost, 0);
        const v: Variant = { candidate: prop.candidate, rationale: prop.rationale, hint, results, fitness };
        variants.push(v);
        // Persist the FULL variant scaffold + result so the user can view every option.
        writeFileSync(
          join(variantsDir, `gen${gen}_v${k}.json`),
          JSON.stringify({ gen, variant: k, hint, fitness, rationale: prop.rationale, perProblem: toPerProblem(results), scaffold: prop.candidate }, null, 2) + "\n",
        );
        appendFileSync(
          join(RUN_DIR, "VARIANTS.md"),
          `- gen${gen} v${k} [${hint.split(":")[0]}]: fitness=${fitness.toFixed(1)} — ${prop.rationale.slice(0, 120)} (variants/gen${gen}_v${k}.json)\n`,
        );
        console.error(`[rsi] gen${gen} v${k} [${hint.split(":")[0]}]: fitness=${fitness.toFixed(1)}`);
      }

      if (!variants.length) { stagnation++; if (stagnation >= stagnationLimit) break; continue; }
      const best = variants.reduce((a, b) => (b.fitness > a.fitness ? b : a));
      const accepted = best.fitness > championFitness;
      history.push({ gen, rationale: best.rationale, fitness: best.fitness, accepted });
      board.append({
        gen,
        scaffoldVersion: best.candidate.version,
        fitness: best.fitness,
        accepted,
        champion: accepted,
        rationale: `[best of ${variants.length}] ${best.rationale}`,
        perProblem: toPerProblem(best.results),
        cost: variants.reduce((a, v) => a + v.results.reduce((s, r) => s + r.cost, 0), 0),
        seconds: Math.round((Date.now() - t0) / 1000),
      });

      if (accepted) {
        const prevFitness = championFitness;
        champion = best.candidate;
        championResults = best.results;
        championFitness = best.fitness;
        writeFileSync(join(RUN_DIR, "champion_scaffold.json"), JSON.stringify(champion, null, 2) + "\n");
        stagnation = 0;
        console.error(`[rsi] gen${gen}: ACCEPTED champion fitness=${best.fitness.toFixed(1)} (was ${prevFitness.toFixed(1)}) via [${best.hint.split(":")[0]}]`);
        const NOTIFY = process.env.HOME + "/.claude/skills/ml-intern/scripts/notify.sh";
        try {
          const { execFileSync } = await import("node:child_process");
          execFileSync("bash", [NOTIFY, "experiment_kept", `OpenRSI gen${gen} champion fitness=${best.fitness.toFixed(0)}`], { stdio: "ignore" });
        } catch { /* notify optional */ }
      } else {
        stagnation++;
        console.error(`[rsi] gen${gen}: no variant beat champion ${championFitness.toFixed(1)} (best ${best.fitness.toFixed(1)}); continuing`);
        if (stagnation >= stagnationLimit) { console.error(`[rsi] stagnation limit; stopping.`); break; }
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
