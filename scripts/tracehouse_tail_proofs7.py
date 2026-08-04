#!/usr/bin/env python3
"""Stream a run7 (fable/pro/sol proofs) campaign to tracehouse as an agent run.

Tails two files in the run directory and pushes them as spans on one trace:
  events.jsonl     — phase/gate lifecycle written by dist/proofs/run7.js
  pro_costs.jsonl  — every oracle call with its USD cost, tokens, and timing

session_id is stable per run dir (proofs7/<name>), and byte offsets persist in
<run_dir>/.thbridge_offsets.json, so a bridge restart resumes the same trace
without duplicating spans. Works live and as a backfill replay of a finished run.

Usage:
  .thvenv/bin/python scripts/tracehouse_tail_proofs7.py <run_dir>
  TRACEHOUSE_PROJECT=<project> overrides the target project (default rsi-proffer).

Credentials: TRACEHOUSE_API_KEY from the environment, else
~/.config/tracehouse/credentials.json (written by `tracehouse login`).
"""
import json
import os
import sys
import time
import uuid

IDLE_GIVEUP_S = 3 * 3600  # both sources silent this long -> assume the runner died
POLL_S = 5
STATE_WAIT_S = 240


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


class Bridge7:
    def __init__(self, run_dir):
        import tracehouse as th
        from tracehouse import client
        self.th, self.client = th, client
        self.run_dir = run_dir
        self.name = os.path.basename(run_dir)
        self.offsets_path = os.path.join(run_dir, ".thbridge_offsets.json")
        try:
            self.offsets = json.load(open(self.offsets_path))
        except Exception:  # noqa: BLE001
            self.offsets = {}
        self.pending = []
        self.done = None  # (outcome, reason, spent_usd)
        state = self.wait_state()
        models = state.get("models", {})
        self.budget = state.get("budget_usd")
        self.run = th.init(
            project=os.environ.get("TRACEHOUSE_PROJECT", "rsi-proffer"),
            session_id=f"proofs7/{self.name}",
            task_name=self.name,
            model=models.get("sol", "?"),
            scaffold="openrsi/proofs7",
        )
        print(f"[thbridge7] trace started: {self.name} budget=${self.budget} models={models}", flush=True)

    def wait_state(self):
        path = os.path.join(self.run_dir, "state.json")
        deadline = time.time() + STATE_WAIT_S
        while time.time() < deadline:
            try:
                return json.load(open(path))
            except Exception:  # noqa: BLE001
                time.sleep(2)
        sys.exit(f"[thbridge7] no readable state.json in {self.run_dir}")

    def span(self, kind, name, attrs, status=None, ts=None):
        now = ts or self.client._utcnow_iso()
        self.pending.append(self.client.Span(
            id=str(uuid.uuid4()), session_id=self.run.session_id, kind=kind,
            name=name, start_at=now, end_at=now, parent_span_id=None,
            attributes=attrs, status=status))

    def flush(self):
        if self.pending:
            try:
                self.run.push_spans(self.pending)
            except Exception as e:  # noqa: BLE001
                print(f"[thbridge7] push_spans failed ({len(self.pending)} spans): {e}", flush=True)
            self.pending.clear()
        try:
            json.dump(self.offsets, open(self.offsets_path, "w"))
        except Exception:  # noqa: BLE001
            pass

    # ---- events.jsonl: phase/gate lifecycle ------------------------------- #

    def on_event(self, rec):
        phase, status, gen = rec.get("phase"), rec.get("status"), rec.get("generation")
        if phase == "done":
            outcome = "bad" if status == "fatal" else "good"
            self.done = (outcome, rec.get("reason") or status, rec.get("spent_usd"))
            self.span("assistant_msg", f"campaign {status}", {
                "text": f"{status}: decision={rec.get('decision')} reason={rec.get('reason')} "
                        f"spent=${rec.get('spent_usd')}",
                "cost_usd": rec.get("spent_usd"),
            }, status="error" if outcome == "bad" else None, ts=rec.get("ts"))
            return
        text = f"gen {gen} {phase} {status}"
        attrs = {"generation": gen, "phase": phase, "status": status}
        if rec.get("decision"):
            attrs["decision"] = rec["decision"]
            text += f" — {rec['decision']}"
        if rec.get("spent_usd") is not None:
            attrs["cost_usd"] = rec["spent_usd"]
            try:
                text += f" (spent ${round(float(rec['spent_usd']), 2)})"
                if self.budget:
                    attrs["budget_frac"] = round(float(rec["spent_usd"]) / float(self.budget), 4)
            except (TypeError, ValueError):
                pass
        attrs["text"] = text
        self.span("assistant_msg", text, attrs, ts=rec.get("ts"))

    # ---- pro_costs.jsonl: every oracle call ------------------------------- #

    def on_cost(self, rec):
        failed = rec.get("status") == "failed"
        model = (rec.get("model") or rec.get("output") or "?").split("/")[-1]
        name = f"{rec.get('mode', 'oracle')}:{model}"
        self.span("tool_use", name, {
            "tool_input": {"question": (rec.get("question") or "")[:300]},
            "cost_usd": rec.get("cost"),
            "prompt_tokens": rec.get("prompt_tokens"),
            "completion_tokens": rec.get("completion_tokens"),
            "seconds": rec.get("seconds"),
        }, status="error" if failed else None, ts=rec.get("ts"))

    # ---- main loop -------------------------------------------------------- #

    def pump(self, fname, handler):
        path = os.path.join(self.run_dir, fname)
        if not os.path.exists(path):
            return 0
        off = int(self.offsets.get(fname, 0))
        handled = 0
        with open(path, "rb") as f:
            f.seek(off)
            for raw in f:
                if not raw.endswith(b"\n"):
                    break  # partial write; retry on the next poll
                off += len(raw)
                line = raw.decode("utf-8", "replace").strip()
                if not line:
                    continue
                try:
                    handler(json.loads(line))
                    handled += 1
                except json.JSONDecodeError:
                    pass
        self.offsets[fname] = off
        return handled

    def loop(self):
        idle = 0.0
        while True:
            n = self.pump("events.jsonl", self.on_event) + self.pump("pro_costs.jsonl", self.on_cost)
            self.flush()
            if self.done:
                self.finish()
                return
            if n:
                idle = 0.0
                continue
            time.sleep(POLL_S)
            idle += POLL_S
            if idle > IDLE_GIVEUP_S:
                self.done = ("bad", "runner went silent (assumed dead)", None)
                self.finish()
                return

    def finish(self):
        outcome, reason, spent = self.done
        try:
            status_md = os.path.join(self.run_dir, "STATUS.md")
            if os.path.exists(status_md):
                self.span("attachment", "STATUS.md", {"text": open(status_md).read()[:20000]})
        except Exception as e:  # noqa: BLE001
            print(f"[thbridge7] STATUS.md attachment failed: {e}", flush=True)
        self.flush()
        meta = {"run_dir": self.run_dir, "reason": reason}
        if self.budget is not None:
            meta["budget_usd"] = self.budget
        if spent is not None:
            meta["final_cost_usd"] = spent
        try:
            self.run.finish(outcome=outcome, metadata=meta)
        except Exception as e:  # noqa: BLE001
            print(f"[thbridge7] finish failed: {e}", flush=True)
        print(f"[thbridge7] finished (outcome={outcome}, reason={reason})", flush=True)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    load_creds()
    Bridge7(os.path.abspath(sys.argv[1]).rstrip("/")).loop()


if __name__ == "__main__":
    main()
