/**
 * Inner solver for KernelBench: one agent writes a `ModelNew` kernel for one problem,
 * iterating on eval feedback (compiled / correct / speedup) under a budget.
 * Returns a SolveResult-shaped object (performance = best speedup) so the generational
 * loop, board, and critique reuse unchanged. Fitness = speedup; correctness is the gate.
 *
 * Modes via OPENRSI_SOLVER: "nudge" (default single-agent loop) | "aide" (draft/improve
 * /debug tree). Per-genre tips (scaffold.domain_knowledge_by_genre) and OPENRSI_SCRATCH
 * apply to both.
 */
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { Type } from "typebox";
import { createAgentSession, defineTool, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";
import type { Scaffold } from "../inner/scaffold.js";
import type { SolveResult } from "../inner/solve.js";
import { composeSystemPrompt } from "../inner/scaffold.js";
import { KernelEvalServer, type KernelEvalResult } from "./evalClient.js";
import { recall, reflectAndStore } from "../memory/memory.js";
import { classifyGenre } from "../genre.js";
import { generateSolution, solveAideTree, SCRATCH_ON, type AideNode } from "../inner/aideTree.js";

const MEMORY_ON = (process.env.OPENRSI_MEMORY ?? "on") !== "off";
const SOLVER = (process.env.OPENRSI_SOLVER ?? "nudge").toLowerCase();

function fmt(r: KernelEvalResult, used: number, budget: number): string {
  const lines = [
    `compiled=${r.compiled} correct=${r.correct} speedup=${r.speedup}x` +
      (r.runtime_us ? ` runtime=${r.runtime_us}us ref=${r.ref_us}us` : ""),
  ];
  if (!r.compiled || !r.correct) lines.push(`FIX FIRST: ${r.error || (!r.compiled ? "did not compile" : "incorrect output")}`);
  else if (r.error) lines.push(`note: ${r.error}`);
  lines.push(`evals ${used}/${budget}${used >= budget ? " — BUDGET EXHAUSTED, finalize" : ""}`);
  return lines.join("\n");
}

export async function solveKernel(opts: {
  server: KernelEvalServer;
  level: number;
  problemId: number;
  scaffold: Scaffold;
  model: Model<any>;
}): Promise<SolveResult> {
  const { server, level, problemId, scaffold, model } = opts;
  const budget = scaffold.max_public_evals;
  const pid = `L${level}P${problemId}`;
  const { ref_src } = await server.openSession(level, problemId);

  const genre = await classifyGenre({ model, benchmark: "kernel", problemId: pid, text: ref_src }).catch(() => "other");
  const memoryBlock = MEMORY_ON ? recall("kernel", pid, 6, genre) : "";
  const systemPrompt = composeSystemPrompt(scaffold, genre) + memoryBlock;
  const log = (m: string) => process.stderr.write(`[kb-solve ${pid}] ${m}\n`);

  const refBlock = ["## Reference PyTorch module (Model)", "```python", ref_src, "```"].join("\n");

  const inner = SOLVER === "aide"
    ? await runAide({ server, level, problemId, pid, budget, lang: scaffold.language, systemPrompt, refBlock, model, log })
    : await runNudge({ server, level, problemId, pid, budget, lang: scaffold.language, systemPrompt, refBlock, model, log });

  if (MEMORY_ON && inner.bestCode) {
    const transcript = `KernelBench ${pid} (genre ${genre}, solver ${SOLVER}). Used ${inner.evalsUsed} submissions; best speedup=${inner.bestScore.toFixed(3)}x correct=${inner.bestValid}.\nBest ModelNew (excerpt):\n${inner.bestCode.slice(0, 900)}`;
    await reflectAndStore({ model, benchmark: "kernel", problemId: pid, score: inner.bestScore, transcript, genre }).catch(() => {});
  }

  return {
    problemId: pid,
    scoreType: "speedup",
    evalsUsed: inner.evalsUsed,
    bestPublicScore: inner.bestValid ? inner.bestScore : null,
    bestValid: inner.bestValid,
    performance: inner.bestValid ? inner.bestScore : 0, // fitness = speedup (0 if never correct)
    rank: null,
    privateScore: inner.bestValid ? inner.bestScore : null,
    privateJudge: inner.bestValid ? "correct" : "incorrect",
    bestCode: inner.bestCode,
    cost: inner.cost,
    genre,
    solver: SOLVER,
    error: inner.error,
  };
}

interface KCommon {
  server: KernelEvalServer;
  level: number;
  problemId: number;
  pid: string;
  budget: number;
  lang: string;
  systemPrompt: string;
  refBlock: string;
  model: Model<any>;
  log: (m: string) => void;
}
interface KInner { bestCode: string; bestValid: boolean; bestScore: number; evalsUsed: number; cost: number; error?: string }

async function runAide(c: KCommon): Promise<KInner> {
  const draftN = Number(process.env.OPENRSI_INNER_CANDIDATES || 3);
  const patience = Number(process.env.OPENRSI_PATIENCE || 4);
  const evalCache = new Map<string, KernelEvalResult>();
  let evalsUsed = 0;

  const generate = async (kind: string, parent: AideNode | null, memory: string) => {
    let user: string;
    if (kind === "draft" || !parent) {
      user = `# KernelBench ${c.pid}\n\n${c.refBlock}\n\nWrite a complete Python file defining ModelNew (same forward signature/numerics as Model) with a custom CUDA/Triton kernel. Correctness is a hard gate; then maximize speedup.`;
    } else if (kind === "debug") {
      user = `# KernelBench ${c.pid}\n\n${c.refBlock}\n\nThe following ModelNew is INCORRECT or did not compile:\n\n\`\`\`python\n${parent.code}\n\`\`\`\n\nEval feedback:\n${parent.feedback}\n\nFix the root cause so it compiles and matches the reference within tolerance. Do not fake outputs.`;
    } else {
      user = `# KernelBench ${c.pid}\n\n${c.refBlock}\n\nHere is the current best CORRECT ModelNew (speedup ${parent.score.toFixed(3)}x):\n\n\`\`\`python\n${parent.code}\n\`\`\`\n\nEval feedback:\n${parent.feedback}\n\nProduce a FASTER version (better fusion, coalesced access, shared memory, block/grid tuning) that stays correct.`;
    }
    return generateSolution({ model: c.model, language: "python", systemPrompt: c.systemPrompt, userPrompt: user + memory, log: c.log });
  };

  const evalFn = async (code: string) => {
    const r = await c.server.evalKernel(c.level, c.problemId, code);
    evalCache.set(code, r);
    return { valid: r.correct, score: r.correct ? r.speedup : (r.compiled ? 0 : -1), feedback: fmt(r, ++evalsUsed, c.budget), error: r.error };
  };

  const tree = await solveAideTree({ budget: c.budget, draftN, patience, generate, evalFn, log: c.log });
  const bestR = tree.bestCode ? evalCache.get(tree.bestCode) : undefined;
  return {
    bestCode: tree.bestCode,
    bestValid: tree.bestValid,
    bestScore: bestR?.correct ? bestR.speedup : 0,
    evalsUsed: tree.evalsUsed,
    cost: tree.cost,
  };
}

async function runNudge(c: KCommon): Promise<KInner> {
  const budget = c.budget;
  let evalsUsed = 0;
  let lastCode = "";
  const best = { code: null as string | null, speedup: 0 };

  const submit = defineTool({
    name: "submit",
    label: "submit",
    description:
      "Compile your full ModelNew source, check numerical correctness against the reference, and (if correct) measure speedup. Iterate to maximize speedup while staying correct.",
    parameters: Type.Object({ code: Type.String({ description: "Complete Python file defining ModelNew (+ inline CUDA/Triton kernel)" }) }),
    async execute(_id, { code }) {
      if (evalsUsed >= budget) {
        return { content: [{ type: "text" as const, text: `BUDGET EXHAUSTED (${budget}/${budget}). Reply with your final summary.` }], details: undefined };
      }
      evalsUsed++;
      lastCode = code;
      let r: KernelEvalResult;
      try {
        r = await c.server.evalKernel(c.level, c.problemId, code);
      } catch (e: any) {
        return { content: [{ type: "text" as const, text: `eval error: ${e?.message || e}` }], details: undefined, isError: true };
      }
      if (r.correct && r.speedup > best.speedup) { best.code = code; best.speedup = r.speedup; }
      return { content: [{ type: "text" as const, text: fmt(r, evalsUsed, budget) }], details: undefined, isError: !r.correct };
    },
  });

  const userPrompt = [
    `# KernelBench ${c.pid}`,
    `You have ${budget} submit calls. Write a faster, numerically-correct ModelNew.`,
    ``,
    c.refBlock,
    ``,
    `Write ModelNew (same forward signature/numerics) with a custom kernel, submit it, then optimize.`,
  ].join("\n");

  let scratchDir: string | undefined;
  const sessionOpts: any = { model: c.model, thinkingLevel: "low", customTools: [submit], systemPrompt: c.systemPrompt };
  if (SCRATCH_ON) {
    scratchDir = mkdtempSync(join(tmpdir(), "openrsi-scratch-"));
    sessionOpts.cwd = scratchDir;
    sessionOpts.sessionManager = SessionManager.inMemory(scratchDir);
  } else {
    sessionOpts.noTools = "builtin";
    sessionOpts.sessionManager = SessionManager.inMemory(process.cwd());
  }
  const { session } = await createAgentSession(sessionOpts);

  const timeoutMs = Number(process.env.OPENRSI_SOLVE_TIMEOUT_S || 360) * 1000;
  let error: string | undefined;
  try {
    let timedOut = false;
    const timer = new Promise<void>((res) => setTimeout(() => { timedOut = true; session.abort().catch(() => {}); res(); }, timeoutMs));
    await Promise.race([(async () => { await session.prompt(userPrompt); await session.waitForIdle(); })(), timer]);
    if (timedOut) error = `solve timed out after ${timeoutMs / 1000}s`;
  } catch (e: any) {
    error = e?.message || String(e);
  } finally {
    if (scratchDir) { try { rmSync(scratchDir, { recursive: true, force: true }); } catch { /* best effort */ } }
  }

  const stats = session.getSessionStats() as any;
  return {
    bestCode: best.code ?? lastCode,
    bestValid: best.code !== null,
    bestScore: best.code ? best.speedup : 0,
    evalsUsed,
    cost: stats?.cost ?? 0,
    error,
  };
}
