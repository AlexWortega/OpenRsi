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

## Validated result (single-generation smoke)

| stage | problem | performance | note |
|-------|---------|-------------|------|
| gen-0 baseline | ahc008 | **780** | default scaffold, agent used 1/6 evals |
| gen-1 champion | ahc008 | **1040** (+260) | outer agent diagnosed early-stopping, added SA + delta-eval + 11 concrete AHC tips |
| held-out | ahc015 | **1380** (rank 314) | never selected on — the champion generalizes |

Cost: $0.37. Reference bars: ALE-Agent avg 1879, human avg 1260.

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

## Next levers

Explicit AIDE draft/improve/debug tree search · per-genre domain-knowledge routing · a scratch bash
tool for the inner agent · multi-candidate generations · **KernelBench on the V100s** (`fast_p`).
