# PRIME_RESULT.md

## Outcome

The former ROADMAP frontier U0 is **retired and rerouted**, not proved.  Its
claimed known-class exclusion was not a well-defined or basis-robust lemma:
the actual universal-circuit factor had not been emitted, the four uniform
fixed-template grammars were unspecified, and the proposed raw support
invariants fail exact class-side tests.  The new frontier is **U0a,
serializer-and-grammar**.  A later U0b must use a row-basis-invariant
column-matroid obstruction.

No 3SAT-to-GapCVP hardness lemma or dimension-dependent gap was proved.

## Builder / prover / breaker split

- **Builder:** froze the standard fixed `A=B=[1]` n-fold family and its actual
  systematic augmentation `[I|-C]`, then audited neighborhood classes,
  treewidth-one certificates, balanced separators, and faithful subdivision.
- **Prover:** formalized, for all sizes, the cumulative-matrix row-rebasing
  counterexample and its exact sparse support after rebasing.
- **Breaker:** supplied a literal fixed-n-fold row-basis stress test and the
  distinction between killing the raw invariant/roadmap edge and refuting a
  future theorem about an actual serializer.

## Machine-checked results

### 1. Ordinary marked neighborhood diversity is not a fixed-class bound

`experiments/verify_gen8_neighborhood_diversity_nfold_counterexample.py`
uses the literal fixed n-fold template `A1=A2=[1]`.

For `n=8,16,32`:

- colored open-neighborhood counts for `C` are `17,33,65`;
- counts for `D=[I|-C]` are `26,50,98`;
- both support graphs are trees of exact treewidth one;
- `D` has exact `2/3`-balanced separator one;
- subdividing every edge once remains a tree and contracts faithfully.

Verified by:

```bash
python3 experiments/verify_gen8_neighborhood_diversity_nfold_counterexample.py
```

The universal companion
`lean/Verify_two_stage_neighborhood_counterexample.lean` proves that the
fixed two-stage template `A=B=[1]` has `n` pairwise distinct scenario-row open
neighborhoods for every `n`.

### 2. Displayed separator/treewidth is not invariant under equality rebasing

`lean/Verify_row_rebasing_support_failure.lean` proves for every `n`:

- integral first differences and prefix sums are mutual inverse row changes;
- first differences turn the cumulative matrix into identity;
- they send systematic `[I|-C_n]` to lower-bidiagonal-plus-`-I` support;
- every rebased row has support at most three and right columns are leaves;
- before rebasing, when `n=2m`, the cumulative support contains an explicit
  `K_{m,m}`.

`lean/Verify_row_rebasing_kernel.lean` proves that an invertible integral left
row rebase preserves the integer kernel exactly, so it does not change the
feasible coefficient vectors or their Euclidean objective.

All Lean files compile sorry-free against Mathlib:

```bash
cd ~/leanverify
~/.elan/bin/lake env lean /home/alexw/autoresearch-runs/prime_agent_cvp_07/lean/Verify_two_stage_neighborhood_counterexample.lean
~/.elan/bin/lake env lean /home/alexw/autoresearch-runs/prime_agent_cvp_07/lean/Verify_row_rebasing_kernel.lean
~/.elan/bin/lake env lean /home/alexw/autoresearch-runs/prime_agent_cvp_07/lean/Verify_row_rebasing_support_failure.lean
```

### 3. Literal fixed-n-fold basis stress test

`experiments/verify_u0_fixed_nfold_support_counterexample.py` starts from the
same literal fixed n-fold template.  At `n=8,16,32`, cumulative unimodular row
presentations have complete-bipartite incidence supports
`K_{9,8}, K_{17,16}, K_{33,32}` and exact balanced separators `6,11,22`.
The explicit bidiagonal inverse returns the fixed n-fold matrix.  It also
checks colored neighborhood counts `17,33,65` and primal cliques of orders
`8,16,32`.

Verified by:

```bash
python3 experiments/verify_u0_fixed_nfold_support_counterexample.py
```

## What is killed, and what is not

Killed:

1. ordinary color-aware neighborhood diversity as a class-wide U0 invariant;
2. displayed incidence separator/treewidth as a **row-basis-robust**
   tractability-exclusion invariant;
3. former U0 as a sufficient pre-serializer roadmap edge.

Not killed:

- the Generation-8 affine-detector matrices specifically;
- a future precisely stated nonmembership theorem for an actual
  universal-circuit factor;
- bipartite support minors under a frozen row basis and explicitly faithful
  connected-fiber equality expansions.

The earlier `lean/Verify_support_minor_channel.lean` remains valid within
that restricted scope.

## Roadmap reroute and next experiment

ROADMAP now splits the old edge:

- **U0a (active frontier):** emit hash-frozen actual factors `C_{S,F}` for
  sizes `8,16,32`; define marks, formula dependence, all four uniform
  fixed-template grammars, and every allowed equality/rebasing operation.
- **U0b (after U0a/U1):** prove a row-basis-invariant marked column-matroid
  connectivity/branch-width lower bound and a separate fixed-template upper
  bound for n-fold, generalized n-fold, tree-fold, and two-stage forms.

The next experiment must serialize actual universal-circuit cores, search
bounded unimodular row rebasings/decompositions, and compute a column-matroid
connectivity profile.  Another raw-support surrogate is not progress.


---

## Autonomous continuation: Generation 10

After the initial U0 reroute, work continued on U0a.

### Finite actual factors now exist

`experiments/verify_u0a_universal_topology_serializer.py` and the frozen JSON
artifacts under `experiments/artifacts/` provide complete numerical `C` and
`D=[I|-C]` at widths 8, 16 and 32.  The verifier checks three honest programs
per width and exact energies `72,176,416`.  It was run both with `--write` and
again in drift-detection mode.  This moves U0a beyond the previous surrogate,
but remains finite and does not prove a total formula compiler. The exact `verify_u0a_frozen_depth_obstruction.py` audit shows the artifacts themselves cannot embed NAND chains of lengths `9,11,13`, because they have only `8,10,12` gate stages. They are therefore candidate factors, not universal circuits.

### Mandatory localized ghost

`experiments/verify_u0a_serialized_gate_kernel_cheat.py` was run successfully.
The local affine rectangle cancels every nonphysical coordinate.  Physical
selector rows contain it, but malformed energies are only `74,178,418`, an
additive two above honest energies.  This is a mandatory U2/U3 state, not a
soundness or recurrence kill.

### Precise grammars

`U0_GRAMMARS.md` now defines the four campaign fixed-template classes,
uniform quantifier order, structural colors versus IDs, and the required
objective-preserving semantic transformations.  U0a is still missing a total
`Serialize(S,F)`, formula compiler, polynomial family bounds, and all-size
completeness/rank proof.

### Column-matroid repair killed

The tentative U0b column-matroid invariant fails under right-unimodular lattice
basis changes:

- `lean/Verify_right_unimodular_lattice_image.lean` proves that `C` and `CQ`
  have exactly the same integer image and attainable output-cost values.
- `experiments/verify_right_unimodular_column_matroid_failure.py` gives an
  exact dimension-two pair with nonisomorphic systematic column matroids.
- `experiments/verify_u0b_right_basis_circuit_failure.py` verifies same-lattice
  fundamental-circuit support changes `2 -> 9,17,33`.
- `lean/Verify_column_matroid_grammar.lean` compiles and correctly establishes
  only left-row/column-permutation circuit invariance.

All new Lean files compile against Mathlib without `sorry`, `admit`, or added
axioms.  The active frontier remains U0a's all-size compiler; U0b now requires
an invariant intrinsic to the embedded lattice and ambient objective.


---

## Autonomous continuation: Generation 11

The shallow candidate serializer was generalized to an explicit depth
parameter without changing the frozen default artifacts.

### Universal dimension theorem

`lean/Verify_u0a_serializer_dimensions.lean` compiles sorry-free and proves
for all widths/depths represented by its count model:

- selector columns `k=4w+20wd`;
- rows `m=30wd+9w-2d`;
- systematic columns `m+k=50wd+13w-2d`;
- explicit quadratic bounds with constants 24, 39 and 63;
- strict-chain placement iff chain depth is at most serializer depth.

`verify_u0a_parameterized_depth_chain.py` cross-checks actual factors through
depth 33.

### Routing classification

- `verify_u0a_repeated_butterfly_routing_obstruction.py`: default width 8
  reaches `18,688/40,320` coordinate permutations; the ninth stage reaches all
  40,320.  The old example output target was witness-dependent.
- `verify_u0a_two_cycle_permutation_routing.py`: two cycles exhaust all `4!`
  and `8!` permutations and a reversal program passes actual `C,D`.

These are finite routing facts, not an all-width theorem.

### Formula-level compiler

`verify_u0a_butterfly_formula_compiler.py` implements unique FREE sources,
COPY fanout, hypercube swaps, NAND evaluation, polynomial padding and final
ZERO cleanup.  The cleanup makes the target assignment-independent.

It passes:

- all 100 ordered two-variable NAND trees with 2--4 leaves;
- all 400 assignments to those trees;
- an 8-leaf width-8 example over all eight assignments;
- actual `C,D`, exact energies, target-role restrictions and `D(Cz,z)=0`.

This is finite completeness/evaluation only.  The remaining U0a frontier is a
Lean proof of the generic compiler and a canonical total `Serialize(S,F)`
interface.  False asserted outputs currently cost only additive one, so no
soundness or GapCVP gap follows.


---

## Autonomous continuation: Generation 12

### Universal semantic compiler theorem

`lean/Verify_nand_formula_compiler.lean` now compiles sorry-free.  It proves
for every NAND formula and assignment that canonical postorder execution equals
recursive evaluation, repeated variables share one assignment, fixed root
assertions are witness-independent, and compilation emits exactly one
instruction per syntax node.  This is the semantic kernel; butterfly placement
and numerical-factor completeness are outside its scope.

### Canonical finite `Serialize(S,F)` manifest

`verify_u0a_canonical_serialize_manifest.py` passes.  It defines canonical
ordered NAND bytes, fixed-S padding, formula/assignment-independent factor
data, declared target mutations and component hashes.  The S=4 audit checks all
100 formulas and 400 assignments against actual `C,D`; factor hash is
`355b469b8ec4c5cc37101ac04c56615b1d64279ba4566d1bcf87078c3ab4b241`.

### Exhaustive scheduler audit and exact blocker

`verify_u0a_butterfly_formula_compiler_exhaustive8.py` passes all 1,901,166
ordered-shape/equality-pattern cases through eight leaves.  Worst raw stage
count is 77 against budget 294.

`verify_u0a_butterfly_deep_formula_counterexample.py` then kills literal Python
totality: a valid right-deep 1,101-leaf formula reproducibly raises
`RecursionError` at recursion limit 1000.  This is an implementation blocker,
not a mathematical routing counterexample.

The active frontier is an iterative/streaming canonical emitter plus a Lean
bridge from postorder semantics to lane placement, COPY fanout, routing,
cleanup targets and actual `C,D` completeness.  Signed soundness and U0b remain
open.


---

## Autonomous continuation: Generation 13

### Deep recursion blocker repaired

The formula compiler now uses iterative postorder traversal and evaluation.
Canonical encoding/decoding is also iterative.  A new dry-run scheduler stores
only live token placement, counters and a streamed trace hash; padding is a
count rather than a stage-by-lane grid.

`verify_u0a_butterfly_deep_formula_iterative_repair.py` passes at recursion
limit 50.  It fully compiles/simulates a 61-leaf width-64 formula and then dry
serializes the former 1,101-leaf blocker at width 2,048 and depth 991,254.
`verify_u0a_butterfly_deep_formula_counterexample.py` is now a historical
regression: its local legacy recursion fails while current iterative traversal
passes.

### Universal fresh-register theorem

`lean/Verify_nand_register_compiler.lean` compiles sorry-free.  It proves the
abstract postorder SSA compiler has consecutive fresh destinations, one
operation per syntax node, older operands, write confinement, correct root
evaluation, and preservation outside the allocated register interval.  Fresh
COPY/NAND instructions preserve their source registers.  Butterfly lane
placement and factor rows are not yet formalized.

### Next exact blocker

`verify_u0a_eager_materialization_resource_counterexample.py` passes complete
S=4 serialization and deep dry scheduling.  In a fresh child capped at 256 MiB,
the valid S=16 complete serializer raises `MemoryError` after dry scheduling
succeeds.  This is a practical finite failure of eager Python containers, not
an asymptotic lower bound: exact dimensions are polynomial and streaming sparse
output may repair it.

The active frontier is canonical streaming emission of program, sparse C,
systematic D and target, followed by a Lean correspondence from the SSA trace
to butterfly lanes and emitted rows.


---

## Autonomous continuation: Generation 14

### Canonical factor streaming repaired

`verify_u0a_canonical_streaming_emitter.py` now streams row/column metadata,
complete sparse C, systematic D and target in eager canonical order without
retaining matrix triples.  It matches eager output exactly at S=4 and completes
S=16 under 256 MiB:

- `C`: `493440x330304`, 4,457,168 nonzeros;
- `D`: `493440x823744`, 4,950,608 nonzeros.

Independent small-grid comparisons found no ordering or target omission.

### Universal COO theorem

`lean/Verify_sparse_coo_stream.lean` compiles sorry-free and proves online COO
fold matvec equals dense materialization and `Matrix.mulVec` for every integer
record stream, including duplicates and negatives.  Chunk and permutation laws
are also proved.

### Metadata repair and next blocker

The eager WAIT logger recorded the next stage's dimension.  This was fixed;
`verify_u0a_dry_full_trace_hash_mismatch.py` now certifies eager/dry hash
agreement and reproduces the retired hash locally.

`verify_u0a_streaming_program_resource_counterexample.py` locates the next
finite cap failure: S=128 retains 3,213,056 dense program mode entries and
raises `MemoryError` under 256 MiB before matrix streaming.  Counts are still
polynomial.  The next task is a sparse program-override stream and target
emission directly from it.


---

## Autonomous continuation: Generation 15

### Sparse program stream

`verify_u0a_sparse_program_stream.py` replaces the dense padded mode dictionary
with:

- COPY_A raw/padding default;
- sorted nondefault stage/lane overrides;
- counted padding;
- ZERO cleanup default with one root COPY_A override;
- analogous source/output defaults.

Small cases exactly match dense modes, canonical program hashes and every
target row.  Under 256 MiB, S=128 hashes 3,213,056 logical cells with zero dense
mode cells retained.

### Independent breaker audit

`verify_u0a_sparse_program_breaker.py` passes 204 exact eager comparisons and
a width-256 child that hashes 16,781,312 logical cells at depth 65,552.  It
checks ordering, uniqueness, lookup, defaults, padding, cleanup, complete target
agreement and program hashes.  The enormous factor is only prefix-consumed at
that size.

### Universal representation theorem

`lean/Verify_sparse_program_overrides.lean` compiles sorry-free and proves:

- sparse lookup equals dense materialization;
- sorted overrides have unique keys and return recorded values;
- absent keys select the default;
- sparse and dense program-row targets agree;
- exactly one mode row is selected per cell.

The active frontier is the Lean correspondence from sparse event generation to
fresh-register semantics, butterfly lane placement, and emitted factor/target
rows.  Complete large output volume, signed soundness and U0b remain open.


---

## Autonomous continuation: Generation 16

### Universal butterfly lane semantics

`lean/Verify_butterfly_lane_semantics.lean` compiles sorry-free.  It proves
honest Boolean semantics for WAIT/padding, SWAP, DUPLICATE, NAND+ZERO, cleanup
and ONE cells on XOR-neighbor butterfly stages.  Any scheduled trace satisfying
local validity has physical lane execution exactly equal to logical event
execution.

### Complete finite numerical bridge

`verify_u0a_sparse_matrix_trace.py` selects one actual state column per node and
checks every streamed C and D row: normalization, program, edge, separator,
output and physical moments, systematic `[I|-C]`, `D(Cz,z)=0`, cleanup and
energy.  It checks 1,150,512 rows including a full width-16 capped pass.

`verify_u0a_sparse_numerical_bridge_breaker.py` independently regenerates every
C coefficient at widths 4 and 8, exhausts formulas/repeated-variable patterns
through five leaves, performs 6,878 packed evaluations and 1,044 full C checks,
and rejects deliberate offset, neighbor, COPY_B and fanout mutations.

The active proof gap is now precise: prove the generic sparse compiler emits a
valid scheduled-event trace and preserves its token map, then connect that map
universally to selected factor columns and streamed rows.  Signed soundness and
U0b remain open.


---

## Autonomous continuation: Generation 17

### Valid-by-construction Lean events

`lean/Verify_butterfly_lane_semantics.lean` now defines smart XOR events and
proves every generated event/trace satisfies adjacency, distinctness and
involution automatically.  Physical and logical lane execution therefore agree
for all smart traces without a validity premise.

### Independent event/token certificate

`verify_u0a_event_token_certificate.py` JSON-round-trips a producer artifact,
then independently verifies formula tables, all event dimensions and token-map
transitions, sparse overrides, padding/cleanup, selected numerical columns and
every projected C row.  It checks 102 formulas, 408 assignments, 1,347 events
and 3,781,920 row projections, including a capped width-16 pass.

`verify_u0a_sparse_event_validity_breaker.py` adds 486 bounded symbolic comb,
balanced and fuzz cases through 129 leaves, covering occupied and empty swaps
and duplication after base-token movement.

### Next blocker

`verify_u0a_event_certificate_resource_counterexample.py` passes a 129-leaf
certificate but reproduces `MemoryError` on a valid 1,025-leaf comb under
256 MiB because every event stores complete token maps before and after.

The active frontier is a streamed delta/checkpoint certificate and a universal
proof that the Python event generator elaborates to the Lean smart-XOR trace,
followed by selected-column/row completeness.  Signed soundness and U0b remain
open.


---

## Autonomous continuation: Generation 18

### Snapshot-free delta certificate

`compile_formula_sparse(..., certificate_version="v2")` now omits every
per-event full token map.  It retains canonical event deltas plus one initial
and final map.  Optional checkpoints are framed hashes of replay state.

`verify_u0a_delta_event_certificate_breaker.py` independently replays the JSON
artifact and rejects seven mutations involving missing/colliding tokens,
reordered events, omitted overrides, checkpoint substitution, and missing
semantic operands.  Under 256 MiB a 4,097-leaf comb passes with 84,863 events
and approximately 122 MiB RSS, repairing the former 1,025-leaf snapshot failure.

### Universal replay theorem

`lean/Verify_event_delta_replay.lean` compiles sorry-free.  It proves sparse
delta append/replay laws and that local transition equality at each reached
state composes to equality with logical execution.  A snapshot-free trace
certificate therefore reaches its claimed final map, pointwise for every token.

The remaining proof obligation is concrete instantiation: prove each Python v2
delta is the token-map update of its corresponding Lean smart XorEvent, then
connect final token placement to selected factor columns and streamed rows.
Signed soundness and U0b remain open.


---

## Autonomous continuation: Generation 19

### Explicit v3 token deltas

Certificate v3 now emits generic token assignments directly:

- WAIT: empty delta;
- SWAP: one or two occupied endpoint moves;
- DUPLICATE: one fresh-token creation;
- NAND: delete left, delete right, create output.

No intermediate token snapshots are built or serialized.  V1/v2 program data
and event fields remain compatible.

`verify_u0a_explicit_token_delta_breaker.py` independently derives the expected
delta at each reached state and rejects nine mutations involving missing SWAP
moves, empty-empty routing, deletion/order errors, duplicate writes, invented
endpoint tokens and lane collisions.  The 4,097-leaf capped audit passes with
84,863 events and 22,091 delta records.

### Universal concrete-delta theorem

`lean/Verify_concrete_event_deltas.lean` compiles sorry-free.  Under exact
occupancy, freeness, freshness and distinctness preconditions, it proves the
canonical WAIT/SWAP/DUPLICATE/NAND Change lists equal logical token-map updates.
These local theorems compose to snapshot-free final-map and pointwise token
correctness.

The remaining universal bridge is to prove the concrete Python scheduler
maintains those preconditions, finite-width lane bounds, and canonical v3
emission throughout formula compilation, then connect the final map to streamed
numerical rows.  Signed soundness and U0b remain open.


---

## Autonomous continuation: Generation 20

### Finite-width XOR theorem

`lean/Verify_butterfly_finite_width.lean` compiles sorry-free and proves that
XOR by a legal dimension remains inside width `2^k`.  It defines the neighbor
on `Fin (2^k)`, proves involution and fixed-point freeness, and gives valid-by-
construction finite smart events.

### Token occupancy and counts

`lean/Verify_concrete_event_deltas.lean` now proves occupancy injectivity is
preserved by valid events and traces.  Exact active-token changes are:

- WAIT: 0;
- SWAP: 0;
- DUPLICATE: +1;
- NAND: -1.

### Boundary breaker

`verify_u0a_v3_power_boundary_breaker.py` passes at 8,191, 8,192 and 8,193
leaves, crossing width 8,192 to 16,384.  It replays hundreds of thousands of
v3 events per capped child and rejects 12 lane, dimension, adjacency, delta,
stage, output and snapshot mutations.

The remaining honest-completeness proof is the scheduler induction itself:
show postorder token demands, free-lane allocation and hypercube paths always
produce the typed finite valid events already covered by the Lean local and
trace theorems.  Signed soundness and U0b remain open.
