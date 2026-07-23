/**
 * Inner solver for WeatherBench-2: the agent builds the BEST forecasting model it can
 * under a FIXED COMPUTE BUDGET. It writes a `model.py` (defining train_and_predict),
 * which is trained for `time_budget_s` on one GPU and scored by area-weighted RMSE /
 * persistence skill. Returns a SolveResult (performance = persistence skill score) so
 * the generational RSI loop, board, and critique reuse unchanged.
 */
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { Type } from "typebox";
import { createAgentSession, defineTool, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";

const RECON_ON = (process.env.OPENRSI_WB_RECON ?? "off") === "on";
const DATA_NPZ = process.env.OPENRSI_WB_DATA || "/mnt/storage/wb2/data/wb2_72h.npz";
import type { Scaffold } from "../inner/scaffold.js";
import type { SolveResult } from "../inner/solve.js";
import { composeSystemPrompt } from "../inner/scaffold.js";
import { WeatherEvalServer, type WeatherEvalResult } from "./evalClient.js";
import { recall, reflectAndStore } from "../memory/memory.js";

const MEMORY_ON = (process.env.OPENRSI_MEMORY ?? "on") !== "off";

const CONTRACT = `Write a single Python file that defines EXACTLY this function:

    def train_and_predict(Xtr, Ytr, Xte, meta, time_budget_s, device):
        # Xtr, Ytr: float32 (Ntr, 2, 32, 64) — channels [z500 geopotential, t850 temperature]
        #   Xtr = state at init (00/12 UTC); Ytr = same fields 72h later (the target).
        # Xte: float32 (Nte, 2, 32, 64) — test init states (year 2020).
        # meta: dict with 'mean','std' (1,2,1,1), 'lat' (32,), 'lon' (64,), 'channels'.
        # time_budget_s: FIXED wall-clock training budget on ONE gpu — train within it.
        # device: 'cuda'. Return Yte_pred float32 (Nte, 2, 32, 64) = your 72h forecast.
        return Yte_pred

Rules: use only numpy/torch (both installed). Respect time_budget_s (check time.time() in your
train loop and stop before it). Longitude is PERIODIC (use circular padding on the lon axis, size 64);
latitude weights are cos(lat). Predictions must be finite. You are scored by area-weighted RMSE;
fitness = persistence skill = 1 - mean(rmse_ch / persistence_ch), so >0 means you beat persistence.`;

function fmt(r: WeatherEvalResult, used: number, budget: number): string {
  if (!r.ok) return `FAILED: ${r.error}\nevals ${used}/${budget}`;
  return [
    `skill=${r.skill.toFixed(4)}${r.repeats && r.repeats > 1 ? ` ±${(r.skill_std ?? 0).toFixed(4)} (mean of ${r.repeats})` : ""} (>0 beats persistence)  z500_RMSE=${r.rmse_z500.toFixed(1)} (pers ${r.pers_z500.toFixed(1)})  t850_RMSE=${r.rmse_t850.toFixed(3)} (pers ${r.pers_t850.toFixed(3)})`,
    `trained ${r.train_s}s / budget ${r.budget_s ?? "?"}s${r.overran ? " — OVERRAN (respect the budget!)" : ""}`,
    `evals ${used}/${budget}${used >= budget ? " — BUDGET EXHAUSTED, finalize" : ""}`,
  ].join("\n");
}

export async function solveWeather(opts: {
  server: WeatherEvalServer;
  scaffold: Scaffold;
  model: Model<any>;
  /** Full pi coding agent (real bash/read/edit/write + recon) vs submit-only. Defaults to env. */
  recon?: boolean;
}): Promise<SolveResult> {
  const { server, scaffold, model } = opts;
  const recon = opts.recon ?? RECON_ON;
  const budget = scaffold.max_public_evals;
  const pid = "wb2_72h";
  let evalsUsed = 0;
  let lastCode = "";
  const best = { code: null as string | null, skill: -Infinity, r: null as WeatherEvalResult | null };

  const submit = defineTool({
    name: "submit",
    label: "submit",
    description:
      "Train your model.py under the fixed compute budget and score it (area-weighted RMSE + persistence skill). Iterate to MAXIMIZE skill. Limited calls.",
    parameters: Type.Object({ code: Type.String({ description: "Complete Python file defining train_and_predict(Xtr,Ytr,Xte,meta,time_budget_s,device)" }) }),
    async execute(_id, { code }) {
      if (evalsUsed >= budget) {
        return { content: [{ type: "text" as const, text: `BUDGET EXHAUSTED (${budget}/${budget}). Reply with your final summary.` }], details: undefined };
      }
      evalsUsed++;
      lastCode = code;
      const r = await server.evalModel(code);
      if (r.ok && r.skill > best.skill) { best.code = code; best.skill = r.skill; best.r = r; }
      return { content: [{ type: "text" as const, text: fmt(r, evalsUsed, budget) }], details: undefined, isError: !r.ok };
    },
  });

  const memoryBlock = MEMORY_ON ? recall("weather", pid, 6) : "";
  // #6: reconnaissance phase — a real scratch shell + explicit recon steps before spending
  // any model-train budget (explore the data, test cheap baselines, then design + submit).
  const reconBlock = recon
    ? [
        ``,
        `## RECONNAISSANCE FIRST (do this before any \`submit\`)`,
        `You have a scratch shell (bash/python/read/write) in a private temp dir. Spend your first steps on recon — it is FREE, \`submit\` is not:`,
        `1. Load the data locally: \`python3 -c "import numpy as np; d=np.load('${DATA_NPZ}'); print({k:d[k].shape for k in d.files})"\` and inspect Xtr/Ytr/Xte, meta mean/std, lat/lon, and the cos(lat) weights w.`,
        `2. Probe cheap baselines in-memory (persistence Xte; a per-(channel,latitude) residual-mean; a 1-layer linear map) and read off their area-weighted RMSE, so you know the bar and where error concentrates (mid-latitudes).`,
        `3. Measure sec/step for a candidate net at this grid to size the model to the ${server.trainBudgetS}s budget.`,
        `4. Only THEN write model.py and \`submit\`. Use the domain knowledge + your recon findings to pick the architecture and loss.`,
        ``,
      ].join("\n")
    : "";
  const userPrompt = [
    `# WeatherBench-2 — build the best 72h forecast model under a FIXED COMPUTE BUDGET (${server.trainBudgetS}s train / model)`,
    `You have ${budget} \`submit\` calls. Each trains your model.py for ${server.trainBudgetS}s on one V100 and scores it (mean over repeated seeds).`,
    reconBlock,
    CONTRACT,
    ``,
    `Baselines to beat: persistence (skill 0) and climatology (worse). ${recon ? "After recon, write" : "Write a first model, submit it, then improve"} the architecture / normalization / loss / training to raise skill within the compute budget.`,
  ].join("\n");

  let scratchDir: string | undefined;
  const sessionOpts: any = { model, thinkingLevel: "low", customTools: [submit], systemPrompt: composeSystemPrompt(scaffold) + memoryBlock };
  if (recon) {
    scratchDir = mkdtempSync(join(tmpdir(), "wb-recon-"));
    sessionOpts.cwd = scratchDir;
    sessionOpts.sessionManager = SessionManager.inMemory(scratchDir);
  } else {
    sessionOpts.noTools = "builtin";
    sessionOpts.sessionManager = SessionManager.inMemory(process.cwd());
  }
  const { session } = await createAgentSession(sessionOpts);

  const log = (m: string) => process.stderr.write(`[wb-solve] ${m}\n`);
  session.subscribe((e: any) => { if (e.type === "tool_execution_start") log(`tool ${e.toolName ?? e.name ?? "?"}`); });

  const timeoutMs = Number(process.env.OPENRSI_SOLVE_TIMEOUT_S || (server.trainBudgetS + 120) * (scaffold.max_public_evals + 2)) * 1000;
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

  if (MEMORY_ON && (best.code || lastCode)) {
    const b = best.r;
    const transcript = `WeatherBench2 72h (fixed ${server.trainBudgetS}s compute). Used ${evalsUsed} submits; best skill=${best.skill > -Infinity ? best.skill.toFixed(4) : "n/a"}` +
      (b ? ` (z500 RMSE ${b.rmse_z500.toFixed(1)}, t850 ${b.rmse_t850.toFixed(3)}).` : ".") +
      `\nBest model.py (excerpt):\n${(best.code ?? lastCode).slice(0, 900)}`;
    await reflectAndStore({ model, benchmark: "weather", problemId: pid, score: best.skill > -Infinity ? best.skill : 0, transcript }).catch(() => {});
  }

  const stats = session.getSessionStats() as any;
  const skill = best.code ? best.skill : 0;
  return {
    problemId: pid,
    scoreType: "skill",
    evalsUsed,
    bestPublicScore: best.code ? best.skill : null,
    bestValid: best.code !== null,
    performance: best.code ? skill : 0, // fitness = persistence skill score (higher=better)
    rank: null,
    privateScore: best.code ? best.skill : null,
    privateJudge: best.r ? `z500=${best.r.rmse_z500.toFixed(1)} t850=${best.r.rmse_t850.toFixed(3)}` : null,
    bestCode: best.code ?? lastCode,
    cost: stats?.cost ?? 0,
    solver: "nudge",
    error,
  };
}
