I did not search for or use the prohibited document or any discussion of it. These are deliberately non-convergent sketches.

### 1. Logarithmic-scope Möbius quotient

**Core trick.** Choose an explicit splitter family of disconnected scopes \(S\), each of size \(L=\Theta(\log n)\), and include all \(2^L\) scope views. Compute the Möbius coefficient vectors of the global restriction map \(a\mapsto\sum_S e_{S,a|S}\), quotient its nonconstant span, then add a dense relative-distance shell on the remaining classes.

**Expected move.** Prove every inconsistent collection misses the legal affine class in \(n^\varepsilon\) shell coordinates.

**Obstruction check.** O1 bounded signatures: full delta signatures have degree \(L\), not \(<L\). O2 marginal/tableau: dense checks act on complete tables, not proper marginals. O3 local hierarchies: scopes grow logarithmically and are disconnected; existing fixed/proper-connected results do not cover this. O4 phase lifts: none. O5 integer fibers: binary. O6 fingerprints: polynomial scope dictionary, not complete assignments. O7 tensor amplification: unused; rank is direct. O8 exact transfer: applies if a binary gap survives.

**Falsification.** Find an illegal table collection in the legal Möbius affine span, or shell distance \(O(1)\).

**Smallest experiment.** \(L=3,4\); enumerate the all-eight core, twisted cycle, Petersen-flow instance, and tiny 3DM fibers; compute exact quotient coset leaders.

**Likely death.** Affine closure recreates the I10 collapse despite larger scopes.

---

### 2. Code-dependent sparse-PIT tensor fold

**Core trick.** For a reduced tensor code, regard coordinate types as products of generator linear forms. Choose code-dependent Kronecker exponents and several moduli \(x^{M_j}-1\); fold every tensor coordinate into its resulting polynomial coefficient bucket, yielding an explicit dense linear map without expanding all tuples.

**Expected move.** A deterministic sparse-polynomial identity lemma could preserve every low-weight NO mixed word while structured YES powers occupy few buckets, with \(\sum M_j\ll N^r\).

**Obstruction check.** O1 bounded signatures: products have growing global degree. O2 marginal/tableau: no wire or marginal interfaces. O3 local hierarchies: no scopes. O4 phase lifts: no phases. O5 integer fibers: binary. O6 fingerprints: operates on a polynomial generator dictionary, not assignments. O7 tensor amplification: precisely outside fixed sampling, puncturing, and type merging; mixed-word soundness remains unproved. O8 exact transfer: immediate after a binary gap.

**Falsification.** One mixed tensor word folding to zero or below the YES bound, or output bucket count comparable to the full tensor length.

**Smallest experiment.** On existing 8-coordinate YES/NO reduced squares, search \(M_j\le32\) and canonical exponents; enumerate every mixed word and all coordinate relabelings.

**Likely death.** General mixed words are dense polynomials with catastrophic modular cancellations; sparse PIT may be irrelevant.

---

### 3. Exterior-algebra separator automaton

**Core trick.** Recursively bisect the 3DM incidence hypergraph. Represent each partial matching’s separator state by an exterior-algebra vector, retaining only a polynomial representative family; columns are whole-interval transitions rather than gate transcripts.

**Expected move.** Show an illegal odd cover has incompatible exterior rank across many separator levels, while a matching follows one sparse transition path, recursively multiplying cost with near-linear state growth.

**Obstruction check.** O1 bounded signatures: transition columns summarize unbounded subinstances. O2 marginal/tableau: outside only if whole-interval transitions remain atomic; bounded-fan-in composition would fall directly under this obstruction. O3 local hierarchies: separators are global and nested, not fixed scopes. O4 phase lifts: none. O5 integer fibers: binary exterior coordinates. O6 fingerprints: states are separator ranks, not assignments. O7 tensor amplification: recursion is not an ordinary tensor product; arbitrary path-flow combinations still require proof. O8 exact transfer: compatible after binary expansion.

**Falsification.** A support-three splice of interval paths, or exponential representative-family dimension.

**Smallest experiment.** Build balanced separator trees for \(q=3,4\) 3DM, all-eight, and twisted-cycle instances; construct wedge-state transition matrices and enumerate all affine path flows.

**Likely death.** General 3DM has exponential separator width, while representative-set compression may preserve reachability but not Hamming cost.

---

### 4. Deterministic isolation followed by a BCH shell

**Core trick.** Expand each BMT triple variable into an equality-linked block whose Hamming cost is a deterministic weight. Use a polynomial family of splitter-derived weightings and a globally protected branch selector; in a successful branch, one matching should be uniquely and substantially cheapest, permitting a BCH shell without quotienting all legal differences.

**Expected move.** Replace the failed “identify every matching” strategy by automatic metric canonicalization of one matching.

**Obstruction check.** O1 bounded signatures: weighting is global, not a clause signature. O2 marginal/tableau: equality blocks are harmless linear interfaces, but the branch selector may satisfy the tableau assumptions unless globally encoded. O3 local hierarchies: unused. O4 phase lifts: selector is formula-dependent, outside the copy-stable phase theorem. O5 integer fibers: binary weighted replication. O6 fingerprints: columns remain triples. O7 tensor amplification: unnecessary if isolation gives polynomial separation. O8 exact transfer: applies to the final unweighted binary system.

**Falsification.** In every branch, an illegal odd cover costs within a constant of the cheapest matching, or branch superpositions splice cheaply.

**Smallest experiment.** Generate all splitter weights for tiny 3DM; construct equality blocks plus a small BCH check; enumerate matchings, odd covers, and cross-branch sums.

**Likely death.** Polynomial-range deterministic isolation with polynomial multiplicative separation is probably too strong; selector splicing is a second failure mode.

---

### 5. Sum-rank condenser instead of Hamming puncturing

**Core trick.** View a mixed reduced-tensor word as a coefficient matrix \(W\). Apply explicit code-dependent rank condensers \(A_iWB_i\), flatten the small outputs, and use dense binary scramblers so surviving rank becomes Hamming support; this seeks near-linear output rather than retaining all coordinate pairs.

**Expected move.** Prove pointed NO fibers force large aggregate condensed rank, while each YES witness has a low-rank structured image with controlled Hamming baseline.

**Obstruction check.** O1 bounded signatures: global matrix operation. O2 marginal/tableau: no local interfaces. O3 local hierarchies: none. O4 phase lifts: none. O5 integer fibers: binary linear maps. O6 fingerprints: acts only on the sparse code generator. O7 tensor amplification: this is a code-dependent dense structured fold, explicitly outside the proved sampling/type no-go; every mixed \(W\) must be covered. O8 exact transfer: valid only after rank is converted to ordinary binary Hamming weight.

**Falsification.** A low-rank NO pure tensor, or a mixed \(W\) killed by every condenser; dense scrambling may also inflate YES as much as NO.

**Smallest experiment.** Enumerate all \(W\) for existing tiny reduced squares; search Toeplitz/Vandermonde \(A_i,B_i\), recording worst YES, best NO, and binary output rank.

**Likely death.** Rank distinguishes zero from nonzero but not matching from odd cover; pure NO tensors may already have rank one.

---

### 6. Nonabelian deck-lift with whole-walk sectors

**Core trick.** Assign formula-dependent voltages in a small nonabelian group and encode complete fundamental-cycle walks as columns, with separate coordinates for deck sheets. A legal assignment occupies one coherent sheet; inconsistent odd holonomy should traverse many sheets rather than cancel as an abelian phase or homology class.

**Expected move.** Convert odd permutation holonomy into expansion in a Cayley graph, producing a polynomial support penalty without identifying different legal witnesses linearly.

**Obstruction check.** O1 bounded signatures: whole-walk columns are global. O2 marginal/tableau: endpoint-composed walk gadgets would be covered; only genuinely whole-cycle columns escape. O3 local hierarchies: detects global monodromy directly. O4 phase lifts: multivalued, nonabelian, formula-dependent selectors violate copy-stable single-valued assumptions. O5 integer fibers: binary sheet incidence. O6 fingerprints: polynomial walk dictionary, not assignments. O7 tensor amplification: unused; mixed sheet superpositions need direct enumeration. O8 exact transfer: applies if the final matrix is binary.

**Falsification.** A rectangle splice across sheets, a legal assignment with nontrivial voltage, or an illegal cover remaining in one sheet.

**Smallest experiment.** Use \(S_3,D_8,A_4\) on twisted cycles, Petersen flow, all-eight, and tiny 3DM; enumerate whole-walk columns and exact coset weights.

**Likely death.** Polynomially many whole walks may not cover all witnesses; compact interval composition reintroduces tableau faults.
