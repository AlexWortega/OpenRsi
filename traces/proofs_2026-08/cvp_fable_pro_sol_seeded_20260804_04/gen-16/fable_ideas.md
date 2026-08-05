1. **Splitter-complete divided-power lift.** Let \(\mathcal H\) be an explicit \(r\)-perfect splitter family on the BMT coordinates. For each \(h\), lift \(x\) to every degree-\(\le r\) product of bucket parities \(\sum_{h(j)=a}x_j\); unlike sampled powers, \(\mathcal H\) deterministically isolates every small support. Expected move: retain powered separation with \(2^{O(r)}\operatorname{poly}(m)\), rather than \(m^r\), coordinates.

**Obstruction check.** O1 bounded signatures: outside only when \(r\) grows; fixed \(r\) is covered. O2 marginals: no wire interfaces. O3 local hierarchies: splitters are global. O4 phases: unused. O5 integer fibers: binary construction. O6 complete-assignment fingerprints: coordinates index buckets, not assignments, though function-space rank may recreate the exponential wall. O7 tensor amplification: every mixed lifted word still needs proof. O8 exact transfer: applies directly if the lift is explicit binary.

**Experiment/falsification.** For \(m=8,r=3,4\), generate a standard splitter family, form the exact lifted span, and enumerate all words on YES/NO, all-eight, affine-closure, and holonomy instances. Reject if hostile distance is at most worst YES or rank exceeds the unfurled tensor rank.

**Likely death.** The message-monomial span has dimension \(\sum_{i\le r}\binom{k}{i}\), despite coordinate compression.

2. **Spectral ellipsoid for signed exact covers.** From the formula’s triple-conflict graph, construct a rational PSD form
\[
Q=p(L)^{\mathsf T}p(L)+\varepsilon I
\]
using a Chebyshev polynomial of its signed Laplacian, then use \(\|Bz\|_2^2=z^{\mathsf T}Qz\) inside the exact integer fiber \(Az=\mathbf1\). The hoped-for move is that matchings lie near a low-frequency subspace while every signed NO cover has high-frequency energy; increasing \(\deg p\) amplifies energy without increasing ambient rank.

**Obstruction check.** O1 bounded signatures: \(B\) depends globally on the entire graph, not a fixed local-view polynomial. O2 marginals and O3 scopes: no tableau or proper-scope consistency. O4 phases: unused. O5 integer exact fibers: directly relevant and not escaped unless every constant-support repair has large \(Q\)-energy. O6 assignment fingerprints: no assignment columns. O7 tensor amplification: unused; any later powering lacks mixed-word soundness. O8 exact transfer: unavailable because this is direct integer CVP, so a binary realization remains mandatory.

**Experiment/falsification.** At \(q=3\), optimize \(Q\) by SDP over all signed exact-fiber vectors, rationalize it, then compare the fixed \(p(L)\) rule on held-out YES/NO, all-eight, and holonomy cases. Reject on any low-energy NO repair or superpolynomial bit complexity.

**Likely death.** Spectral relaxations probably have constant-size integrality-gap witnesses.

3. **Bose–Chowla protected witness addresses.** Give every triple an order-\(h\) \(B_h\) label \(\alpha_j\) in a growing extension field, with \(h\ge q+2\), so distinct supports of size at most \(h\) have distinct sums. Couple \(y=\sum_j\alpha_jx_j\) to an instance-derived address code whose matching fingerprints have sparse leaders but other short odd-cover fingerprints are far; this protects witnesses separately rather than quotienting all legal differences.

**Obstruction check.** O1 bounded signatures: labels are global and \(h\) grows, although any bounded-degree address decoder falls back inside O1. O2 marginals: direct field equations avoid wire tables; a circuit implementation would not. O3 scopes: fingerprints see the whole support. O4 phases: unused. O5 integer fibers: binary extension-field linear algebra, not affine integer slack. O6 complete-assignment fingerprints: columns are triples and label length \(O(h\log m)\), not complete assignments; the protected-address set may nevertheless become exponential. O7 tensor: not used, so no mixed-word issue yet. O8 exact transfer: expand field equations in a binary basis.

**Experiment/falsification.** For \(q=3,m=8,h=5\), exhaustively search small binary address codes using only incidence-derived invariants; test every cover and all-eight/holonomy words, recording leader cost and rank. Reject unless one frozen rule generalizes to permuted held-out instances.

**Likely death.** Making all unknown matching addresses cheap either costs exponential sectors or also makes illegal affine combinations cheap.

4. **Higher cohomology rather than linear homology.** Build the exchange complex of the 3DM instance, but lift a selected chain by global cup-\(i\) or length-\(r\) Massey-product coordinates, not merely its homology class. Legal matchings should admit sparse isotropic lifts, while odd holonomy or an odd affine combination can be homologically trivial yet carry a nonzero higher operation; use \(r=\Theta(\log n)\) and an outer linear code to spread that operation.

**Obstruction check.** O1 bounded signatures: fixed-order cup products are covered; only growing, genuinely global operations escape. O2 marginals: no local interfaces unless the operation is circuit-linearized. O3 local hierarchies: operations use full cycles and intersections. O4 phase lifts: these are multichain operations, not single-valued local phases. O5 integer fibers: binary. O6 assignment fingerprints: chains, not complete assignments. O7 tensor amplification: the span of all lifted chains contains arbitrary mixed words, with no current soundness theorem. O8 exact transfer: applies once an explicit binary lift exists.

**Experiment/falsification.** Construct the complete \(q=2\) all-eight complex and the smallest twisted/Petersen examples; compute cup and triple-Massey coordinates and enumerate the full lifted span. Reject if the known illegal words cancel, or worst YES support grows comparably.

**Likely death.** Polynomial linearization either restores finite-difference trades or requires exponentially many cochains.

5. **Adversarially certified matroid fold.** Given the actual pointed tensor generator \(G\), enumerate its small flats and cocircuits, then solve a deterministic covering LP for dense parity rows: each dangerous low-support mixed word must be hit many times, while every rank-one pointed word must be hit few times. Round row weights to repetitions, producing a code-dependent binary fold selected from the matroid rather than frozen hashes, column types, or a test-suite-trained modulus.

**Obstruction check.** O1 bounded signatures, O2 marginals, O3 scopes, O4 phases, and O5 integer fibers do not apply: this acts globally on an already formed code. O6 assignment fingerprints: it uses generator-matroid data, not assignment groups. O7 tensor amplification: this lies exactly in the unexcluded code-dependent dense-fold opening, but must prove constraints for every mixed word. O8 exact transfer: the folded output is binary.

**Experiment/falsification.** On one reduced \(8\times8\) tensor instance at a time, enumerate all mixed words, solve the exact row-selection ILP without semantic YES/NO labels, freeze its invariant tie-breaking, and test relabelings plus held-out YES/NO, affine-closure, all-eight, and holonomy instances. Reject on a kernel, ratio \(\le25/9\), or rank at least 65.

**Likely death.** The LP separation oracle is nearest-codeword hard; small-flat surrogates will overfit just as sampled folds did.

6. **Partial-assignment consistency algebra.** Work in
\[
A_n=\mathbb F_2[e_i^0,e_i^1]/((e_i^b)^2=e_i^b,\ e_i^0e_i^1=0),
\]
so products encode consistent partial assignments and conflicting choices vanish. The product over clauses of their satisfying-literal sums is nonzero exactly when a consistent clause-choice exists; seek a formula-dependent polynomial-dimensional quotient module in which a nonzero product has a sparse factor-path, while zero products admit no short superposed representation.

**Obstruction check.** O1 bounded signatures: the product has formula-growing degree; bounded truncations remain covered. O2 tableau encodings: a gate-by-gate multiplication circuit is covered, so the proposal requires one-shot quotient multiplication. O3 scopes: the algebra is global. O4 phases and O5 integer fibers: unused. O6 complete-assignment fingerprints: the full algebra has an exponential partial-assignment basis, so only a genuinely sparse quotient escapes. O7 tensor: no tensor powering; all linear combinations in the quotient still require soundness. O8 exact transfer: multiplication matrices and the quotient must be explicitly binary.

**Experiment/falsification.** For three variables, build the full \(27\)-dimensional algebra, test all-eight and twisted-holonomy formulas, then search invariant quotients of dimensions \(8\)–\(16\) and enumerate every sparse factor-path and mixed sum. Reject on any false short target representation.

**Likely death.** A polynomial faithful quotient would compress the SAT consistency algebra so strongly that constructing it likely hides the original NP-hard decision.
