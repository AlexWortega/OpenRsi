1. **Number-field valuation shell**

**Mechanism.** Replace scalar CRT slacks by ideals in a degree-\(d\) number field. Encode each global exact-cover defect into prime-ideal valuations, then expose residue symbols through trace maps and BCH inner blocks; the product formula is intended to turn any nonzero global defect into many binary coordinates while a matching occupies one sparse principal-ideal representative.

**Expected move.** Obtain multiplicative soundness without tensor rank growth.

**Obstruction check.** O1 **bounded signatures**, O2 **marginal/tableau**, O3 **local hierarchies**, and O4 **phase lifts** do not apply if valuations are computed by global ideal arithmetic, not local interfaces. O5 **integer exact fibers** is the main threat: ordinary CRT residues or polynomial slacks fall exactly inside it. O6 **assignment fingerprints** is avoided because columns are triples and ideal generators, not assignments. O7 **tensor amplification** is irrelevant; all signed/mixed representations must be charged directly. O8 **exact transfer** applies after trace blocks produce binary \(H,t\), with their full rank counted.

**Falsification/experiment.** For \(q=2,3\), use \(\mathbb Q(\zeta_7)\), two split primes, and enumerate coefficients in \([-2,2]\) on all-eight, holonomy, and tiny YES/NO 3DM.

**Likely death.** A one-prime repair has small trace weight, reproducing O5, or honest principal representatives have comparable baseline.

---

2. **Deterministic isolation bank with BCH-protected sectors**

**Mechanism.** Build a polynomial family of restrictions/weightings intended to isolate at least one satisfying matching. Give each branch a BCH label whose sums of at most \(K=N^c\) distinct branch labels cannot masquerade as another branch; only the isolated branch should need a short exact-cover representative.

**Expected move.** Break the three-legal-witness affine-closure attack without discovering which witness or branch succeeds.

**Obstruction check.** O1 **bounded signatures**, O2 **marginals**, O3 **scope hierarchies**, and O4 **phases** are bypassed only if branch selection is one global BCH syndrome—not a one-hot selector tableau. O5 **integer fibers** is irrelevant in the binary version. O6 **complete fingerprints** does not apply to a polynomial branch bank, although an exponential bank would fall back into it. O7 **tensoring** is unused; every mixed branch sum must satisfy the BCH bound. O8 **transfer** is immediate if bank size, BCH length, and rank remain polynomial.

**Falsification/experiment.** Enumerate all affine hash restrictions for the \(q=2\) all-eight and \(q=3\) affine-closure families; construct one combined syndrome matrix and exhaust every mixed word.

**Likely death.** A polynomial deterministic isolation family for arbitrary witness sets is essentially the missing isolation derandomization; selector encoding may also reintroduce rectangle trades.

---

3. **Pfaffian forced-edge canonical aggregate**

**Mechanism.** First map a planar exact-one SAT family to a signed perfect-matching instance. Compute, without finding a matching, Pfaffians of the graph and every forced-edge minor; use the first nonzero \(2\)-adic layer of this derivative vector as a canonical center, then surround it by a BCH coset shell.

**Expected move.** Give each satisfiable instance one computable protected center rather than making every witness cheap, defeating affine closure.

**Obstruction check.** O1 **local signatures**, O2 **tableaus**, O3 **local scopes**, and O4 **phases** do not cover a globally computed Pfaffian aggregate. O5 **integer repairs** applies if the aggregate is compiled through local determinant gates; direct Pfaffian arithmetic is required. O6 **assignment fingerprints** is avoided because only polynomially many graph minors are retained. O7 **tensoring** is absent; aggregate cancellation must be analyzed for all matching superpositions. O8 **transfer** applies after a fixed binary expansion, with characteristic-two and rank accounting explicit.

**Falsification/experiment.** Enumerate planar graphs with at most eight vertices, compare forced-edge Pfaffian vectors against every perfect matching and illegal odd cover, then test the all-eight gadget after planarization.

**Likely death.** Pfaffian sums cancel, vanish for even witness counts, or no parsimonious planar matchgate encoding of 3SAT exists.

---

4. **Syndrome-aware multiscale rank condenser**

**Mechanism.** For a reduced tensor matrix \(W\), derive canonical flags from the actual parity-check pair \((H,t)\). Apply two-sided condensers only to successive syndrome-visible quotients, using geometrically increasing block multiplicities: a planted pure square should activate one quotient per scale, while every NO mixed matrix should activate many independent scales.

**Expected move.** Compress \(n^2\) tensor coordinates to \(n^{1+\varepsilon}\) while preserving a powered gap against arbitrary mixed words.

**Obstruction check.** O1 **signatures**, O2 **marginals**, O3 **hierarchies**, O4 **phases**, O5 **integer fibers**, and O6 **assignment fingerprints** are inapplicable: this operates directly on the instance code. O7 **tensor amplification** is directly relevant but does not rule out code-dependent dense structured folds; the required theorem must quantify over every mixed \(W\), not merely rank-one squares. O8 **transfer** applies to the resulting binary image, so actual image rank—not nominal block count—must be used.

**Falsification/experiment.** On the existing \(8\times8\) reduced squares, compute contraction flags from row-reduced \(H\), freeze \(2\times m\), \(4\times m\), and kernel-quotient maps, and enumerate all mixed words plus all-eight and holonomy.

**Likely death.** Syndrome visibility measures nonzeroness/rank rather than Hamming support, repeating the \(F_8\) condenser’s completeness inflation.

---

5. **Nonabelian two-holonomy projector**

**Mechanism.** Place \(S_3\) or \(A_5\) labels on an explicit two-dimensional expander complex built from the formula. Assignments are global gauge sections; inconsistency produces face curvature. Instead of local phase labels, apply a formula-dependent projector in the full noncommutative group algebra and binary-expand selected irreducible matrix coefficients.

**Expected move.** Make odd permutation holonomy and affine splices create extensive noncommuting curvature.

**Obstruction check.** O1 **bounded signatures** and O2 **tableaus** are avoided only if the projector is applied globally; local multiplication gadgets would be covered. O3 **local hierarchies** misses a genuine global cosystolic theorem, but connected-scope implementations are covered. O4 **phase lifts** assumes single-valued abelian-like copy-stable phases; a multivalued nonabelian projector is outside it. O5 **integer fibers** and O6 **assignment fingerprints** are unrelated. O7 **tensoring** is unused; all group-algebra mixed sums require soundness. O8 **transfer** applies only after an explicit polynomial-size binary linearization.

**Falsification/experiment.** Build the twisted 3-cycle and all-eight complexes, use the six-dimensional regular representation of \(S_3\), and enumerate every odd sum of lifted sections.

**Likely death.** Binary linearization restores affine closure, while implementing group products through local gates falls back under O1/O2.

---

6. **Expander-sparse moment/SOS dictionary**

**Mechanism.** Use only monomials indexed by walks in a constant-degree expander on variables, up to degree \(D=\Theta(\log n)\). Construct a truncated Boolean quotient/moment matrix globally; a satisfying assignment supplies a rank-one sparse evaluation vector, while UNSAT should force every syndrome representative to spread across many walk moments.

**Expected move.** Approximate logarithmic-level SOS amplification with only \(n\Delta^D=\operatorname{poly}(n)\) coordinates.

**Obstruction check.** O1 **bounded signatures** may apply if the selected moments contain an independently flippable \((D+1)\)-cube; this must be checked, not assumed away. O2 **marginals** is avoided only if rows are global moments rather than restriction tables. O3 **local hierarchies** does not fully exclude growing logarithmic scopes at fixed arity, but odd holonomy is an explicit threat. O4 **phases** and O5 **integer fibers** are irrelevant. O6 **fingerprints** is avoided because no assignment columns are listed. O7 **tensoring** is replaced by sparse moments, but arbitrary mixed pseudo-moments need a theorem. O8 **transfer** requires an actual binary linear matrix and polynomial rank.

**Falsification/experiment.** Degree \(2,3,4\) walk bases on all-eight, Petersen-flow, holonomy, and tiny 3DM; solve exact minimum support over the lifted span.

**Likely death.** A sparse pseudoexpectation survives, or the necessary moment closure becomes \(n^{\Theta(\log n)}\).

---

7. **Toric normal-form shield for exact cover**

**Mechanism.** Regard triple selections as monomials in the exact-cover toric semigroup. Compute a truncated Gröbner normal-form signature under a canonical term order, then BCH-encode the remainder: legal matchings may have distinct monomials, but an illegal signed cover should require a long sequence of high-degree Markov moves before sharing any protected normal form.

**Expected move.** Replace the failed linear quotient by nonlinear canonicalization while retaining a polynomial sparse triple dictionary.

**Obstruction check.** O1 **bounded signatures**, O2 **marginals**, O3 **scope hierarchies**, and O4 **phases** do not cover a genuinely global normal form. O5 **integer fibers** returns if reduction uses bounded-degree move/slack tableaux. O6 **complete fingerprints** is avoided because normal forms belong to triple monomials, not all assignments. O7 **tensoring** is unused; every signed/mixed representation must have its remainder charged. O8 **transfer** applies only if the truncated remainder map is realized by a polynomial-size binary linear syndrome system.

**Falsification/experiment.** Compute exact toric ideals for the \(q=2\) all-eight and existing \(q=3\) affine-closure dictionaries; enumerate Gröbner bases, normal forms, Markov degrees, and shortest illegal representatives.

**Likely death.** Computing the relevant normal form is NP-hard or requires exponentially many Gröbner states; linearizing it recreates the affine quotient or tableau obstruction.
