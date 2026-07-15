/**
 * Inner solver for KernelBench: one AIDE-style agent writes a `ModelNew` kernel for
 * one problem, iterating on eval feedback (compiled / correct / speedup) under a budget.
 * Returns a SolveResult-shaped object (performance = best speedup) so the generational
 * loop, board, and critique reuse unchanged. Fitness = speedup; correctness is the gate.
 */
import { Type } from "typebox";
import { createAgentSession, defineTool, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";
import type { Scaffold } from "../inner/scaffold.js";
import type { SolveResult } from "../inner/solve.js";
import { composeSystemPrompt } from "../inner/scaffold.js";
import { KernelEvalServer, type KernelEvalResult } from "./evalClient.js";

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
        r = await server.evalKernel(level, problemId, code);
      } catch (e: any) {
        return { content: [{ type: "text" as const, text: `eval error: ${e?.message || e}` }], details: undefined, isError: true };
      }
      if (r.correct && r.speedup > best.speedup) { best.code = code; best.speedup = r.speedup; }
      return { content: [{ type: "text" as const, text: fmt(r, evalsUsed, budget) }], details: undefined, isError: !r.correct };
    },
  });

  const userPrompt = [
    `# KernelBench ${pid}`,
    `You have ${budget} submit calls. Write a faster, numerically-correct ModelNew.`,
    ``,
    `## Reference PyTorch module (Model)`,
    "```python",
    ref_src,
    "```",
    ``,
    `Write ModelNew (same forward signature/numerics) with a custom kernel, submit it, then optimize.`,
  ].join("\n");

  const { session } = await createAgentSession({
    model,
    thinkingLevel: "low",
    customTools: [submit],
    noTools: "builtin",
    systemPrompt: composeSystemPrompt(scaffold),
    sessionManager: SessionManager.inMemory(process.cwd()),
  } as any);

  const timeoutMs = Number(process.env.OPENRSI_SOLVE_TIMEOUT_S || 360) * 1000;
  let error: string | undefined;
  try {
    let timedOut = false;
    const timer = new Promise<void>((res) => setTimeout(() => { timedOut = true; session.abort().catch(() => {}); res(); }, timeoutMs));
    await Promise.race([(async () => { await session.prompt(userPrompt); await session.waitForIdle(); })(), timer]);
    if (timedOut) error = `solve timed out after ${timeoutMs / 1000}s`;
  } catch (e: any) {
    error = e?.message || String(e);
  }

  const stats = session.getSessionStats() as any;
  return {
    problemId: pid,
    scoreType: "speedup",
    evalsUsed,
    bestPublicScore: best.code ? best.speedup : null,
    bestValid: best.code !== null,
    performance: best.code ? best.speedup : 0, // fitness = speedup (0 if never correct)
    rank: null,
    privateScore: best.code ? best.speedup : null,
    privateJudge: best.code ? "correct" : "incorrect",
    bestCode: best.code ?? lastCode,
    cost: stats?.cost ?? 0,
    error,
  };
}
