I use the following exhaustive obstruction labels from the supplied map: **Slack** (G1); **Affine/splice** (G2–7, G11, G13, G15, G19); **metric–DROP–additivity** (G9, G12, G31–32, G37); **fixed-bag scaling** (G14, G38); **recursion/tensor** (G28, G30); **exterior completeness** (G33–34); and **validity/specification** (G6, G40).

### 1. Logarithmic-width Walsh uncertainty bags

**Core trick.** Use bags of \(w=\lceil\gamma\log_2 n\rceil\) variables, \(q=2^w=n^\gamma\) assignment selectors, and a full \(H_q\) Walsh block. Proper-moment consistency forces any hidden top-character deviation to occupy many labels; its Walsh energy can then be \(\Theta(q^2)\) against honest energy \(\Theta(q)\).

**Expected move.** Prove squared NO/YES ratio \(\Omega(q)\), hence distance gap \(n^{\gamma/2}\), using a deterministic bag family where every non-Dirac signed section becomes dense somewhere.

**Obstruction audit.** **Slack:** no slack variables. **Affine/splice:** not escaped; \(2\delta_a-\delta_b\) is the decisive countertest. **Metric–DROP–additivity:** growing \(q\), normalization weight \(>q^2\), and shared rather than copied bags lie outside fixed G31/G37 assumptions, but G32-style additivity remains possible. **Fixed-bag:** explicitly leaves constant-width G14/G38. **Recursion/tensor:** neither recursion nor coefficient tensors. **Exterior:** Walsh norms are exactly cospherical. **Validity:** use \(C=[2I;H_q;WA]\), fixed target, and derive the shell from \(C^TC\succeq4I\).

**Smallest experiment.** Replace G38’s 16-label full-variable bags by \(H_{16}\) blocks and compute exact NO/control minima.

**Likely death.** A constant-support integral section survives every overlap, yielding only a constant ratio.

---

### 2. History-binding tree-code flow

**Core trick.** Augment each branching-program edge with a deterministic convolutional history label having large column distance: two paths that splice after diverging disagree in labels for a linear suffix. Emit all label-transition checks, so an accepting signed flow must either be an affine combination of complete rejecting histories or pay many history residuals.

**Expected move.** Turn G19’s two-negative local splice into \(\Omega(L)\) violated rows while honest paths satisfy every row; scale those zero-on-completeness rows to obtain polynomial excess.

**Obstruction audit.** **Slack:** no slack. **Affine/splice:** directly targets G19; G13/G15 affine combinations of complete paths still vanish at ACCEPT, so only genuine splices should be charged. **Metric–DROP–additivity:** history checks are longitudinal, not copy-additive; source/sink normalization must make DROP cost exceed threshold. **Fixed-bag:** no bags. **Recursion/tensor:** no min-plus or tensoring. **Exterior:** labels can be simplex columns with certified equal norm. **Validity:** G40 remains unsatisfied until an explicit integer encoder, termination rule, factor, and unrestricted shell are frozen.

**Smallest experiment.** Take the first 12 layers of G19, search binary rate-\(1/2\) memory-3 convolutional generators, and exactly enumerate accepting signed flows with anchor excess at most 24.

**Likely death.** Signed superpositions splice both path and history streams so that every linear label check cancels; asymptotically good explicit tree distance may also smuggle in PCP machinery.

---

### 3. Ramified algebraic-norm residuals

**Core trick.** Replace scalar residuals by elements of a totally real number field and measure all conjugates through an integral trace-form lattice. Choose ramified prime-power labels so any nonzero legal residual has algebraic norm divisible by \(p^k\), forcing at least one conjugate—and hopefully the Euclidean trace norm—to be polynomially large.

**Expected move.** Amplify one unavoidable clause defect without repeated completeness coordinates: \(k=\Theta(\log n)\) would give \(p^{\Theta(k)}=n^{\Theta(1)}\).

**Obstruction audit.** **Slack:** outside G1 only if no freely adjustable algebraic slack is emitted. **Affine/splice:** not escaped—any exact integral selector kernel has algebraic residual zero and kills the proposal. **Metric–DROP–additivity:** conjugate spreading is multiplicative rather than copied PSD energy, but DROP and baseline trace norm require separate bounds. **Fixed-bag:** unrelated. **Recursion/tensor:** no tensor iteration. **Exterior:** equal trace norm of all honest labels must be checked; it is not automatic. **Validity:** regular-representation and trace Gram must be explicitly integral and positive definite; no external congruence filters.

**Smallest experiment.** Over \(K=\mathbb Q(\sqrt5)\), assign eight local labels prime-power-separated algebraic integers, emit the trace Gram for the eight-clause core, and enumerate the complete shell.

**Likely death.** Linearity permits the G7/G13 zero-residual identities; alternatively equal completeness consumes exactly the norm amplification.

---

### 4. Compound-matrix determinant amplification

**Core trick.** Build a global affine constraint matrix whose harmful integer fibers are nonsingular but have small first singular value, then pass to its \(k\)-th compound matrix. Products of \(k\) singular values can amplify an integral determinant/minor lower bound without repeating the original anchor baseline.

**Expected move.** Obtain a polynomial lower bound on every NO affine representative from many nonzero minors, while a YES witness lies in a designated low-distance coset.

**Obstruction audit.** **Slack:** no clause slack is required. **Affine/splice:** outside only if every signed kernel changes a certified minor; exact kernels remain fatal. **Metric–DROP–additivity:** determinant growth is global and nonadditive, unlike G32/G37, but zero vectors and rank-deficient DROP states need explicit exclusion. **Fixed-bag:** unrelated. **Recursion/tensor:** G30 does apply conceptually: unrestricted compound coordinates need not be decomposable wedges, so “entangled” integer points must be audited. **Exterior:** unlike G33, compounds amplify constraints rather than tag honest labels; nevertheless equal completeness is required. **Validity:** no decomposability may be imposed externally.

**Smallest experiment.** Form first and second compounds of the exact G3 survivor and of one G5 overlap matrix; enumerate every unrestricted compound coefficient vector through twice the control radius.

**Likely death.** A short nondecomposable wedge vector defeats all determinant reasoning, or determinant amplification increases dimension and completeness radius at the same rate.

---

### 5. Sublevel-set rounding by diagonally dominant geometry

**Core trick.** Search for an integer quadratic factor whose low-radius sublevel set has a rounding theorem: every unrestricted integer selector vector can be changed to a nonnegative one-hot section without increasing objective. Use signed column choices and auxiliary equality rows to make the relevant Gram block an \(M\)-matrix or an obtuse-superbase form only inside the promised shell.

**Expected move.** Once signed cheats provably round away, scale zero-on-honest clause rows by \(W=n^{c+1}\); every NO instance then pays \(W^2\) over an \(O(\mathrm{poly}(n))\) completeness radius.

**Obstruction audit.** **Slack:** no free slack. **Affine/splice:** directly attempts a theorem excluding all G7/G13/G19 signed vectors, not merely enumerating them. **Metric–DROP–additivity:** scaling follows only after rounding; DROP must round to an honest section or exceed the shell. **Fixed-bag:** could apply to any bag system. **Recursion/tensor:** neither. **Exterior:** no tag sphere needed beyond exact honest radius. **Validity:** freeze \(Q=C^TC\), target, eigenvalue floor, and prove shell rounding without box assumptions, addressing G6/G40.

**Smallest experiment.** On the nine-clause instance, solve a rational feasibility program for column signs and diagonal weights making all shell-relevant off-diagonals nonpositive; then exhaustively verify the rounding map.

**Likely death.** Such geometry may make the whole nearest-vector problem polynomial-time, or G13 creates an unavoidable positive Gram cycle.

---

### 6. Torsion cosets with a certified Euclidean cosystole

**Core trick.** Encode consistency as an integral chain complex and place the target in a torsion affine coset, but supplement Smith data with a genuine cosystolic inequality: every representative of the nontrivial class must have large weighted support. Clause gadgets attach 2-cells so satisfiable instances trivialize the target, whereas unsatisfiable instances leave a long torsion representative.

**Expected move.** A bounded-degree complex with cosystole \(N^\alpha\) would yield distance gap \(N^{\alpha/2}\) after controlling completeness.

**Obstruction audit.** **Slack:** no slack. **Affine/splice:** signed chains are allowed; the proposed cosystole must lower-bound them, directly confronting G13/G19 rather than assuming nonnegativity. **Metric–DROP–additivity:** a quotient-class invariant is nonadditive, but Euclidean support—not merely torsion order—must defeat DROP. **Fixed-bag:** global topology replaces fixed bags. **Recursion/tensor:** no tile or tensor composition. **Exterior:** irrelevant. **Validity:** G40’s Smith-normal-form objection fully applies unless the complex, target class, weights, and shortest-representative certificate are explicit.

**Smallest experiment.** Attach the eight-clause core to the standard six-vertex triangulation of \(\mathbb{RP}^2\); compute SNF and enumerate the shortest representative of each torsion coset under formula-dependent attachments.

**Likely death.** Abelianization forgets SAT’s noncommutative logic, producing a constant-support signed representative; constructing formula-dependent cosystolic expansion may itself be PCP-equivalent.

---

### 7. Symmetric-power correlation decay tags

**Core trick.** Give every local label a rational unit-vector tag \(u_\ell\), but emit \(u_\ell^{\otimes k}\) as a precomputed column rather than tensoring coefficient spaces. With \(k=\Theta(\log n)\) and constant base dimension, the feature dimension remains polynomial while correlations \(\langle u_\ell,u_{\ell'}\rangle^k\) decay polynomially.

**Expected move.** Make incompatible local histories nearly orthogonal, so any signed pseudosection requiring many incompatible labels has feature energy \(n^\gamma\) above the exactly equal honest radius.

**Obstruction audit.** **Slack:** none. **Affine/splice:** G13 remains a direct threat; sparse \(2\delta_a-\delta_b\) combinations retain constant coefficient norm, so soundness needs a support-growth lemma. **Metric–DROP–additivity:** nonlinear correlation decay lies outside G31/G37’s fixed orbit weights, but copied compatible parity may still be additive as in G32; normalization tags must charge DROP. **Fixed-bag:** can use growing overlap histories rather than fixed bags. **Recursion/tensor:** unlike G30, coefficients are ordinary scalars and no unrestricted tensor variable exists. **Exterior:** rational simplex tags are automatically cospherical, avoiding G33/G34’s center failure. **Validity:** emit exact rational tensors, Gram, center, eigenvalue floor, and full shell.

**Smallest experiment.** Use rational tetrahedral tags, tensor powers \(k=1,2,3\), and the G19 or G38 coefficient space; compare exact minima and enumerate all sparse affine attacks.

**Likely death.** Correlation decay cannot amplify a two-point affine collision, so the ratio remains constant unless an unproved support-expansion theorem is supplied.
