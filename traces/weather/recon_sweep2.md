# WeatherBench-2 seed sweep — de-noised baseline vs champion

3 seeds/scaffold, fixed 120s compute, inner=anthropic/claude-sonnet-5

## baseline_v0
- skill: **0.2621 ± 0.0109**  (min 0.2500, max 0.2709, n=3)
- z500 RMSE: 697.3 ± 7.4   t850 RMSE: 2.917 ± 0.058
- raw skills: 0.266, 0.250, 0.271

## champion
- skill: **0.2715 ± 0.0108**  (min 0.2590, max 0.2781, n=3)
- z500 RMSE: 686.0 ± 8.9   t850 RMSE: 2.891 ± 0.051
- raw skills: 0.278, 0.259, 0.277

## Verdict
Δ(champion − baseline) skill = **+0.0093**  (pooled sd ≈ 0.0108, ~0.86σ)
→ delta is within ~1 pooled sd — not clearly above the noise; needs more seeds/compute.
