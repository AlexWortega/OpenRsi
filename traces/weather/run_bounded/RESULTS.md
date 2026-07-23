# OpenRSI WeatherBench-2 results

Champion scaffold v1, mean persistence skill: **0.3389**
Baseline (gen0) skill: 0.3130  |  RSI delta: +0.0259

Fixed compute budget: 120s / model on one V100.
Total OpenRouter cost: $2.84

## Champion domain knowledge
- Predict the residual (Y - X) not the absolute field: at 72h the state is highly autocorrelated, so learning the tendency beats regressing the whole field.
- Longitude (size 64) is periodic — use padding_mode='circular' on the lon axis; zero-pad or reflect latitude.
- The score is cos(lat)-weighted RMSE averaged over z500 and t850. MATCH the training loss to the metric: compute per-pixel squared error in std-normalized residual space, multiply by cos(lat) weights broadcast over the lat axis (normalize weights to mean 1 so LR stays comparable), and average the two channels equally so neither dominates. Optimizing the exact weighted objective, not plain MSE, directly lifts skill.
- Fill the fixed compute budget: pick model size + batch so training runs until just before time_budget_s; underusing the budget leaves skill on the table.
- Add a small spatial-gradient regularizer to the loss: penalize the L2 difference between adjacent-pixel finite differences (use circular diff on lon, forward diff on lat) of prediction vs target, weighted ~0.05-0.2 of the main term. The 72h residual field is smooth, so this suppresses high-frequency CNN noise and improves weighted RMSE without over-smoothing large-scale structure. Tune the weight; drop it if skill drops.
- Balance channels adaptively: if one variable (e.g., t850) has higher residual RMSE, upweight its loss term slightly (inverse-RMSE weighting from a quick validation split) rather than fixed 50/50. Keep weights bounded (e.g., 0.3-0.7) to avoid destabilizing the better channel.
