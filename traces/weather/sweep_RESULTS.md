# WeatherBench-2 seed sweep — de-noised baseline vs champion

5 seeds/scaffold, fixed 120s compute, inner=anthropic/claude-sonnet-5

## baseline_v0
- skill: **0.3127 ± 0.0341**  (min 0.2715, max 0.3531, n=5)
- z500 RMSE: 641.1 ± 34.1   t850 RMSE: 2.753 ± 0.129
- raw skills: 0.296, 0.300, 0.271, 0.342, 0.353

## champion
- skill: **0.3255 ± 0.0225**  (min 0.3029, max 0.3563, n=5)
- z500 RMSE: 630.5 ± 25.6   t850 RMSE: 2.697 ± 0.073
- raw skills: 0.304, 0.303, 0.356, 0.333, 0.332

## Verdict
Δ(champion − baseline) skill = **+0.0127**  (pooled sd ≈ 0.0289, ~0.44σ)
→ delta is within ~1 pooled sd — not clearly above the noise; needs more seeds/compute.
