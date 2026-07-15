/** Smoke test the agent memory: reflect a fake session -> store -> recall. */
import { recall, reflectAndStore, loadMemory } from "./memory/memory.js";
import { assertKey, tierModel } from "./provider.js";

async function main() {
  assertKey();
  const model = tierModel("inner");
  console.log("[mem] reflecting a fake ahc008 session...");
  await reflectAndStore({
    model,
    benchmark: "ale",
    problemId: "ahc008",
    score: 1096,
    transcript:
      "ahc008 pet-capture grid problem. A greedy wall-building baseline that confines pets before humans get trapped reached performance 1096. An early attempt printed the wrong output length and got RUNTIME_ERROR. Simulated annealing on wall placement with a strict 1.9s timer improved the score.",
  });
  const all = loadMemory("ale");
  console.log(`[mem] stored ${all.length} memory item(s):`);
  for (const m of all.slice(-3)) console.log(`  - (${m.problemId}) [${m.tags.join(",")}] ${m.observation}`);
  console.log("[mem] recall block for a NEW ahc008 solve:");
  console.log(recall("ale", "ahc008"));
  process.exit(0);
}
main().catch((e) => { console.error("[mem] ERR", e?.stack || e); process.exit(1); });
