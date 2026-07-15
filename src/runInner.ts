/**
 * Run the inner solver on one (or more) ALE-Bench problems with the current scaffold.
 *
 *   node --env-file=.env dist/runInner.js ahc008 [ahc011 ...]
 *
 * Prints a JSON line per problem. This is the gen-0 baseline harness.
 */
import { AleEvalServer } from "./ale/evalServer.js";
import { loadScaffold } from "./inner/scaffold.js";
import { solveProblem } from "./inner/solve.js";
import { assertKey, modelSlug, tierModel } from "./provider.js";

async function main() {
  assertKey();
  const problems = process.argv.slice(2);
  if (problems.length === 0) problems.push("ahc008");
  const numWorkers = Number(process.env.OPENRSI_NUM_WORKERS || 12);

  const scaffold = loadScaffold();
  const model = tierModel("inner");
  console.error(`[runInner] model=openrouter:${modelSlug("inner")} scaffold.v=${scaffold.version} budget=${scaffold.max_public_evals} problems=${problems.join(",")}`);

  const server = new AleEvalServer();
  await server.start();

  try {
    for (const problemId of problems) {
      const t0 = Date.now();
      const res = await solveProblem({
        evalServer: server,
        problemId,
        scaffold,
        model,
        numWorkers,
        lite: true,
      });
      const secs = ((Date.now() - t0) / 1000).toFixed(0);
      console.log(JSON.stringify({ ...res, bestCode: `<${res.bestCode.length} chars>`, secs }));
      console.error(
        `[runInner] ${problemId}: perf=${res.performance} rank=${res.rank} publicScore=${res.bestPublicScore} valid=${res.bestValid} evals=${res.evalsUsed} cost=$${res.cost.toFixed(3)} ${secs}s${res.error ? " ERR=" + res.error : ""}`,
      );
    }
  } finally {
    await server.stop();
  }
  process.exit(0);
}

main().catch((e) => {
  console.error("[runInner] FATAL:", e?.stack || e);
  process.exit(1);
});
