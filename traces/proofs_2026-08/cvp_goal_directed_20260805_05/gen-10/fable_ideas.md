I treat G14/G31/G38 as finite passes only, and G13/G15/G19/G32/G37 as mandatory adversarial witnesses. First, a compact audit key used in every sketch:

- **A:** G1 RS slack, G6 external quotient, G12 clause drop, augmented-Gram DROP.  
- **B:** G2 affine/Graver isolation, G3 unbounded fibers, G14 pair-bag pass, G31 Walsh pass.  
- **C:** G5 private-row overlap. **D:** G7 radix kernel.  
- **E:** G9/G11 parity, G13 affine collision, G15 affine hierarchy lift.  
- **F:** G19 signed flow, GD1 diagonal closure.  
- **G:** G28 min-plus failure, G32 additive parity, G37 parity cut, G38 finite splitter pass.  
- **H:** G30 tensor isometry. **I:** G33/G34 exterior-tag failures.  
- **J:** all three \(D_4\) shell obstructions. **K:** both \(E_6\) port obstructions.  
- **L:** GD2 bicyclic group-ring units. **P:** satisfiable-padding dilution.

### 1. Prove a padding no-go for the FRONTIER as written

**Mechanism.** Let \(U\) be unsatisfiable and \(S\) a satisfiable sheaf whose exact minimum equals its honest radius. For any component-preserving lift and \(X_k=U\sqcup S^{\sqcup k}\),
\[
\rho(X_k)=\frac{d_U+kR_S^2}{R_U^2+kR_S^2}\to1,\qquad
\rho(\mathcal LX_k)=\frac{d_{\mathcal LU}+k\mu R_S^2}{\mu R_U^2+k\mu R_S^2}\to1.
\]
Thus \(\rho(\mathcal LX_k)\ge(257/256)\rho(X_k)\) eventually fails.

**Expected move.** Refute the current lemma under the natural locality assumption; amend it to amplify \(\rho-1\), restrict to a connected robust class, or define global cross-component coupling.

**Audit.** A–F are irrelevant: the counterexample uses exact honest padding, no slack, kernel, affine, or cycle attack. G strengthens its additive-composition warning. H–L use no tensor, tags, shells, ports, or convolution. P is the mechanism itself.

**Falsification.** Exhibit a constant-degree lift that couples arbitrary disconnected components while preserving the rank and canonical-radius clauses.

**Experiment.** Use exact G28 control \(R_S^2=32\), obstruction \(d_U=57\), and symbolically solve the first violating \(k\) for any frozen componentwise lift.

**Likely death.** ROADMAP may silently intend connected inputs or nonlocal coupling.

---

### 2. Full commutant SDP instead of another hand-chosen metric

**Mechanism.** For a frozen replacement graph, compute the entire rational commutant of its incidence automorphism action and optimize an arbitrary invariant Gram form, not the two-parameter orthogonal family killed by G37. Homogenize with a final coordinate \(1\); an exact PSD inequality on the saturated adverse module would cover every real—and hence integer—coefficient at once.

**Expected move.** Either obtain a rational dual certificate giving \(257/256\) growth, or prove that completeness forces an adverse isotypic component to have eigenvalue at most the legal one.

**Audit.** A/D are included in the homogenized module, including zero and residual kernels. B avoids shell extrapolation via global PSD domination. C uses the full overlap commutant. E/F are inserted as explicit module vectors; shared isotypy causes rejection. G is outside G37’s restricted metric and G32’s orthogonal composition. H uses no Kronecker product. I–L use no exterior tags, shells, affine ports, or group rings. P requires connected/excess amendment first.

**Falsification.** A G13, G19, or DROP vector yields an exact dual cut \(\delta\le0\).

**Experiment.** Compute the commutant for one depth-two lift of the twelve G38 bags; solve the SDP, rationally reconstruct, and verify by exact LDL\(^{\top}\).

**Likely death.** Legal and affine-adverse vectors occupy the same irreducible representation.

---

### 3. Nonlinear label code with expander concatenation

**Mechanism.** Map each local legal label \(a\) to an equal-norm constant-length spherical codeword \(C(a)\), then enumerate legal edge-pairs so all code-coordinate marginals are emitted. Iteration concatenates the label code along an expander; unlike a compatible linear syndrome, the Gram energy of \(\sum\alpha_a C(a)\) need not equal honest energy when \(\sum\alpha_a=1\).

**Expected move.** Make G13/G15 affine pseudosections acquire multiplicative anchor excess even when every agreement residual is zero.

**Audit.** A emits normalization, pair legality, code marginals, and DROP coordinates. B seeks an all-coefficient frame inequality, not a finite-shell inference. C uses complete marginals. D’s exact kernel remains subject to code Gram energy. E is the principal target; affine combinations are tested directly. F includes signed pair-cycle states, without diagonal inference. G uses G38 only as seed and is neither min-plus nor additive moments. H is concatenation, not Kronecker tensoring. I uses an a priori simplex/code sphere, not repaired exterior tags. J/K/L use no Delaunay shell, affine port, or group algebra. P requires connected/excess form.

**Falsification.** Any diagonal affine or signed lift has energy growth no larger than \(\mu\).

**Experiment.** Enumerate equal-norm \(\{\pm1\}^d\) codes for the at-most-16 bag labels, \(d\le8\), and run exact depth-two DP.

**Likely death.** The affine combination of lifted honest codewords remains an additive-cost witness.

---

### 4. Naturality no-go for all affine-functorial agreement lifts

**Mechanism.** Formalize a lift whose new stalk maps and overlap rows are natural linear transformations of selector modules. Compute the universal rational natural-transformation space; if a normalized harmful pseudosection lies in the affine span of honest local sections, every such lift transports it with zero disagreement.

**Expected move.** Refute the entire “agreement-only, affine-functorial” interpretation of FRONTIER, forcing the roadmap to require label-nonlinear replacement or input-dependent global coupling.

**Audit.** A/D do not matter because one exact zero-residual affine witness suffices. B supplies the rational/unbounded method rather than a bounded search. C shows private overlap is within the no-go class. E provides the decisive G13/G15 witnesses. F is separately represented by the cycle part of the universal kernel. G32/G37 support additivity; G14/G31/G38 cannot establish escape. H and L are covered only when tensor/convolution maps are linear-natural; otherwise explicitly outside the theorem. I/J/K are outside because they use geometric label embeddings or ports, not selector-module naturality. P remains an independent no-go.

**Falsification.** Find a frozen lift row not expressible as a natural linear map and show it charges the affine witness.

**Experiment.** Build the incidence category of the G15 hierarchy and solve exactly for all natural maps of output rank at most four per stalk.

**Likely death.** A genuinely nonlinear finite-label replacement falls outside the proved class.

---

### 5. Integer sparse–dense dichotomy via lossless expansion

**Mechanism.** For a normalized integral stalk vector \(z\), the anchor excess is governed by \(\sum_i z_i(z_i-1)\), nonnegative and large when many entries are non-Boolean. Use a splitter/lossless-expander measurement so sparse malformed support is isolated and charged, while dense signed support already pays enough anchor excess; iterate this inequality for excess over honest radius.

**Expected move.** Prove
\[
E_{\mathcal LX}-R_{\mathcal LX}^2\ge(257/256)\mu\bigl(E_X-R_X^2\bigr),
\]
an explicitly padding-safe amendment suggested by G38 rather than the false raw-\(\rho\) recurrence.

**Audit.** A is handled by normalization branches and explicit drop measurements. B/G38 become a uniform support theorem, not shell extrapolation. C uses global complete overlaps. D exact kernels fall into sparse or dense support. E affine parity must pay replicated negative mass. F signed cycles are analyzed by support, not flow semantics. G28/G32/G37 are avoided because the recurrence is on excess, not total additive energy. H–L use no tensor, exterior metric, shells, ports, or group ring. P is exactly repaired.

**Falsification.** Find a balanced \(\{-1,0,1\}\) kernel vector whose support expands but whose anchor excess scales only by \(\mu\).

**Experiment.** Exhaust every connected degree-\(\le4\) replacement graph on at most eight vertices; certify sparse isolation and enumerate the dense boundary case.

**Likely death.** Dense affine parity may replicate with exactly legal-rate anchor growth.

---

### 6. Relative integral Hodge lift with explicit period coordinates

**Mechanism.** Repair the invalid “cycles are bounded by their boundary” idea by measuring three separate pieces: divergence, 2-cell curl, and every saturated harmonic period. Compute an integral cycle basis by SNF, realize dense period rows through sparse accumulator trees, and seek an exact norm equivalence for cut, boundary, and free \(H_1\) components.

**Expected move.** Prove the cycle-space portion of FRONTIER—including G19—while cleanly isolating the remaining zero-disagreement affine stalk module; a surviving affine module would refute agreement amplification unless another mechanism handles it.

**Audit.** A emits accumulator normalization and DROP coordinates. B is an SNF theorem over unrestricted integers. C uses the whole overlap complex. D kernels are classified into cut/curl/period pieces. E is honestly not solved: zero-disagreement G13/G15 is the explicit stop condition. F is the direct target; diagonal cycles receive period charge. G is structural rather than min-plus, additive moments, or a G38 shell claim. H uses no tensor. I–L use no exterior tags, Voronoi shells, affine ports, or convolution. P still requires connected/excess amendment.

**Falsification.** A primitive cycle has zero divergence, curl, and all emitted periods, or period accumulators violate constant-rank accounting.

**Experiment.** Compute the saturated Hodge decomposition of the twelve-bag G38 overlap graph and exhaust all primitive cycles of \(\ell_1\)-norm at most eight.

**Likely death.** The true cheapest witness lies in \(H^0\), not \(H_1\).

---

### 7. Ramified finite-ring label lift

**Mechanism.** Replace each label by a constant-size multiplication table over a ramified local ring, using nonlinear Teichmüller representatives; legal labels are equal-energy units, while inconsistent pair compositions expose a first nonzero associated-graded carry. Carries are finite enumerated selectors with all glue coordinates emitted—never free integer slack.

**Expected move.** Turn an affine collision that is invisible in ordinary marginals into either a nonzero graded defect or increased trace-form anchor energy, while retaining constant rank expansion.

**Audit.** A emits every carry, normalization, zero selector, and drop coordinate. B requires exact module injectivity plus an unrestricted energy bound. C uses complete ring-valued ports. D zero ordinary residual is harmless only if the graded defect is nonzero; otherwise the candidate fails. E tests Teichmüller images of G13/G15 explicitly rather than invoking a linear syndrome. F includes signed/diagonal classes in the graded kernel. G is valuation-based, not min-plus or additive parity; G38 is only the test sheaf. H uses no literal tensor. I–K use no exterior repair, Delaunay shell, or affine shell port. L is outside bicyclic units because the chosen algebra is a commutative local domain/quotient, but zero divisors must still be audited. P requires connected/excess amendment.

**Falsification.** The known affine coefficients give zero carry in every grade with legal-rate energy.

**Experiment.** Test \(\mathbb Z/9\mathbb Z\) and \(\mathbb Z[\sqrt2]/\mathfrak p^2\) label tables on one G38 depth-two graph by SNF and exact DP.

**Likely death.** Linearity in selector coefficients recreates the honest affine span despite nonlinear representatives.

Classical inspiration for Sketches 3 and 5: Sipser–Spielman, “Expander Codes,” *IEEE Transactions on Information Theory* 42 (1996), 1710–1722.
