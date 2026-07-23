# OpenRSI WeatherBench-2 results

Champion scaffold v2, mean persistence skill: **0.3430**
Baseline (gen0) skill: 0.3030  |  RSI delta: +0.0400

Fixed compute budget: 120s / model on one V100.
Total OpenRouter cost: $9.16

## Champion domain knowledge
- Predict the residual (Y - X) and standardize it. Prefer PER-(channel, latitude-row) residual std r_std[c,lat]=std over (samples,lon) of (Ytr-Xtr) with a small floor; residual variance is much larger in mid-latitudes than tropics/poles, so a single scalar lets a few rows dominate the gradient. Broadcast as [1,C,H,1].
- Keep a per-channel scalar r_std as fallback and pick per-(channel,lat) vs scalar on the held-out split by lower cos(lat)-weighted RMSE. Never reuse the INPUT std for the target.
- At inference: pred = X + alpha[c] * (r_std * net_output_standardized). Use a PER-CHANNEL trainable shrinkage alpha[c] in [0,1] via sigmoid (init ≈0.5); optionally grid-search alpha on held-out after training.
- Loss must be cos(lat)-weighted MSE (weights normalized to mean 1 over the 32 latitude rows) to match scoring; apply on standardized residuals so channels and latitudes contribute equally.
- Longitude (64) is periodic — padding_mode='circular' on lon; latitude (32) is not periodic — reflect or zero pad. Optionally roll lon for augmentation (rolling X,Y together preserves the residual).
- Always de-standardize and add X back before returning; guard NaN/Inf and fall back to persistence X for any non-finite element.
- Optionally smooth r_std[c,lat] lightly across latitude to avoid noisy per-row estimates from small samples.
- Fill the compute budget: measure sec/step early, size steps to just under time_budget_s; hold out ~10-15% to pick best checkpoint, choose r_std scheme, and tune alpha.
