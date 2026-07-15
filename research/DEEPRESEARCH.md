# DEEPRESEARCH

## AIDE² / RSI (Weco blog)
- Bi-level loop: outer agent (Claude Opus class) proposes a rewrite of the inner agent's own code,
  evaluates it, keeps it only if better than the previous best (~90% rejection). 100 steps / 8 days.
  https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement
- Selection is on a **private** score the inner agent cannot observe → public-score gaming does not
  survive → the loop "taught itself to cheat less" (KernelBench reward-hack 63%→34%).
- Inner agent = AIDE (arXiv 2502.13138): ML/code engineering as **tree search over code solutions**;
  refine promising nodes. Open-source ref: github.com/wecoai/aideml.

## ALE-Bench (SakanaAI, arXiv 2506.09050)
- AtCoder Heuristic Contest optimization problems; **score-based** (not pass/fail).
- Lite = 10 problems: ahc008, ahc011, ahc015, ahc016, ahc024, ahc025, ahc026, ahc027, ahc039, ahc046.
- API: `ale_bench.start(problem_id, lite_version, num_workers)`; `session.public_eval(code, lang)` →
  Result(overall_absolute_score, overall_judge_result, case_results[]); `session.private_eval(...)` →
  (Result, rank, performance). **private_eval is limited to 1 call/session** → inner iterates on
  public, fitness = 1 private_eval on the best valid solution.
- Metric: raw score → AtCoder **performance** (0–3500). Baselines: ALE-Agent avg **1879**; o4-mini-high
  1520; Gemini 2.5 Pro 1352; human avg 1260. Frontier LLMs are weak on long-horizon consistency —
  the exploitable gap.
- CPU-only, local Docker judge (`ale-bench:<lang>-<version>`); we built cpp23-202301 + python-202301.

## KernelBench (Stanford, arXiv 2502.10517) — Phase 3 stretch
- Write correct + faster GPU kernels (`ModelNew`) vs a torch reference. Metric `fast_p` (correct AND
  speedup>p). Needs an NVIDIA GPU; regenerate baseline timings on the exact GPU (eva01 V100). Frontier
  one-shot fast_1 <20%; agent scaffolds reach ~1.8× avg.

## pi skeleton (earendil-works/pi, npm @earendil-works/* 0.80.7)
- `pi-coding-agent`: `createAgentSession({model, customTools, tools, noTools})`, `defineTool`,
  `AgentSession.prompt()/subscribe()/waitForIdle()`, `getSessionStats()`.
- `pi-ai`: OpenRouter provider auto-reads `OPENROUTER_API_KEY`; `getBuiltinModel("openrouter", slug)`.
- Custom tools = typebox `defineTool`; result `{content, details}`.

## Reusable local prior work
- `vibellm/benchsolve/`: tool_swarm + `execute_python` hit 80–93% on AIME; native tool-calls ≫ JSON.
