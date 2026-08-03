# Budget

The live USD cap is intentionally not guessed. Set `OPENRSI_PROOFS_BUDGET_USD` explicitly before launch.

Defaults once a cap is supplied:

- max generations: 8
- Fable/Pro ideation calls per generation: 2 (parallel)
- cross-reviews per generation: 2 (parallel)
- result reviews per generation: 2 (parallel)
- split-verdict rebuttals: at most 2 (one parallel round)
- per-oracle completion cap: 12,000 tokens
- unknown/failed oracle-call reserve: $2 per call (override with `OPENRSI_UNKNOWN_CALL_COST_USD`)
- Sol turn reserve: $5 (override with `OPENRSI_SOL_TURN_RESERVE_USD`)
- Sol model: one persistent session, high reasoning, 12,000-token turn cap
- candidate rule: reproducible verifier failure or unanimous KILL records an autopsy and kills only that candidate; the next generation proposes a fresh route
- campaign stop rule: unresolved split without rebuttal budget, max generations, or exhausted USD budget

Reservations prevent a new stage from launching when too little budget remains. Provider-reported actual cost replaces the reserve after a successful call; an individual in-flight API call can still finish above its reserve, so the USD cap is a launch cap rather than a provider-side billing guarantee.
