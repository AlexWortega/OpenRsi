/**
 * KernelBench-Mega AIDE arm — the "new stack" for the A/B vs the single-agent runner
 * (src/mega/run.ts). Instead of ONE long agent editing solution.py, this grows an
 * explicit AIDE draft/improve/debug tree, gated by a grok-build goal plan.
 *
 *   - draft   : from baseline.py, write a fused single-launch megakernel solution.py
 *               (best-of-N sequential drafts — one GPU, so nodes run one at a time).
 *   - debug   : the best node FAILs check.py -> fix correctness to reach PASS.
 *   - improve : the best node PASSes -> push geomean decode speedup higher.
 *
 * Each node is a time-boxed agent turn in its OWN copy of the problem dir (real
 * bash/edit, so it profiles + runs check.py/benchmark.py itself), then the harness
 * scores it authoritatively: valid = `python check.py` prints PASS, score = the
 * `peak_fraction:` (geomean speedup) from `python benchmark.py`. The best node's
 * solution.py is copied back to OPENRSI_MEGA_DIR for the final measurement.
 *
 *   OPENRSI_MEGA_DIR=/workspace/mega/.../02_kimi_linear_decode_aide \
 *   OPENRSI_MEGA_HOURS=1 node --env-file=.env dist/mega/aideRun.js
 */
import { cpSync, mkdtempSync, readFileSync, rmSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { execFile } from "node:child_process";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createAgentSession, SessionManager } from "@earendil-works/pi-coding-agent";
import { assertKey, modelSlug, tierModel } from "../provider.js";
import { recall, reflectAndStore } from "../memory/memory.js";
import { checkGoalProgress, formatVerdict, writeGoalPlan, type GoalPlan, type GoalVerdict } from "../goal/plan.js";

const MEGA_SYS = `You are an elite GPU kernel engineer competing on KernelBench-Mega — a focused, autonomous worker with ONE goal: MAXIMIZE the geomean decode speedup of a fused megakernel while staying numerically correct. Do not broaden scope beyond that goal.

You work in a live directory with real bash/read/edit/write tools on an RTX PRO 6000 (Blackwell SM120). READ reference.py and baseline.py fully BEFORE writing anything, and re-read any file before you edit it. Write a fused single-launch megakernel in solution.py that beats baseline.py on decode latency while matching reference.py (cosine >= 0.98). Ensure your code runs immediately — after every edit, actually run it.

Correctness gate: \`python check.py\` MUST print PASS (non-negotiable; a spot-check is not a substitute). Score: geomean decode speedup over context lengths 2048/8192/16384 via \`python benchmark.py\` (read the \`peak_fraction:\` line). Hard rule: the timed step() must be ONE kernel launch (one @triton.jit grid or one load_inline CUDA __global__) — no CUDA graphs, torch.compile, or per-op loops; an authenticity judge rejects those. Do not import prebuilt quant/model libs.

Flywheel: implement -> \`python check.py\` -> \`python benchmark.py\` -> read the exact number -> profile -> improve -> re-measure. ALWAYS keep your best PASSING solution.py and never overwrite it with something unverified.`;

function sh(cmd: string, args: string[], cwd: string, timeoutMs: number): Promise<{ code: number; out: string }> {
  return new Promise((resolve) => {
    execFile(cmd, args, { cwd, timeout: timeoutMs, maxBuffer: 16 * 1024 * 1024, killSignal: "SIGKILL" }, (err, stdout, stderr) => {
      const out = `${stdout || ""}${stderr ? "\n[stderr]\n" + stderr : ""}`;
      resolve({ code: err && typeof (err as any).code === "number" ? (err as any).code : err ? 1 : 0, out });
    });
  });
}

const PY = process.env.OPENRSI_MEGA_PYTHON || "python";
const EVAL_TIMEOUT_MS = Number(process.env.OPENRSI_MEGA_EVAL_TIMEOUT_S || 900) * 1000;

/** Authoritative eval of a solution in `dir`: PASS gate + geomean speedup. */
async function evalDir(dir: string): Promise<{ passed: boolean; geomean: number; checkTail: string; benchTail: string }> {
  const chk = await sh(PY, ["check.py"], dir, EVAL_TIMEOUT_MS);
  const passed = chk.code === 0 && /(^|\n)\s*PASS\s*(\n|$)/.test(chk.out);
  let geomean = 0;
  let benchTail = "(check failed — benchmark skipped)";
  if (passed) {
    const bench = await sh(PY, ["benchmark.py"], dir, EVAL_TIMEOUT_MS);
    const m = bench.out.match(/peak_fraction:\s*([\d.]+)/);
    geomean = m ? parseFloat(m[1]) : 0;
    benchTail = bench.out.slice(-1200);
  }
  return { passed, geomean, checkTail: chk.out.slice(-1200), benchTail };
}

interface MegaNode { id: number; kind: "draft" | "improve" | "debug"; parentId: number | null; code: string; passed: boolean; geomean: number; feedback: string }

async function main() {
  assertKey();
  const baseDir = process.env.OPENRSI_MEGA_DIR || "/workspace/mega/benchmarks/mega/problems/02_kimi_linear_decode";
  const hours = Number(process.env.OPENRSI_MEGA_HOURS || 1);
  const deadline = Date.now() + hours * 3600_000;
  const draftN = Number(process.env.OPENRSI_INNER_CANDIDATES || 2);
  const nodeMin = Number(process.env.OPENRSI_MEGA_NODE_MIN || 12);
  const epsilon = Number(process.env.OPENRSI_AIDE_EPSILON || 0.25);
  const runDir = process.env.OPENRSI_RUN_DIR || join(baseDir, "..", "_aide_run");
  mkdirSync(runDir, { recursive: true });
  const model = tierModel("outer");
  const log = (m: string) => process.stderr.write(`[mega-aide ${new Date().toISOString().slice(11, 19)}] ${m}\n`);
  log(`model=openrouter:${modelSlug("outer")} base=${baseDir} budget=${hours}h draftN=${draftN} nodeMin=${nodeMin}`);

  const prompt = readFileSync(join(baseDir, "PROMPT.txt"), "utf8");
  const baseline = existsSync(join(baseDir, "baseline.py")) ? readFileSync(join(baseDir, "baseline.py"), "utf8") : "";

  // ---- goal plan (grok-build): gating criteria from the real task ----
  let goalPlan: GoalPlan | null = null;
  try {
    goalPlan = await writeGoalPlan({
      model,
      objective: "Maximize geomean decode speedup of a fused single-launch Kimi-Linear W4A16 megakernel vs baseline.py, correct within cosine 0.98",
      metric: "geomean decode speedup (peak_fraction from benchmark.py)",
      taskText: prompt,
    });
    writeFileSync(join(runDir, "goal_plan.json"), JSON.stringify(goalPlan, null, 2) + "\n");
    log(`goal plan: ${goalPlan.criteria.length} gating criteria`);
  } catch (e: any) {
    log(`goal plan skipped: ${e?.message || e}`);
  }
  const criteriaBlock = goalPlan ? `\n\n## Gating criteria (all must hold)\n${goalPlan.criteria.map((c) => `${c.id}. ${c.outcome}`).join("\n")}` : "";

  const mem = recall("mega", "02_kimi_linear_decode", 8);
  const nodes: MegaNode[] = [];
  let nextId = 0;
  const fitnessHistory: number[] = [];

  const bestNode = (): MegaNode | null => {
    const passing = nodes.filter((n) => n.passed);
    if (passing.length) return passing.reduce((a, b) => (b.geomean > a.geomean ? b : a));
    return nodes.length ? nodes[nodes.length - 1] : null;
  };

  const runNode = async (kind: MegaNode["kind"], parent: MegaNode | null): Promise<MegaNode> => {
    const nodeDir = mkdtempSync(join(tmpdir(), "mega-node-"));
    cpSync(baseDir, nodeDir, { recursive: true, filter: (s) => !s.includes("__pycache__") && !s.endsWith("/_aide_run") });
    // Seed solution.py with the parent's code for improve/debug. Draft nodes write
    // from scratch — baseline.py imports reference.py, which check.py forbids in a
    // solution, so it cannot be used as a seed.
    const seed = parent ? parent.code : "";
    if (seed) writeFileSync(join(nodeDir, "solution.py"), seed);

    let userPrompt: string;
    if (kind === "draft" || !parent) {
      userPrompt = `Read reference.py and baseline.py fully to understand the math and layout (but do NOT import them — check.py hard-fails on \`import reference\`/\`import baseline\`). Then WRITE solution.py from scratch: a fused single-launch megakernel that beats baseline.py on decode latency while passing check.py (cosine >= 0.98). Fuse the int4 dequant-GEMV yourself. Run \`python check.py\` until it prints PASS, then \`python benchmark.py\` and push the geomean (peak_fraction) up. You have ~${nodeMin} minutes.`;
    } else if (kind === "debug") {
      userPrompt = `The current solution.py does NOT pass check.py. Fix its correctness (root cause) so \`python check.py\` prints PASS, then confirm with \`python benchmark.py\`.\n\nLatest check.py output:\n${parent.feedback.slice(-800)}\n\nYou have ~${nodeMin} minutes.`;
    } else {
      userPrompt = `The current solution.py PASSes check.py at geomean ${parent.geomean.toFixed(2)}x. Make the fused megakernel FASTER (better int4 dequant-GEMV fusion, coalesced weight streaming, block-size tuning) while KEEPING check.py PASS. Re-run \`python check.py\` and \`python benchmark.py\` after each change. You have ~${nodeMin} minutes.`;
    }

    const { session } = await createAgentSession({
      model,
      thinkingLevel: "high",
      cwd: nodeDir, // built-in bash/read/edit/write operate here
      systemPrompt: MEGA_SYS + criteriaBlock + mem,
      sessionManager: SessionManager.inMemory(nodeDir),
    } as any);
    session.subscribe((e: any) => { if (e.type === "tool_execution_start") log(`node#${nextId} ${kind} tool ${e.toolName ?? e.name ?? "?"}`); });

    const nodeDeadline = Math.min(deadline, Date.now() + nodeMin * 60_000);
    try {
      await Promise.race([
        (async () => {
          await session.prompt(userPrompt + "\n\nBegin now.");
          await session.waitForIdle();
          while (Date.now() < nodeDeadline) {
            await session.prompt(`Keep going (${Math.round((nodeDeadline - Date.now()) / 60000)} min left on this node). Run \`python check.py\` and \`python benchmark.py\`, read the numbers, and improve. Do not stop while check.py fails or the speedup can still rise.`);
            await session.waitForIdle();
          }
        })(),
        new Promise<void>((r) => setTimeout(() => { session.abort().catch(() => {}); r(); }, Math.max(1000, nodeDeadline - Date.now()) + 30_000)),
      ]);
    } catch (e: any) {
      log(`node#${nextId} ${kind} error: ${e?.message || e}`);
    }

    const code = existsSync(join(nodeDir, "solution.py")) ? readFileSync(join(nodeDir, "solution.py"), "utf8") : "";
    const ev = await evalDir(nodeDir);
    const node: MegaNode = { id: nextId++, kind, parentId: parent?.id ?? null, code, passed: ev.passed, geomean: ev.geomean, feedback: ev.checkTail + "\n" + ev.benchTail };
    nodes.push(node);
    const stats = session.getSessionStats() as any;
    log(`node#${node.id} ${kind}${parent ? "<-#" + parent.id : ""}: PASS=${node.passed} geomean=${node.geomean.toFixed(3)}x cost=$${(stats?.cost ?? 0).toFixed(2)}`);
    writeFileSync(join(runDir, `node${node.id}_${kind}.json`), JSON.stringify({ id: node.id, kind, parentId: node.parentId, passed: node.passed, geomean: node.geomean, feedbackTail: node.feedback.slice(-600) }, null, 2) + "\n");
    try { rmSync(nodeDir, { recursive: true, force: true }); } catch { /* best effort */ }
    return node;
  };

  // ---- draft phase (sequential best-of-N; one GPU) ----
  for (let i = 0; i < draftN && Date.now() < deadline; i++) await runNode("draft", null);

  // ---- search phase ----
  while (Date.now() < deadline) {
    const best = bestNode();
    let kind: MegaNode["kind"];
    let parent: MegaNode | null;
    if (!best || !best.passed) { kind = "debug"; parent = best; }
    else if (Math.random() < epsilon) { kind = "draft"; parent = null; }
    else { kind = "improve"; parent = best; }

    // grok-build direction check before spending the node.
    if (goalPlan) {
      const champ = best?.geomean ?? 0;
      fitnessHistory.push(champ);
      const v: GoalVerdict = await checkGoalProgress({
        model, plan: goalPlan, baselineFitness: 1.0, championFitness: champ, fitnessHistory,
        perProblem: [{ problemId: "02_kimi_linear_decode", fitness: champ, valid: !!best?.passed }],
      });
      log(`goal ${formatVerdict(v)} steer="${v.steer.slice(0, 80)}"`);
    }

    await runNode(kind, parent);
  }

  // ---- finalize: copy the best node's solution.py back for authoritative measurement ----
  const best = bestNode();
  let finalGeomean = 0;
  if (best?.code) {
    writeFileSync(join(baseDir, "solution.py"), best.code);
    const ev = await evalDir(baseDir);
    finalGeomean = ev.geomean;
    log(`FINAL best node#${best.id}: authoritative PASS=${ev.passed} geomean=${ev.geomean.toFixed(3)}x`);
    writeFileSync(join(runDir, "best_solution.py"), best.code);
  }

  const passing = nodes.filter((n) => n.passed);
  const lines = [
    "# KernelBench-Mega — AIDE arm results", "",
    `Budget: ${hours}h  nodes: ${nodes.length} (${passing.length} PASS)  draftN: ${draftN}`,
    `Best geomean decode speedup: **${(best?.geomean ?? 0).toFixed(3)}x** (authoritative re-measure ${finalGeomean.toFixed(3)}x)`, "",
    "## Nodes",
    ...nodes.map((n) => `- node#${n.id} ${n.kind}${n.parentId !== null ? "<-#" + n.parentId : ""}: PASS=${n.passed} geomean=${n.geomean.toFixed(3)}x`),
  ];
  writeFileSync(join(runDir, "RESULTS.md"), lines.join("\n") + "\n");
  console.log(JSON.stringify({ arm: "aide", hours, nodes: nodes.length, passing: passing.length, best_geomean: best?.geomean ?? 0, final_geomean: finalGeomean }));

  await reflectAndStore({ model, benchmark: "mega", problemId: "02_kimi_linear_decode", score: best?.geomean ?? 0, transcript: `AIDE arm: ${nodes.length} nodes (${passing.length} PASS), best geomean ${(best?.geomean ?? 0).toFixed(3)}x over ${hours}h.` }).catch(() => {});
  process.exit(0);
}

main().catch((e) => { console.error("[mega-aide] FATAL", e?.stack || e); process.exit(1); });
