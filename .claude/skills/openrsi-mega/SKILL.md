---
name: openrsi-mega
description: >-
  Run and push the OpenRSI KernelBench-Mega solver — an Opus coding agent that writes a fused
  W4A16 Kimi-Linear decode megakernel, scored by geomean decode speedup, gated on correctness
  (cosine ≥ 0.98) AND authenticity (a real fused kernel, not a CUDAGraph/torch trick). Use when
  the user wants to: run/improve the mega solve, push a verified megakernel speedup higher,
  seed-chain kernels toward the ~20× target, benchmark a model on this task, or reproduce/verify
  a saved kernel. Encodes the hard-won discipline: verify-before-trust, the anti-gaming judge,
  median-of-N scoring, the three watchdogs, and seed-chaining. Triggers: "run mega", "push the
  megakernel", "chain from the best kernel", "verify this kernel number", "benchmark X on mega",
  "why is 18x not reproducing".
---

# OpenRSI KernelBench-Mega solver

An inner coding agent (Opus by default) writes `solution.py` for `02_kimi_linear_decode`:
a **batch-1 W4A16 Kimi-Linear decode step fused into ONE genuine kernel launch**. Scored by
**geomean decode speedup over `baseline.py`** across context lengths, gated on **correctness**
(check.py, cosine ≥ 0.98) and **authenticity** (a post-run judge that rejects CUDAGraph /
torch.compile / per-op-loop / kernels=0 tricks). Harness: TS orchestration (`src/mega/solveMega.ts`,
`src/megaRsiLoop.ts`) driving `@earendil-works/pi-coding-agent`; Python eval on a Blackwell GPU box.

## THE ONE THING: verify-before-trust (do not skip)

A recorded number means nothing until the **saved artifact** re-loads, re-passes `check.py`, and
clears the **authenticity judge**. This is the whole point of this project — the famous **18–19×
"record" is a CUDAGraph fake** (per the bench's own `docs/megakernel_authenticity_judge.md`: ~12
per-op kernels replayed as "one launch"), and an earlier in-house **8.5×** was `import mega` with
the kernel never saved → doesn't even load. Before reporting ANY number:

```bash
# on the GPU box, from a clean copy of the problem dir + the SAVED artifact set:
CUDA_VISIBLE_DEVICES=0 $PY check.py            # must print PASS (cosine ≥ 0.98)
CUDA_VISIBLE_DEVICES=0 $PY benchmark.py        # read peak_fraction (it is a speedup ×, not a fraction)
CUDA_VISIBLE_DEVICES=0 $PY $JUDGE .            # kernel_count.total ≥ 1, ALL tripwires false, forbidden==[]
```
Judge verdict = `kernels ≥ 1 AND not(graph|compile|codegen|obfuscation) AND forbidden==[]`.
If it fails, the number is **0** — a fast-but-fake kernel ranks like a FAIL.

## Second thing: benchmark.py is NOISY (~30%) → always median

Same kernel re-benched swings e.g. `11.76 / 13.50 / 15.35`. A single measurement records a lucky
draw (a run once recorded **16.729×** that median'd to **13.68×**). The harness now medians
`OPENRSI_MEGA_BENCH_REPEATS` (default 3) runs. When hand-checking a number, run benchmark.py
**5–8×** and take the median; never quote a single draw.

## Environment

- **GPU box**: `ssh $OPENRSI_HOST` (set to `openrsi@<blackwell-box>`; RTX PRO 6000, SM120).
- **Python**: `PY=/mnt/hf/wsg_venv/.venv/bin/python3`
- **Problem dir**: `/mnt/rsi/mega/benchmarks/mega/problems/02_kimi_linear_decode`
- **Judge**: `JUDGE=/mnt/rsi/mega/benchmarks/mega/scripts/megakernel_evidence.py` (static, source-only, cheap)
- **Harness**: `/mnt/rsi/openrsi` (`node --env-file=.env dist/megaRsiLoop.js`); OpenRouter key in `.env`.
- **Deploy after editing TS**: `npx`-free build then rsync — `node node_modules/typescript/bin/tsc -p tsconfig.json && rsync -az dist/ $OPENRSI_HOST:/mnt/rsi/openrsi/dist/`

## Run a solve

```bash
ssh $OPENRSI_HOST 'cd /mnt/rsi/openrsi; rm -rf /mnt/rsi/<name>_run; \
  CUDA_VISIBLE_DEVICES=0 \
  OPENRSI_MEGA_SCAFFOLD=agent/mega/scaffold_v3.json \  # v3 = target single-launch fusion / ~20×
  OPENRSI_MEGA_SEED=/mnt/rsi/<seed_dir> \               # optional: seed from a prior kernel (see chaining)
  OPENRSI_OUTER_MODEL=anthropic/claude-opus-4.8 \       # any OpenRouter slug; provider.ts clones for unknown ones
  OPENRSI_MEGA_PYTHON=$PY \
  OPENRSI_MEGA_DIR=/mnt/rsi/mega/benchmarks/mega/problems/02_kimi_linear_decode \
  OPENRSI_MEGA_JUDGE=/mnt/rsi/mega/benchmarks/mega/scripts/megakernel_evidence.py \
  OPENRSI_RUN_DIR=/mnt/rsi/<name>_run \
  OPENRSI_GENERATIONS=0 \                               # 0 = single solve; >0 = RSI scaffold-evolution loop
  OPENRSI_MEGA_SOLVE_S=57600 OPENRSI_MEGA_COST_CAP=75 \ # time ceiling + $ cap (the real limiter)
  OPENRSI_MEGA_STALL_MIN=25 OPENRSI_MEGA_BENCH_REPEATS=3 \
  OPENRSI_MODEL_MAX_TOKENS=16000 \                      # REQUIRED: prevents one-giant-turn hang
  PATH=$HOME/.cargo/bin:$PATH \                         # for keenable (internet research) if the scaffold uses it
  nohup node --env-file=.env dist/megaRsiLoop.js > /mnt/rsi/<name>.log 2>&1 &'
```

Key env vars: `OPENRSI_MEGA_PLAIN=1` = bare agent, no scaffold/memory/coaching (baseline).
`OPENRSI_MEMORY=off` disables the shared memory. Result → `/mnt/rsi/<name>_run/`: `board.jsonl`
(fitness/verified/cost), `solution_v0/` (FULL artifact set incl. sidecars), `RESULTS.md` (on finish).

## The three watchdogs (why runs don't hang or overspend)

OpenRouter streams occasionally hang open and the SDK never times out (3 silent 10-h hangs one
campaign), and PLAIN turns can be huge. `solveMega.ts` races the solve against:
- **time**: hard cap at `SOLVE_S`.
- **cost**: polls session cost every 30 s, aborts at `COST_CAP` mid-turn. NOTE: session-stats cost
  **undercounts actual OpenRouter billing by ~8%** — a "$75 cap" bills ~$80–88 real. Budget for it.
- **stall**: aborts if no session event for `STALL_MIN` (25) min → a hung stream fails fast, not in 10 h.

## Seed-chaining (how the number actually climbs to ~20×)

From-scratch, even Opus **satisfices on a correct pure-torch version** and the anti-gaming gate
holds it at 0 — it will NOT write a hard fused kernel unaided. The lever that works is **chaining**:
each run is SEEDED (`OPENRSI_MEGA_SEED`) with the prior run's kernel, so the agent optimizes real
working code. Observed honest (median, verified) trajectory: **4.09 → 7.4 → 11.5 → 13.7 → ~19–21×**.

Snapshot a seed = copy the prior run's `solution_v0/solution.py` + `megakernel_src.py` (and any
sidecars solution.py imports) into a fresh dir; point `OPENRSI_MEGA_SEED` at it. Run steps
**sequentially** — two concurrent solves both running benchmark.py corrupt each other's timing.
A self-chaining loop (`while: wait for prev RESULTS.md → seed next → launch; stop on plateau /
`STOP_CHAIN` file) can run unattended on the box.

## The thesis (what the target really is)

The **~20× speedup is real and honestly reachable** — only the CUDAGraph *method* of faking "one
launch" is disqualified. Batch-1 decode is **launch-bound**: baseline.py fires dozens–hundreds of
tiny kernels/token; **collapsing the whole step into ONE genuine fused kernel** is the order-of-
magnitude lever, on top of **int4 = ¼ the bytes** (fuse the dequant into the GEMV, never
materialize bf16). 4–5× = partial fusion (fast GEMV, rest still separate launches). `scaffold_v3`
makes full single-launch fusion the objective and drives the **launch count → 1** (profile with
`nsys profile --stats=true`). Honest single-fused ceiling on this task ≈ **13–21× (noisy)**, not 20+
as a hard number; `sota.py` is a stub, so there is no reference kernel — the ceiling is empirical.

## Anti-gaming is an active gate, not a flag

The judge runs **in-loop every turn** (it is static/source-only, cheap): if the current
`solution.py` is gamed (`kernels=0` / a graph tripwire) the next nudge tells the agent its kernel
**scores 0** and to write a real fused kernel (a fast benchmark.py alone won't warn it). The final
score is **gated**: judge-rejected ⇒ `performance=0`, so the leaderboard/RSI/BoN can never select a
trick. Never disable this.

## Knowledge transfer between runs

- **Seed** (code) — the actual kernel, strongest.
- **Memory** — `agent/memory/mega.jsonl` (shared, append-only): `reflectAndStore` saves a distilled
  observation + score after each solve; `recall` injects the top-K (weighted same-problem +5,
  fitness +score/500, recency) into the next agent's prompt. Carries findings AND (de-weighted) failures.
- **Outer history** (RSI only, `GENERATIONS>0`): the scaffold-proposer sees past scaffold-edits +
  their measured fitness, so it evolves the *instructions*, not the code.

## Gotchas learned the hard way

- Always re-verify a headline number (correctness + judge + median) before quoting it — this bit us
  on our OWN 16.7× → 13.7×.
- OpenRouter keys die on credits (402) or return empty content on some slugs → the run hangs; the
  stall watchdog catches it. Check `curl .../api/v1/key` and a live completion when a run stalls.
- `OPENRSI_MODEL_MAX_TOKENS=16000` is mandatory (uncapped → one 128k-token turn hangs).
- gpt-5.6-sol is very slow (~50 tool calls in 26 h); qwen3.6-35b-a3b / qwen3.5-9b returned empty
  content mid-run (provider issue) → VOID.
- Cost cap is session-stats, not billing: real spend runs ~8% over the cap.
- Monitor via `nohup` + poll for `RESULTS.md`; the runs are independent of your machine/ssh.

## Files to read first

`src/mega/solveMega.ts` (inner solve + watchdogs + judge gate + median), `src/megaRsiLoop.ts` (outer
RSI loop), `agent/mega/scaffold_v3.json` (the target-20× scaffold), `benchmark.md` (the honest
leaderboard + median ceiling), `agent/memory/mega.jsonl` (accumulated lessons).
