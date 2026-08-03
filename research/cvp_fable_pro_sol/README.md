# Fable / Pro / Sol CVP loop

Build and verify the state machine without API calls or filesystem writes:

```bash
npm run build
node dist/proofs/run7.js --dry-run
```

Launch a live run only after choosing the USD launch cap:

```bash
OPENRSI_PROOFS_BUDGET_USD=30 \
OPENRSI_MAX_GENERATIONS=3 \
npm --silent run proofs:run7
```

For a genuinely fresh campaign with no copied checkpoint, prior idea population, status, proof draft, literature digest, or verifiers:

```bash
OPENRSI_FROM_SCRATCH=1 \
OPENRSI_PROOFS_BUDGET_USD=30 \
node --env-file=.env dist/proofs/run7.js
```

Optional model overrides are `OPENRSI_FABLE_MODEL`, `OPENRSI_PRO_MODEL`, and `OPENRSI_SOL_MODEL`. Use a fresh `OPENRSI_PROOFS_DIR` for every launch. The orchestrator records `state.json`, per-generation proposals/reviews, `SOL_RESULT.json`, independently rerun verifier evidence in `MACHINE_VERIFICATION.json`, and the final `GATE.json`.

The USD value is a conservative stage-launch cap, not a provider-side billing ceiling: parallel calls reserve a configurable amount before launch, but an in-flight provider request may finish above its reserve. Defaults and overrides are documented in `BUDGET.md`.
