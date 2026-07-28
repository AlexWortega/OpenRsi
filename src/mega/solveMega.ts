/**
 * Inner mega solve for the RSI loop: run a full pi coding agent (real bash/read/edit/
 * write) on the Kimi-Linear W4A16 megakernel, driven by an EVOLVABLE scaffold (system
 * prompt + domain knowledge), time-boxed to a per-solve compute budget, then scored
 * authoritatively (check.py PASS + benchmark.py geomean). Returns a SolveResult so the
 * generational RSI loop + bounded-edit proposer reuse unchanged. fitness = geomean speedup.
 */
import { cpSync, existsSync, mkdtempSync, readdirSync, readFileSync, rmSync, statSync } from "node:fs";
import { execFile } from "node:child_process";
import { tmpdir } from "node:os";
import { join, relative } from "node:path";
import { createAgentSession, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";
import type { Scaffold } from "../inner/scaffold.js";
import type { SolveResult } from "../inner/solve.js";
import { composeSystemPrompt } from "../inner/scaffold.js";
import { recall, reflectAndStore } from "../memory/memory.js";

const PY = process.env.OPENRSI_MEGA_PYTHON || "python";
const EVAL_TIMEOUT_MS = Number(process.env.OPENRSI_MEGA_EVAL_TIMEOUT_S || 900) * 1000;
const MEMORY_ON = (process.env.OPENRSI_MEMORY ?? "on") !== "off";
// Authenticity judge (megakernel_evidence.py). Not shipped in the problem dir —
// point at it via env; when set + present we run it as the verify gate so a
// "fast" number that hides launches (CUDAGraph/compile) is not silently trusted.
const JUDGE = process.env.OPENRSI_MEGA_JUDGE || "";
// Harness modules that ship with the problem — everything else *.py in the workdir
// is an agent-written artifact (solution.py entry + any sidecar like mega.py).
const HARNESS_PY = new Set(["reference", "baseline", "shapes", "check", "benchmark", "problem", "sota"]);

// Collect every agent-written .py in the workdir (recursively, minus __pycache__ and
// harness modules) so a PASSing kernel with sidecar modules is fully reproducible.
function collectArtifacts(dir: string): Record<string, string> {
  const out: Record<string, string> = {};
  const walk = (d: string) => {
    for (const name of readdirSync(d)) {
      if (name === "__pycache__" || name === ".git") continue;
      const p = join(d, name);
      const st = statSync(p);
      if (st.isDirectory()) walk(p);
      else if (name.endsWith(".py") && !HARNESS_PY.has(name.replace(/\.py$/, ""))) {
        try { out[relative(dir, p)] = readFileSync(p, "utf8"); } catch { /* skip */ }
      }
    }
  };
  walk(dir);
  return out;
}

function sh(cmd: string, args: string[], cwd: string, timeoutMs: number): Promise<{ code: number; out: string }> {
  return new Promise((resolve) => {
    execFile(cmd, args, { cwd, timeout: timeoutMs, maxBuffer: 16 * 1024 * 1024, killSignal: "SIGKILL" }, (err, stdout, stderr) => {
      const out = `${stdout || ""}${stderr ? "\n[stderr]\n" + stderr : ""}`;
      resolve({ code: err && typeof (err as any).code === "number" ? (err as any).code : err ? 1 : 0, out });
    });
  });
}

// benchmark.py on this task swings ~30% run-to-run (measured 11.76 / 13.50 / 15.35 on
// the SAME kernel), so a single measurement records a lucky/unlucky draw — a recorded
// 16.7x reproduced at 11.9x. Score the MEDIAN of N repeats to de-noise: the recorded
// number then matches a stable re-measurement. OPENRSI_MEGA_BENCH_REPEATS (default 3).
const BENCH_REPEATS = Math.max(1, Number(process.env.OPENRSI_MEGA_BENCH_REPEATS || 3));
async function evalDir(dir: string): Promise<{ passed: boolean; geomean: number; tail: string }> {
  const chk = await sh(PY, ["check.py"], dir, EVAL_TIMEOUT_MS);
  const passed = chk.code === 0 && /(^|\n)\s*PASS\s*(\n|$)/.test(chk.out);
  let geomean = 0;
  let tail = chk.out.slice(-500);
  if (passed) {
    const vals: number[] = [];
    let lastOut = "";
    for (let i = 0; i < BENCH_REPEATS; i++) {
      const bench = await sh(PY, ["benchmark.py"], dir, EVAL_TIMEOUT_MS);
      lastOut = bench.out;
      const v = parseFloat(bench.out.match(/peak_fraction:\s*([\d.]+)/)?.[1] ?? "0");
      if (v > 0) vals.push(v);
    }
    vals.sort((a, b) => a - b);
    const mid = Math.floor(vals.length / 2);
    geomean = vals.length === 0 ? 0 : vals.length % 2 ? vals[mid] : (vals[mid - 1] + vals[mid]) / 2; // median
    tail = `bench x${vals.length}: [${vals.map((v) => v.toFixed(2)).join(", ")}] median=${geomean.toFixed(3)}\n` + lastOut.slice(-360);
  }
  return { passed, geomean, tail };
}

// Verify-before-trust: run the authenticity evidence extractor (megakernel_evidence.py)
// on the final workdir and gate deterministically on its evidence. The extractor is
// STATIC (reads solution.py + every local sidecar it imports), emitting JSON with
// kernel_count, tripwires{graph,compile,codegen,obfuscation}, forbidden_import_hits.
// A kernel is authentic iff it has >=1 real kernel and trips NO hidden-launch wire
// and no forbidden import. Returns undefined when no judge is configured (unknown,
// NOT asserted true). Also writes the evidence bundle to the dir for the record.
async function runJudge(dir: string): Promise<{ ok: boolean | undefined; reason: string }> {
  if (!JUDGE || !existsSync(JUDGE)) return { ok: undefined, reason: "judge not configured" };
  const r = await sh(PY, [JUDGE, "."], dir, EVAL_TIMEOUT_MS);
  const jsonStart = r.out.indexOf("{");
  if (jsonStart < 0) return { ok: undefined, reason: "no evidence emitted" };
  try {
    const ev = JSON.parse(r.out.slice(jsonStart));
    const tw = ev.tripwires || {};
    const kernels = ev.kernel_count?.total ?? 0;
    const forbidden = (ev.forbidden_import_hits || []) as string[];
    const wires = Object.entries(tw).filter(([k, v]) => k !== "detail" && v).map(([k]) => k);
    const ok = kernels >= 1 && wires.length === 0 && forbidden.length === 0;
    const reason = ok ? `authentic (${kernels} real kernels)`
      : kernels < 1 ? "NO real GPU kernel (kernels=0) — pure torch ops, not a fused kernel"
      : wires.length ? `hidden-launch tripwire: ${wires.join(",")} (torch.compile / CUDAGraph / codegen)`
      : `forbidden import: ${forbidden.join(",")}`;
    return { ok, reason };
  } catch { return { ok: undefined, reason: "evidence parse error" }; }
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
  // SEED: start from a prior solution (+ its sidecars) instead of a blank slate, so the
  // agent CONTINUES/FIXES an existing kernel rather than re-solving from scratch. Used to
  // let a bare agent fix a correct-but-benchmark-crashing kernel (its own earlier output).
  const seedDir = process.env.OPENRSI_MEGA_SEED || "";
  if (seedDir && existsSync(seedDir)) {
    for (const f of readdirSync(seedDir)) if (f.endsWith(".py")) cpSync(join(seedDir, f), join(dir, f));
    process.stderr.write(`[mega-solve] seeded workdir from ${seedDir}: ${readdirSync(seedDir).filter((f) => f.endsWith(".py")).join(", ")}\n`);
  }

  // PLAIN mode: a bare Opus coding agent with NO OpenRSI self-improvement — no evolved
  // scaffold (domain knowledge / strategy), no accumulated memory, no strategy coaching
  // in the nudge. Isolates what the SI machinery adds over just letting the agent code.
  const PLAIN = process.env.OPENRSI_MEGA_PLAIN === "1";
  const prompt = readFileSync(join(baseDir, "PROMPT.txt"), "utf8");
  const mem = !PLAIN && MEMORY_ON ? recall("mega", "02_kimi_linear_decode", 6) : "";
  const t0 = Date.now();
  const log = (m: string) => process.stderr.write(`[mega-solve ${new Date().toISOString().slice(11, 19)}] ${m}\n`);

  const { session } = await createAgentSession({
    model,
    thinkingLevel: (process.env.OPENRSI_MEGA_THINK as "low" | "medium" | "high") || "high",
    cwd: dir, // full pi coding agent operates here
    systemPrompt: PLAIN
      ? "You are an expert GPU kernel engineer and autonomous coding agent. Solve the task in this working directory: make it numerically correct first, then as fast as you can. Iterate on your own — edit code, run the checks, read the output, and keep improving until you are satisfied."
      : composeSystemPrompt(scaffold) + mem,
    sessionManager: SessionManager.inMemory(dir),
  } as any);
  let lastActivity = Date.now();
  session.subscribe((e: any) => { lastActivity = Date.now(); if (e.type === "tool_execution_start") log(`tool ${e.toolName ?? e.name ?? "?"}`); });

  // HARD wall-clock cap: abort the session at the deadline regardless of how long a
  // single agent turn runs (the between-turns deadline check alone lets one long turn
  // overrun the budget by hours).
  let timedOut = false;
  const hardTimer = new Promise<void>((res) => setTimeout(() => { timedOut = true; log(`WATCHDOG: hard cap ${solveS}s reached — aborting`); session.abort().catch(() => {}); res(); }, solveS * 1000 + 30000));
  const costCap = Number(process.env.OPENRSI_MEGA_COST_CAP || 0); // $ runaway guard (0 = off)
  const curCost = () => ((session.getSessionStats() as any)?.cost ?? 0);
  // HARD cost cap: poll cost DURING a turn (not only between turns) and abort the moment
  // the cap is exceeded. The between-turns check alone lets one long turn overshoot ~2x
  // (a 14h PLAIN-mode turn blew a $50 cap to $92.77). 30s poll ⇒ overshoot bounded to
  // one model step, not one full turn.
  const costPoller = costCap > 0 ? setInterval(() => {
    if (curCost() >= costCap) { timedOut = true; log(`COST WATCHDOG: $${costCap} exceeded ($${curCost().toFixed(2)}) mid-turn — aborting`); session.abort().catch(() => {}); }
  }, 30000) : null;
  // STALL watchdog: OpenRouter streams occasionally hang open and the SDK never times
  // them out — the run then sleeps for hours with no activity (3 such silent hangs this
  // campaign). Abort if no session event fires for STALL_MIN minutes (default 25).
  const stallMs = Number(process.env.OPENRSI_MEGA_STALL_MIN || 25) * 60000;
  const stallPoller = setInterval(() => {
    if (Date.now() - lastActivity > stallMs) { timedOut = true; log(`STALL WATCHDOG: no activity ${Math.round(stallMs / 60000)}min — aborting hung stream`); session.abort().catch(() => {}); }
  }, 60000);
  const runLoop = (async () => {
    const mins = () => Math.max(0, Math.round((deadline - Date.now()) / 60000));
    const begin = seedDir && existsSync(seedDir)
      ? `\n\nBegin: a solution.py (and its helper modules) ALREADY EXISTS in this directory from a prior attempt. Run \`python check.py\` and \`python benchmark.py\` FIRST to see its current state, diagnose any failure (e.g. a crash under benchmark), FIX it so both pass, then optimize. Do NOT rewrite from scratch. You have ~${mins()} min.`
      : `\n\nBegin: read reference.py and baseline.py first, then implement solution.py, run \`python check.py\`, run \`python benchmark.py\`, and iterate. You have ~${mins()} min.`;
    // Authenticity is part of the objective, stated up front: a gamed kernel scores 0.
    const authRule = ` IMPORTANT: the speedup ONLY counts if the kernel is a GENUINE fused GPU kernel — an authenticity judge scores it ZERO if it uses torch.compile, CUDAGraph, hidden per-op launches, or a pure-torch fallback (no real kernel). benchmark.py alone does NOT tell you this; a fast torch trick still scores 0.`;
    await session.prompt(prompt + begin + authRule);
    await session.waitForIdle();
    let authWarn = "";
    while (!timedOut && Date.now() < deadline) {
      if (costCap > 0 && curCost() >= costCap) { log(`COST CAP $${costCap} reached ($${curCost().toFixed(2)}) — stopping`); break; }
      await session.prompt((PLAIN
        ? `Keep going (${mins()} min left). Continue on your own until \`python check.py\` PASSes and the kernel is as fast as you can make it, then stop.`
        : `Keep going (${mins()} min left). Work in SMALL FAST steps: if you don't yet PASS, make the SIMPLEST change to reach \`python check.py\` PASS and snapshot it (cp solution.py best_solution.py). If you DO pass, make ONE focused optimization, run \`python check.py\` then \`python benchmark.py\`, read peak_fraction, and repeat. Keep this turn SHORT — one small edit + one run, not a big rewrite. Never lose your best passing snapshot.`) + authWarn);
      await session.waitForIdle();
      // In-loop anti-gaming gate: the judge is STATIC (reads source, no GPU) so it is
      // cheap to run every turn. If the current solution.py is a gamed/torch-only kernel,
      // escalate a warning into the next nudge — the agent otherwise sees a fast
      // benchmark.py and wrongly believes it won.
      if (JUDGE && existsSync(join(dir, "solution.py"))) {
        const v = await runJudge(dir);
        authWarn = v.ok === false
          ? `\n\n⚠ AUTHENTICITY — YOUR CURRENT solution.py SCORES 0: the judge REJECTED it — ${v.reason}. A fast benchmark.py means nothing if the kernel is not genuine. Replace it with a REAL fused GPU kernel (Triton @triton.jit or raw CUDA), no torch.compile / CUDAGraph / hidden launches.`
          : "";
        if (v.ok === false) log(`in-loop judge: solution.py REJECTED — ${v.reason}`);
      }
    }
  })();
  try {
    await Promise.race([runLoop, hardTimer]);
  } catch (e: any) {
    log(`error: ${e?.message || e}`);
  } finally {
    if (costPoller) clearInterval(costPoller);
    clearInterval(stallPoller);
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
  // Capture the FULL artifact set BEFORE any cleanup — solution.py alone is often a
  // stub that `import mega`s a sidecar holding the real kernel; saving only the stub
  // makes the PASS non-reproducible (this exact bug voided the Opus 8.5x record).
  const artifacts = collectArtifacts(dir);
  const sidecars = Object.keys(artifacts).filter((f) => f !== "solution.py");
  if (ev.passed && sidecars.length) log(`captured ${sidecars.length} sidecar artifact(s): ${sidecars.join(", ")}`);
  // Verify-before-trust: run the authenticity judge on the passing kernel.
  const judged = ev.passed ? await runJudge(dir) : { ok: false as boolean | undefined, reason: "FAIL" };
  const verified = judged.ok;         // true | false | undefined(no judge)
  const gamed = verified === false;   // judge ran and REJECTED -> gaming
  // ANTI-GAMING SCORE GATE: a gamed kernel games benchmark.py but is not a real fused
  // kernel — it is worth ZERO, exactly like a correctness fail. This is what stops the
  // leaderboard/RSI/BoN from ever selecting a CUDAGraph/torch trick (the old 18x class).
  const scored = ev.passed && !gamed;
  const perf = scored ? ev.geomean : 0;
  if (gamed) log(`AUTHENTICITY JUDGE REJECTED — ${judged.reason} — geomean ${ev.geomean.toFixed(3)}x SCORED 0`);
  const stats = session.getSessionStats() as any;
  log(`v${scaffold.version}: PASS=${ev.passed} verified=${verified} scored=${perf.toFixed(3)}x (raw ${ev.geomean.toFixed(3)}x) ${Math.round((Date.now() - t0) / 60000)}min $${(stats?.cost ?? 0).toFixed(2)}`);

  if (MEMORY_ON && code) {
    await reflectAndStore({ model, benchmark: "mega", problemId: "02_kimi_linear_decode", score: ev.geomean, transcript: `Scaffold v${scaffold.version}: PASS=${ev.passed} geomean=${ev.geomean.toFixed(3)}x.\nsolution.py (excerpt):\n${code.slice(0, 900)}` }).catch(() => {});
  }
  // Keep the workdir when we could NOT fully capture the artifacts (defensive), or on
  // FAIL for diagnosis. A PASS with all artifacts in hand is safe to clean.
  if (ev.passed && Object.keys(artifacts).length) { try { rmSync(dir, { recursive: true, force: true }); } catch { /* best effort */ } }
  else if (!ev.passed) log(`FAILED — workdir kept for diagnosis: ${dir}`);
  else log(`PASS but no artifacts captured — workdir kept: ${dir}`);

  return {
    problemId: "mega_kimi",
    scoreType: "speedup",
    evalsUsed: 1,
    bestPublicScore: scored ? ev.geomean : null,
    bestValid: scored,
    performance: perf,
    rank: null,
    privateScore: scored ? ev.geomean : null,
    privateJudge: ev.passed ? `geomean=${ev.geomean.toFixed(3)}x${verified === undefined ? "" : verified ? " (authentic)" : ` (REJECTED: ${judged.reason} → scored 0)`}` : "FAIL",
    bestCode: code,
    artifacts,
    verified: verified === true,
    cost: stats?.cost ?? 0,
    solver: "mega",
    error: !ev.passed ? ev.tail.slice(-200) : gamed ? `authenticity judge REJECTED (scored 0): ${judged.reason}` : undefined,
  };
}
