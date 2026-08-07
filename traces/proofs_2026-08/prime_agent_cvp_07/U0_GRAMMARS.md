# U0_GRAMMARS.md — precise campaign conventions (version 1)

This file fixes terminology for the U0a/U0b tractability gate.  It is a
campaign definition, not a claim that the current finite serializer satisfies
or avoids any class.

## Numerical object and semantic equivalence

A CVP factor is an integer matrix `C in Z^(m x n)` of full column rank, a
target `t in Q^m`, and a radius.  Its lattice is

`L(C) = { C z : z in Z^n }`.

The systematic equality presentation is

`D=[I_m|-C]`, with variables `(y,z)` and objective `||y-t||_2^2` subject to
`D(y,z)=0`.  Only the numerical pair `(C,t)` is the algorithmic input.

The following preprocessing is semantically free and must be covered by any
claim that a known algorithm cannot apply:

1. signed permutation of ambient `y` coordinates, applied also to `t`;
2. any lattice-basis change `C -> C Q`, `z -> Q^-1 z` with
   `Q in GL_n(Z)`;
3. any equality-row change `D -> U D` with `U in GL_m(Z)`;
4. addition/removal of auxiliary variables only when an explicit
   polynomial-bit integer bijection between feasible sets is supplied and the
   ambient objective is preserved exactly (or by a declared common scale).

Kernel preservation alone is not enough for item 4: new objective coordinates,
targets, and weights must be included in the certificate.

## IDs versus structural colors

Row/column IDs (stage, lane, gate number, selector number) may grow with the
instance and are used only for serialization.  A **structural color** belongs
to one fixed finite alphabet independent of `S` and the formula.  Unique IDs
are never colors.  Marks invisible in `(C,t)` cannot obstruct an unmarked
algorithm unless the claimed color is proved intrinsically recoverable from
`(C,t)`.

For `u0a-butterfly-nand-copy-factor-v1`, the version-1 structural row colors
are the seven `kind` values

`NORM_DROP_GUARD, SOURCE_PROGRAM, GATE_PROGRAM, EDGE_CONSISTENCY,
 DYADIC_SEPARATOR, OUTPUT_INTERFACE, PHYSICAL_SELECTOR`,
and the structural column colors are `SOURCE_SELECTOR,GATE_SELECTOR`.
Stage/lane/mode/state fields are semantic metadata, not automatically colors.
These two displayed sets are the version-1 structural alphabets; any refinement must itself be fixed and finite before quantifying over instances.

## Fixed-template n-fold grammar

A template is two fixed integer matrices

`A in Z^(r x q)`, `B in Z^(s x q)`.

For a variable brick count `N`, rows are `Global(r)` followed by
`Local(i,s)` for `i<N`; columns are `Brick(i,q)`.  Entry `(row,column)` is
`A[a,b]` for a global row and `B[a,b]` when row and column have the same brick,
and zero otherwise.  The integers `r,s,q`, all entries, and the finite
structural-color maps are independent of `N,S,F`.

## Fixed-finite-type generalized n-fold grammar

A template has a fixed finite type set `T`.  Type `tau` carries fixed blocks
`A_tau in Z^(r x q_tau)` and `B_tau in Z^(s_tau x q_tau)`.  An instance is a
sequence of brick types.  The global/local block formula is the same as above.
`T,r,q_tau,s_tau`, coefficients, and structural colors are uniform.  This is
the precise campaign class; no claim is made here that every use of the phrase
“generalized n-fold” in the literature has identical parameter conventions.

## Fixed-depth tree-fold grammar

A template fixes a depth `h`, finite node types at every level, a fixed leaf
column width for each leaf type, and one fixed row block for each permitted
ancestor/leaf type pair.  An instance chooses a rooted tree of depth at most
`h` and assigns allowed types.  A node-row block is supported exactly on the
columns of descendant leaves and uses the fixed block selected by the two
types.  Depth, type sets, block dimensions, coefficients, and colors are
independent of `S,F`; only the tree and its branching vary.

## Fixed-finite-type two-stage grammar

A template fixes a shared first-stage width `q0`, a finite scenario type set
`T`, and for every `tau` fixed matrices

`A_tau in Z^(s_tau x q0)`, `B_tau in Z^(s_tau x q_tau)`.

An instance has one shared column block and a variable sequence of scenarios.
Scenario `i` has rows `[A_tau | B_tau]` on the shared columns and its own local
columns, and zero on other scenarios' columns.  All dimensions, types,
coefficients, and structural colors are uniform.

## Recognition and exclusion quantifiers

“Syntactically in a fixed-template class” means equality after the class's
allowed row/column permutations with one template fixed independently of the
whole family.  Finite evidence at `W=8,16,32` cannot prove family
nonmembership.

“Excluded from direct known-class preprocessing” is stronger: there must be no
polynomial-bit sequence of the semantic equivalences above that reaches a
syntactic fixed-template instance.  Raw incidence support, ordinary marked
neighborhood diversity, and integral column circuits of one chosen basis are
not yet proved invariant under this full closure.  U0b remains open until a
lattice-intrinsic invariant and four separate template bounds are certified.

## Equality gadget certificate

The gadget library, its arities, and its integer coefficients are fixed independently of `S,F`; alternatively a uniform generator must have separately proved bounds that cannot encode the whole instance as one gadget.  Every allowed auxiliary equality gadget must ship:

- the expanded integer matrix and target;
- forward and inverse integer maps between feasible coefficient sets;
- polynomial bit-length bounds for both maps;
- exact equality of ambient vectors and objective values (or one declared
  global scale);
- a fixed finite structural-color map;
- if a support-minor argument is used, the connected-fiber edge-lift
  certificate of `Verify_support_minor_channel.lean`.

A connected-fiber graph contraction without the objective/bijection data is
only minor plumbing, not a CVP equivalence.

## Current finite serializer status

`experiments/verify_u0a_universal_topology_serializer.py` freezes complete
integer `C,D`, targets/interfaces, IDs, and hashes at widths `8,16,32` and
checks three honest programs per width.  It does not provide a total
`Serialize(S,F)`, formula compiler, polynomial family proof, full-rank theorem,
class recognition, or soundness.  Its dyadic separator rows are redundant
integer sums of edge rows and therefore add no row-space information.  The
frozen gate depths `8,10,12` also fail to embed strict chains of lengths
`9,11,13`; an all-size serializer needs a separate polynomial depth parameter.


## Generation-11 parameterized compiler status

The numerical generator now has a positive depth parameter, and
`Verify_u0a_serializer_dimensions.lean` proves its exact polynomial dimension
formulas.  The finite formula compiler fixes the previous output-target issue
by cleaning unused lanes and asserting only the root.  It has passed the
finite family recorded in STATUS.  These executable routines do not yet
constitute the universal `Serialize(S,F)` lemma: generic compiler correctness,
canonical input encoding, bit complexity, and emission time still require a
compiled proof or a verifier whose universal kernel is formalized in Lean.


## Generation-12 semantic and totality status

`Verify_nand_formula_compiler.lean` proves assignment-independent NAND
formula semantics and linear postorder instruction count for all inductive
formulas.  The finite canonical manifest implements the version-1 byte
interface.  Python traversal and exact canonical encode/decode are now
iterative, and the former 1,101-leaf recursion witness passes an exact dry
scheduler.  That compressed path omits its enormous modes grid and actual
`C,D,target_y`, however.  Until an actual streamed emitter and its
physical-trace correctness theorem exist, the Lean semantic compiler and
numerical serializer remain components without a universal connecting theorem.


## Generation-13 streaming status

Canonical formula parsing and scheduling are iterative.  The large dry
manifest is a count/hash certificate and explicitly is not the numerical CVP
output.  The complete `serialize` implementation still eagerly materializes
program dictionaries, sparse C/D triple lists and targets; its certified
256-MiB S=16 failure means it does not yet meet the campaign's total streaming
interface.  A future emitter must define canonical record order and hash while
streaming every required triple/target coordinate.


## Generation-14 factor stream status

Complete sparse factor and target emission is canonical and cap-tested at
S=16, with a universal COO matvec semantics theorem.  The program remains a
dense padded dictionary, so the total streaming contract is not yet met.  A
version-2 program grammar must specify a default mode, ordered sparse overrides,
padding and cleanup in a way that determines every GATE_PROGRAM target bit
without full expansion.


## Generation-15 sparse program grammar

Program v1 uses a raw COPY_A default, a strictly stage/lane-sorted unique list
of non-COPY_A overrides, an explicit COPY_A padding interval, and a cleanup
stage with ZERO default and one root COPY_A override.  Source/output defaults
and overrides are ordered separately.  `Verify_sparse_program_overrides.lean`
proves the generic dense/target semantics of this convention.  A future schema
change must preserve these boundary and uniqueness properties or increment the
version.


## Generation-16 honest lane bridge

Sparse program events now have a formal honest-Boolean semantics.  A valid
scheduled event records an involutive neighbor map and local adjacency facts;
physical gate modes equal the logical WAIT/SWAP/DUPLICATE/NAND+ZERO/cleanup
effect.  The schema still lacks a universal proof that its generated event
stream satisfies these validity facts and maps to the streamed factor rows.


## Generation-17 event certificate status

Butterfly events are valid by construction when encoded as dimension plus one
endpoint, with the partner generated by XOR.  The finite JSON certificate also
includes full token-map snapshots, but those are nonessential and fail the
1,025-leaf resource test.  A versioned delta-certificate schema should retain
formula tables, ordered events, operands/endpoints, overrides and optional
checkpoints while omitting per-event full maps.


## Generation-18 delta certificate schema

Event certificate v2 omits per-event token maps.  It contains canonical formula
tables, one initial/final map, ordered event deltas and optional framed
checkpoint hashes.  Checkers must replay deltas against their own state and
bind flattened mode overrides to the sparse program.  Version 1 remains only a
bounded diagnostic format.


## Generation-19 explicit delta schema

Event certificate v3 uses generic `(token,newLaneOrNull)` assignments.  Event
records have unique token names; WAIT is empty, SWAP lists occupied endpoint
moves, DUPLICATE lists one creation, and NAND orders two deletions before one
creation.  Version-3 checkers apply removals before insertions and reject lane
collisions.  Initial/final maps remain the only snapshots.


## Generation-20 finite-lane convention

For width `2^k`, physical lanes are `Fin (2^k)` and stage dimensions are
`Fin k`; neighbor is XOR by the corresponding power of two.  This typed
convention makes range closure and non-self adjacency theorem-level facts.
Concrete event validity additionally carries occupancy injectivity, destination
freeness and freshness; valid traces preserve these invariants.
