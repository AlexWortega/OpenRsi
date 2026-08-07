# OpenRSI

A working reproduction of **AIDE²-style recursive self-improvement (RSI)**, built on the
[**pi**](https://github.com/earendil-works/pi) agent skeleton, targeting score-based algorithm-
engineering benchmarks — **ALE-Bench** first, **KernelBench** next.

An **outer** agent rewrites an **inner** solver agent's own *scaffold* (system prompt, search
strategy, domain knowledge) and keeps the rewrite only if a **private** score — hidden test cases
the inner agent never sees — improves. That private-score selection is the mechanism that, per the
[Weco RSI blog](https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement), keeps the
loop from gaming the public metric.

```
outer agent (Opus 4.8)  ──proposes a scaffold rewrite──▶  candidate scaffold
        ▲                                                        │
        │ keep iff mean PRIVATE performance improves             ▼
        └──────────────  private_eval (held-out cases)  ◀── inner agent (Sonnet 5)
                                                              solves ALE problems,
                                                              iterating on public_eval
```

- **Inner solver** (`src/inner/`): a pi `AgentSession` given ONE ALE-Bench problem + a `submit`
  tool. It iterates on `public_eval` (visible cases) under a budget; its best VALID solution is
  scored once via `private_eval` → AtCoder **performance** (0–3500), the fitness.
- **Outer loop** (`src/outer/`, `src/rsiLoop.ts`): each generation, a strong agent reads the
  champion scaffold plus its per-problem results and proposes ONE rewrite via a structured tool.
  The candidate is evaluated on the private cases and becomes champion only if mean performance
  beats the incumbent. Checkpointed to a shared board every generation.
- **The mutable artifact** is `agent/inner/scaffold.json` — system prompt, domain-knowledge tips,
  eval budget. This is what the RSI loop evolves.

## Results

Every row is a real benchmark run with a baseline it's measured against — either a published
board/SOTA number, a human-average reference, or our own gen-0 (pre-RSI) score. Full logs, cost,
and per-run detail: [`benchmark.md`](benchmark.md) and [`full40_RESULTS.md`](full40_RESULTS.md).

| Benchmark | Baseline | OpenRSI result | Detail |
|---|---|---|---|
| KernelBench-Mega, Kimi-Linear W4A16 decode (RTX PRO 6000 Blackwell), single from-scratch run | published board record 14.40× (opus-4-8, native harness) | **18.45×**, PASS, correctness-first recipe | [`mega_results/opus_18.45x_RECORD.py`](mega_results/opus_18.45x_RECORD.py) |
| Same task, RSI seed-chain (each run seeded with the prior run's kernel) | chain start 4.09× | **23.18×**, median-of-3, judge-verified authentic (3 real launches, no CUDAGraph/compile trick) | [`traces/mega/opus_chain_23x_run/`](traces/mega/opus_chain_23x_run/), see caveat below |
| KernelBench L2 fusion (Conv2D+ReLU+BiasAdd), earliest end-to-end RSI validation | unfused baseline 1.000× | gen-1 **1.137×** (agent wrote a fused CUDA kernel), 1.268× on independent re-eval | `benchmark.md` §"Earlier validation" |
| ALE-Bench Lite (10 curated AHC problems, AtCoder performance 0–3500) | human average 1260 | **1625.5** mean (Opus, deep eval budget); ahc011=1878, ahc015=1791 individually clear the 1790 target | ALE-Agent (SOTA) sits at 1879 — not beaten |
| ALE-Bench Full (all 40 problems, harder Full-seed limits) | human average 1260 | **1432.9** mean | [`full40_RESULTS.md`](full40_RESULTS.md) — below our own Lite number; ~8 problems TLE on the tighter Full limits |
| ALE-Bench smoke test, single problem (ahc008), first end-to-end RSI check | gen-0 780 | gen-1 **1040** (+260); scaffold rewrite generalized to held-out ahc015=1380 | confirms the private-score gate transfers, not just memorizes |
| ALE-Bench, same harness with a cheaper model (gpt-5.6-sol, low reasoning effort) | human average 1260 | **1544.8** mean, ~3× cheaper than the Opus run | RSI rewrites plateaued at gen-0 here too |

**Caveats we keep on the record rather than smooth over:**
- The 23.18× seed-chain is a chain of runs, each handed the prior kernel — not a single independent
  solve, so it's not eligible for the per-model kernelbench.com leaderboard (their contamination
  tripwire excludes seeded runs by design; a from-scratch Opus run lands at 18.45×, the row above).
  See [`docs/mega_23x_submission_ask.md`](docs/mega_23x_submission_ask.md).
- A stricter re-verification pass (full-artifact capture + an authenticity judge that rejects
  CUDAGraph/compile/codegen tricks) found two earlier internal numbers were unbacked — an 8.503×
  Opus claim lost its sidecar module and couldn't reload, and a 0.765× gpt-5.6-sol number collided
  with a stale JIT cache. Re-run clean, the honest floor is Opus+scaffold at **4.088×**, verified
  and reproducible. Kept here so the table above doesn't inherit a number we can no longer stand
  behind. Full audit: `benchmark.md` §"Reproducibility / authenticity audit".
- On the mega task, two neighbor models were tried and did **not** succeed: GLM-5.2 attempted to
  `import reference` (caught by the authenticity check), and Kimi-2.7-code produced a numerically
  incorrect kernel (cosine ≈ 0). Only Opus reached a correct, record-setting kernel in that sweep.

## Agent memory (a claude-mem analog for the solver)

Each solver session ends by **reflecting** itself into 1–2 durable, tagged observations ("a greedy
wall-build baseline scored 1096; SA improved it", "RUNTIME_ERROR from wrong output length —
validate line count"), stored per-benchmark in `agent/memory/<benchmark>.jsonl`. On the next
problem those observations are **recalled** (ranked by same-problem match + fitness + recency) and
injected into the prompt, so knowledge compounds across problems, generations, and runs —
orthogonally to the scaffold rewrites the outer loop makes. Toggle with `OPENRSI_MEMORY=off`; see
`src/memory/memory.ts`.

## Generational loop (adapted from the autoresearch skill)

Each generation runs a **propose → critique → evaluate → verify → keep** cycle so eval budget is
spent only on the most promising, non-duplicate hypotheses:

1. **Propose (parallel).** N outer agents concurrently propose diverse variants — search strategy,
   domain knowledge, time management, robustness, algorithmic reframe, tuning. Every proposal must
   pass the **think-first protocol** — a causal *mechanism*, an *expected numeric delta*, and a
   *falsification condition* — or it isn't a hypothesis.
2. **Peer-critique before compute.** A panel of critic agents scores every proposal (quality 0–10 +
   keep vote) before any benchmark eval. Only the top survivors are evaluated; weak/duplicate
   proposals are pruned for free.
3. **Evaluate survivors** on the benchmark — the only place GPU/CPU compute is spent.
4. **Adversarially verify.** A candidate that beats the champion is re-evaluated on a fresh solve;
   it's crowned only if the averaged score still wins, guarding against inner-agent variance.
5. **Keep & share.** The champion, leaderboard, shared board, and every proposal (survived or
   pruned) are checkpointed each generation. The loop runs for `OPENRSI_GENERATIONS` with no early
   stop by default.

## Architecture

```
agent/inner/scaffold.json   # the mutable solver scaffold (evolved by the RSI loop)
benches/ale/eval_server.py  # persistent multi-session ALE-Bench eval server (Docker judge)
src/
  provider.ts               # OpenRouter model wiring (env key), tier = inner|outer
  ale/evalServer.ts         # TS client + lifecycle for the Python eval server
  inner/{scaffold,solve}.ts # load scaffold; run one AIDE-style solve (public loop -> private fitness)
  outer/improve.ts          # outer agent proposes one scaffold rewrite (structured tool)
  board.ts                  # board.jsonl + leaderboard.md + FINDINGS.md
  rsiLoop.ts                # generational driver: baseline -> propose/eval/keep -> verify
runs/<name>/                # per-run board, leaderboard, RESULTS.md, champion_scaffold.json
research/                   # TASK / DEEPRESEARCH / BUDGET / EXPERIMENTS
```

## Running

Requires: Node ≥ 20, an OpenRouter key in `.env` (`OPENROUTER_API_KEY`), and a host with Docker +
Python 3.10–3.14 for ALE-Bench (this project runs on **eva01**: 48 cores, 4× V100, Docker). See
`research/DEEPRESEARCH.md` for setup specifics.

```bash
npm install && npx tsc -p tsconfig.json

# One inner solve (baseline harness):
node --env-file=.env dist/runInner.js ahc008

# Full RSI loop:
OPENRSI_PROBLEMS=ahc008,ahc011,ahc016 OPENRSI_HELDOUT=ahc015 OPENRSI_GENERATIONS=6 \
  node --env-file=.env dist/rsiLoop.js
```

Models default to `claude-sonnet-5` (inner) / `claude-opus-4.8` (outer) via OpenRouter; override
with `OPENRSI_INNER_MODEL` / `OPENRSI_OUTER_MODEL`.

Run knobs: `OPENRSI_GENERATIONS` (default 12), `OPENRSI_VARIANTS` (proposals per generation,
default 3), `OPENRSI_STAGNATION` (early-stop after N no-improvement gens; default off),
`OPENRSI_PROBLEMS`, `OPENRSI_HELDOUT`.

## Inspecting variants & giving feedback (human-in-the-loop)

Each generation proposes several diverse variants (different angles: search strategy, domain
knowledge, time management, robustness, …), evaluates all of them, and keeps the best. Every
variant is saved in full so you can review the search:

- `runs/<name>/variants/gen<G>_v<K>.json` — the complete proposed scaffold + its per-problem
  results.
- `runs/<name>/VARIANTS.md` — a one-line index of every variant and its fitness.
- `runs/<name>/leaderboard.md`, `board.jsonl`, `FINDINGS.md` — the running RSI curve.

To steer a run, write guidance into `runs/<name>/FEEDBACK.md`. The outer agent re-reads it at the
start of every generation and treats it as high-priority instruction (e.g. "focus on ahc011, its
scores are lowest" or "try tabu search instead of SA").

## Levers (shipped)

All default to the previous behavior so the headline runs are unchanged unless a flag is set:

- **Explicit AIDE draft/improve/debug tree search** — `OPENRSI_SOLVER=aide` swaps the single-agent
  "nudge" inner loop for an explicit search tree (`src/inner/aideTree.ts`): best-of-N parallel
  **drafts** at the root, **debug** on a buggy best node, **improve** on a valid one. `nudge` (the
  original validated path) stays the default.
- **Per-genre domain-knowledge routing** — each problem is classified into a genre (`src/genre.ts`);
  only the matching `domain_knowledge_by_genre` tips are injected, and same-genre memory is
  preferred on recall. The outer loop can grow per-genre buckets. Disable with `OPENRSI_GENRE=off`.
- **Scratch bash tool for the inner agent** — `OPENRSI_SCRATCH=on` gives the solver a private temp
  dir with pi's built-in bash/read/write/edit, so it compiles & tests locally (free) before
  spending a budgeted `submit`.
- **Multi-candidate generations** — `OPENRSI_INNER_CANDIDATES` (default 3 in AIDE mode) best-of-N
  drafts at the root, on top of the existing parallel-hypothesis outer search.
- **grok-build goal plan + direction checker** — at gen-0 the objective is converted into 3–5
  gating criteria (`runs/<name>/goal_plan.json`, adopted from `xai-org/grok-build`'s
  `goal_planner_prompt`); each generation a checker reports `achieved` / `onTrack` + a **steer**
  fed into the proposer as auto-feedback. `OPENRSI_GOAL_STOP=on` lets the loop stop once all
  criteria hold.
- **KernelBench `fast_p`** — the kernel loop selects on `fast_p@1.0` (fraction of problems that are
  correct **and** ≥ torch), with a p-sweep {0, 0.5, 1, 2} on the board; target hardware is the RTX
  PRO 6000 (the 18.45× machine). `OPENRSI_KB_FITNESS=mean` reverts to mean speedup;
  `OPENRSI_KB_FASTP_P` sets the threshold.

New env knobs: `OPENRSI_SOLVER` (nudge|aide), `OPENRSI_SCRATCH` (off|on),
`OPENRSI_INNER_CANDIDATES`, `OPENRSI_GENRE` (on|off), `OPENRSI_GOAL_STOP` (off|on),
`OPENRSI_KB_FITNESS` (fast_p|mean), `OPENRSI_KB_FASTP_P`, `OPENRSI_AIDE_EPSILON`,
`OPENRSI_NODE_TIMEOUT_S`.
