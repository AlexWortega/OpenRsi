#!/usr/bin/env python3
"""
ALE-Bench eval server for OpenRSI.

A long-lived HTTP server that owns ale_bench sessions (each session holds Docker
containers, resource-usage state, and the public/private seed split). The TS
orchestrator starts ONE of these; the inner solver's tools hit it over localhost.

Why a server (not a one-shot CLI): a session is expensive to spin up and must
persist across the inner agent's many public_eval calls so resource-usage limits
and container reuse work as intended.

Routes (all POST unless noted, newline JSON body):
  POST /session   {problem_id, lite, num_workers, session_seconds} -> {session_id, problem}
  POST /public    {session_id, code, lang}                         -> {score, ...feedback}
  POST /private   {session_id, code, lang}                         -> {score, rank, performance}
  POST /problem   {session_id}                                     -> {statement, constraints, score_type}
  POST /usage     {session_id}                                     -> {current, remaining}
  POST /close     {session_id}                                     -> {ok}
  GET  /health                                                     -> {ok, sessions}

Run:  python eval_server.py --port 8137
Env:  ALE_BENCH_DATA (optional local dataset), HF_HOME (cache).
"""
import argparse
import json
import threading
import traceback
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import ale_bench  # type: ignore

_LOCK = threading.Lock()
_SESSIONS: dict[str, object] = {}
_META: dict[str, dict] = {}


def _score_type(session) -> str:
    try:
        return str(session.problem.metadata.score_type)
    except Exception:
        return "unknown"


def _jr(c) -> str:
    return str(getattr(c, "judge_result", "")).replace("JudgeResult.", "")


def _result_to_dict(session, result) -> dict:
    """Serialize an ale_bench Result into feedback the agent can act on.

    Real fields (ale_bench 1.6.0): Result has overall_absolute_score,
    overall_relative_score, overall_judge_result, case_results[]. Each CaseResult
    has absolute_score, judge_result, error_str, message, execution_time,
    output_str, memory_usage.
    """
    from collections import Counter

    out: dict = {
        "overall_absolute_score": getattr(result, "overall_absolute_score", None),
        "overall_relative_score": getattr(result, "overall_relative_score", None),
        "overall_judge_result": str(getattr(result, "overall_judge_result", "")).replace("JudgeResult.", ""),
        "score_type": _score_type(session),
    }
    crs = list(getattr(result, "case_results", []) or [])
    out["num_cases"] = len(crs)
    counts = Counter(_jr(c) for c in crs)
    out["judge_counts"] = dict(counts)
    out["num_ac"] = sum(v for k, v in counts.items() if k.upper() in ("ACCEPTED", "AC"))

    # Compile error: if every case is a compilation error, surface the message once.
    compile_like = [c for c in crs if "COMPIL" in _jr(c).upper()]
    if compile_like and len(compile_like) == len(crs):
        msg = getattr(compile_like[0], "error_str", "") or getattr(compile_like[0], "message", "")
        out["compile_error"] = str(msg)[:4000]

    # A small sample of failing cases (non-AC) with their error text.
    errs = []
    for c in crs:
        jr = _jr(c)
        if jr.upper() not in ("ACCEPTED", "AC"):
            es = getattr(c, "error_str", "") or getattr(c, "message", "") or ""
            errs.append({
                "judge": jr,
                "error": str(es)[:300],
                "time": getattr(c, "execution_time", None),
                "score": getattr(c, "absolute_score", None),
            })
        if len(errs) >= 5:
            break
    if errs:
        out["case_errors"] = errs

    out["case_scores"] = [getattr(c, "absolute_score", None) for c in crs[:20]]
    return out


def _problem_payload(session) -> dict:
    p = session.problem
    payload = {
        "problem_id": session.problem_id,
        "score_type": _score_type(session),
        "num_public_cases": getattr(session, "num_public_cases", None),
        "num_private_cases": getattr(session, "num_private_cases", None),
    }
    try:
        payload["statement"] = p.statement
    except Exception:
        payload["statement"] = None
    try:
        c = p.constraints
        payload["constraints"] = c if isinstance(c, (str, dict)) else str(c)
    except Exception:
        payload["constraints"] = None
    return payload


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # silence default logging
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
        raw = self.rfile.read(n) if n else b"{}"
        return json.loads(raw or b"{}")

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"ok": True, "sessions": list(_SESSIONS.keys())})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        try:
            req = self._body()
            if self.path == "/session":
                self._session(req)
            elif self.path == "/public":
                self._eval(req, private=False)
            elif self.path == "/private":
                self._eval(req, private=True)
            elif self.path == "/problem":
                s = _SESSIONS[req["session_id"]]
                self._send(200, _problem_payload(s))
            elif self.path == "/usage":
                s = _SESSIONS[req["session_id"]]
                self._send(200, {
                    "current": str(getattr(s, "current_resource_usage", "")),
                    "remaining": str(getattr(s, "remaining_resource_usage", "")),
                    "session_remaining_time": str(getattr(s, "session_remaining_time", "")),
                })
            elif self.path == "/close":
                self._close(req)
            else:
                self._send(404, {"error": "not found"})
        except KeyError as e:
            self._send(400, {"error": f"unknown session_id or missing field: {e}"})
        except Exception as e:
            self._send(500, {"error": str(e), "trace": traceback.format_exc()[-2000:]})

    def _session(self, req: dict):
        problem_id = req["problem_id"]
        lite = bool(req.get("lite", True))
        num_workers = int(req.get("num_workers", 8))
        session_seconds = req.get("session_seconds")
        kwargs = dict(
            problem_id=problem_id,
            lite_version=lite,
            num_workers=num_workers,
            run_visualization_server=False,
        )
        if session_seconds:
            kwargs["session_duration"] = float(session_seconds)
        s = ale_bench.start(**kwargs)
        sid = uuid.uuid4().hex[:12]
        with _LOCK:
            _SESSIONS[sid] = s
            _META[sid] = {"problem_id": problem_id, "lite": lite}
        self._send(200, {"session_id": sid, "problem": _problem_payload(s)})

    def _eval(self, req: dict, private: bool):
        s = _SESSIONS[req["session_id"]]
        code = req["code"]
        lang = req.get("lang", "cpp23")
        reuse = bool(req.get("reuse_containers", True))
        print(f"[eval_server] {'private' if private else 'public'}_eval "
              f"session={req['session_id']} code_len={len(code)} lang={lang}", flush=True)
        if private:
            result, rank, performance = s.private_eval(
                code, code_language=lang, reuse_containers=reuse
            )
            payload = _result_to_dict(s, result)
            payload.update({"rank": rank, "performance": performance})
            self._send(200, payload)
        else:
            result = s.public_eval(code, code_language=lang, reuse_containers=reuse)
            self._send(200, _result_to_dict(s, result))

    def _close(self, req: dict):
        sid = req["session_id"]
        with _LOCK:
            s = _SESSIONS.pop(sid, None)
            _META.pop(sid, None)
        if s is not None:
            try:
                s.close()
            except Exception:
                pass
        self._send(200, {"ok": True})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8137)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"[eval_server] listening on http://{args.host}:{args.port}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
