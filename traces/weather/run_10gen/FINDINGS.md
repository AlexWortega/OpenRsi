# OpenRSI findings (shared board)
Generations run: 10
Baseline (gen-0) fitness: 0.3
Current champion: gen6 scaffold.v2 fitness=0.3
RSI delta: +0.0 over baseline
Goal: achieved=true onTrack=true holding=[1,2,3,4] failing=[]
Steer: All gating criteria are met: model.py runs end-to-end with finite, correctly-shaped predictions; the champion achieves a positive persistence skill score (0.373 > 0), beating the 72h persistence basel
## Generation log
- gen0 v0: fitness=0.303 ACCEPTED ★champion — baseline weather scaffold (no RSI)
- gen1 v1: fitness=0.327 ACCEPTED ★champion [goal ACHIEVED] — [survived critique] Refocus the scaffold on the target and normalization pipeline: standardize the RESIDUAL by its own per-channel std (comp
- gen2 v2: fitness=0.319 rejected [goal ACHIEVED] — [survived critique] Keep the champion's winning residual+shrinkage pipeline intact and target THIS variant's angle: the loss. Make the train
- gen3 v2: fitness=0.298 rejected [goal ACHIEVED] — [survived critique] Keep the champion's winning residual+per-channel-std+shrinkage pipeline and cos(lat)-weighted loss exactly, and target T
- gen4 v2: fitness=0.304 rejected [goal ACHIEVED] — [survived critique] Keep the champion's winning residual + per-channel r_std standardization + cos(lat)-weighted loss + alpha shrinkage pipe
- gen5 v2: fitness=0.307 rejected [goal ACHIEVED] — [survived critique] Keep the champion's proven residual + per-channel r_std standardization + cos(lat)-weighted loss + alpha shrinkage pipel
- gen6 v2: fitness=0.343 ACCEPTED ★champion [goal ACHIEVED] — [survived critique] Stay on the champion's residual+shrinkage pipeline but sharpen exactly the normalization angle: replace the single per-c
- gen7 v3: fitness=0.312 rejected [goal ACHIEVED] — [survived critique] Keep the champion's residual + per-(channel,lat) std + shrinkage + cos(lat) loss pipeline exactly, and sharpen only the 
- gen8 v3: fitness=0.341 rejected [goal ACHIEVED] — [survived critique] Keep the champion residual plus per-channel-lat r_std plus per-channel trainable alpha shrinkage plus cos-lat-weighted M
- gen9 v3: fitness=0.236 rejected [goal ACHIEVED] — [survived critique] Keep the champion's winning residual + per-(channel,latitude) r_std standardization + per-channel trainable alpha shrink
- gen10 v3: fitness=0.295 rejected [goal ACHIEVED] — [survived critique] Keep the champion's winning residual + per-(channel,latitude) r_std standardization + per-channel trainable alpha shrink
## Levers (shipped)
- Explicit AIDE draft/improve/debug tree search (OPENRSI_SOLVER=aide).
- Per-genre domain-knowledge routing (scaffold.domain_knowledge_by_genre).
- Scratch bash shell for the inner agent (OPENRSI_SCRATCH=on).
- Multi-candidate generations (OPENRSI_INNER_CANDIDATES best-of-N at the draft root).
- grok-build goal plan + direction checker (goal_plan.json + per-gen verdict above).
- KernelBench fast_p fitness on the RTX PRO 6000 (OPENRSI_KB_FITNESS=fast_p).
