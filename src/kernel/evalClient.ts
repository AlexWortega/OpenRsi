/**
 * TS client + lifecycle for the Python KernelBench eval server (benches/kernel/eval_server.py).
 * Runs co-located on the GPU pod; the inner solver hits it over localhost.
 */
import { spawn, type ChildProcess } from "node:child_process";
import { setTimeout as sleep } from "node:timers/promises";

export interface KernelEvalResult {
  compiled: boolean;
  correct: boolean;
  speedup: number;
  runtime_us: number | null;
  ref_us: number | null;
  error: string;
}

const PY = process.env.OPENRSI_KB_PYTHON || "python";
const SERVER = process.env.OPENRSI_KB_SERVER || "/workspace/openrsi/benches/kernel/eval_server.py";
const KB_SRC = process.env.OPENRSI_KB_PYTHONPATH || "/workspace/KernelBench/src";
const CUDA_BIN = "/usr/local/cuda/bin";

export class KernelEvalServer {
  private proc?: ChildProcess;
  private base: string;
  constructor(private port = Number(process.env.OPENRSI_KB_PORT || 8147), host = "127.0.0.1") {
    this.base = `http://${host}:${this.port}`;
  }

  async start(): Promise<void> {
    this.proc = spawn(PY, [SERVER, "--port", String(this.port)], {
      stdio: ["ignore", "pipe", "pipe"],
      env: {
        ...process.env,
        PYTHONPATH: `${KB_SRC}:${process.env.PYTHONPATH || ""}`,
        PATH: `${CUDA_BIN}:${process.env.PATH || ""}`,
      },
    });
    this.proc.stdout?.on("data", (d) => process.stderr.write(`[kb] ${d}`));
    this.proc.stderr?.on("data", (d) => process.stderr.write(`[kb-err] ${d}`));
    this.proc.on("exit", (c) => process.stderr.write(`[kb] server exited code=${c}\n`));
    for (let i = 0; i < 120; i++) {
      try {
        if ((await fetch(`${this.base}/health`)).ok) return;
      } catch { /* not up */ }
      await sleep(1000);
    }
    throw new Error("kernel eval server did not become healthy");
  }

  private async post<T>(path: string, body: unknown): Promise<T> {
    const r = await fetch(`${this.base}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const txt = await r.text();
    let j: any;
    try { j = JSON.parse(txt); } catch { throw new Error(`kb ${path} non-JSON: ${txt.slice(0, 200)}`); }
    if (!r.ok) throw new Error(`kb ${path} ${r.status}: ${j.error || txt.slice(0, 200)}`);
    return j as T;
  }

  async openSession(level: number, problemId: number): Promise<{ ref_src: string }> {
    return this.post("/session", { level, problem_id: problemId });
  }

  evalKernel(level: number, problemId: number, code: string): Promise<KernelEvalResult> {
    return this.post("/eval", { level, problem_id: problemId, code });
  }

  async stop(): Promise<void> {
    this.proc?.kill("SIGTERM");
    await sleep(200);
  }
}
