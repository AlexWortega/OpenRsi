/**
 * TS client + lifecycle manager for the Python ALE-Bench eval server
 * (benches/ale/eval_server.py). The orchestrator starts ONE server process; the
 * inner/outer loops open per-problem sessions against it over localhost HTTP.
 */
import { spawn, type ChildProcess } from "node:child_process";
import { setTimeout as sleep } from "node:timers/promises";

export interface AleCaseError {
  judge: string;
  error: string;
  time?: number;
  score?: number | null;
}

export interface AleEvalResult {
  overall_absolute_score?: number | null;
  overall_relative_score?: number | null;
  overall_judge_result?: string;
  score_type: string;
  num_cases?: number;
  num_ac?: number;
  judge_counts?: Record<string, number>;
  compile_error?: string;
  case_errors?: AleCaseError[];
  case_scores?: (number | null)[];
  // private only:
  rank?: number;
  performance?: number;
}

export interface ProblemPayload {
  problem_id: string;
  score_type: string;
  num_public_cases: number | null;
  num_private_cases: number | null;
  statement: string | null;
  constraints: string | null;
}

const PY = process.env.OPENRSI_PYTHON || "/mnt/storage/openrsi/.venv/bin/python";
const SERVER_PY =
  process.env.OPENRSI_ALE_SERVER ||
  new URL("../../benches/ale/eval_server.py", import.meta.url).pathname;

export class AleEvalServer {
  private proc?: ChildProcess;
  private base: string;
  constructor(private port = Number(process.env.OPENRSI_ALE_PORT || 8137), host = "127.0.0.1") {
    this.base = `http://${host}:${this.port}`;
  }

  async start(): Promise<void> {
    this.proc = spawn(PY, [SERVER_PY, "--port", String(this.port)], {
      stdio: ["ignore", "pipe", "pipe"],
      env: {
        ...process.env,
        HF_HOME: process.env.HF_HOME || "/mnt/storage/openrsi/caches/hf",
      },
    });
    this.proc.stdout?.on("data", (d) => process.stderr.write(`[ale] ${d}`));
    this.proc.stderr?.on("data", (d) => process.stderr.write(`[ale-err] ${d}`));
    this.proc.on("exit", (c) => process.stderr.write(`[ale] server exited code=${c}\n`));
    // Wait for /health.
    for (let i = 0; i < 120; i++) {
      try {
        const r = await fetch(`${this.base}/health`);
        if (r.ok) return;
      } catch {
        /* not up yet */
      }
      await sleep(1000);
    }
    throw new Error("ALE eval server did not become healthy in 120s");
  }

  private async post<T>(path: string, body: unknown): Promise<T> {
    const r = await fetch(`${this.base}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const txt = await r.text();
    let json: any;
    try {
      json = JSON.parse(txt);
    } catch {
      throw new Error(`ALE ${path} returned non-JSON (${r.status}): ${txt.slice(0, 300)}`);
    }
    if (!r.ok) throw new Error(`ALE ${path} ${r.status}: ${json.error || txt.slice(0, 300)}`);
    return json as T;
  }

  async openSession(opts: {
    problemId: string;
    lite?: boolean;
    numWorkers?: number;
    sessionSeconds?: number;
  }): Promise<{ sessionId: string; problem: ProblemPayload }> {
    const res = await this.post<{ session_id: string; problem: ProblemPayload }>("/session", {
      problem_id: opts.problemId,
      lite: opts.lite ?? true,
      num_workers: opts.numWorkers ?? 8,
      session_seconds: opts.sessionSeconds,
    });
    return { sessionId: res.session_id, problem: res.problem };
  }

  publicEval(sessionId: string, code: string, lang = "cpp23"): Promise<AleEvalResult> {
    return this.post<AleEvalResult>("/public", { session_id: sessionId, code, lang });
  }

  privateEval(sessionId: string, code: string, lang = "cpp23"): Promise<AleEvalResult> {
    return this.post<AleEvalResult>("/private", { session_id: sessionId, code, lang });
  }

  async closeSession(sessionId: string): Promise<void> {
    await this.post("/close", { session_id: sessionId }).catch(() => {});
  }

  async stop(): Promise<void> {
    this.proc?.kill("SIGTERM");
    await sleep(200);
  }
}

/** Higher score is better after normalizing minimize problems. */
export function betterScore(a: number, b: number, scoreType: string): boolean {
  const min = /min/i.test(scoreType);
  return min ? a < b : a > b;
}
