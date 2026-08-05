I did not consult or use the prohibited document or any account of it.

**Obstruction key used in every audit:**  
**A** = G1 RS slack, G7 radix kernel. **B** = G2–3 local affine isolation, G5 private-row overlap, G6 external quotient. **C** = G9 degree-two parity, G11 unique-triple parity, G13 honest-affine-span, G15 laminar lift, G32 additive parity, G37 universal parity cut. **D** = G12 fingerprint DROP, Goal G8 augmented-Gram DROP. **E** = finite-only G14 pair bags, G31 Walsh Gram, G38 splitter bags. **F** = G19 signed splicing, Goal G1 diagonal splice. **G** = G28 \(\lambda\le\mu\), G30 seed isometry. **H** = G33–34 exterior failures. **I** = Goal G2 \(A_5\) zero divisors. **J** = Goals G3–5 \(D_4\). **K** = Goals G6–7 \(E_6\). **L** = Goal G11 canonical \(\mathbb F_{289}\) grade-zero attack. **M** = Goal G12 redundant NAND plus the current grade-zero/COPY splice.

### 1. Heisenberg-cocycle quaternion port

**Mechanism.** Enlarge each boundary from three bits to a lift in \(H_{17}\), with multiplication  
\((x,y,z)(x',y',z')=(x+x',y+y',z+z'+xy')\). Emit the central cocycle coordinate as an ordinary integral selector row, then inject its discrepancy into \(P/P^2\) and multiply it by a quaternion uniformizer at each transfer.

**Expected move.** Break the `111 = -001+011+101` affine pseudosection and prove Q2 from the cocycle identity; promotion requires a Lean induction on composed lifted transitions.

**Audit A–M.** A,B: no slack, radix, filtering, or private rows. C is escaped only if the central coordinate explicitly separates every old affine parity; otherwise G13 kills it. D is enumerated. E is replaced by an all-depth cocycle theorem. F remains a required signed-cycle audit. G uses genuine \(17\)-adic multiplication and sheet labels. H–K are unused. L–M use different enlarged columns; projection back to the old splice is fatal.

**Falsification.** Any legal-compatible lift with zero central defect on `111`, or a signed zero-cocycle seam.

**Experiment.** Enumerate bounded central lifts for all eight NAND words and four COPY pairs; emit one depth-two tile and exhaust \(P^2/P^3\), DROP, and both orientations.

---

### 2. Bidirectional-COPY Nakayama no-go

**Mechanism.** Try to refute the frontier rather than construct it. If the two COPY orientations induce maps \(A,B\) on a nonzero finitely generated defect module \(M\), legal reversibility gives \(BA=1\), while Q2 in both orientations gives \(A(M),B(M)\subseteq PM\); hence \(M\subseteq P^2M\), contradicting Nakayama’s lemma.

**Expected move.** Amend Q2: strict gain cannot be demanded across both orientations of a reversible COPY; gain must instead be charged only at NANDs or over directed COPY. State and prove the module lemma in Lean 4.

**Audit A–M.** A–D,F,H–K are neither assumed nor escaped: the theorem quantifies over residual, affine/parity, DROP, flow, geometric, or group realizations. E’s finite passes cannot settle it. G is directly refuted for reversible COPY. L–M motivate the nonzero defect module but are not required.

**Falsification.** COPY orientations need not compose to identity on adverse classes, or their source and target graded modules differ, invalidating \(BA=1\).

**Experiment.** Extract mod-\(P\) transfer matrices from the smallest proposed COPY tile and test \(BA=I\) together with \(A\equiv B\equiv0\pmod P\). Independently formalize the elementary matrix contradiction in Lean before invoking full Nakayama.

---

### 3. Free-monoid path coordinates

**Mechanism.** Replace scalar defect transfer by noncommutative path labels: every root-to-leaf adverse history writes to its own word coordinate. For depth \(d=O(\log S)\), all \(2^d=O(S)\) words fit polynomial dimension; a coordinate at remaining depth \(r\) receives weight \(17^r\).

**Expected move.** Amend Q2–Q4: prove a unique-word lemma rather than quaternionic valuation transfer—an earliest false transition leaves one uncancellable highest-weight word. The necessary beyond-finite step is a Lean induction over the compiled circuit tree.

**Audit A–M.** A,B: all coordinates are emitted, with no slack or quotient. C is avoided only if path labels prevent compatible parity blocks sharing a word. D includes the zero selector. E becomes an all-depth word theorem. F squarely applies: signed diagonal cancellation is the principal threat. G28 remains a required \(\lambda>\mu\) check; G30 is avoided by formula-dependent labels. H–K are unused. L–M are not assumed, but their pseudosections must be tested after tagging.

**Falsification.** Two adverse signed subcomputations reach the same word with opposite coefficients, or completeness pays comparable weighted energy.

**Experiment.** Emit the depth-two NAND–COPY–NAND tree with length-two word tags and solve the unrestricted exact CVP shell; specifically seed the known false-`111` splice.

---

### 4. Boolean coordinate-ring saturation certificate

**Mechanism.** Give each port the complete eight-idempotent basis of the Boolean coordinate ring, not three affine bits. The four forbidden-word indicators vanish on legal NAND states but equal one on their respective false states; seek a Gröbner certificate expressing each parent forbidden idempotent as a uniformizer times a child idempotent modulo gate and glue ideals.

**Expected move.** Prove Q1/Q2 through an explicit ideal identity and saturation theorem. A CAS may discover the certificate, but Lean must verify the polynomial identity and induction for progress beyond FINITE.

**Audit A–M.** A,B: no slack/filtering, and overlap uses full idempotents. C’s old affine combinations are separated by forbidden idempotents, but a new signed scheme-point would revive C. D is represented by the constant idempotent and quantified. E is replaced by ideal induction. F remains possible in the integral selector module. G must be proved by the uniformizer identity, not inferred. H–K and I are unused. L–M lie outside the three-bit affine port, though their projections are mandatory tests.

**Falsification.** Saturation introduces a component at infinity, or a signed integral point annihilates every idempotent/glue equation without being legal.

**Experiment.** Build one full-state NAND and COPY in Sage/Singular, compute  
\((I_{\mathrm{gate}}:P^\infty)\), and search for the four transfer identities; verify any returned identity using Lean `ring_nf`.

---

### 5. Maximum-distance-profile convolutional checks

**Mechanism.** Replace per-seam gain by a four-level causal code. Feed enlarged adverse syndromes into a fixed superregular Toeplitz parity-check matrix over \(\mathbb F_{17}\); its nonzero minors should ensure that every nonzero defect stream produces a check within four levels, after which a \(P\)-weighted accumulator raises valuation.

**Expected move.** Amend Q2 to “one certified gain in every four levels,” exactly matching the existing \(17>2^4\) Lean telescope. Prove in Lean that the stated minor conditions imply the sliding-window transfer bound for arbitrary finite streams.

**Audit A–M.** A: no slack/radix. B: checks are global causal rows, fully emitted. C is escaped only for enlarged syndromes; any G13-zero syndrome kills the code before distance matters. D is a code symbol and must be searched. E becomes a uniform window theorem. F is addressed only if the code detects signed streams. G directly targets strict average growth and uses formula-independent superregularity, avoiding G30. H–K and I are unused. L–M fail the required nonzero input syndrome unless the interface is enlarged.

**Falsification.** A zero syndrome for `111`, a carry-dependent lift, or a weight-four signed stream in the Toeplitz kernel.

**Experiment.** Construct the smallest Cauchy-Toeplitz matrix with window four; enumerate all streams over \(\mathbb F_{17}\), then every lift modulo \(17^2\), and test the current NAND/COPY splice first.

---

### 6. Finite-cover obstruction for adverse walks

**Mechanism.** Regard NAND/COPY compositions as paths in a finite state graph and lift that graph to a nonabelian finite cover. Legal computations close on a designated sheet, while an adverse transition inserts a deck generator; choose a cover with no nontrivial reduced adverse word of length at most \(d\), of size exponential in \(d\) and therefore polynomial in \(S\).

**Expected move.** Amend Q2 from valuation growth to unique path lifting, then weight nonidentity sheets by depth. Lean would need both the covering-space path-lift theorem and a shell-to-path decomposition for unrestricted integral selectors.

**Audit A–M.** A–B: incidence, sheet, and target rows are emitted directly. C is outside only for genuine paths; affine signed chains may still collapse sheets. D is an explicit vertex state. E becomes a depth-uniform cover theorem. F is fully applicable—G19 warns that integral flows need not be paths. G requires a new weighted recurrence; sheet asymmetry avoids G30. H–K and I are unused. L–M are tested as adverse words rather than assumed absent.

**Falsification.** A short signed 1-chain has legal boundary and trivial deck label although no honest path does; this is the expected failure mode.

**Experiment.** Form the NAND/COPY transition graph, lift it to the order-\(17^3\) Heisenberg cover, and use exact ILP to find the shortest signed accepting chain through depth three.
