/**
 * Inner mega solve for the RSI loop: run a full pi coding agent (real bash/read/edit/
 * write) on the Kimi-Linear W4A16 megakernel, driven by an EVOLVABLE scaffold (system
 * prompt + domain knowledge), time-boxed to a per-solve compute budget, then scored
 * authoritatively (check.py PASS + benchmark.py geomean). Returns a SolveResult so the
 * generational RSI loop + bounded-edit proposer reuse unchanged. fitness = geomean speedup.
 */
import { cpSync, existsSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import { execFile } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createAgentSession, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";
import type { Scaffold } from "../inner/scaffold.js";
import type { SolveResult } from "../inner/solve.js";
import { composeSystemPrompt } from "../inner/scaffold.js";
import { recall, reflectAndStore } from "../memory/memory.js";

const PY = process.env.OPENRSI_MEGA_PYTHON || "python";
const EVAL_TIMEOUT_MS = Number(process.env.OPENRSI_MEGA_EVAL_TIMEOUT_S || 900) * 1000;
const MEMORY_ON = (process.env.OPENRSI_MEMORY ?? "on") !== "off";

function sh(cmd: string, args: string[], cwd: string, timeoutMs: number): Promise<{ code: number; out: string }> {
  return new Promise((resolve) => {
    execFile(cmd, args, { cwd, timeout: timeoutMs, maxBuffer: 16 * 1024 * 1024, killSignal: "SIGKILL" }, (err, stdout, stderr) => {
      const out = `${stdout || ""}${stderr ? "\n[stderr]\n" + stderr : ""}`;
      resolve({ code: err && typeof (err as any).code === "number" ? (err as any).code : err ? 1 : 0, out });
    });
  });
}

async function evalDir(dir: string): Promise<{ passed: boolean; geomean: number; tail: string }> {
  const chk = await sh(PY, ["check.py"], dir, EVAL_TIMEOUT_MS);
  const passed = chk.code === 0 && /(^|\n)\s*PASS\s*(\n|$)/.test(chk.out);
  let geomean = 0;
  let tail = chk.out.slice(-500);
  if (passed) {
    const bench = await sh(PY, ["benchmark.py"], dir, EVAL_TIMEOUT_MS);
    geomean = parseFloat(bench.out.match(/peak_fraction:\s*([\d.]+)/)?.[1] ?? "0");
    tail = bench.out.slice(-500);
  }
  return { passed, geomean, tail };
}

export async function solveMega(opts: {
  baseDir: string;
  scaffold: Scaffold;
  model: Model<any>;
}): Promise<SolveResult> {
  const { baseDir, scaffold, model } = opts;
  const solveS = Number(process.env.OPENRSI_MEGA_SOLVE_S || 2400); // per-solve compute budget
  const deadline = Date.now() + solveS * 1000;
  const dir = mkdtempSync(join(tmpdir(), "mega-solve-"));
  cpSync(baseDir, dir, { recursive: true, filter: (s) => !s.includes("__pycache__") });
  rmSync(join(dir, "solution.py"), { force: true });
  rmSync(join(dir, "framework.txt"), { force: true });

  const prompt = readFileSync(join(baseDir, "PROMPT.txt"), "utf8");
  const mem = MEMORY_ON ? recall("mega", "02_kimi_linear_decode", 6) : "";
  const t0 = Date.now();
  const log = (m: string) => process.stderr.write(`[mega-solve ${new Date().toISOString().slice(11, 19)}] ${m}\n`);

  const { session } = await createAgentSession({
    model,
    thinkingLevel: (process.env.OPENRSI_MEGA_THINK as "low" | "medium" | "high") || "high",
    cwd: dir, // full pi coding agent operates here
    systemPrompt: composeSystemPrompt(scaffold) + mem,
    sessionManager: SessionManager.inMemory(dir),
  } as any);
  session.subscribe((e: any) => { if (e.type === "tool_execution_start") log(`tool ${e.toolName ?? e.name ?? "?"}`); });

  // HARD wall-clock cap: abort the session at the deadline regardless of how long a
  // single agent turn runs (the between-turns deadline check alone lets one long turn
  // overrun the budget by hours).
  let timedOut = false;
  const hardTimer = new Promise<void>((res) => setTimeout(() => { timedOut = true; log(`WATCHDOG: hard cap ${solveS}s reached — aborting`); session.abort().catch(() => {}); res(); }, solveS * 1000 + 30000));
  const costCap = Number(process.env.OPENRSI_MEGA_COST_CAP || 0); // $ runaway guard (0 = off)
  const curCost = () => ((session.getSessionStats() as any)?.cost ?? 0);
  const runLoop = (async () => {
    const mins = () => Math.max(0, Math.round((deadline - Date.now()) / 60000));
    await session.prompt(prompt + `\n\nBegin: read reference.py and baseline.py first, then implement solution.py, run \`python check.py\`, run \`python benchmark.py\`, and iterate. You have ~${mins()} min.`);
    await session.waitForIdle();
    while (!timedOut && Date.now() < deadline) {
      if (costCap > 0 && curCost() >= costCap) { log(`COST CAP $${costCap} reached ($${curCost().toFixed(2)}) — stopping`); break; }
      await session.prompt(`Keep going (${mins()} min left). Work in SMALL FAST steps: if you don't yet PASS, make the SIMPLEST change to reach \`python check.py\` PASS and snapshot it (cp solution.py best_solution.py). If you DO pass, make ONE focused optimization, run \`python check.py\` then \`python benchmark.py\`, read peak_fraction, and repeat. Keep this turn SHORT — one small edit + one run, not a big rewrite. Never lose your best passing snapshot.`);
      await session.waitForIdle();
    }
  })();
  try {
    await Promise.race([runLoop, hardTimer]);
  } catch (e: any) {
    log(`error: ${e?.message || e}`);
  }

  // Prefer the agent's best PASSING snapshot if it kept one. At a hard-cap abort the
  // live solution.py is often mid-edit/broken, while best_solution.py holds the last
  // passing kernel — scoring only solution.py throws that away (yields a false 0).
  let ev = await evalDir(dir);
  const bestSnap = join(dir, "best_solution.py");
  if (existsSync(bestSnap)) {
    cpSync(bestSnap, join(dir, "solution.py"));
    const evSnap = await evalDir(dir);
    if (evSnap.passed && (!ev.passed || evSnap.geomean > ev.geomean)) { ev = evSnap; log(`used best_solution.py snapshot: PASS geomean=${ev.geomean.toFixed(3)}x`); }
  }
  const code = existsSync(join(dir, "solution.py")) ? readFileSync(join(dir, "solution.py"), "utf8") : "";
  const stats = session.getSessionStats() as any;
  log(`v${scaffold.version}: PASS=${ev.passed} geomean=${ev.geomean.toFixed(3)}x ${Math.round((Date.now() - t0) / 60000)}min $${(stats?.cost ?? 0).toFixed(2)}`);

  if (MEMORY_ON && code) {
    await reflectAndStore({ model, benchmark: "mega", problemId: "02_kimi_linear_decode", score: ev.geomean, transcript: `Scaffold v${scaffold.version}: PASS=${ev.passed} geomean=${ev.geomean.toFixed(3)}x.\nsolution.py (excerpt):\n${code.slice(0, 900)}` }).catch(() => {});
  }
  if (ev.passed) { try { rmSync(dir, { recursive: true, force: true }); } catch { /* best effort */ } }
  else log(`FAILED — workdir kept for diagnosis: ${dir}`);

  return {
    problemId: "mega_kimi",
    scoreType: "speedup",
    evalsUsed: 1,
    bestPublicScore: ev.passed ? ev.geomean : null,
    bestValid: ev.passed,
    performance: ev.passed ? ev.geomean : 0,
    rank: null,
    privateScore: ev.passed ? ev.geomean : null,
    privateJudge: ev.passed ? `geomean=${ev.geomean.toFixed(3)}x` : "FAIL",
    bestCode: code,
    cost: stats?.cost ?? 0,
    solver: "mega",
    error: ev.passed ? undefined : ev.tail.slice(-200),
  };
}
