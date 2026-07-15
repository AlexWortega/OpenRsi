/**
 * Inner solver: run one AIDE-style agent on ONE ALE-Bench problem.
 *
 * The agent iterates with a budget of `public_eval` calls (cheap, visible score),
 * then we spend the session's single `private_eval` on its best VALID solution to
 * get the held-out performance — the fitness the outer RSI loop selects on.
 */
import { Type } from "typebox";
import { createAgentSession, defineTool, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";
import { AleEvalServer, betterScore, type AleEvalResult } from "../ale/evalServer.js";
import { composeSystemPrompt, type Scaffold } from "./scaffold.js";
import { recall, reflectAndStore } from "../memory/memory.js";

const MEMORY_ON = (process.env.OPENRSI_MEMORY ?? "on") !== "off";

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
  const budget = scaffold.max_public_evals;

  const { sessionId, problem } = await evalServer.openSession({
    problemId,
    lite: opts.lite ?? true,
    numWorkers: opts.numWorkers ?? 8,
    sessionSeconds: opts.sessionSeconds,
  });
  const scoreType = problem.score_type;

  let evalsUsed = 0;
  let lastCode = "";
  const best: { code: string | null; score: number } = { code: null, score: 0 };

  const submit = defineTool({
    name: "submit",
    label: "submit",
    description:
      "Compile and run your full source on the public test cases. Returns your score, per-case judge results, and any compile/runtime errors. Use it to iterate. You have a limited number of calls.",
    parameters: Type.Object({
      code: Type.String({ description: "Complete source code (a single file) in " + lang }),
    }),
    async execute(_id, { code }) {
      if (evalsUsed >= budget) {
        return {
          content: [
            {
              type: "text" as const,
              text: `BUDGET EXHAUSTED (${budget}/${budget}). Do not submit again — reply with your final summary.`,
            },
          ],
          details: undefined,
        };
      }
      evalsUsed++;
      lastCode = code;
      let r: AleEvalResult;
      try {
        r = await evalServer.publicEval(sessionId, code, lang);
      } catch (e: any) {
        return {
          content: [{ type: "text" as const, text: `eval error: ${e?.message || e}` }],
          details: undefined,
          isError: true,
        };
      }
      const valid = (r.num_cases ?? 0) > 0 && r.num_ac === r.num_cases;
      const score = Number(r.overall_absolute_score ?? 0);
      if (valid && (best.code === null || betterScore(score, best.score, scoreType))) {
        best.code = code;
        best.score = score;
      }
      return {
        content: [{ type: "text" as const, text: fmtFeedback(r, evalsUsed, budget) }],
        details: undefined,
        isError: !valid,
      };
    },
  });

  const userPrompt = [
    `# Problem ${problemId} (score type: ${scoreType})`,
    `You have ${budget} \`submit\` calls. Output format must be exact.`,
    ``,
    `## Statement`,
    problem.statement ?? "(statement unavailable)",
    problem.constraints ? `\n## Constraints\n${problem.constraints}` : "",
    ``,
    `Begin: write a correct baseline, submit it, then improve until the budget is spent.`,
  ].join("\n");

  const memoryBlock = MEMORY_ON ? recall("ale", problemId) : "";
  const { session } = await createAgentSession({
    model,
    thinkingLevel: opts.thinkingLevel ?? "low",
    customTools: [submit],
    noTools: "builtin",
    systemPrompt: composeSystemPrompt(scaffold) + memoryBlock,
    sessionManager: SessionManager.inMemory(process.cwd()),
  } as any);

  // Live event logging so a run is observable (and stalls are visible).
  const t0 = Date.now();
  const el = () => ((Date.now() - t0) / 1000).toFixed(0).padStart(4) + "s";
  const log = (m: string) => process.stderr.write(`[solve ${problemId} ${el()}] ${m}\n`);
  const unsub = session.subscribe((e: any) => {
    switch (e.type) {
      case "turn_start": log(`turn_start`); break;
      case "tool_execution_start": log(`tool_start ${e.toolName ?? e.name ?? "?"}`); break;
      case "tool_execution_end": log(`tool_end   ${e.toolName ?? e.name ?? "?"}`); break;
      case "auto_retry_start": log(`AUTO_RETRY attempt=${e.attempt}/${e.maxAttempts} err=${String(e.errorMessage).slice(0, 120)}`); break;
      case "agent_end": log(`agent_end willRetry=${e.willRetry}`); break;
    }
  });

  // Watchdog: abort a stalled solve so one problem can't hang the RSI loop.
  const timeoutMs = Number(process.env.OPENRSI_SOLVE_TIMEOUT_S || 300) * 1000;
  let timedOut = false;
  let error: string | undefined;
  try {
    const timer = new Promise<void>((resolve) =>
      setTimeout(() => {
        timedOut = true;
        log(`WATCHDOG timeout after ${timeoutMs / 1000}s — aborting`);
        session.abort().catch(() => {});
        resolve();
      }, timeoutMs),
    );
    // Optional budget-nudge (default OFF): a harness lever to cut early-stopping
    // variance. Kept off for the headline run so the RSI loop must EARN budget-usage
    // improvements itself (as it did in validation). Enable via OPENRSI_MAX_NUDGES.
    const maxNudges = Number(process.env.OPENRSI_MAX_NUDGES ?? 0);
    const run = async () => {
      await session.prompt(userPrompt);
      await session.waitForIdle();
      for (let n = 0; n < maxNudges && !timedOut && evalsUsed < budget; n++) {
        log(`nudge ${n + 1}: ${evalsUsed}/${budget} evals used, continuing`);
        await session.prompt(
          `You still have ${budget - evalsUsed} submit call(s) left. Do NOT stop — take your current best solution and improve it further, then submit again.`,
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
  }

  const stats = session.getSessionStats() as any;
  const cost = stats?.cost ?? 0;

  // Fitness: single private_eval on the best valid solution (fallback: last code).
  const finalCode = best.code ?? lastCode;
  let performance: number | null = null;
  let rank: number | null = null;
  let privateScore: number | null = null;
  let privateJudge: string | null = null;
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

  // Reflect the session into durable memory (best-effort; recalled on future problems).
  if (MEMORY_ON && finalCode) {
    const score = performance ?? (best.code ? best.score : 0);
    const transcript = `Score type ${scoreType}. Used ${evalsUsed} submissions; best valid=${best.code !== null}. ` +
      `Final private judge=${privateJudge ?? "n/a"} performance=${performance ?? "n/a"}.\nBest solution (excerpt):\n${finalCode.slice(0, 900)}`;
    await reflectAndStore({ model, benchmark: "ale", problemId, score: Number(score) || 0, transcript }).catch(() => {});
  }

  return {
    problemId,
    scoreType,
    evalsUsed,
    bestPublicScore: best.code !== null ? best.score : null,
    bestValid: best.code !== null,
    performance,
    rank,
    privateScore,
    privateJudge,
    bestCode: finalCode,
    cost,
    error,
  };
}
