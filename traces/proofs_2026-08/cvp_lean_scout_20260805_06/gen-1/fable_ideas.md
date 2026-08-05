I did not consult the prohibited document or any account of it. The sketches are deliberately unordered.

### 1. Finite residue transducer with a Lean lifting theorem

**Mechanism.** Model one composed gate as a complete transducer on boundary class, DROP status, and normalized leading defect in \(P^a/P^{a+2}\). Prove in Lean that scale-equivariance and saturation make this finite table complete for every \(a\), so a table certificate excluding weight-zero adverse transitions proves Q2 by depth induction—or returns a concrete counterexample.

**Expected move.** State `valuation_transfer_of_mod_P_sq_certificate`; apply it first to NAND–NAND, later NAND–COPY.

**Smallest experiment.** Build the full \(P^2\)-state relation for two copies of the best \(N=8\) NAND survivor with one legal input fixed. Emit transition witnesses plus a Lean-checkable exhaustive certificate.

**Falsification / likely death.** A normalized signed state whose parent leading term is grade zero.

**Obstruction audit.** G1 RS/G7 radix use neither slack nor digits; G6 residues are proof-side, not filtered coordinates. G2–3 affine isolation, G5 overlap, G12 and Goal G8 DROP are explicitly enumerated. G9/G11/G13–15/G31–32/G37–38 assume moment/bag/parity metrics absent here, while all signed states remain. G19/G30/G33–34 and Goals G1–7 concern flows, literal tensors, exterior tags, group rings, D4/E6, none used. G28 is exactly tested. Goal G11 canonical is bypassed; Goal G12 remains only the finite seed.

---

### 2. Rees-module colon certificate

**Mechanism.** Encode each tile over the Rees module \(\bigoplus_k P^k t^k\). Grade-zero return is then a kernel/colon failure: Q2 reduces to an explicit inclusion such as \((K:P)\cap A\subseteq K+P A\), where \(K\) is the glued relation module; SNF or Gröbner calculations can produce either a violating syzygy or matrices certifying the inclusion.

**Expected move.** Prove a Lean matrix lemma turning certified colon inclusions for NAND and COPY composition types into all-depth filtration growth.

**Smallest experiment.** Form the exact integer multiplication matrices for a two-NAND chain, compute \((K:P)/K\), and export inclusion identities \(UX+VY=I\) for Lean verification.

**Falsification / likely death.** Gluing creates a low-support colon element invisible in each isolated tile.

**Obstruction audit.** G1/G7 introduce slack or radix; neither occurs. G6’s quotient is invalid only when externally filtering CVP vectors; here Rees quotients certify the unchanged emitted lattice. G2–3, G5, G12/Goal G8 are precisely saturation, gluing, and zero-class terms in the colon test. G9/G11/G13–15/G31–32/G37–38 are linear-moment/bag parity mechanisms, absent here. G19/G30/G33–34 and Goals G1–7 use flows, literal tensors, exterior tags, group rings, D4/E6. G28 becomes strict colon growth. Goal G11’s canonical module is not used; Goal G12 remains insufficient without this certificate.

---

### 3. Residue-direction ping-pong

**Mechanism.** In \(\operatorname{gr}(\mathcal O)\cong\mathbb F_{289}[\pi;\sigma]\), cancellation at the leading grade requires matching residue directions. Enlarge signatures so the two fan-in branches constrain leading coefficients to distinct one-dimensional \(\mathbb F_{17}\)-subspaces of \(\mathbb F_{289}\); two nonzero terms from distinct lines cannot cancel, while unit conjugations rotate line labels between levels.

**Expected move.** Prove Q2 via a finite “line coloring” invariant; simultaneously synthesize COPY as a color-preserving tile.

**Smallest experiment.** SAT-search assignments among the 18 projective \(\mathbb F_{17}\)-lines for one NAND–NAND and one COPY–NAND composition, then enumerate every leading-residue fiber. Formalize the two-line noncancellation lemma in Lean.

**Falsification / likely death.** Unrestricted coefficients may range over all of \(\mathbb F_{289}\), destroying the claimed \(\mathbb F_{17}\)-line restriction.

**Obstruction audit.** G1/G7 slack/radix and G6 filtered quotients are absent. G2–3/G5 are not assumed away: line confinement must be proved for saturated glued fibers. G12/Goal G8 include the zero line explicitly. G9/G11/G13–15/G31–32/G37–38 concern moment, affine-span, or bag parity rather than skew leading directions. G19/G30/G33–34 and Goals G1–7 concern flows, tensors, exterior, group rings, D4/E6. G28 is replaced by strict noncancellation. Goal G11 used unrestricted grade-zero residues and therefore directly falsifies any failed confinement; Goal G12 supplies only the starting NAND code.

---

### 4. Vector-valued \(P\)-adic tree code

**Mechanism.** Amend Q2 from one scalar defect to \(r\) quaternionic defect channels. Each gate applies branch-dependent superregular matrices plus one \(P\)-shift; parity checks make every signed adverse computation have a nonzero channel whose accumulated valuation grows linearly with depth, analogous to column distance in convolutional codes.

**Expected move.** Replace Q2 by a Lean theorem: a certified finite-state column-distance inequality implies \(d_{\mathrm{NO}}^2\ge 17^{\delta d}\), with Q5 adjusted by constant \(r\).

**Smallest experiment.** For \(r=2\), search monomial unit matrices and diagonal \(P\)-shifts through depth four over \(\mathcal O/P^4\), including DROP and all signed mergers. Export a candidate recurrence for Lean induction.

**Falsification / likely death.** Completeness energy or channel count grows as fast as the adverse distance; alternatively a diagonal signed splice annihilates every check.

**Obstruction audit.** G1/G7 and G6 are absent because channels are emitted coordinates, not slack, digits, or filters. G2–3/G5 and G12/Goal G8 are quantified by the decoder theorem. G9/G11/G13–15/G31–32/G37–38 assume additive moment/bag metrics; this uses ordered matrix products, though their parity witnesses remain mandatory tests. G19 and Goal G1 are not outside scope: their signed splices must be decoded. G30’s literal Kronecker seed, G33–34, Goal G2, and Goals G3–7 are absent. G28 is the column-distance inequality itself. Goal G11 is bypassed only after new channels; Goal G12 is merely the seed.

---

### 5. Extension classes and Yoneda powers

**Mechanism.** Regard a saturated tile as an exact sequence \(0\to K\to F\to B\to0\) over \(\operatorname{gr}(\mathcal O)\). A grade-zero pseudosection is a splitting; recursive composition corresponds to Yoneda products, so nonvanishing powers of the adverse extension class would prove Q2, while a zero square would give a principled depth-two refutation.

**Expected move.** State an elementary Lean version using quotient modules and explicit matrices, avoiding dependence on a large Ext library.

**Smallest experiment.** Reduce the NAND survivor modulo \(P^3\), compute its adverse extension matrices, and solve the splitting equations for the Yoneda square. Have Lean verify either the splitting map or the matrix non-splitting certificate.

**Falsification / likely death.** The skew graded ring may have low homological dimension, forcing higher extension products to vanish.

**Obstruction audit.** G1/G7 slack/radix and G6 external filtering are absent. G2–3/G5 become exactness under pushout; they are assumptions requiring certificates, not escaped. G12/Goal G8 are the zero-section cases. G9/G11/G13–15/G31–32/G37–38 concern affine moment or bag kernels, whereas this tests module splitting, including signed sections. G19/G30/G33–34 and Goals G1–7 use unrelated flows, tensors, exterior tags, group rings, D4/E6. G28 is nonnilpotence versus splitting. Goal G11 already exhibits a split canonical extension and is therefore an explicit negative control. Goal G12 supplies a nonsplit depth-one candidate only.

---

### 6. Algebraic-geometric avoidance of bad transfer cycles

**Mechanism.** Parameterize saturated redundant NAND/COPY tiles by a Stiefel-type open set over \(\mathbb F_{289}\). For the finite normalized residue automaton, every simple zero-growth adverse cycle imposes determinantal polynomial equations; prove that their union is not the whole parameter space, select a rational point deterministically, and Hensel-lift it to integral tiles.

**Expected move.** Amend Q1/Q2 jointly: a Lean-checked nonzero polynomial evaluation plus a finite-cycle lemma yields an all-depth positive cycle mean.

**Smallest experiment.** Restrict to a two-parameter perturbation of the \(N=8\) NAND survivor and an \(N=9\) COPY ansatz. Enumerate simple bad cycles, multiply one witness minor per cycle, and search for a point where the product is nonzero.

**Falsification / likely death.** A universal syzygy makes one bad-cycle variety equal the entire saturated parameter space; alternatively \(\mathbb F_{289}\) is too small for the counting bound.

**Obstruction audit.** G1/G7 and G6 are absent; residue geometry is proof-side and final coordinates are integral. Saturation, overlap, and DROP—G2–3, G5, G12/Goal G8—define explicit open/closed conditions. G9/G11/G13–15/G31–32/G37–38 concern fixed moment/bag families; their attacks appear here as bad varieties rather than being ignored. G19/G30/G33–34 and Goals G1–7 have different flow, tensor, exterior, group-ring, D4/E6 assumptions. G28 is exactly positive cycle mean. Goal G11 is one point lying in a bad variety; Goal G12 provides only the initial good depth-one point.
