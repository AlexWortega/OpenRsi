#!/usr/bin/env python3
"""Upload OpenRSI trace runs (board.jsonl) to tracehouse, wandb-style.

Each run dir's board.jsonl is one experiment: per-generation fitness + per-problem
scores become logged metrics; the dir name is the run name. No wandb in this project
(the harness is TypeScript + Python eval), so this is the native bridge.

Usage:
  pip install tracehouse-sdk
  export TRACEHOUSE_API_KEY=...        # live credential, NOT committed
  export TRACEHOUSE_API_BASE=https://tracehouse.ai
  python scripts/tracehouse_upload.py [run_dir ...]   # default: all under traces/

The key is read from the environment only — never hard-code or commit it.
"""
import os
import sys
import glob
import json


def load_board(run_dir):
    p = os.path.join(run_dir, "board.jsonl")
    if not os.path.exists(p):
        return []
    rows = []
    for line in open(p):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return rows


def bench_of(run_dir):
    d = run_dir.lower()
    if "weather" in d or "run_10gen" in d or "sweep" in d or "bounded" in d:
        return "weatherbench2"
    if "mega" in d or "glm" in d or "kimi" in d or "qwen" in d or "laguna" in d or "bon" in d:
        return "kernelbench-mega"
    return "ale"


def upload_dir(cm, run_dir, project="openrsi"):
    rows = load_board(run_dir)
    if not rows:
        print(f"skip {run_dir} (no board.jsonl)")
        return
    name = os.path.basename(run_dir.rstrip("/"))
    metric = next((r.get("metricLabel") for r in rows if r.get("metricLabel")), "fitness").replace(" ", "_")
    run = cm.init_run(
        project=project,
        name=name,
        config={
            "benchmark": bench_of(run_dir),
            "metric": metric,
            "generations": len(rows),
            "final_fitness": rows[-1].get("fitness"),
        },
    )
    for r in rows:
        log = {
            metric: r.get("fitness"),
            "accepted": int(bool(r.get("accepted"))),
            "champion": int(bool(r.get("champion"))),
            "cost_usd": r.get("cost"),
            "seconds": r.get("seconds"),
        }
        for p in r.get("perProblem", []) or []:
            if p.get("performance") is not None:
                log[f"perf/{p.get('problemId')}"] = p["performance"]
        # fast_p sweep, if present (kernel runs)
        for s in r.get("fastP", []) or []:
            log[f"fast_p/{s.get('p')}"] = s.get("value")
        run.log({k: v for k, v in log.items() if v is not None}, step=r.get("gen", 0))
    best = max((r.get("fitness", 0) or 0) for r in rows)
    run.summary["best_fitness"] = best
    run.finish(status="finished")
    print(f"uploaded {name}: {len(rows)} gens, best={best:.4f} ({bench_of(run_dir)})")


def main():
    if not os.environ.get("TRACEHOUSE_API_KEY"):
        sys.exit("set TRACEHOUSE_API_KEY in the environment (do not hard-code it)")
    try:
        import tracehouse as cm
    except ImportError:
        sys.exit("pip install tracehouse-sdk")
    dirs = sys.argv[1:]
    if not dirs:
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dirs = sorted(
            glob.glob(os.path.join(here, "traces", "*", "*_run"))
            + glob.glob(os.path.join(here, "traces", "*", "run_*"))
        )
    print(f"uploading {len(dirs)} run dir(s) to tracehouse ...")
    for d in dirs:
        try:
            upload_dir(cm, d)
        except Exception as e:  # noqa: BLE001
            print(f"skip {d}: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
