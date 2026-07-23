# OpenRSI — Benchmark Log

Everything that ran, with scores, tool-calling validity, budget, cost and notes.
Hardware: **eva01** (4× V100), **eva02** (A6000), **RunPod** (RTX PRO 6000 Blackwell),
**Azure** (RTX PRO 6000 Blackwell, MIG 4g.96gb). Models via OpenRouter.

`tools` = did the model correctly see + call the harness tools. `valid`/PASS = produced a
scoreable (correct) solution. Higher = better except where noted.

---

## 1. Model × capability matrix (KernelBench-Mega, the hardest coding task)

Task: Kimi-Linear W4A16 fused single-launch decode megakernel; correctness gate cosine ≥ 0.98;
score = geomean decode speedup over baseline.py (>1 beats baseline).

Ranked by best correct geomean. `budget` = per-solve wall-clock. All non-Opus rows are the
**20h correctness-first campaign** (fast-iterate recipe + snapshot-eval + maxTokens=16000 cap +
$150 cost-cap), same Blackwell GPU. Smoke first confirmed each model's tool-calling + latency.

| model | slug | tools (latency) | correct | best geomean | budget | notes |
|-------|------|:---------------:|:-------:|:------------:|:------:|-------|
| **Opus 4.8** | `anthropic/claude-opus-4.8` | ✅ ~38s/step | ✅ | **18.45×** record · 6.12× BoN | 3h · 4×1h | headline record, beats SOTA 14.4×; correct **and** fast |
| **Kimi-k2.7-code** | `moonshotai/kimi-k2.7-code` | ✅ 4s | ✅ | **4.619×** | 20h | ~~was incorrect-FAIL~~ → now correct+fast (**#2**); 1031 tool calls, $30 |
| **Qwen3.5-122b-a10b** | `qwen/qwen3.5-122b-a10b` | ✅ 2s | ✅ | **1.984×** | 20h | correct, ~2× over baseline; $34 |
| **laguna-s-2.1** | `poolside/laguna-s-2.1` | ✅ **73s** | ✅ | **0.079×** | 6h | correct but **12× SLOWER**; slow inference + one-giant-turn (needed maxTokens cap); $28 |
| **GLM-5.2** | `z-ai/glm-5.2` | ✅ 4s | ❌ (0.9782) | 0 | 20h | ~~was cheat-FAIL (`import reference`)~~ → honest **near-miss**, −0.0018 to the 0.98 cosine gate; $11 |

**Takeaway:** with **20h + a correctness-first scaffold**, **4 of 5 non-Opus models reached
correctness** (vs the prior README where GLM/Kimi both FAILED). The bottleneck was **budget +
scaffold discipline, not model capability** — a cheap open model (Kimi) hit **4.6×**, near Opus's
own 4.96–6.12× at ≤3h. Only **Opus** is both correct *and* fast cheaply; **GLM** sits one rounding
error (0.0018 cosine) below the gate; **laguna** is correct but can't optimize and is impractically
slow.

---

## 2. KernelBench-Mega — the budget/recipe arc (Opus, Blackwell)

| run | budget | recipe | geomean | PASS |
|-----|--------|--------|:-------:|:----:|
| A/B single-agent | 1 h | baseline | 4.00× | ✅ |
| A/B AIDE tree (draft/improve/debug) | 1 h | tree search | 3.08× | ✅ |
| ambitious high-think | 2 h | one big turn | **0.000×** | ❌ (never validated) |
| fast-iterate, no snapshot-eval | 90 min | medium think + correctness-first | 0.000× | ❌ (harness lost snapshot) |
| **fast-iterate + snapshot-eval fix** | 90 min | winning recipe | **4.956×** | ✅ |
| record-attempt | 3 h | same recipe | **5.513×** | ✅ |
| **best-of-N (4×, 2 concurrent)** | 4×60 min | BoN | **6.116×** | ✅ (1/4 hit; 3/4 whiffed at 0×) |
| published record *(prior)* | 3 h | — | 18.45× | ✅ |

Findings:
- **Depth beats a fancy tree** at 1 h (single-agent 4.00× > AIDE 3.08×).
- **More time barely helps**: 90 min→4.96×, 3 h→5.51× (2× time = +0.55×). Ceiling is variance-bound.
- **The winning recipe = fast-iterate (medium think, ~38s/step) + correctness-first (get PASS,
  snapshot best_solution.py) + snapshot-eval** (score the best passing snapshot, not the aborted
  final). This converted repeated 0× → reliable ~5×.
- **BoN wins**: best-of-4 @60min (**6.116×**) > single @3h (5.51×). More independent samples > more
  time — 3/4 draws whiffed (0×), 1 tail draw beat everything. Cost ~$66 for the 4.

---

## 3. WeatherBench-2 (build best 72h z500/t850 model under fixed compute; metric = persistence skill)

Baselines (test-2020, 64×32): persistence z500=929 / t850=4.02 (skill 0); climatology worse.
Inner = Sonnet 5 unless noted. Fitness = persistence skill (1 − mean(RMSE/pers)), higher better.

| run | setup | skill | notes |
|-----|-------|:-----:|-------|
| gen-0 smoke | 45 s train | 0.265 | pipeline validation |
| **10-gen RSI** | scaffold-rewrite | 0.303 → **0.343** | single-eval; accepts gen1+gen6 |
| seed sweep (de-noised) | 5 seeds each | base **0.313±0.034** vs champ **0.326±0.023** | Δ+0.013 = **0.44σ → not significant** |
| recon+deep-research sweep | 3 seeds, fixed timeout | base **0.262±0.011** vs recon **0.272±0.011** | Δ+0.009 = **0.86σ**, consistent but sub-threshold |
| recon sweep (1440s timeout) | 3 seeds | **void** | 8/8 timed out — recon ate the solve budget (bug) |
| **pi full-agent A/B** | submit-only vs full-coding-agent, 3 seeds | submit-only **0.324±0.017** vs full **0.302±0.057** | full agent = higher ceiling (0.367) but **3× variance**, no mean gain |
| bounded-edit RSI (SkillOpt #1) | 6 gens | 0.313 → 0.339 | accept-rate **1/6** ≈ full-rewrite (2/10) → step size not the bottleneck |
| laguna weather | custom `submit` tool | **void** ($0, 0 evals) | laguna didn't engage the custom tool on the big prompt (latency/one-shot) |

Findings:
- Scaffold-RSI **plateaus in the noise** (+0.013–0.04, ≤0.86σ). The keep-if-better gate can't rank
  scaffolds separated by less than per-solve noise.
- **Bounded edits (SkillOpt #1) ≈ full rewrite** → step size isn't the constraint; **noise is** (fix
  = minibatch/repeated validation, SkillOpt #2, built as `OPENRSI_WB_REPEATS` but not yet run at gen).
- **Full coding agent**: higher ceiling, worse consistency — not a free upgrade under fixed budget.

---

## 4. ALE-Bench (AtCoder Heuristic; performance 0–3500; from prior runs, surveyed)

| run | model | result | RSI helped? |
|-----|-------|:------:|:-----------:|
| smoke (ahc008) | Opus | 780 → **1040**, held-out ahc015=1380 | ✅ |
| mvp1 | Opus | gen1 **1262** accepted | ✅ |
| mvp2 / mvp3 | Opus | 1175 / 1181 (gen0) | ⏸ plateau |
| push1790 | Opus | 1414.8 (held-out FAIL) | ⏸ plateau |
| push1790b | Opus | 0.0 (run broke) | ❌ |
| **push1790c** | Opus | **1625.5** (gen0) — 6 gens all rejected → final 1625.5 | ⏸ baseline = ceiling |
| push_gpt56 | gpt-5.6-sol | **1544.8** (~3× cheaper), gen2 rejected | ⏸ plateau |
| full40 | Opus | mean **1399.7** over 40 problems | — |

All strong numbers are **gen-0 baselines**; RSI rewrites got rejected → same plateau as weather/mega.

---

## 5. Cross-cutting findings

1. **The binding constraint is VARIANCE, not compute or step size.** Outcome ≈ a wide random draw
   dominated by (A) agent non-determinism, (B) random fixed-budget spend, (C) the PASS/FAIL threshold.
   Verified: same scaffold re-evaluated swings 0.24–0.37 (weather) and 0×–6× (mega).
2. **Automated scaffold-RSI (the nominal mechanism) is the weakest link** — plateaus at noise, most
   rewrites rejected. Bounded edits didn't help. Fix direction: de-noise the gate (minibatch) + BoN.
3. **What actually improved the agent**: (L1) **agent memory** compounded real lessons (mega
   `0→5.5× recipe`); (L4) **human diagnosis → structural scaffold/harness fixes** (correctness-first,
   snapshot-eval) drove 0→5×. The automated RSI loop couldn't discover those.
4. **BoN is the highest-leverage lever** — chases the variance jackpot *and* de-noises the gate.
5. **Model tool-calling validity matters**: laguna's tools work (smoke ✅) but 73s/trivial-call
   latency + one-giant-turn (128k maxTokens) behavior made it hang until `maxTokens` was capped.

## Known harness gaps (surfaced this session, fixable)
- No **hard cost cap** (`$X and run`) — laguna mega overshot $20 → **$28.14**.
- `solveWeather` has **no nudge loop** → a model that doesn't tool-call on turn 1 yields a $0/0-eval
  void (bit laguna).
- Winning kernels **not saved** (temp cleaned on PASS) → 5.5× kernel lost; should copy to run dir +
  run the authenticity judge.

## Cost (this session, approx, OpenRouter)
Mega (Opus, Azure+RunPod): ~$83 solves + ~$66 BoN. laguna mega: $28.14. Weather sweeps: ~$10–15.
