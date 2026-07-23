# OpenRSI WeatherBench-2 results

Champion scaffold v0, mean persistence skill: **0.0000**
Baseline (gen0) skill: 0.0000  |  RSI delta: +0.0000

Fixed compute budget: 300s / model on one V100.
Total OpenRouter cost: $0.00

## Champion domain knowledge
- Predict the residual (Y - X) not the absolute field: at 72h the state is highly autocorrelated, so learning the tendency beats regressing the whole field.
- Longitude (size 64) is periodic — use padding_mode='circular' on the lon axis; zero-pad or reflect latitude.
- The score is cos(lat)-weighted RMSE averaged over z500 and t850; normalize each channel by its std so the loss balances the two very different scales.
- Fill the fixed compute budget: pick model size + batch so training runs until just before time_budget_s; underusing the budget leaves skill on the table.
