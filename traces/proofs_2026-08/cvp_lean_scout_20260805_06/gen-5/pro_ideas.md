I use only the supplied campaign record and classical tools; the prohibited document was not consulted.

1. **Perfect-hash direct-sum transfer — amend Q1.**  
**Mechanism/move:** Replace the dimension-two single \(F_{289}\) symbol by \(r\) product-tag coordinates. A deterministic perfect-hash family isolates one support cell of every non-honest Graver move, making its corresponding coordinate nonzero; this amendment is justified by the proved three-symbol dependency obstruction.

**Audit:** G1/G6/G7 (slack/filter/radix): every hash is emitted, with no slack. G2–3/G5/G9/G11/G13/G15/G19/Goal-G1/toric exchange: injectivity is tested on the complete enlarged signed kernel, not named attacks; honest-affine collisions remain fatal if unchanged after pair lifting. G12/Goal-G8: include zero/DROP fibers. G14/G28/G31/G32/G37/G38: only Q1 is claimed; no finite pass implies growth. G30: use formula-dependent calibrated tags. G33–34 and Goal-G3–7: no exterior, \(D_4\), or \(E_6\). Goal-G2: no group algebra. Goal-G11/G12/affine-COPY: start from the redundant survivor but add genuinely pair-dependent coordinates. Carry/lumpability is downstream and unresolved.

**Experiment/falsifier:** On the 18-variable skeleton, synthesize the minimum \(r\le4\), serialize all factors, and enumerate every fiber below \(17E\). Lean target: injective transfer on the seam quotient implies Q1(3). Likely death: equal-completeness calibration forces a kernel intersecting the harmful quotient.

---

2. **Chordal kernel surgery — prove Q1 with one symbol.**  
**Mechanism/move:** Add pair-dependent separator rows forming a junction-tree/network matrix, chosen to vanish on every honest NAND/COPY fiber. The goal is to make the surviving seam lattice saturated of rank at most two modulo \(17\), where one \(F_{289}\) transfer can be injective.

**Audit:** G1/G6/G7: all separator equations are emitted. G2–3/G5/G9/G11/G13/G15/G19/Goal-G1/toric exchange: not automatically escaped; exact quotient/SNF must show those signed directions were removed. G12/Goal-G8: DROP is an explicit fiber. G14/G28/G31/G32/G37/G38: this is a constant-tile lemma only; Q3 remains required. G30: no tensor seed. G33–34 and Goal-G3–7: no closed geometric family. Goal-G2: no convolution algebra. Goal-G11/G12/affine-COPY: redundant NAND is retained, but COPY receives new pair rows. Carry/lumpability is irrelevant until Q2.

**Experiment/falsifier:** MILP-select \(0,\pm1\) rows on the current 18 variables, constrained to agree on all 16 legal fibers; require saturated SNF and seam rank \(\le2\). Then recompute the complete Graver basis and exact \(17E\) shell. Lean target: a saturated rank-two kernel plus injective residue map excludes zero-transfer moves. Likely death: G13’s honest-affine-span witness annihilates every row preserving completeness, or the rows destroy COPY saturation.

---

3. **Higher \(P\)-adic jets — amend “nonzero initial symbol.”**  
**Mechanism/move:** Emit one product tag modulo \(P^k\), but classify a defect by its first nonzero graded digit rather than demanding grade zero be nonzero. The existing \(F_{17}^2\) dependency then only pushes a movement into a higher grade; it need not annihilate the full truncated tag.

**Audit:** G1/G6/G7: truncated digits are emitted lattice coordinates. G2–3/G5/G9/G11/G13/G15/G19/Goal-G1/toric exchange: every signed seam move must be tested modulo \(P^k\), not merely modulo \(P\). G12/Goal-G8: include DROP through every grade. G14/G28/G31/G32/G37/G38: no amplification follows from finite jet separation. G30: no seed tensor. G33–34 and Goal-G3–7: unused. Goal-G2: the maximal order is a division algebra, not an \(A_5\) group ring. Goal-G11/G12/affine-COPY: higher digits specifically target grade-zero pseudosections and the affine splice. Carry/lumpability is **not escaped**: promotion requires lift-independent sections at every digit.

**Experiment/falsifier:** Using the certified maximal order, enumerate pair labels in \(\mathcal O/P^3\), test the known weight-8 and \((2,-1)\) movements, then recompute the full truncated kernel. Lean target: equality modulo \(P^k\) plus a stabilized section yields a well-defined first-nonzero-grade transition. Likely death: a movement vanishes exactly modulo \(P^k\), or successors depend on unrecorded carries.

---

4. **Nonabelian holonomy tile.**  
**Mechanism/move:** Replace additive transfer summation by an ordered finite-state connection: pair selectors choose unit-valued edge labels, and auxiliary multiplication selectors certify the accumulated quaternionic holonomy. Honest COPY paths have identity holonomy; every non-honest primitive cycle should have nonidentity holonomy.

**Audit:** G1/G6/G7: multiplication states and constraints are emitted. G2–3/G5/G9/G11/G13/G15/Goal-G1/toric exchange: ordered holonomy lies outside affine-checksum assumptions, but the full signed kernel still needs auditing. G19 signed splicing is **not escaped** and is the first test. G12/Goal-G8: DROP states are explicit. G14/G28/G31/G32/G37/G38: no finite holonomy pass proves growth. G30: no literal tensor. G33–34 and Goal-G3–7: unused. Goal-G2’s bicyclic group-ring zero divisor is outside the division-ring unit model, although analogous virtual-flow attacks may survive. Goal-G11/G12/affine-COPY: multiplication is pair-dependent and non-affine. Carry/lumpability remains for \(P^2\) state reduction.

**Experiment/falsifier:** Build the smallest two-step state-expanded seam over units of \(\mathcal O/P^2\); enumerate coefficients in \([-2,2]\), starting with the G19 two-negative and diagonal witnesses. Lean target: multiplication-table constraints plus one-hot low-energy bounds imply certified path holonomy. Likely death: signed selectors form a virtual flow with identity holonomy, reproducing G19 in expanded state space.

---

5. **Geometry-of-numbers no-go for single-coordinate Q1.**  
**Mechanism/move:** Strengthen the existing Lean dependency lemma using Minkowski’s first theorem: a rank-\(r\ge3\) seam lattice mapped to \(F_{17}^2\) has an index-\(\le289\) transfer kernel containing a quantitatively short vector. Combine this with the exact tile quadratic form to prove that some malformed zero-transfer lift costs below \(17E\).

**Audit:** G1/G6/G7 and G12/Goal-G8 are included through the actual emitted matrix and target. G2–3/G5/G9/G11/G13/G15/G19/Goal-G1/toric exchange are not escaped; they become possible witnesses covered uniformly by the lattice theorem. G14/G28/G31/G32/G37/G38 and G30 are irrelevant because the refutation occurs before recursion. G33–34 and Goal-G3–7 are outside the theorem’s linear seam architecture. Goal-G2 is irrelevant. Goal-G11/G12/affine-COPY motivate, but do not imply, its hypotheses. Carry/lumpability is irrelevant if Q1 already fails.

**Experiment/falsifier:** Compute the Gram determinant, successive minima, and exact shortest zero-transfer vector for the 40-by-18 factors; infer the sharp constant needed in the theorem. Lean target: under explicit rank, covolume, malformedness, and operator-norm hypotheses, produce \(x\neq0\) with \(T(x)=0\) and \(Q(x)<17E\). Likely death: extra rows reduce rank below three or make the determinant bound far too weak.

---

6. **Quaternionic Delaunay coercion — make transfer unnecessary.**  
**Mechanism/move:** Search for an \(\mathcal O\)-Hermitian Delaunay cell whose legal NAND/COPY fibers lie on one sphere while every other lattice point in every port fiber is already beyond \(17E\). Then Q1(2) holds by geometric energy alone and Q1(3) is vacuous.

**Audit:** G1/G6/G7: the lattice and target are fully emitted. G2–3/G5/G9/G11/G13/G15/G19/Goal-G1/toric exchange: exact all-lattice shell enumeration includes these, rather than attempting affine detection. G12/Goal-G8: zero and all DROP fibers are included. G14/G28/G31/G32/G37/G38: this proves only the local tile; Q3 still needs strict growth. G30: forbid seed isometries explicitly. G33–34 and Goal-G3–5 (\(D_4\)) and Goal-G6–7 (\(E_6\)): outside their frozen exterior/grid/Gosset families; use a new \(\mathcal O\)-Hermitian Construction-A family. Goal-G2: no group ring. Goal-G11/G12/affine-COPY: no grade-zero detection is needed. Carry/lumpability disappears locally because no transfer is used.

**Experiment/falsifier:** Search rank-two and rank-three \(\mathcal O\)-modules with small rational Hermitian Grams, then certify the complete \(17E\) shell by exact Fincke–Pohst enumeration. Lean target: verified enumeration implies all nonlegal fibers exceed \(17E\). Likely death: a midpoint or coordinate-recombination intruder generalizes the \(D_4\) obstructions, or the required radius ratio is impossible.

---

7. **Nullstellensatz certificate for the bounded Q1 architecture.**  
**Mechanism/move:** Treat the \(N=8\), one-transfer, bounded-row Q1 architecture as an exact polynomial feasibility problem: variables are pair rows, product labels, calibration, Gram, and legal centers. Either extract a rational tile or produce a Gröbner/Nullstellensatz certificate that completeness plus saturation forces a zero-transfer malformed movement.

**Audit:** G1/G6/G7, G12/Goal-G8, and carry constraints are explicit polynomial equations/inequalities, not external filters. G2–3/G5/G9/G11/G13/G15/G19/Goal-G1/toric exchange are universally quantified through kernel-minor and witness ideals. G14/G28/G31/G32/G37/G38 and G30 are outside this local bounded-architecture claim. G33–34 and Goal-G3–7 are unused. Goal-G2 is unused. Goal-G11/G12/affine-COPY are included as mandatory witness ideals rather than assumed absent.

**Experiment/falsifier:** Freeze \(N=8\), at most four pair-dependent rows, coefficients in \(\{-2,\ldots,2\}\), and one \(F_{289}\) tag. Eliminate calibration variables first; ask Singular/Macaulay2 for a certificate that either the known three seam directions are blocked or a zero-tag lift exists. Lean target: check the resulting polynomial identity and the finite coefficient enumeration by reflection. Likely death: inequalities and saturation cause prohibitive case explosion; any certificate only closes the declared row/size bound, requiring an explicit roadmap amendment rather than refuting Q1 generally.
