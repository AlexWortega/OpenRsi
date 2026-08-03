# Classical-literature digest for surviving constructions

Only pre-2024 machinery independently relevant to the search is retained. One prohibited-source search hit was reported by the scout as discarded unread; it is not used here. Web snippets are leads, not trusted proofs: any construction adopted below must be checked against the cited primary paper.

## 1. Exact-cover incidence reduction to binary syndrome decoding

Berlekamp–McEliece–van Tilborg (1978) reduce 3-dimensional matching to binary syndrome decoding. For triples `U ⊆ T1×T2×T3`, `|Ti|=q`, let `A` be the `3q × |U|` incidence matrix, target `1`, and threshold `q`. If `Ax=1` and `|x|≤q`, every row has positive odd selected degree, while total incidence is `3|x|`; hence equality forces exactly one selected triple at each element, i.e. a perfect matching.

**Use:** a polynomial sparse dictionary with global counting soundness and no complete-assignment columns.

**Limitation:** only `q` versus `q+1`. Distinct perfect matchings create kernel words of weight at most `2q`, so ordinary kernel girth cannot be made much larger while all YES witnesses coexist.

## 2. Relative distance / quotient-code invariant

For nested binary spaces `B ⊆ C`, define

`d(C/B)=min{|z| : z ∈ C\B}`.

If a feasible fiber is `x0+C`, legal witnesses are exactly `x0+B`, and illegal witnesses lie in `x0+(C\B)`, then every illegal witness has weight at least `d(C/B)-|x0|`. This is the right invariant when many sparse legal witnesses differ by short vectors: legal exchanges may lie in `B`, while only spurious directions need high weight.

Tillich–Zémor hypergraph-product/CSS codes (2009/2014) provide explicit quotient distances. From an `[n,k,d]` code they obtain block length `n²+(n-k)²`, encoded dimension `k²`, and protected distance `d` in the symmetric construction. Chain-complex systoles and CSS distance are instances of relative distance.

**Use:** potentially quotient out all differences among satisfying witnesses while making every non-satisfying syndrome solution a nontrivial high-distance class.

**Missing interface:** construct `B⊆C` from exact cover/SAT so that *all and only* legal exchanges lie in `B`, with `d(C/B)` polynomially larger than the YES baseline. No cited theorem supplies this.

## 3. Explicit sparse-recovery / high-girth shells

BCH/Reed–Solomon/Goppa parity checks give explicit matrices with kernel distance `>2K` using `O(K log N)` binary rows in standard parameter ranges. If `Hx0=t`, then another solution `x` obeys `|x|≥d(ker H)-|x0|`. Lossless-expander and bitmasked-expander matrices similarly give for-all sparse injectivity/recovery over finite fields; unique neighbors prevent cancellation for supports up to `K`.

Sipser–Spielman/Tanner matrices give sparse linear codes with linear kernel distance from expansion.

**Use:** exact anti-cancellation once a single canonical sparse witness, or a quotient version, is available.

**Limitation:** ordinary distance is incompatible with many sparse legal witnesses in one fiber. These results give injectivity or approximately linear support growth, not compounding of a nearby-coset ratio.

## 4. Product/tensor codes

Classical product codes (Elias; modern proof also used by Dumer–Micciancio–Sudan) satisfy `d(C1⊗C2)=d(C1)d(C2)` for every mixed tensor word. The pointed analogue is exact: `p(D⊗E)=p(D)p(E)`. This is already proved in `prior/proof_cvp.md`.

**Use:** definitive mixed-word amplification.

**Limitation:** length multiplies as `n^r`; relative to explicit output length, a base ratio `γ` becomes exponent `log_n γ`, tending to zero for a nearby base gap. No classical code-dependent Hamming-preserving dense fold was found.

## 5. Concatenation and distance amplifiers

Equidistant simplex/Hadamard inner codes multiply every nonzero outer symbol by a fixed Hamming weight, preserving symbol-weight ratios exactly but not compounding them. Alon–Edmonds–Luby/expander amplification can drive absolute relative distance toward a constant, but its lower transform is saturating and can flatten a YES/NO ratio. DMS locally dense affine-coset composition couples blocks through one coefficient vector and has useful exact distance accounting, but its hardness application uses inadmissible PCP machinery and its dense center is probabilistic; it does not compound a nearby ratio.

**Conclusion:** these are useful shells, not the missing gap source.

## 6. Rank condensers and subspace designs

Guruswami–Kopparty subspace designs and Forbes–Guruswami rank condensers give explicit families of quotient maps such that no low-dimensional mixed subspace is killed by too many maps. This directly addresses arbitrary mixed combinations and code-dependent projections.

**Limitation:** guarantees distinguish rank/nonzero from zero, not Hamming support. Stacking quotient maps tends to give almost the same block weight to every nonzero word, flattening rather than amplifying the pointed-distance ratio. A new rank-to-Hamming lemma would be required.

## 7. Homological/systolic codes

Boundary/coboundary quotients naturally classify gauge-trivial differences versus global holonomy. Classical high-dimensional complexes, including unconditional systolic results for Ramanujan complexes (Kaufman–Kazhdan–Lubotzky era), provide sparse boundary matrices where nontrivial homology classes require linear support.

**Use:** conceptually targets the inherited odd-holonomy cheats: legal differences could be boundaries, while inconsistent global holonomy is a nontrivial class.

**Missing interface:** map an arbitrary 3SAT/exact-cover instance into a designated homology class such that SAT has a sparse representative and UNSAT forces nontrivial systole. Building this interface via local agreement checks risks recreating the already-killed pseudoassignments or a PCP-strength lemma.

## 8. Global polynomial codes

Reed–Solomon maximum-likelihood decoding is classically NP-hard (Guruswami–Vardy 2005) via a single global polynomial witness, demonstrating global algebraic consistency without local marginals. AG codes provide longer explicit global evaluation codes with good rate/distance.

**Limitation:** exact hardness is not a polynomial approximation gap. Native symbol Hamming weight does not transfer automatically to binary bit weight, and one-hot symbol gadgets can reintroduce short linear trades.

## 9. Superimposed/disjunct matrices

Kautz–Singleton matrices isolate columns against small *sets* and are excellent nonnegative/OR selectors. They do not imply an XOR nullspace property; binary linear combinations can cancel. They may be an auxiliary indexing layer only, not syndrome soundness itself.

## Ranked construction leads

1. **Exact-cover incidence + quotient relative distance.** Most conceptually aligned: retain global exact counting and quotient all legal matching exchanges. The missing classification `illegal ⇔ nontrivial quotient class` must be explicit and tested.
2. **Homological encoding of exact-cover inconsistency.** Use a sparse chain complex to make spurious parity covers represent nontrivial homology. Must avoid merely relabeling local marginal constraints.
3. **Code-dependent tensor folding via rank condensers.** Classical machinery protects low-dimensional mixed spaces but lacks support sensitivity; a concrete fold should be attacked before theorizing.
4. **Canonicalize then attach BCH/expander shell.** Works only if one can deterministically select one legal witness without solving SAT, or quotient all legal differences.

## Small experiments suggested by the scouts

* Build tiny exact-cover incidence matrices and enumerate all coset leaders/short kernel vectors.
* Construct a small CSS/hypergraph product (e.g. from the `[7,4,3]` Hamming code) and enumerate relative coset leaders.
* Attempt an explicit map from matching exchanges to a boundary subspace and check whether parity covers that are not matchings can remain boundaries.
* Test Kautz–Singleton disjunctness against actual shortest XOR dependencies.
* For any rank-condensing fold, enumerate every mixed pointed tensor word, not just pure tensors.

## 10. Fresh symmetry through bisets/lifted products

A targeted follow-up scout found a classical mechanism outside the residual-lineage no-go. If `U` is an `(H,G)`-biset and `V` a `(G,K)`-biset, the balanced quotient

`U ×_G V = (U×V)/((ug,v)~(u,gv))`

retains a fresh commuting `K`-action. When the spent `G` action is free, size is `|U||V|/|G|`; chains of bisets divide by every intermediate group. Balanced/lifted products of chain complexes are the linear algebraic version, with distance theorems for homological classes and arbitrary mixed chains in specific expander families.

**Opening:** the next group need not descend from `(G×G)/diag G`, so old fixed-cross sectors can in principle be remobilized. This is genuinely outside the theorem in `proof_cvp.md`.

**Pointed caveat found by exact implementation:** adjoining a distinguished fixed coordinate to both factors makes every class `[u,*]` fixed under the fresh right action, because that action acts only on the second factor. `experiments/verify_pointed_biset_cross.py` checks 54 regular cyclic biset products: the new action is free everywhere else, but has exactly `1+R_U` fixed classes when the first factor has `R_U` moving regular orbits. Thus fresh biset symmetry renews most coordinates but does not automatically eliminate pointed cross-sector growth.

Voltage/deck lifts and explicit abelian/quasi-cyclic lifts provide fresh free actions, while balanced products spend them. The unresolved task is to build a sequence of bimodule **codes**, not merely coordinate bisets, with a sparse invariant pointed YES word and mixed-word distance. Ordinary lifts expand by the same group factor later spent. Projecting away star-cross sectors has exact distance results only with extra gauge/chain-complex structure in special terminal sectors; plain nonrectangular puncturing has no general product-distance theorem.

## 11. Code-dependent parity-check simplification (fresh scout)

A targeted pre-2024 scout isolated one exact, basis-invariant compression.  If
`H=[h_1 ... h_n]` is binary, delete zero columns and keep one representative
of each distinct nonzero column.  For every target `t`, the minimum of
`|x|` subject to `Hx=t` is unchanged: replace all selected coordinates in a
parallel class by their parity, and conversely lift a selected class to one
representative.  This is representable-matroid simplification (Crapo--Rota;
Dodunekov--Simonis' projective-multiset code correspondence), specialized to
syndrome decoding.

This exactly identifies a possible tensor-compression invariant: the number
of distinct parity-check column types, rather than formal tensor coordinates.
However, it gives no compression for the reduced tensor family tested here.
For a code `K=ker H`, two columns of `H` coincide iff `e_i+e_j in K`, and a
column is zero iff `e_i in K`.  Hence a kernel of distance at least three has
no simplifiable columns.  In the BMT 3DM pointed construction the moving span
`C` has distance at least three (distinct nonzero incidence columns rule out
kernel weights one/two, while the target fiber has weight at least `q>=3`).
After reduced tensoring the star-zero code lies inside `C tensor C`, whose
ordinary distance is `d(C)^2>=9`.  Thus every formal parity-check column is
again distinct and nonzero, inductively.  `verify_parity_type_tensor.py`
checks 8 -> 64 -> 4096 distinct types on both tiny YES and NO fibers.

The scout also confirmed the limitations of nearby classical tools:
projective multisets retain exact *weighted* generalized weights but do not
convert multiplicity to short unweighted binary Hamming length; product-code
weight hierarchies control arbitrary mixed words but do not compress length;
lossless expanders transform sparse support only linearly; rank condensers
flatten most nonzero vectors to nearly equal block weight; relative
generalized weights still require the failed legal/illegal quotient
classifier; group-algebra correlation has exact difference-set collapse
witnesses; puncturing, shortening, and residual codes give additive bounds.
The full digest is in `scout_code_dependent.txt`.

## 12. Permutation-union / tensor-soundness follow-up

A targeted pre-2024 scout found no equation-only polynomial lattice
representation of the permutation union with sublinear honest norm.  The
integer affine hull of all permutation matrices is the full lattice of signed
row/column-sum-one tables: rectangle moves are differences of permutations
(Birkhoff/Hoffman--Kruskal; contingency-table move literature).  Thus equations
can only make permutations the *minimum-norm* points, recreating the linear
`q` baseline proved above.

The best global selector is the Cauchy--Binet determinant/common-basis
polynomial: its monomial support is exactly the permutations (Brändén's
regular-matroid basis polynomial framework).  Waksman/Beneš networks
parametrize permutations with `O(q log q)` Boolean controls but local
linearization risks tableau faults.  Compound/exterior powers turn spectral
quantities multiplicatively but have dimension `binom(n,k)`.  The Birkhoff
toric ideal has degree-three Markov moves, giving systematic short signed
relations for additive aggregate interfaces.  Nisan's noncommutative ABP
ranks give an exponential barrier when one robustly preserves partial
permutation identity.

The scout also highlighted Haviv--Regev's classical all-sublattices tensor
criterion: multiplicative lattice soundness against arbitrary mixed tensors
requires lower bounds on every rank-r sublattice (support/parity/determinant),
not merely individual NO vectors.  This is the right invariant for a future
integer tensor attempt, but does not compress rank by itself.  Full details and
primary references are in `scout_permutation_union.txt`.

`verify_determinant_permutation_dictionary.py` immediately tests the global
determinant lead at `q=3,4`; explicit monomial dictionaries retain
support-three virtual states, and adding every compound state changes only
finite constants while keeping exponential dictionary/state size.

## Honest assessment

The literature search found no classical theorem that directly yields a deterministic polynomial-factor NCP gap. Relative distance modulo legal differences fails directly because legal affine hulls contain illegal covers. Fresh/balanced tensor symmetry yielded rigorous one-step lemmas but conserved or worsened the standard rank exponent. Exact parity-check simplification is a clean code-dependent operation, but a distance-at-least-three theorem shows that it performs no compression on the BMT reduced tensor ladder. The surviving opening is a genuinely asymmetric code-dependent operation that compresses YES affine fibers more than NO fibers without computing a nearest witness; no classical theorem located here supplies it.
