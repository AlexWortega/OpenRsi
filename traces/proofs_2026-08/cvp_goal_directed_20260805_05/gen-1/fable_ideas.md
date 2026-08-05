### 1. Pure-moment lift of the signed splice — **refute FRONTIER**

**Core trick.** Extract the Generation-19 accepting signed flow \(s\), with total mass one, and form the ordered-tuple moment \(z^{(k)}=s^{\otimes k}\). Marginals, source/sink conditions, repeated-query totals, and ACCEPT often tensor exactly; if so this gives an explicit all-\(k\) adversary rather than merely a \(k=2\) counterexample.

**Expected move.** Symbolically compute its energy and refute \(E_k\ge(4/3)^kR_k^2\), or identify the first coherence row that destroys tensor closure.

**Obstruction audit.** G1/G7: no slack or radix; attack is zero-residual. G2/G3: formula covers unbounded integers. G5/G6: check every emitted tuple port and row. G9/G11/G13/G15/G19: deliberately preserves these signed/affine/parity phenomena, so they are not escaped. G12: normalization is verified, not dropped. G14/G38: no bag extrapolation. G28: no min-plus tile. G30: tensors coefficients, not the CVP factor/target; nevertheless test seed isometries. G31: symbolic all-\(k\), not a finite shell. G32/G37: multiplicative, not additive-copy coupling. G33/G34: no exterior tags or metric repair.

**Experiment.** Reconstruct the smallest two-negative splice, emit \(s^{\otimes2}\), verify every row exactly, and compare with \(4R_2^2/3\).

**Likely death.** A diagonal/repeated-query coherence row is not inherited by tensor products.

---

### 2. Principal-angle tensorization — **prove FRONTIER spectrally**

**Core trick.** Regard marginal consistency, query consistency, and acceptance as affine subspaces of the real tuple-flow Hilbert space. After removing honest-path directions, prove that the relevant projection product has squared singular value at most \(3/4\); tensorization would then multiply this contraction at every level, without positivity assumptions.

**Expected move.** Convert the \(4/3\) energy growth into a sharp Friedrichs-angle or generalized-eigenvalue inequality.

**Obstruction audit.** G1/G7: the norm acts on zero-residual kernels. G2/G3: a real-subspace bound covers all integers. G5/G6: projections use every emitted port and constraint. G9/G11/G13/G15/G19: each becomes an explicit invariant mode; eigenvalue \(1\) honestly falsifies the approach. G12: DROP is a separate affine mode. G14/G38: no bags. G28: no transfer-table recursion. G30: tensorizes projection operators, not a seed factor/target. G31: an operator identity supplies scaling, not shell extrapolation. G32/G37: compatible parity copies must appear in the spectrum; additivity is not assumed. G33/G34: original Euclidean anchors only.

**Experiment.** For the minimal G19 splice at \(k=2\), build exact rational Gram matrices for the constraint projections and compute the largest generalized eigenvalue after quotienting honest paths.

**Likely death.** The signed splice lies in an exact common subspace, forcing singular value \(1\).

---

### 3. Parametric Graver decomposition — **prove FRONTIER combinatorially**

**Core trick.** Let \(A_k\) be the complete integral constraint matrix of the accepting \(k\)-flow fiber. Decompose every displacement from a reference flow sign-compatibly into Graver elements, then classify primitive elements as either path exchanges yielding an honest accepting path or circuits with a quantitative anchor/coherence cost.

**Expected move.** Reduce unrestricted soundness to a finite-width circuit inequality stable under increasing program length and \(k\).

**Obstruction audit.** G1/G7: circuits in \(\ker A_k\) are charged by coefficient norm. G2/G3: this is an exact unbounded-fiber theorem, not bounded isolation. G5/G6: \(A_k\) includes all ports and emitted rows. G9/G11/G13/G15/G19: parity, affine lifts, and signed splices must appear among primitive circuits; no exclusion is assumed. G12: normalization-changing circuits are classified separately. G14/G38: no pair/splitter bags. G28: no min-plus growth. G30: no literal factor tensor. G31: requires a uniform circuit theorem. G32/G37: no orthogonal-copy additivity. G33/G34: no tag metric.

**Experiment.** Minimize the G19 program to its splice-support layers; compute the \(k=2\) Graver basis with 4ti2 or exact circuit enumeration and test each element against the \(4/3\) inequality.

**Likely death.** Repeated-query rows create primitive circuits of unbounded support but constant excess energy.

---

### 4. Toric/Veronese coherence — **amend the lift**

**Core trick.** Replace raw tuple coordinates by local monomial coordinates and emit linearized toric relations—normalization, multiplication consistency, and \(2\times2\) minors—whose integral points model rank-one path moments. Signed splices are secant points of the path variety; the hoped-for statement is that degree \(k=O(\log L)\) separates ACCEPT from that secant locus with growing \(\ell_2\) cost.

**Expected move.** Prove a modified FRONTIER via degree growth, or refute it by constructing a low-degree pseudomoment extension.

**Obstruction audit.** G1/G7: no slack/radix; exact toric kernels remain norm-charged. G2/G3: quantify over all integral pseudomoments. G5/G6: all multiplication and marginal rows are emitted. G9/G11: parity survives exactly when the chosen degree is too low. G12: degree-zero normalization blocks DROP. G13: outside raw linear syndromes because coordinates are nonlinear monomials. G14/G15/G38: no fixed bag or laminar extrapolation. G19: the splice is the seed secant. G28: no tile. G30: not factor tensoring. G31: needs a degree theorem, not a finite pass. G32/G37: mixed monomials couple copies nonadditively. G33/G34: no exterior tags or synthesized Gram.

**Experiment.** Build degree-two Macaulay/toric rows for the smallest splice and solve the unrestricted \(k=2\) integer fiber exactly.

**Likely death.** The splice extends to a low-degree pseudomoment, or the required degree makes rank superpolynomial.

---

### 5. Relative homology and cosystolic expansion — **amend the coherence edge**

**Core trick.** Interpret transition flows as chains, conservation as boundary equations, and signed splices as relative cycles between SOURCE and ACCEPT. Complete tuple consistency with higher cells chosen so that every non-path accepting class has a cosystolic norm expansion under cellular products, while honest paths retain a canonical relative class.

**Expected move.** Replace “tensor energy” by a relative systolic inequality giving the same exponential-in-\(k\) growth.

**Obstruction audit.** G1/G7: zero-residual cycles pay chain norm. G2/G3: the systole ranges over all integral chains. G5/G6: every boundary and gluing map is emitted. G9/G11/G13/G15/G19: these become named homology classes and must be killed or expanded explicitly. G12: DROP is a wrong-boundary class. G14/G38: no bag-family inference. G28: no min-plus tables. G30: cellular products are not literal CVP-factor tensors, though product isometries remain an audit. G31: requires a uniform expansion theorem. G32/G37: shared higher cells prevent orthogonal additivity. G33/G34: topology replaces exterior tags and Gram repair rather than reusing them.

**Experiment.** Build the \(k=2\) cubical completion of the minimal splice support; compute relative homology by Smith normal form and the smallest nontrivial integral cosystole by MILP.

**Likely death.** A constant-weight torsion-free cycle survives every local higher-cell completion, or the completion also fills honest paths.

---

### 6. Polynomial-calculus certificate with norm control — **prove or refute the logarithmic edge**

**Core trick.** Encode transition choice, repeated queries, path multiplication, and ACCEPT as a Boolean polynomial system. Its degree-\(k\) Macaulay linearization is a signed pseudomoment system; a degree-\(O(\log L)\) refutation with controlled coefficient norm would yield FRONTIER, while a low-norm pseudomoment gives a direct counterexample.

**Expected move.** Identify the frontier with a quantitative proof-complexity statement instead of assuming rank-one decomposition.

**Obstruction audit.** G1/G7: no slack or residual-only amplification. G2/G3: rational certificates exclude the whole integral fiber. G5/G6: every consistency polynomial is linearized and emitted. G9/G11: parity is a degree lower-bound witness, not omitted. G12: \(\sum z=1\) is part of the ideal. G13: higher-degree multiplication targets the affine collision. G14/G15/G38: no bag or hierarchy scaling. G19: its exact degree-one pseudodistribution is the starting witness. G28: no tile recursion. G30: no literal tensor seed. G31: a uniform degree/norm theorem is mandatory. G32/G37: mixed monomials include cross-copy parity. G33/G34: no geometric tags or metric synthesis.

**Experiment.** Compute degree \(1\)–\(4\) Macaulay matrices for the minimal splice; find either an exact ACCEPT refutation and minimum-norm certificate or an integral/rational pseudomoment extension.

**Likely death.** Polynomial-calculus degree is \(\Omega(L^\alpha)\), making the lifted rank superpolynomial and invalidating the roadmap exponent.
