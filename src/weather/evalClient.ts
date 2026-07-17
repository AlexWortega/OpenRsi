/**
 * WeatherBench-2 eval runner: writes an agent-authored `model.py` (which must define
 * train_and_predict(Xtr,Ytr,Xte,meta,time_budget_s,device)) into a work dir, runs the
 * fixed harness `run_model.py` under a FIXED COMPUTE BUDGET on one GPU, and parses the
 * area-weighted RMSE + persistence skill score. Runs co-located on eva01.
 */
import { execFile } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

export interface WeatherEvalResult {
  ok: boolean;
  skill: number; // persistence skill score: 1 - mean(rmse_ch/pers_ch); >0 beats persistence
  rmse_z500: number;
  rmse_t850: number;
  pers_z500: number;
  pers_t850: number;
  train_s: number;
  budget_s?: number;
  overran: boolean;
  error?: string;
}

const PY = process.env.OPENRSI_WB_PYTHON || "python3";
const RUN = process.env.OPENRSI_WB_RUNNER || "/mnt/storage/wb2/run_model.py";
const WORK = process.env.OPENRSI_WB_WORK || "/mnt/storage/wb2/work";

export class WeatherEvalServer {
  constructor(
    private budgetS = Number(process.env.OPENRSI_WB_TRAIN_S || 120),
    private gpu = process.env.OPENRSI_WB_GPU || "3",
  ) {}

  get trainBudgetS(): number {
    return this.budgetS;
  }

  /** Train + score one candidate model.py under the fixed compute budget. */
  evalModel(code: string): Promise<WeatherEvalResult> {
    const dir = mkdtempSync(join(WORK, "m-"));
    writeFileSync(join(dir, "model.py"), code);
    // Hard wall-clock kill = train budget + generous margin for data load + scoring.
    const timeoutMs = (this.budgetS + 180) * 1000;
    return new Promise((resolve) => {
      execFile(
        PY,
        [RUN, dir, String(this.budgetS), this.gpu],
        { timeout: timeoutMs, maxBuffer: 8 * 1024 * 1024, killSignal: "SIGKILL" },
        (err, stdout, stderr) => {
          try { rmSync(dir, { recursive: true, force: true }); } catch { /* best effort */ }
          const lines = (stdout || "").trim().split("\n").filter(Boolean);
          const last = lines[lines.length - 1] || "";
          try {
            const j = JSON.parse(last);
            resolve(j as WeatherEvalResult);
          } catch {
            const msg = err ? `${(err as any).killed ? "TIMEOUT/killed" : "exit"} ${err.message}` : "no JSON";
            resolve({ ok: false, skill: -1, rmse_z500: 0, rmse_t850: 0, pers_z500: 0, pers_t850: 0, train_s: 0, overran: false, error: `${msg}; stderr=${(stderr || "").slice(-400)}` });
          }
        },
      );
    });
  }
}
