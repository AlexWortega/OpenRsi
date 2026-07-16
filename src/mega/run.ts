/**
 * KernelBench-Mega runner: a long-running pi coding agent (real bash/read/edit/write
 * tools) that iterates on solution.py in the problem directory against check.py +
 * benchmark.py, targeting maximum decode speedup. This is the single autonomous
 * session the mega benchmark expects (3h budget), driven with Opus + recalled memory.
 *
 *   OPENRSI_MEGA_DIR=/workspace/mega/benchmarks/mega/problems/02_kimi_linear_decode \
 *   OPENRSI_MEGA_HOURS=3 node --env-file=.env dist/mega/run.js
 */
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { createAgentSession, SessionManager } from "@earendil-works/pi-coding-agent";
import { assertKey, modelSlug, tierModel } from "../provider.js";
import { recall, reflectAndStore } from "../memory/memory.js";

const SYS = `You are an elite GPU kernel engineer competing on KernelBench-Mega — a focused, autonomous worker with one goal: MAXIMIZE the geomean decode speedup of a fused megakernel while staying numerically correct. Do not broaden scope beyond that goal; do not refactor or explore unrelated things.

You work in a live directory with real bash/read/edit/write tools on an RTX PRO 6000 (Blackwell SM120). READ reference.py and baseline.py fully BEFORE writing anything, and re-read any file before you edit it. Write a fused single-launch megakernel in solution.py that beats baseline.py on decode latency while matching reference.py (cosine >= 0.98). Ensure your code runs immediately — after every edit, actually run it.

Correctness gate: \`python check.py\` MUST print PASS (this is non-negotiable; a spot-check is not a substitute). Score: geomean decode speedup over context lengths 2048/8192/16384 via \`python benchmark.py\`. Hard rule: the timed step() must be ONE kernel launch (one @triton.jit grid or one load_inline CUDA __global__) — no CUDA graphs, torch.compile, or per-op loops; an authenticity judge rejects those. Do not import prebuilt quant/model libs.

Flywheel (repeat relentlessly): implement -> \`python check.py\` -> \`python benchmark.py\` -> read the exact number -> profile the bottleneck -> improve -> re-measure. ALWAYS keep a snapshot of your best PASSING solution and never overwrite it with something unverified. Persistence: this is a hard frontier task — do NOT stop while check.py fails OR the speedup can still go up. Report your best verified geomean speedup clearly.`;

async function main() {
  assertKey();
  const dir = process.env.OPENRSI_MEGA_DIR || "/workspace/mega/benchmarks/mega/problems/02_kimi_linear_decode";
  const hours = Number(process.env.OPENRSI_MEGA_HOURS || 3);
  const deadline = Date.now() + hours * 3600_000;
  const model = tierModel("outer"); // strongest model for the hardest task
  console.error(`[mega] model=openrouter:${modelSlug("outer")} dir=${dir} budget=${hours}h`);

  const prompt = readFileSync(join(dir, "PROMPT.txt"), "utf8");
  const mem = recall("mega", "02_kimi_linear_decode", 8);

  const { session } = await createAgentSession({
    model,
    thinkingLevel: "high",
    cwd: dir, // built-in bash/read/edit/write operate here
    systemPrompt: SYS + mem,
    sessionManager: SessionManager.inMemory(dir),
  } as any);

  session.subscribe((e: any) => {
    if (e.type === "tool_execution_start") process.stderr.write(`[mega ${new Date().toISOString().slice(11, 19)}] tool ${e.toolName ?? e.name ?? "?"}\n`);
  });

  // First pass: the full task. Then keep nudging until the wall-clock deadline.
  await session.prompt(prompt + "\n\nBegin. Read reference.py and baseline.py first, then implement, run check.py, run benchmark.py, and iterate.");
  await session.waitForIdle();

  let round = 0;
  while (Date.now() < deadline) {
    round++;
    const remainMin = Math.round((deadline - Date.now()) / 60000);
    console.error(`[mega] nudge ${round}, ${remainMin} min left`);
    await session.prompt(
      `Keep going (${remainMin} min budget left). Run \`python benchmark.py\` and report the current geomean speedup and whether \`python check.py\` prints PASS. Then push the latency lower — profile the megakernel, improve the int4 dequant-GEMV fusion, tune block sizes. Do not stop; maximize the speedup.`,
    );
    await session.waitForIdle();
  }

  const stats = session.getSessionStats() as any;
  console.error(`[mega] DONE after ${round} rounds, cost=$${(stats?.cost ?? 0).toFixed(2)}`);
  await reflectAndStore({ model, benchmark: "mega", problemId: "02_kimi_linear_decode", score: 0, transcript: `Worked ${hours}h on the Kimi W4A16 megakernel over ${round} rounds. See solution.py in ${dir}.` }).catch(() => {});
  process.exit(0);
}
main().catch((e) => { console.error("[mega] FATAL", e?.stack || e); process.exit(1); });
