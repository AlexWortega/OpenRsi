# Solution traces

Raw run logs + run dirs (board.jsonl, RESULTS.md, goal_plan.json, node/variant JSONs) +
agent-generated `solution.py` kernels from the experiment campaign. See `../benchmark.md`
for the scoreboard. Third-party benchmark harness files (reference.py/check.py/etc.) are
NOT included — only our logs and the agent's own outputs.

## mega/ — KernelBench-Mega (Kimi-Linear W4A16 decode megakernel), Blackwell

Model 20h campaign (correctness-first recipe + snapshot-eval + maxTokens=16000 + $150 cost-cap):
- `glm_mega.log` / `glm_mega_run/` — GLM-5.2: 20h, cosine **0.9782** near-miss (PASS=false), $11
- `kimi_mega.log` / `kimi_mega_run/` — Kimi-k2.7-code: 20h, **4.619× PASS**, 1031 tool calls, $30
- `qwen_mega.log` / `qwen_mega_run/` — Qwen3.5-122b-a10b: 20h, **1.984× PASS**, $34
- `laguna_mega.log` / `laguna_mega_run/` — laguna-s-2.1: 6h, **0.079× PASS** (correct but 12× slower), $28

Opus recipe arc (single-solve, GENERATIONS=0) + BoN + early RSI probe:
- `mega_rsi.log` / `mega_rsi_run/` — 45min bounded-edit RSI probe (confounded 0-baseline)
- `mega_2h.log` — 2h ambitious high-think → 0 (never validated)
- `mega_fast.log` — 90min fast-iterate, no snapshot-eval → 0 (harness lost snapshot)
- `mega_fast2.log` / `mega_fast2_run/` — 90min fast-iterate + snapshot fix → **4.956×**
- `mega_record.log` / `mega_record_run/` — 3h same recipe → **5.513×**
- `bon_{1..4}.log`, `bon_master.log` — best-of-4 @60min → best **6.116×**
- `*_solution.py` — surviving agent kernels (NOT the 4.6×/1.98× winners — those temp dirs were
  cleaned on PASS; the "save winning kernel" gap. `bon_fail_solution.py`, leftover from GLM/Kimi).

## weather/ — WeatherBench-2 (72h z500/t850 model under fixed compute), eva01 V100

- `run_10gen*` — 10-gen scaffold-RSI: 0.303 → 0.343 (single-eval)
- `sweep*` — de-noised seed sweep: base 0.313±0.034 vs champ 0.326±0.023 (Δ 0.44σ, n.s.)
- `recon_sweep*` — recon+deep-research vs base (Δ 0.86σ); `recon_sweep.*` void (1440s timeout bug)
- `agent_ab.log` — submit-only vs full-coding-agent A/B (full agent = higher ceiling, 3× variance)
- `run_bounded*` — bounded-edit (SkillOpt #1) RSI: 0.313→0.339, accept 1/6
- `laguna.log` / `laguna_run/` — laguna weather: void ($0, 0 evals — didn't engage custom submit tool)
