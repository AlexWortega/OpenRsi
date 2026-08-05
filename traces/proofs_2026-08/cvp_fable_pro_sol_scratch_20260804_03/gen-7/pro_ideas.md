I treat Generation 6 as killed by `GATE.json`, despite the older “bounded survivor” wording.

**Audit key:** **S** = slack annihilation; **LI** = constant-size local isolation without scaling; **O** = freed-marginal/private-row overlap circuits; **M** = normalization/consistency imposed only by an external filter; **P** = nine-clause four-variable mod-2 parity bypass; **T** = changing-reference rather than one fixed target; **X** = exponentially many assignment relations; **B** = bounded evidence/no polynomial gap/constant repetition; **H** = SNF alone not proving lattice equality.

### 1. Disjunct-measurement Tanner lattice
**Core trick.** Put normalization, occurrence consistency, and clause legality residuals into the actual lattice coordinates. Apply an explicit \(t\)-disjunct integer measurement matrix (Kautz–Singleton, 1964) so every sufficiently sparse signed residual has an isolating row, then encode the measured syndrome with an asymptotically good expander code.

**Expected move.** Prove: vectors below radius \(R=n^c\) have \(t\)-sparse residuals, hence either are honest or incur \(\Omega(N)\) coded weight.

**Obstruction audit.** **S:** no free slack. **LI/O:** measurements mix all clauses and marginals globally. **M:** every check is a basis row. **P:** integer isolation, not binary incidence, though odd-prime bypasses remain untested. **T:** one fixed target. **X:** disjunct matrices are polynomial-size for \(t=n^{O(c)}\). **B:** potentially asymptotic via code distance, but the sparse-residual lemma is unproved. **H:** certify the emitted basis directly by HNF/determinant, not quotient SNF.

**Falsification/test.** On the supplied nine-clause instance, use \(t=4\), solve unrestricted bounded CVP, and search for zero measured syndrome.

**Likely death.** A short signed selector lies in the exact residual kernel, so no measurement sees it.

---

### 2. Number-field norm amplifier without slack
**Core trick.** Combine all actual affine residuals as an algebraic integer \(s=\sum r_i\alpha_i\), where the \(\alpha_i\) form an integral basis of a degree-\(d\) number field. If \(s\neq0\), its Minkowski embeddings satisfy \(\prod_\sigma|\sigma(s)|\ge1\), hence AM–GM gives Euclidean squared norm at least \(d\).

**Expected move.** With \(d=N^\delta\), turn any nonzero global consistency defect into an \(N^{\delta/2}\) distance contribution without repetition.

**Obstruction audit.** **S:** outside the killed algebraic-slack variant because there is no residual-cancelling slack. **LI/O:** one global algebraic syndrome includes every overlap. **M:** embeddings are lattice coordinates, not search filters. **P:** characteristic zero, so the specific XOR bypass does not apply. **T:** fixed target. **X:** only \(O(N)\) basis elements. **B:** degree supplies scaling, conditional on proving \(s\neq0\). **H:** use an explicit integral basis and exact embeddings; no relation-lattice SNF claim.

**Falsification/test.** For the nine-clause instance, construct a degree-\(d\) field in Sage, enumerate unrestricted short coefficients, and test whether all residuals can vanish exactly.

**Likely death.** Signed selectors produce \(s=0\); alternatively, rational approximation of Minkowski embeddings destroys the promised gap.

---

### 3. Toric normal-form penalty
**Core trick.** Represent local assignment patterns as monomials in a Segre/Boolean toric model. Use a Lawrence lifting and a Gröbner weight order (cf. Sturmfels, 1996) so honest assignment moves reduce to designated standard monomials, while inconsistent signed combinations leave a large weighted normal-form remainder.

**Expected move.** Tensor to constant degree \(r\): a nonstandard remainder should occupy \(N^{\Omega(r)}\) monomial coordinates while the output dimension remains polynomial for fixed \(r\).

**Obstruction audit.** **S:** no slack variables. **LI:** replaces isolated local fibers by a global toric normal form. **O:** shared variables are literally shared monomial exponents, not freed marginals. **M:** binomial relations and penalties are emitted lattice columns. **P:** integral Gröbner reduction, not mod 2. **T:** one target standard monomial. **X:** degree-\(r\) monomials number \(N^{O(r)}\), not complete assignments. **B:** not cleared—the required remainder lower bound is conjectural. **H:** Gröbner reduction plus mutual-containment certificates can prove the exact relation lattice.

**Falsification/test.** On four variables at degrees \(2\) and \(3\), compute the toric ideal, emit the Lawrence lattice, and solve unrestricted bounded CVP for the nine-clause target.

**Likely death.** Small overlap circuits are toric binomials and reduce illegal selectors to zero or a constant-size remainder.

---

### 4. Systolic filling complex
**Core trick.** Build an integral chain complex in which a fixed target cycle has a short filling for every satisfying assignment. Glue clause gadgets through a cosystolic-expander thickening (in the spirit of Evra–Kaufman, 2016), aiming to make every non-honest integral filling either locally expensive or represent a homology class with polynomial systole.

**Expected move.** Identify CVP with nearest integral boundary and obtain a filling-norm gap \(N^c\).

**Obstruction audit.** **S:** no residual slack; variables are chain coefficients. **LI/O:** the complex is globally glued, so private-clause cycles should become nontrivial globally. **M:** the boundary matrix is the actual lattice basis. **P:** use a torsion-free integral complex; the mod-2 argument then is outside its assumptions, but odd/integral cycles must be tested. **T:** one fixed target cycle. **X:** local cells plus polynomial thickening. **B:** an explicit polynomial systole would clear scaling; none is established. **H:** verify chain maps and boundary-lattice equality by explicit HNF and mutual containment.

**Falsification/test.** Attach the nine-clause gadget to the smallest candidate expander, then compute its exact shortest target filling by branch-and-bound.

**Likely death.** A constant-support contractible chain fills the target, or gadget gluing introduces torsion enabling a cheap signed filling.

---

### 5. Multi-order radix barriers
**Core trick.** For residual vector \(r\), add coordinates \(\sum_i r_i B^{\pi(i)}\) for a polynomial family of permutations \(\pi\). Choose \(B\) above the entire candidate short-vector coefficient range; a permutation placing any surviving residual above all opposing residuals prevents carry cancellation. Exponentially large entries still have polynomial bit length.

**Expected move.** Conditional on “every short illegal selector has a nonzero residual,” obtain a superpolynomial numerical distance and therefore an \(n^c\) promise gap.

**Obstruction audit.** **S:** no slack; all selector and consistency residuals are radix-encoded. **LI/O:** each coordinate globally orders every clause and marginal. **M:** radix coordinates occur in the emitted lattice. **P:** ordered integer magnitudes, not parity. **T:** one target. **X:** \(O(N)\) cyclic permutations already place every check first; no assignments are listed. **B:** conditionally cleared by scale rather than repetition. **H:** the construction is an explicit matrix identity, not an SNF inference.

**Falsification/test.** Use the all-eight-clause and nine-clause instances, \(B=33\), all cyclic orders, and exact unrestricted CVP below the Boolean completeness radius.

**Likely death.** An exact signed-selector kernel makes every residual zero; radix weighting cannot amplify zero.

---

### 6. Multi-prime Fourier uncertainty
**Core trick.** Regard each clause selector as an integer-valued function on \(\{0,1\}^3\). Record higher-order Fourier characters drawn from explicit small-bias families over several odd primes; finite uncertainty principles (Donoho–Stark, 1989) suggest that a sparse signed pseudoassignment cannot be simultaneously sparse and spectrally invisible.

**Expected move.** Show every short non-honest global selector has nonzero syndrome on many characters, then feed those values to an algebraic code of polynomial relative distance.

**Obstruction audit.** **S:** no slack. **LI/O:** characters include cross-clause occurrence products, not private marginals. **M:** character and carry coordinates are in the lattice. **P:** the exact \(F_2\) odd-component bypass is avoided by \(q=3,5\), but analogous zero spectra are not excluded. **T:** all characters compare with one fixed target. **X:** explicit small-bias families are polynomial-size. **B:** the needed uncertainty bound under consistency constraints is unproved; outer-code distance alone is insufficient. **H:** compare explicit character lattices by HNF/mutual containment.

**Falsification/test.** On the nine-clause instance, emit all degree-\(\le2\) characters modulo \(3\) and \(5\), include carries, and solve the unrestricted coset minimum exactly.

**Likely death.** A signed pseudoassignment supported on an affine subspace annihilates every selected character over every tested prime.

---

### 7. Bounded-degree integer moment lattice
**Core trick.** Introduce moment coordinates \(y_S\) for \(|S|\le d\). Boolean identities and clause equations become linear after multilinearization; Möbius blocks penalize integral moment vectors that do not arise from point masses, while a code amplifies any remaining moment residual. This is an integral analogue of bounded-level Sherali–Adams (Sherali–Adams, 1990), not an LP relaxation.

**Expected move.** For constant \(d\), prove every short integral feasible moment vector is a convex-sign combination containing an actual assignment, or has polynomially many nonzero Möbius coefficients.

**Obstruction audit.** **S:** clauses use moment identities, not slack. **LI/O:** moments spanning shared variable sets couple overlaps globally. **M:** normalization \(y_\varnothing=1\), Boolean identities, and consistency are lattice coordinates. **P:** characteristic-zero Möbius inversion avoids the stated parity argument. **T:** fixed target \(y_\varnothing=1\). **X:** \(O(n^d)\) coordinates for constant \(d\). **B:** not cleared; constant-degree integrality gaps are the central risk. **H:** monomial coordinates give a direct explicit matrix, checked by HNF.

**Falsification/test.** Build levels \(d=2,3\) for the nine-clause instance and enumerate unrestricted integral moment vectors up to the completeness radius.

**Likely death.** A low-degree signed pseudo-measure satisfies every lifted clause while retaining constant norm.
