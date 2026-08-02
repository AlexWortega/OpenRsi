#!/usr/bin/env python3
"""Stream a proofs run to tracehouse as an AGENT run (default project: rsi-proffer).

Preferred source: <run_dir>/events.jsonl written by dist/proofs/run2.js — full
fidelity: agent messages (text + thinking) become assistant_msg/thinking spans,
tool calls become tool_use spans with real inputs, tool results become
tool_result spans linked to their tool_use parent, nudges become user_msg spans
with cost attributes, and the done record closes the trace (STATUS.md attached).

Fallback source (legacy runs without events.jsonl): <run_dir>.log stderr lines —
tool-name-only spans, as before.

session_id is stable per run dir, so a bridge restart resumes the same trace.
Works both live (follows the file) and as a backfill replay of a finished run.

Usage:
  .thvenv/bin/python scripts/tracehouse_tail_proofs.py <run_dir>
  TRACEHOUSE_PROJECT=<project> overrides the target project.

Credentials: TRACEHOUSE_API_KEY from the environment, else read from
~/.config/tracehouse/credentials.json (written by `tracehouse login`).
"""
import json
import os
import re
import sys
import time
import uuid

HEADER_RE = re.compile(r"^\[(proofs\d*)\] model=(\S+) dir=\S+ budget=\$([0-9.]+)")
TOOL_RE = re.compile(r"^\[(proofs\d*) (\d\d):(\d\d):(\d\d)\] tool (\w+)")
NUDGE_RE = re.compile(r"^\[(proofs\d*)\] nudge (\d+), spent \$([0-9.]+) of \$([0-9.]+)")
DONE_RE = re.compile(r"^\[(proofs\d*)\] DONE after (\d+) rounds, cost=\$([0-9.]+)")
FATAL_RE = re.compile(r"^\[(proofs\d*)\] FATAL")

IDLE_GIVEUP_S = 3 * 3600  # source silent this long -> assume the runner died
BATCH = 30                # max spans per push_spans call
EVENTS_WAIT_S = 60        # how long to wait for events.jsonl before legacy fallback


def load_creds():
    if os.environ.get("TRACEHOUSE_API_KEY"):
        return
    path = os.path.expanduser("~/.config/tracehouse/credentials.json")
    try:
        creds = json.load(open(path))
        os.environ["TRACEHOUSE_API_KEY"] = creds["api_key"]
        os.environ.setdefault("TRACEHOUSE_API_BASE", creds.get("api_base", "https://tracehouse.ai"))
    except Exception as e:  # noqa: BLE001
        sys.exit(f"no TRACEHOUSE_API_KEY and cannot read {path}: {type(e).__name__}: {e}")


def as_text(content):
    """Flatten a pi message content (string or block list) to plain text."""
    if isinstance(content, str):
        return content
    parts = []
    for block in content if isinstance(content, list) else []:
        if isinstance(block, str):
            parts.append(block)
        elif isinstance(block, dict):
            for key in ("text", "thinking", "content"):
                if isinstance(block.get(key), str):
                    parts.append(block[key])
                    break
    return "\n".join(p for p in parts if p)


class Bridge:
    def __init__(self, run_dir):
        self.run_dir = run_dir
        self.name = os.path.basename(run_dir)
        self.project = os.environ.get("TRACEHOUSE_PROJECT", "rsi-proffer")
        self.run = None
        self.budget = None
        self.pending = []
        self.tool_span_ids = {}  # toolCallId -> tool_use span uuid
        self.end = None          # (outcome, rounds, cost, text)
        import tracehouse as th
        from tracehouse import client
        self.th, self.client = th, client

    def init_run(self, model, variant, rich=False):
        # Rich (events.jsonl) traces use a distinct session_id so they never mix
        # with skeleton spans pushed earlier from the bare log by old bridges.
        self.run = self.th.init(
            project=self.project,
            session_id=f"{'proofs2' if rich else 'proofs'}/{self.name}",
            task_name=self.name,
            model=model,
            scaffold=f"openrsi/{variant}",
        )
        print(f"[thbridge] agent trace started: {self.project}/{self.name} (rich={rich})", flush=True)

    def span(self, kind, name, attrs, span_id=None, parent=None, status=None):
        now = self.client._utcnow_iso()
        self.pending.append(self.client.Span(
            id=span_id or str(uuid.uuid4()), session_id=self.run.session_id,
            kind=kind, name=name, start_at=now, end_at=now,
            parent_span_id=parent, attributes=attrs, status=status,
        ))
        if len(self.pending) >= BATCH:
            self.flush()

    def flush(self):
        if not (self.run and self.pending):
            return
        try:
            self.run.push_spans(self.pending)
        except Exception as e:  # noqa: BLE001
            print(f"[thbridge] push_spans failed ({len(self.pending)} spans): {e}", flush=True)
        self.pending.clear()

    # ---- rich source: events.jsonl ---------------------------------------- #

    def handle_event(self, rec):
        t = rec.get("t")
        if t == "header":
            self.budget = rec.get("budget")
            if self.run is None:
                self.init_run(rec.get("model", "?"), rec.get("variant", "proofs2"), rich=True)
                self.span("user_msg", "run header", {
                    "text": f"model={rec.get('model')} budget=${rec.get('budget')}",
                    "budget_usd": rec.get("budget"), "run_dir": self.run_dir,
                })
            return
        if self.run is None:
            return
        if t == "tool_start":
            sid = str(uuid.uuid4())
            self.tool_span_ids[rec.get("id")] = sid
            self.span("tool_use", rec.get("tool", "?"),
                      {"tool_input": rec.get("args") or {}}, span_id=sid)
        elif t == "tool_end":
            text = rec.get("result")
            if not isinstance(text, str):
                text = json.dumps(text, ensure_ascii=False)[:4000] if text is not None else ""
            self.span("tool_result", rec.get("tool", "?"),
                      {"result_text": text, "is_error": bool(rec.get("isError"))},
                      parent=self.tool_span_ids.pop(rec.get("id"), None),
                      status="error" if rec.get("isError") else None)
        elif t == "message":
            msg = rec.get("message") or {}
            role = msg.get("role", "")
            content = msg.get("content")
            if role == "assistant":
                blocks = content if isinstance(content, list) else [content]
                for block in blocks:
                    if isinstance(block, dict) and isinstance(block.get("thinking"), str) and block["thinking"]:
                        self.span("thinking", "thinking", {"text": block["thinking"][:8000]})
                    elif isinstance(block, dict) and isinstance(block.get("text"), str) and block["text"]:
                        self.span("assistant_msg", "assistant message", {"text": block["text"][:8000]})
                    elif isinstance(block, str) and block:
                        self.span("assistant_msg", "assistant message", {"text": block[:8000]})
                    # toolCall blocks are covered by tool_start events
            elif role == "user":
                text = as_text(content)
                if text:
                    self.span("user_msg", "user message", {"text": text[:4000]})
            # toolResult-role messages are covered by tool_end events
        elif t == "nudge":
            self.flush()
            self.span("user_msg", f"nudge {rec.get('n')}", {
                "text": f"nudge {rec.get('n')} — spent ${rec.get('spent')} of ${rec.get('budget')}",
                "nudge": rec.get("n"), "cost_usd": rec.get("spent"),
                "budget_frac": round(rec.get("spent", 0) / rec["budget"], 4) if rec.get("budget") else None,
            })
            self.flush()
        elif t == "done":
            self.end = ("good", rec.get("rounds"), rec.get("cost"),
                        f"DONE after {rec.get('rounds')} rounds, cost=${rec.get('cost')}")

    # ---- legacy source: <run_dir>.log ------------------------------------- #

    def handle_log_line(self, line):
        m = HEADER_RE.match(line)
        if m and self.run is None:
            self.budget = float(m.group(3))
            self.init_run(m.group(2), m.group(1))
            self.span("user_msg", "run header", {"text": line, "budget_usd": self.budget,
                                                 "run_dir": self.run_dir})
            return
        if self.run is None:
            return
        m = TOOL_RE.match(line)
        if m:
            self.span("tool_use", m.group(5), {"tool_input": {},
                      "log_time": f"{m.group(2)}:{m.group(3)}:{m.group(4)}"})
            return
        m = NUDGE_RE.match(line)
        if m:
            self.flush()
            spent = float(m.group(3))
            self.span("user_msg", f"nudge {m.group(2)}", {
                "text": line, "nudge": int(m.group(2)), "cost_usd": spent,
                "budget_frac": round(spent / float(m.group(4)), 4)})
            self.flush()
            return
        m = DONE_RE.match(line)
        if m:
            self.end = ("good", int(m.group(2)), float(m.group(3)), line)
        elif FATAL_RE.match(line):
            self.end = ("bad", None, None, line)

    # ---- main loop -------------------------------------------------------- #

    def tail(self, path, handler):
        f = open(path)
        idle = 0.0
        while True:
            line = f.readline()
            if not line:
                self.flush()
                if self.end:
                    return
                time.sleep(5)
                idle += 5
                if idle > IDLE_GIVEUP_S:
                    self.end = ("bad", None, None, "runner went silent (assumed dead)")
                    return
                continue
            idle = 0.0
            handler(line.strip())

    def finish(self):
        if not self.run:
            return
        outcome, rounds, cost, done_text = self.end or ("neutral", None, None, "bridge stopped")
        self.span("assistant_msg", "run finished", {"text": done_text})
        try:
            status_md = os.path.join(self.run_dir, "STATUS.md")
            if os.path.exists(status_md):
                self.span("attachment", "STATUS.md", {"text": open(status_md).read()[:20000]})
        except Exception as e:  # noqa: BLE001
            print(f"[thbridge] STATUS.md attachment failed: {e}", flush=True)
        self.flush()
        meta = {"run_dir": self.run_dir}
        if self.budget is not None:
            meta["budget_usd"] = self.budget
        if rounds is not None:
            meta["rounds"] = rounds
        if cost is not None:
            meta["final_cost_usd"] = cost
        try:
            self.run.finish(outcome=outcome, metadata=meta)
        except Exception as e:  # noqa: BLE001
            print(f"[thbridge] finish failed: {e}", flush=True)
        print(f"[thbridge] finished (outcome={outcome})", flush=True)


def handle_event_line(bridge, line):
    if not line:
        return
    try:
        rec = json.loads(line)
    except json.JSONDecodeError:
        return
    bridge.handle_event(rec)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    run_dir = os.path.abspath(sys.argv[1]).rstrip("/")
    events_path = os.path.join(run_dir, "events.jsonl")
    log_path = run_dir + ".log"
    load_creds()
    bridge = Bridge(run_dir)

    # Prefer events.jsonl: wait for it up to EVENTS_WAIT_S even when the bare
    # log already exists (the runner may create it a moment later); only then
    # fall back to legacy log parsing.
    deadline = time.time() + EVENTS_WAIT_S
    while time.time() < deadline and not os.path.exists(events_path):
        time.sleep(2)
    if os.path.exists(events_path):
        print(f"[thbridge] source: {events_path}", flush=True)
        bridge.tail(events_path, lambda line: handle_event_line(bridge, line))
    elif os.path.exists(log_path):
        print(f"[thbridge] source (legacy): {log_path}", flush=True)
        bridge.tail(log_path, bridge.handle_log_line)
    else:
        sys.exit(f"neither {events_path} nor {log_path} appeared")
    bridge.finish()


if __name__ == "__main__":
    main()
