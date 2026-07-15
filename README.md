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

## Results

**ALE-Bench (multi-problem RSI run, mean private performance over ahc008/ahc011/ahc016):**

| generation | mean performance | outcome |
|------------|------------------|---------|
| gen-0 baseline | **1090** | default scaffold |
| gen-1 | **1262** (+16%) | ✅ accepted — outer agent diagnosed early-stopping, added SA + delta-eval + concrete AHC domain knowledge |
| gen-2, gen-3 | 1204, 1123 | rejected (didn't beat champion) — realistic ~90% rejection |

The outer agent rewrote the inner solver's scaffold; the rewrite raised performance on **hidden**
test cases the inner agent never saw, and the champion generalized to a held-out problem (`ahc015`).
Reference bars: ALE-Agent (SOTA) avg 1879, human avg 1260.

**KernelBench:** the GPU eval path is validated on an NVIDIA A40 (RunPod) — a candidate `ModelNew`
is compiled, checked for numerical correctness against the torch reference, and timed for speedup
(`fast_p`). The same RSI loop retargets to `fast_p`; see `benches/kernel/`.

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
