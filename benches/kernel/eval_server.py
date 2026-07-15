#!/usr/bin/env python3
"""
KernelBench eval server for OpenRSI (runs on a GPU pod).

Long-lived HTTP server that loads KernelBench reference architectures and evaluates
candidate `ModelNew` kernels against them (compile + correctness + speedup). The TS
orchestrator's inner solver hits it over localhost.

Routes (POST, JSON):
  POST /session {level, problem_id}                 -> {name, ref_src, ...}
  POST /eval    {level, problem_id, code, backend,  -> {compiled, correct, speedup,
                 num_correct_trials, num_perf_trials}    runtime_us, ref_us, error}
  GET  /health

Run:  PYTHONPATH=<KernelBench>/src python eval_server.py --port 8147
Env:  needs a CUDA GPU + nvcc on PATH.
"""
import argparse
import json
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from kernelbench.eval import (  # type: ignore
    eval_kernel_against_ref,
    fetch_ref_arch_from_level_problem_id,
)

_LOCK = threading.Lock()
_REF: dict[str, str] = {}  # (level,problem_id) -> ref source


def _ref_src(level: int, problem_id: int) -> str:
    key = f"{level}/{problem_id}"
    with _LOCK:
        if key not in _REF:
            _REF[key] = fetch_ref_arch_from_level_problem_id(level, problem_id)
    return _REF[key]


def _eval(level: int, problem_id: int, code: str, backend: str,
          n_correct: int, n_perf: int) -> dict:
    ref_src = _ref_src(level, problem_id)
    try:
        r = eval_kernel_against_ref(
            ref_src, code,
            num_correct_trials=n_correct,
            num_perf_trials=n_perf,
            measure_performance=True,
            backend=backend,
            check_for_excessive_speedup=True,  # reward-hacking guard
        )
    except Exception as e:  # compile/exec failure surfaced as structured feedback
        return {
            "compiled": False, "correct": False, "speedup": 0.0,
            "runtime_us": None, "ref_us": None,
            "error": f"{type(e).__name__}: {e}"[:1500],
        }
    speedup = (r.ref_runtime / r.runtime) if (r.runtime and r.runtime > 0 and r.ref_runtime > 0) else 0.0
    meta = r.metadata or {}
    err = ""
    for k in ("compilation_error", "runtime_error", "correctness_issue", "error", "warning"):
        if meta.get(k):
            err += f"{k}: {str(meta[k])[:600]}\n"
    return {
        "compiled": bool(r.compiled),
        "correct": bool(r.correctness),
        "speedup": round(float(speedup), 4),
        "runtime_us": round(float(r.runtime), 3) if r.runtime and r.runtime > 0 else None,
        "ref_us": round(float(r.ref_runtime), 3) if r.ref_runtime and r.ref_runtime > 0 else None,
        "error": err.strip()[:1500],
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code: int, obj: dict):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length", 0) or 0)
        return json.loads(self.rfile.read(n) or b"{}") if n else {}

    def do_GET(self):
        self._send(200 if self.path == "/health" else 404, {"ok": self.path == "/health"})

    def do_POST(self):
        try:
            req = self._body()
            if self.path == "/session":
                src = _ref_src(int(req["level"]), int(req["problem_id"]))
                self._send(200, {"level": req["level"], "problem_id": req["problem_id"], "ref_src": src})
            elif self.path == "/eval":
                print(f"[kb_eval] eval level={req.get('level')} pid={req.get('problem_id')} code_len={len(req.get('code',''))}", flush=True)
                out = _eval(
                    int(req["level"]), int(req["problem_id"]), req["code"],
                    req.get("backend", "cuda"),
                    int(req.get("num_correct_trials", 5)),
                    int(req.get("num_perf_trials", 100)),
                )
                self._send(200, out)
            else:
                self._send(404, {"error": "not found"})
        except Exception as e:
            self._send(500, {"error": str(e), "trace": traceback.format_exc()[-1500:]})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8147)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"[kb_eval_server] listening on http://{args.host}:{args.port}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
