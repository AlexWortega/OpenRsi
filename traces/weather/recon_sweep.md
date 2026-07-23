# WeatherBench-2 seed sweep — de-noised baseline vs champion

4 seeds/scaffold, fixed 120s compute, inner=anthropic/claude-sonnet-5

## baseline_v0
- skill: **0.2311 ± 0.0411**  (min 0.1699, max 0.2568, n=4)
- z500 RMSE: 718.2 ± 37.5   t850 RMSE: 3.076 ± 0.173
- raw skills: 0.257, 0.170, 0.245, 0.252

## champion
- skill: **0.1781 ± 0.1190**  (min 0.0000, max 0.2491, n=4)
- z500 RMSE: 712.9 ± 7.0   t850 RMSE: 3.048 ± 0.054
- raw skills: 0.000, 0.249, 0.234, 0.229

## Verdict
Δ(champion − baseline) skill = **-0.0530**  (pooled sd ≈ 0.0890, ~-0.60σ)
→ delta is within ~1 pooled sd — not clearly above the noise; needs more seeds/compute.
