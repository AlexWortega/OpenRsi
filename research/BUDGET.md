metric                = ale_performance   # AtCoder performance 0..3500 from private_eval
direction             = higher
seed_experiments      = 1                 # gen-0 baseline scaffold
seconds_per_experiment = ~160/problem     # inner solve wall-clock (Sonnet 5, budget 6)
parallelism           = 1                 # sequential problems (num_workers=12 per eval)
compute_cap           = eva01 (48 cores, 4x V100), OpenRouter tokens
# --- generational loop ---
max_generations       = 6
hypotheses_per_gen    = 1                 # one candidate scaffold / generation (keep-if-better)
proposers             = 1 (Opus 4.8 outer)
critics               = private_eval selection (held-out cases)
stagnation            = 3
--- spent ---
generations_run = 0
experiments_run = 1                       # gen-0 ahc008 validated
best_metric     = 1096 (ahc008, gen-0 baseline)
champion        = scaffold v0 (default)
