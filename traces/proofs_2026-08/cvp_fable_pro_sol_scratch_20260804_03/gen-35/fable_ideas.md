No route is preferred; each is intended as an independently falsifiable restart.

### 1. Anisotropic Delaunay clause cells

**Mechanism.** Replace selector variables by direct integer variables \(x_i\), anchored so \(0,1\) are nearest, and one auxiliary integer \(u_C\) per clause. Search for a rational positive-definite quadratic \(q(s,u)\), \(s\) the literal sum, whose fibers \(s=1,2,3\) have equal radius \(R\), while \(s=0\) has minimum \(R+\Delta\) with \(\Delta/R\) polynomially large.

**Expected move.** A Boolean NO assignment pays \(\Delta\); non-Boolean \(x_i\) pay heavily through anchors, potentially giving \(d_{\rm NO}/d_{\rm YES}\ge n^c\).

**Obstruction audit.** G1 RS-slack/G7 radix: no residual slack. G2–3 affine isolation, G5 overlap, G9/G11 parity, G13 affine collision, G15 affine lift, G32 additive parity: no selector affine fibers. G6: every auxiliary is unrestricted and emitted. G12 DROP becomes an explicitly minimized \(u\)-fiber. G14/G31 are benchmarks only. G19: no flow. G28: no frozen recursion. G30: no tensor seed. G33–34: no exterior tags/shared \(6\times6\) metric.

**Experiment/falsification.** Enumerate \(C\in[-3,3]^{d\times2}\), half-integral targets, \(d\le5\), and certify all integer fibers by eigenvalue bounds. Kill if no \(\Delta>0\), or an off-range integer point enters the legal shell. Most likely death: convexity bounds \(\Delta/R\) by a constant.

---

### 2. Nonabelian orbit fingerprints on logarithmic bags

**Mechanism.** Make bags containing \(k=\lceil\log_2 n\rceil\) clauses, with one selector for each bag assignment. Tag each assignment by several integral orthogonal representations of a finite nonabelian group; use tensor depth \(O(\log n)\), still polynomial-dimensional, and search for tags placing all honest global lifts on one sphere.

**Expected move.** Noncommuting word information could make every inconsistent signed bag distribution acquire \(n^{\Omega(1)}\) fingerprint energy.

**Obstruction audit.** G1/G7: no slack or radix. G2–3/G5: full logarithmic bags replace fixed-marginal local isolation. G6: all bag and overlap equations enter CVP. G9/G11 parity, G13 affine collision, G15 lift, G32 additive parity are **not excluded**; failure to lift them is the primary test. G12 DROP is also live. G14 pair bags and G31 Walsh are strict depth-one special benchmarks, not proofs against nonlinear bag enlargement. G19: no unit-flow encoding. G28: no fixed min-plus tile. G30: no seed tensoring. G33–34: orthogonal group orbits, not Vandermonde bivectors; cosphericity is nevertheless mandatory.

**Experiment/falsification.** On the nine-clause instance, use \(k=3\), groups \(D_8,S_3\), tensor depths \(1,2\); solve exact sphere equations and enumerate through \(4/3\) of control. Most likely death: the G13 affine combination lifts through every bag and remains invisible.

---

### 3. Minkowski-norm amplification after a nonlinear graph lift

**Mechanism.** Lift each bounded clause neighborhood to complete assignment-table coordinates, then map every emitted consistency defect to an algebraic integer \(\alpha\) in a totally real degree-\(D\) field. The rational trace Gram satisfies  
\[
\|\alpha\|_{\text{Mink}}^2=\sum_\sigma \sigma(\alpha)^2\ge D
\]
for nonzero \(\alpha\), by the integral norm and AM–GM.

**Expected move.** If every low-cost NO vector has nonzero lifted syndrome, taking polynomial \(D\gg Bn^{2c}\) gives a polynomial distance ratio with polynomial dimension and bit complexity.

**Obstruction audit.** G1 slack and G7 radix are avoided: amplification has no carries or free annihilators. G2–3/G5 are replaced by enlarged neighborhood tables. G6: trace factors and all coordinates are emitted exactly. G9/G11/G13/G15/G32 remain dangerous exact-zero syndromes; the nonlinear lift, not the number field, must defeat them. G12 DROP must yield nonzero \(\alpha\). G14/G31 are finite antecedents only. G19 no flow; G28 no tile recurrence; G30 no tensor seed; G33–34 no exterior common metric.

**Experiment/falsification.** Use \(K=\mathbb Q(\sqrt2)\), then a totally real quartic field, on G7/G11/G13/DROP witnesses lifted to G14-style triples; compute exact trace Gram and syndrome kernels. Most likely death: an affine pseudodistribution lifts with \(\alpha=0\), making field degree irrelevant.

---

### 4. Integer cosystolic/period amplification

**Mechanism.** Interpret local assignment discrepancies as integer cochains on a bounded-degree 2-complex. Coboundary rows charge non-cocycles, while explicit integral period rows—computed from Smith normal form—charge nontrivial cocycles; honest assignments occupy the designated trivial relative class.

**Expected move.** An explicit family with growing integral cosystole would force any exact NO cheat to have polynomial support; heavily scale the coboundary and period coordinates to obtain \(n^c\) distance.

**Obstruction audit.** G1/G7: no slack/radix. G2–3/G5: global relative homology replaces local marginal isolation. G6: periods are emitted rows, not external filters; mod-2 and torsion are separately audited by SNF. G9/G11/G13/G15/G32 become candidate cocycles and are **not automatically excluded**. G12 DROP is a relative boundary candidate. G14/G31 give test encodings only. G19 signed flow is precisely the one-dimensional warning; period rows are the proposed missing ingredient, so signed splicing remains live. G28 no min-plus rule; G30 no tensor seed; G33–34 no sphere tags.

**Experiment/falsification.** Build the incidence 2-complex of the nine-clause instance plus one deterministic 2-lift; compute \(H^1(\mathbb Z)\), torsion, and the shortest harmful cochain by ILP. Kill if any known attack is a zero-period short cocycle. Most likely death: relative homology contains constant-support circuits under every polynomial-size attachment.

---

### 5. Tree-fold matrices with provable Graver girth

**Mechanism.** Design a recursive block matrix whose ports contain complete separator assignments, not merely marginals. Seek a family where every harmful zero-residual integer vector contains a Graver element of norm at least \(N^{1/2+c}\), while honest vectors retain \(O(\sqrt N)\) norm.

**Expected move.** Weight nonzero residuals above threshold; then either a NO vector has residual, or its zero-residual kernel move is already polynomially long.

**Obstruction audit.** G1/G7: no slack or radix. G2–3 supply possible leaf matrices but no composition theorem. G5 is directly relevant; complete separator ports are intended to prevent its freed-marginal circuit, but this is unproved. G6: unrestricted kernel only. G9/G11/G13/G15/G32 are explicit short-Graver falsifiers. G12 DROP is included as a port state. G14 is a possible leaf benchmark; G31 only a metric benchmark. G19 no flow. G28 is the closest obstruction, but tested min-plus cost growth rather than Graver girth; \(\lambda\le\mu\) may recur. G30 no tensor seed. G33–34 irrelevant.

**Experiment/falsification.** Start from one G2 survivor, expose all eight separator labels, enumerate two alternating glue matrices, and compute Graver bases at depths \(1,2,3\) using exact circuits/4ti2. Most likely death: a bounded-support circuit embeds unchanged at every depth.

---

### 6. Index-gadget lifting from communication discrepancy

**Mechanism.** Replace each Boolean variable by an explicit indexing gadget \(\mathrm{IND}_k(a,b)=a_b\), \(k=\Theta(\log n)\), and lift clause labels to complete gadget transcripts. Factor a discrepancy matrix into rational Euclidean rows so any signed transcript distribution simulating mutually inconsistent labels should require large \(\ell_2\)-mass.

**Expected move.** A bound \(2^{\Omega(k)}=n^{\Omega(1)}\) on harmful signed mass would translate directly into a polynomial CVP gap, without random tests.

**Obstruction audit.** G1/G7: no slack/radix. G2–3/G5: gadget transcripts globally replace sparse local hashes. G6: all transcript constraints and factors are emitted. G9/G11/G13/G15/G32 are **not outside the assumptions**; each must be shown unable to lift at low norm. G12 DROP corresponds to a missing transcript and is explicitly searched. G14 pair bags and G31 Walsh are lower-complexity comparison cases. G19 no path flow. G28 no serialized recurrence. G30 no lattice tensor seed—the tensor is only a gadget relation. G33–34 no exterior geometry.

**Experiment/falsification.** For \(k=2,3\), gadgetize two overlapping clauses, compute exact singular/discrepancy data, and enumerate all integer transcript vectors through the honest radius plus 32. Most likely death: real discrepancy controls signed \(\ell_1\) correlation but does not imply the required unrestricted integral \(\ell_2\) bound.

---

### 7. Redundant \(p\)-adic normal-form automata

**Mechanism.** Encode every coefficient by balanced digits simultaneously in bases \(2,3,5\), with transition variables for carries and CRT agreement at every level. Unlike G1, carries are not free slack: each transition is selected from a complete finite table, and overlapping digit windows redundantly determine the whole integer.

**Expected move.** Any signed splice preserving one automaton should violate another base or many overlapping windows; \(O(\log n)\) levels could force polynomial cumulative cost.

**Obstruction audit.** G1’s free-slack defect is explicitly removed; G7’s zero raw-residual kernel remains a serious risk because a globally valid signed digit table could still annihilate every base. G2–3/G5 local kernels are replaced by multilevel windows. G6: no bounded/external digit assumption—overflow states and terminal carries are emitted. G9/G11/G13/G15/G32 may lift as signed table distributions and are direct falsifiers. G12 DROP must break normalization across all bases. G14/G31 are benchmarks only. G19 signed splicing is the central warning; redundant CRT, not conservation alone, is the distinction. G28 no fixed tile objective; G30 no seed isometry; G33–34 no tags.

**Experiment/falsification.** Encode one falsified OR core with two digit levels, bases \(2,3\), window length two; exhaust all coefficients within the exact radius bound and test G7/G11/G19 attacks. Most likely death: a two-negative signed cycle synchronizes all carry automata exactly.
