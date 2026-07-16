# OpenRSI

A working reproduction of **AIDE²-style recursive self-improvement (RSI)** built on the
[**pi**](https://github.com/earendil-works/pi) agent skeleton, targeting score-based algorithm-
engineering benchmarks (**ALE-Bench** first, **KernelBench** next).

An **outer** agent rewrites an **inner** solver agent's own *scaffold* (its system prompt, search
strategy, and domain knowledge) and keeps the rewrite only if a **private** score — hidden test
cases the inner agent never sees — improves. That private-score selection is the mechanism that,
in the [Weco RSI blog](https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement),
made the loop "cheat less": public-score gaming does not survive.

```
outer agent (Opus 4.8)  ──proposes a scaffold rewrite──▶  candidate scaffold
        ▲                                                        │
        │ keep iff mean PRIVATE performance improves             ▼
        └──────────────  private_eval (held-out cases)  ◀── inner agent (Sonnet 5)
                                                              solves ALE problems,
                                                              iterating on public_eval
```

- **Inner solver** (`src/inner/`): a pi `AgentSession` given ONE ALE-Bench problem + a `submit`
  tool. It iterates on `public_eval` (visible cases) under a budget, then its best VALID solution
  is scored once via `private_eval` → AtCoder **performance** (0–3500) = the fitness.
- **Outer loop** (`src/outer/`, `src/rsiLoop.ts`): each generation, a strong agent reads the
  champion scaffold + its per-problem results and proposes ONE rewrite via a structured tool. The
  candidate is evaluated on the private cases and becomes champion only if mean performance beats
  the incumbent. Checkpointed to a shared board every generation.
- **The mutable artifact** is `agent/inner/scaffold.json` — system prompt + domain-knowledge tips +
  eval budget. This is what the RSI loop evolves (kept as data → safe to rewrite, schema intact).

### Agent memory (a claude-mem analog for the solver)

Each solver session ends by **reflecting** itself into 1–2 durable, tagged observations ("a greedy
wall-build baseline scored 1096; SA improved it", "RUNTIME_ERROR from wrong output length — validate
line count"), stored per-benchmark in `agent/memory/<benchmark>.jsonl`. On the next problem those
observations are **recalled** (ranked by same-problem match + fitness + recency) and injected into the
prompt. So knowledge compounds across problems, generations, and runs — orthogonally to the scaffold
rewrites the outer loop makes. Toggle with `OPENRSI_MEMORY=off`; see `src/memory/memory.ts`.

### Generational loop (adapted from the autoresearch skill)

Each generation runs a **propose → critique → evaluate → verify → keep** cycle so eval budget is
spent only on the most promising, non-duplicate hypotheses:

1. **Propose (parallel).** N outer agents concurrently propose diverse variants, each covering a
   distinct angle (search strategy, domain knowledge, time management, robustness, algorithmic
   reframe, tuning). Every proposal must pass the **think-first protocol** — a causal *mechanism*, an
   *expected numeric delta*, and a *falsification condition* — or it isn't a hypothesis.
2. **Peer-critique before compute.** A panel of critic agents scores every proposal (quality 0–10 +
   keep vote) *before any benchmark eval*. Only the top survivors are evaluated; weak/duplicate
   proposals are pruned for free.
3. **Evaluate survivors** on the benchmark (the only place GPU/CPU compute is spent).
4. **Adversarially verify.** A candidate that beats the champion is re-evaluated on a fresh solve;
   it's crowned only if the averaged score still wins — guarding against inner-agent variance.
5. **Keep & share.** The champion, leaderboard, shared board, and every proposal (survived or pruned)
   are checkpointed each generation. The loop runs for `OPENRSI_GENERATIONS` with no early stop by
   default.

## Results

### 🏆 KernelBench-Mega — new record on RTX PRO 6000: 18.45× (beats published SOTA 14.4×)

On the **Kimi-Linear W4A16 whole-block decode megakernel** (`kernelbench.com/mega`, single fused
kernel launch, correctness cosine ≥ 0.98, geomean decode speedup over context 2048/8192/16384), the
OpenRSI agent (Opus 4.8) iterated to a **new high on the RTX PRO 6000**:

| attempt | geomean speedup | PASS | note |
|---------|-----------------|------|------|
| #1 | 11.23× | ✓ | first correct fused megakernel, from scratch |
| #4 | 14.53× | ✓ | already beats the published SOTA (claude-opus-4-8 = 14.399×) |
| **#5** | **18.45×** | ✓ | **target (18×) exceeded** |

Published board (native harness) on RTX PRO 6000: opus-4-8 14.40×, glm-5.2 11.14×, gpt-5.5 4.34×.
Record kernel + full write-up in [`mega_results/`](mega_results/). Runner: `src/mega/run.ts`.

### KernelBench-Mega — model comparison (same harness, same GPU, fresh 3h each)

| model | geomean | PASS |
|-------|---------|------|
| Opus 4.8 | **18.45×** | ✓ |
| Kimi-2.7-code | _running_ | — |
| GLM-5.2 | _running_ | — |

### ALE-Bench (AtCoder Heuristic Contests, mean AtCoder performance; higher is better)

The RSI loop reached a strong baseline via deep dynamic-budget solving; scaffold rewrites plateaued
at the baseline (a strong prompt is hard to beat by rewriting). Reference bars: ALE-Agent (SOTA) 1879,
human avg 1260.

| model | mean performance | note |
|-------|------------------|------|
| Opus 4.8 (deep budget) | **1625.5** | above human avg; per-problem ahc011=1878, ahc015=1791 exceed 1790 |
| gpt-5.6-sol (low effort) | ~1545 baseline | ~3× cheaper; competitive per-problem (ahc015=1968) |

### Earlier validation (single-generation, standard KernelBench L2 fusion)

The identical propose → critique → evaluate → adversarially-verify loop on a Conv2D+ReLU+BiasAdd
fusion: gen-0 baseline 1.000× → gen-1 champion **1.137×** (agent wrote a fused custom CUDA kernel,
verify re-eval 1.268×). And on ALE-Bench a smoke run lifted ahc008 780 → 1040 (+260) with held-out
ahc015 = 1380, confirming the RSI mechanism end-to-end before the large runs above.

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

Models default to `claude-sonnet-5` (inner) / `claude-opus-4.8` (outer) via OpenRouter; override with
`OPENRSI_INNER_MODEL` / `OPENRSI_OUTER_MODEL`.

Run knobs: `OPENRSI_GENERATIONS` (default 12), `OPENRSI_VARIANTS` (proposals per generation, default
3), `OPENRSI_STAGNATION` (early-stop after N no-improvement gens; default off), `OPENRSI_PROBLEMS`,
`OPENRSI_HELDOUT`.

## Inspecting variants & giving feedback (human-in-the-loop)

Each generation proposes several **diverse variants** (different angles: search strategy, domain
knowledge, time management, robustness, …), evaluates all of them, and keeps the best. Every variant
is saved in full so you can review the search:

- `runs/<name>/variants/gen<G>_v<K>.json` — the complete proposed scaffold + its per-problem results.
- `runs/<name>/VARIANTS.md` — a one-line index of every variant and its fitness.
- `runs/<name>/leaderboard.md`, `board.jsonl`, `FINDINGS.md` — the running RSI curve.

To **steer** the run, write guidance into `runs/<name>/FEEDBACK.md`. The outer agent re-reads it at
the start of every generation and treats it as high-priority instruction (e.g. "focus on ahc011,
its scores are lowest" or "try tabu search instead of SA").

## Next levers

Explicit AIDE draft/improve/debug tree search · per-genre domain-knowledge routing · a scratch bash
tool for the inner agent · multi-candidate generations · **KernelBench on the V100s** (`fast_p`).
