/**
 * Inner solver: run one AIDE-style agent on ONE ALE-Bench problem.
 *
 * Two solver modes, chosen by OPENRSI_SOLVER (default "nudge"):
 *   - "nudge" : one agent iterates with a budget of `submit` calls, nudged to keep
 *               using its budget until convergence. (The original, validated path.)
 *   - "aide"  : an explicit draft/improve/debug tree search (src/inner/aideTree.ts).
 *
 * Either way the agent iterates on `public_eval` (cheap, visible score), then we spend
 * the session's single `private_eval` on its best VALID solution to get the held-out
 * performance — the fitness the outer RSI loop selects on. Per-genre domain knowledge
 * (scaffold.domain_knowledge_by_genre) and an optional scratch shell (OPENRSI_SCRATCH)
 * apply to both modes.
 */
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { Type } from "typebox";
import { createAgentSession, defineTool, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";
import { AleEvalServer, betterScore, type AleEvalResult } from "../ale/evalServer.js";
import { composeSystemPrompt, type Scaffold } from "./scaffold.js";
import { recall, reflectAndStore } from "../memory/memory.js";
import { classifyGenre } from "../genre.js";
import { generateSolution, solveAideTree, SCRATCH_ON, type AideNode } from "./aideTree.js";

const MEMORY_ON = (process.env.OPENRSI_MEMORY ?? "on") !== "off";
const SOLVER = (process.env.OPENRSI_SOLVER ?? "nudge").toLowerCase();

export interface SolveResult {
  problemId: string;
  scoreType: string;
  evalsUsed: number;
  bestPublicScore: number | null;
  bestValid: boolean;
  // Fitness (held-out):
  performance: number | null;
  rank: number | null;
  privateScore: number | null;
  privateJudge: string | null;
  bestCode: string;
  cost: number;
  genre?: string;
  solver?: string;
  error?: string;
}

function fmtFeedback(r: AleEvalResult, used: number, budget: number): string {
  const lines: string[] = [];
  lines.push(`score(${r.score_type}) = ${r.overall_absolute_score}  judge = ${r.overall_judge_result}`);
  lines.push(`cases: ${JSON.stringify(r.judge_counts)} (AC ${r.num_ac}/${r.num_cases})`);
  if (r.compile_error) lines.push(`COMPILE ERROR:\n${r.compile_error}`);
  if (r.case_errors?.length) {
    lines.push(`failing cases (sample):`);
    for (const e of r.case_errors as any[]) {
      lines.push(`  - ${e.judge} t=${e.time?.toFixed?.(2)}s ${e.error ? "err=" + e.error : ""}`);
    }
  }
  lines.push(`evals used ${used}/${budget}${used >= budget ? " — BUDGET EXHAUSTED, finalize now" : ""}`);
  return lines.join("\n");
}

function isValid(r: AleEvalResult): boolean {
  return (r.num_cases ?? 0) > 0 && r.num_ac === r.num_cases;
}

export async function solveProblem(opts: {
  evalServer: AleEvalServer;
  problemId: string;
  scaffold: Scaffold;
  model: Model<any>;
  numWorkers?: number;
  lite?: boolean;
  sessionSeconds?: number;
  thinkingLevel?: "low" | "medium" | "high";
}): Promise<SolveResult> {
  const { evalServer, problemId, scaffold, model } = opts;
  const lang = scaffold.language;
  const budget = Number(process.env.OPENRSI_EVAL_CAP || Math.max(scaffold.max_public_evals, 12));

  const { sessionId, problem } = await evalServer.openSession({
    problemId,
    lite: opts.lite ?? true,
    numWorkers: opts.numWorkers ?? 8,
    sessionSeconds: opts.sessionSeconds,
  });
  const scoreType = problem.score_type;

  // Per-genre routing: classify once, inject genre-specific tips + prefer same-genre memory.
  const genre = await classifyGenre({ model, benchmark: "ale", problemId, text: problem.statement ?? problemId }).catch(() => "other");
  const memoryBlock = MEMORY_ON ? recall("ale", problemId, 6, genre) : "";
  const systemPrompt = composeSystemPrompt(scaffold, genre) + memoryBlock;

  const t0 = Date.now();
  const el = () => ((Date.now() - t0) / 1000).toFixed(0).padStart(4) + "s";
  const log = (m: string) => process.stderr.write(`[solve ${problemId} ${el()}] ${m}\n`);

  const statement = [
    `# Problem ${problemId} (score type: ${scoreType})`,
    ``,
    `## Statement`,
    problem.statement ?? "(statement unavailable)",
    problem.constraints ? `\n## Constraints\n${problem.constraints}` : "",
  ].join("\n");

  const common = { sessionId, scoreType, lang, budget, genre, systemPrompt, statement, evalServer, model, problemId, scaffold, log };

  const inner = SOLVER === "aide" ? await runAide(common) : await runNudge(common, opts.thinkingLevel);

  // Fitness: single private_eval on the best valid solution (fallback: last code).
  const finalCode = inner.bestCode;
  let performance: number | null = null;
  let rank: number | null = null;
  let privateScore: number | null = null;
  let privateJudge: string | null = null;
  let error = inner.error;
  if (finalCode) {
    try {
      const pr = await evalServer.privateEval(sessionId, finalCode, lang);
      performance = (pr.performance ?? null) as number | null;
      rank = (pr.rank ?? null) as number | null;
      privateScore = Number(pr.overall_absolute_score ?? 0);
      privateJudge = (pr.overall_judge_result as string) ?? null;
    } catch (e: any) {
      error = (error ? error + "; " : "") + `private_eval: ${e?.message || e}`;
    }
  }

  await evalServer.closeSession(sessionId);

  if (MEMORY_ON && finalCode) {
    const score = performance ?? inner.bestPublicScore ?? 0;
    const transcript = `Score type ${scoreType} (genre ${genre}, solver ${SOLVER}). Used ${inner.evalsUsed} submissions; best valid=${inner.bestValid}. ` +
      `Final private judge=${privateJudge ?? "n/a"} performance=${performance ?? "n/a"}.\nBest solution (excerpt):\n${finalCode.slice(0, 900)}`;
    await reflectAndStore({ model, benchmark: "ale", problemId, score: Number(score) || 0, transcript, genre }).catch(() => {});
  }

  return {
    problemId,
    scoreType,
    evalsUsed: inner.evalsUsed,
    bestPublicScore: inner.bestValid ? inner.bestPublicScore : null,
    bestValid: inner.bestValid,
    performance,
    rank,
    privateScore,
    privateJudge,
    bestCode: finalCode,
    cost: inner.cost,
    genre,
    solver: SOLVER,
    error,
  };
}

interface Common {
  sessionId: string;
  scoreType: string;
  lang: string;
  budget: number;
  genre: string;
  systemPrompt: string;
  statement: string;
  evalServer: AleEvalServer;
  model: Model<any>;
  problemId: string;
  scaffold: Scaffold;
  log: (m: string) => void;
}

interface InnerResult {
  bestCode: string;
  bestValid: boolean;
  bestPublicScore: number | null;
  evalsUsed: number;
  cost: number;
  error?: string;
}

/** AIDE tree-search inner loop (OPENRSI_SOLVER=aide). */
async function runAide(c: Common): Promise<InnerResult> {
  const draftN = Number(process.env.OPENRSI_INNER_CANDIDATES || 3);
  const patience = Number(process.env.OPENRSI_PATIENCE || 4);
  const evalCache = new Map<string, AleEvalResult>();
  let evalsUsed = 0;

  const normalize = (abs: number) => (/min/i.test(c.scoreType) ? -abs : abs);

  const generate = async (kind: string, parent: AideNode | null, memory: string) => {
    let user: string;
    if (kind === "draft" || !parent) {
      user = `${c.statement}\n\nWrite a CORRECT baseline that always emits valid output within the time limit, then make it as strong as you can (local search / simulated annealing under a precise wall-clock timer). Output format must be exact.`;
    } else if (kind === "debug") {
      user = `${c.statement}\n\nThe following solution is INVALID or failing (it must be fixed before it can score):\n\n\`\`\`${c.lang}\n${parent.code}\n\`\`\`\n\nEval feedback:\n${parent.feedback}\n\nProduce a corrected version that compiles and produces valid output on every case. Fix the root cause; do not regress working logic.`;
    } else {
      user = `${c.statement}\n\nHere is the current best VALID solution (normalized score ${parent.score.toFixed(2)}):\n\n\`\`\`${c.lang}\n${parent.code}\n\`\`\`\n\nEval feedback:\n${parent.feedback}\n\nProduce a STRONGER version that raises the score (deeper local search, better time usage, better neighbourhoods) while staying valid. Keep what works.`;
    }
    return generateSolution({ model: c.model, language: c.lang, systemPrompt: c.systemPrompt, userPrompt: user + memory, log: c.log });
  };

  const evalFn = async (code: string) => {
    const r = await c.evalServer.publicEval(c.sessionId, code, c.lang);
    evalCache.set(code, r);
    const abs = Number(r.overall_absolute_score ?? 0);
    return { valid: isValid(r), score: isValid(r) ? normalize(abs) : -Infinity, feedback: fmtFeedback(r, ++evalsUsed, c.budget), error: r.compile_error };
  };

  const tree = await solveAideTree({ budget: c.budget, draftN, patience, generate, evalFn, log: c.log });
  const bestR = tree.bestCode ? evalCache.get(tree.bestCode) : undefined;
  return {
    bestCode: tree.bestCode,
    bestValid: tree.bestValid,
    bestPublicScore: bestR ? Number(bestR.overall_absolute_score ?? 0) : null,
    evalsUsed: tree.evalsUsed,
    cost: tree.cost,
  };
}

/** Original single-agent "nudge" inner loop (default). */
async function runNudge(c: Common, thinkingLevel?: "low" | "medium" | "high"): Promise<InnerResult> {
  const patience = Number(process.env.OPENRSI_PATIENCE || 4);
  let sinceImprove = 0;
  let evalsUsed = 0;
  let lastCode = "";
  const best: { code: string | null; score: number } = { code: null, score: 0 };

  const submit = defineTool({
    name: "submit",
    label: "submit",
    description:
      "Compile and run your full source on the public test cases. Returns your score, per-case judge results, and any compile/runtime errors. Use it to iterate. You have a limited number of calls.",
    parameters: Type.Object({
      code: Type.String({ description: "Complete source code (a single file) in " + c.lang }),
    }),
    async execute(_id, { code }) {
      if (evalsUsed >= c.budget || sinceImprove >= patience) {
        const why = evalsUsed >= c.budget ? `hard cap ${c.budget} reached` : `converged (${sinceImprove} submits with no improvement)`;
        return { content: [{ type: "text" as const, text: `STOP: ${why}. Do not submit again — reply with your final summary.` }], details: undefined };
      }
      evalsUsed++;
      lastCode = code;
      let r: AleEvalResult;
      try {
        r = await c.evalServer.publicEval(c.sessionId, code, c.lang);
      } catch (e: any) {
        return { content: [{ type: "text" as const, text: `eval error: ${e?.message || e}` }], details: undefined, isError: true };
      }
      const valid = isValid(r);
      const score = Number(r.overall_absolute_score ?? 0);
      if (valid && (best.code === null || betterScore(score, best.score, c.scoreType))) {
        best.code = code;
        best.score = score;
        sinceImprove = 0;
      } else {
        sinceImprove++;
      }
      return { content: [{ type: "text" as const, text: fmtFeedback(r, evalsUsed, c.budget) }], details: undefined, isError: !valid };
    },
  });

  const userPrompt = [
    `# Problem ${c.problemId} (score type: ${c.scoreType})`,
    `You have ${c.budget} \`submit\` calls. Output format must be exact.`,
    ``,
    c.statement,
    ``,
    `Begin: write a correct baseline, submit it, then improve until the budget is spent.`,
  ].join("\n");

  // Optional scratch shell: private temp cwd + built-in bash/read/write/edit so the
  // agent can compile & test locally (free) before spending a `submit`.
  let scratchDir: string | undefined;
  const sessionOpts: any = { model: c.model, thinkingLevel: thinkingLevel ?? "low", customTools: [submit], systemPrompt: c.systemPrompt };
  if (SCRATCH_ON) {
    scratchDir = mkdtempSync(join(tmpdir(), "openrsi-scratch-"));
    sessionOpts.cwd = scratchDir;
    sessionOpts.sessionManager = SessionManager.inMemory(scratchDir);
  } else {
    sessionOpts.noTools = "builtin";
    sessionOpts.sessionManager = SessionManager.inMemory(process.cwd());
  }
  const { session } = await createAgentSession(sessionOpts);

  const unsub = session.subscribe((e: any) => {
    switch (e.type) {
      case "turn_start": c.log(`turn_start`); break;
      case "tool_execution_start": c.log(`tool_start ${e.toolName ?? e.name ?? "?"}`); break;
      case "tool_execution_end": c.log(`tool_end   ${e.toolName ?? e.name ?? "?"}`); break;
      case "auto_retry_start": c.log(`AUTO_RETRY attempt=${e.attempt}/${e.maxAttempts} err=${String(e.errorMessage).slice(0, 120)}`); break;
      case "agent_end": c.log(`agent_end willRetry=${e.willRetry}`); break;
    }
  });

  const timeoutMs = Number(process.env.OPENRSI_SOLVE_TIMEOUT_S || 300) * 1000;
  let timedOut = false;
  let error: string | undefined;
  try {
    const timer = new Promise<void>((resolve) =>
      setTimeout(() => {
        timedOut = true;
        c.log(`WATCHDOG timeout after ${timeoutMs / 1000}s — aborting`);
        session.abort().catch(() => {});
        resolve();
      }, timeoutMs),
    );
    const maxNudges = Number(process.env.OPENRSI_MAX_NUDGES || c.budget);
    const run = async () => {
      await session.prompt(userPrompt);
      await session.waitForIdle();
      for (let n = 0; n < maxNudges && !timedOut && evalsUsed < c.budget && sinceImprove < patience; n++) {
        c.log(`nudge ${n + 1}: ${evalsUsed} evals, sinceImprove=${sinceImprove}/${patience}, continuing`);
        await session.prompt(
          `Keep going — you have budget left and your score can still improve. Take your best solution, make it stronger (deeper local search / better time usage / fix any failing cases), and submit again.`,
        );
        await session.waitForIdle();
      }
    };
    await Promise.race([run(), timer]);
    if (timedOut) error = `solve timed out after ${timeoutMs / 1000}s`;
  } catch (e: any) {
    error = e?.message || String(e);
  } finally {
    unsub();
    if (scratchDir) { try { rmSync(scratchDir, { recursive: true, force: true }); } catch { /* best effort */ } }
  }

  const stats = session.getSessionStats() as any;
  return {
    bestCode: best.code ?? lastCode,
    bestValid: best.code !== null,
    bestPublicScore: best.code !== null ? best.score : null,
    evalsUsed,
    cost: stats?.cost ?? 0,
    error,
  };
}
