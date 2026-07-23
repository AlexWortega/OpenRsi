# OpenRSI findings (shared board)
Generations run: 6
Baseline (gen-0) fitness: 0.3
Current champion: gen1 scaffold.v1 fitness=0.3
RSI delta: +0.0 over baseline
Goal: achieved=true onTrack=true holding=[1,2,3,4,5] failing=[]
Steer: All gating criteria hold: model.py defines a working train_and_predict producing finite, correctly-shaped predictions; it predicts the residual (Y-X) with mean/std normalization and circular longitude
## Generation log
- gen0 v0: fitness=0.313 ACCEPTED ★champion — baseline weather scaffold (no RSI)
- gen1 v1: fitness=0.339 ACCEPTED ★champion [goal ACHIEVED] — [survived critique] Target the loss to match the metric: cos(lat)-weighted MSE in std-normalized residual space with per-channel balancing, 
- gen2 v2: fitness=0.320 rejected [goal ACHIEVED] — [survived critique] This variant targets the training schedule. I add two bounded tips: one giving a concrete optimizer+LR-schedule recipe (
- gen3 v2: fitness=0.293 rejected [goal ACHIEVED] — [survived critique] This variant targets augmentation & regularization. I add a tip prescribing free lon-roll augmentation (valid because lo
- gen4 v2: fitness=0.318 rejected [goal ACHIEVED] — [survived critique] This variant targets architecture. I add two bounded tips: one prescribing a U-Net with residual blocks + a dilated-conv
- gen5 v2: fitness=0.318 rejected [goal ACHIEVED] — [survived critique] This variant targets the target & normalization angle. I add a tip prescribing per-channel residual-std normalization (u
- gen6 v2: fitness=0.332 rejected [goal ACHIEVED] — [survived critique] This variant targets compute-budget efficiency. I add one tip prescribing mixed-precision (AMP autocast + GradScaler) on
## Levers (shipped)
- Explicit AIDE draft/improve/debug tree search (OPENRSI_SOLVER=aide).
- Per-genre domain-knowledge routing (scaffold.domain_knowledge_by_genre).
- Scratch bash shell for the inner agent (OPENRSI_SCRATCH=on).
- Multi-candidate generations (OPENRSI_INNER_CANDIDATES best-of-N at the draft root).
- grok-build goal plan + direction checker (goal_plan.json + per-gen verdict above).
- KernelBench fast_p fitness on the RTX PRO 6000 (OPENRSI_KB_FITNESS=fast_p).
