I do not use the prohibited recent material. The routes below rely only on classical machinery and the supplied obstruction map. None is currently a proof; each identifies a concrete frontier lemma.

## Common quantitative endpoint

Let \(N\) be the 3SAT input length. Each strategy targets a balanced depth

\[
k=\lfloor \log_2 N\rfloor
\]

construction with:

- legal squared transfer cost multiplying by \(\mu\);
- false squared transfer cost multiplying by at least
  \[
  \lambda\ge \frac{17}{16}\mu;
  \]
- output dimension \(n\le N^{21}\).

Then the distance gap is at least

\[
(\lambda/\mu)^{k/2}
  \ge \text{const}\cdot N^{\frac12\log_2(17/16)}
  \ge n^{1/1000}
\]

after harmless padding for small \(N\). Thus all three routes would prove the theorem with the explicit choice

\[
\boxed{c=10^{-3}}.
\]

---

# Strategy 1: redundant signatures plus ramified quaternion filtration

This is the most direct continuation of the sole surviving local NAND gadget.

### Lemma Q1 — complete NAND/COPY modules

Construct explicit integral NAND and COPY modules of rank at most \(2^{20}\), extending the Generation-12 redundant-signature NAND code, with equal legal squared energy \(E\). For every unrestricted integral coefficient vector in a boundary fiber:

1. a legal boundary has minimum exactly \(E\);
2. a false boundary has a nonzero defect in the ramified ideal \(P\) of a definite quaternion order;
3. DROP and every signed affine representative also have energy at least \((17/16)E\).

The statement must quantify over the entire integral fiber, not bounded coefficients.

### Lemma Q2 — graded transfer injectivity

For every legal composition of modules, if a boundary defect has valuation \(a\) and the next adverse transfer has valuation \(b\), the output defect has valuation at least \(a+b\). Equivalently, the induced maps on

\[
\operatorname{gr}_{P}(\mathcal O)
\]

have no false-boundary kernel in any grade. In particular, a false root at circuit depth \(j\) lies in \(P^j\setminus\{0\}\).

### Lemma Q3 — universal signed-composition theorem

Every integral witness for a composed circuit is a conformal sum of local Graver moves, and every such move either:

- preserves an honest legal state, or
- creates the nonzero graded defect certified by Q2.

Consequently signed overlap, diagonal embeddings, and two-copy Lawrence relations cannot cancel the quaternion defect.

### Lemma Q4 — Euclidean transfer inequality

Under the positive trace embedding,

\[
\operatorname{Trd}(x\bar x)=2\operatorname{Nrd}(x)
   \ge 2\cdot17^j\qquad(0\ne x\in P^j).
\]

Choose fixed rational weights so that legal and adverse min-plus transfer tables satisfy

\[
\lambda/\mu\ge17/16
\]

at every level, including all malformed ports.

### Lemma Q5 — circuit compilation and reduction

Balance the clause conjunction into a depth-\(k+O(1)\) NAND/COPY circuit, emit Q1 modules, and prove rank and bit complexity at most \(N^{21}\). Satisfying assignments give legal witnesses; an unsatisfiable formula gives a false root, so Q2–Q4 yield the required \(n^{1/1000}\) gap.

**Why sufficient.** Q1–Q4 establish an all-integral, multiplicative soundness invariant; Q5 converts it into the desired deterministic many-one reduction.

**Crux.** Q2: false defects must enter positive filtration and remain nonzero under every COPY and composition, rather than surviving in grade zero.

**First experiment.** Over \(\mathcal O/P^2\), enumerate COPY signature multisets of length \(8\)–\(12\). For the surviving NAND signature, compute all boundary fibers and their Graver bases; reject any candidate having a false grade-zero class or a depth-two product with valuation below the sum. This is a finite exact-field/ILP computation.

---

# Strategy 2: Möbius defects, unique-neighbor checks, and min-plus recursion

### Lemma M1 — kernel-free local coordinates

For every \(m\le 20\) variable bag, emit all \(2^m\) Boolean zeta coordinates. The resulting matrix is unimodular, with integral Möbius inverse. Hence equality of complete local coordinates implies equality of integral distributions—not merely equality of low-degree moments.

### Lemma M2 — shell sparsity/nonnegativity dichotomy

Construct equal-radius local tags such that every integral witness below \((17/16)\) times legal squared cost satisfies one of:

1. every bag coefficient vector is a nonnegative one-hot vector; or
2. its Möbius defect has support at most \(K=20\); or
3. its local energy already exceeds the adverse threshold.

This must include zero vectors, negative coefficients, and dropped bags.

### Lemma M3 — deterministic sparse-defect elimination

Use an explicit lossless expander or splitter matrix \(H\) with a unique neighbor for every support of size at most \(K\). Apply \(H\) only to defects that vanish identically on honest encodings. Then

\[
0\ne\Delta,\quad |\operatorname{supp}\Delta|\le K
   \Longrightarrow H\Delta\ne0
\]

over the integers, independently of coefficient size.

### Lemma M4 — Graver-complete composition inequality

For the fixed bag-gluing template, compute/prove a symbolic Graver and Markov decomposition. Every primitive composed move is either charged by M3 or is an honest reassignment. The exact transfer tables therefore obey

\[
\lambda\ge(17/16)\mu
\]

under arbitrary overlaps, not merely for named attacks.

### Lemma M5 — explicit splitter hierarchy

Build a deterministic balanced hierarchy of bags and splitters with dimension \(n\le N^{21}\), while preserving exact completeness. M4 iterated for \(k\) levels gives the common quantitative endpoint.

**Why sufficient.** M1 removes local affine kernels; M2–M3 exclude every near-shell sparse signed defect; M4 converts this into all-depth soundness; M5 supplies polynomial size.

**Crux.** M2. Ordinary anchor energy does not presently imply sparse defect support or nonnegativity.

**First experiment.** On the Generation-38 twelve-bag instance, replace pair marginals by full Möbius defects. Enumerate the exact shell through \(17B/16\), record maximum defect support, and compute all Graver elements attaining that shell. A single dense low-energy signed element falsifies M2.

---

# Strategy 3: rank-\(\le43\) affine tile and E-type tensor amplification

### Lemma T1 — nonisometric rank-\(\le43\) semantic tile

Construct NAND and COPY CVP tiles of rank at most \(43\), using redundant nonlinear signatures rather than affine \(D_4/E_6\) ports. Legal fibers have equal minimum \(E\); every false, DROP, or malformed fiber has minimum at least \((17/16)E\). YES and NO tiles must not be related by coefficient or ambient isometries.

### Lemma T2 — primitive affine homogenization

For each tile \((L,t)\), construct a positive-definite augmented lattice \(\widehat L\) such that every relevant shortest vector has homogenizing coordinate exactly \(\pm1\). Vectors in the zero layer and coordinates \(|h|\ge2\) are strictly longer than the adverse threshold.

### Lemma T3 — affine E-type no-entanglement theorem

Prove for these augmented rank-\(\le43\) factors that every shortest vector in each iterated semantic tensor contraction is decomposable and has all homogenizing coordinates \(\pm1\). Thus legal and adverse minima multiply exactly. Kitaoka’s classical E-type theorem supplies decomposability once T2 has reduced the affine problem to the correct homogeneous minimum.

### Lemma T4 — tensor circuit routing

Encode the balanced NAND/COPY circuit by permutations and contractions of the fixed factors, without introducing an unrestricted linear coherence kernel. Prove dimension at most \(N^{21}\) and squared ratio \((17/16)^k\).

**Why sufficient.** T1 gives a constant semantic gap, T2–T3 rule out affine and entangled shortcuts, and T4 amplifies it to \(n^{1/1000}\).

**Crux.** T3 is stronger than ordinary E-type: it must survive affine targets and semantic contractions.

**First experiment.** Synthesize COPY signatures compatible with the rank-8 NAND survivor, homogenize the smallest pair, and exactly enumerate the tensor square. Check whether every shortest adverse vector is a pure tensor with homogenizing coordinates \(\pm1\).

---

# Complete obstruction check

- **RS slack (G1), radix kernel (G7):** no free slack or residual-only amplification.
- **Affine isolation/overlap (G2–3, G5), invalid quotient (G6):** Q3/M1–M4/T1 quantify over emitted unrestricted fibers; no external filters.
- **Parity and affine-span kernels (G9, G11, G13, G15, G32, G37):** Q1–Q3 use nonlinear ideal defects; M1 uses full Möbius coordinates; T1 forbids the fiber exactly.
- **Fingerprint/DROP (G12; goal G8):** explicitly included in Q1, M2, and T1.
- **Pair/splitter finite passes (G14, G38):** M-strategy supplies the missing scaling and universal Graver theorem; Q/T do not rely on them.
- **Signed flow and diagonal splice (G19; goal G1):** avoided; Q3/M4 exclude corresponding Lawrence moves universally.
- **Failed recursion and seed isometry (G28, G30):** all routes require \(\lambda>\mu\); T1 additionally requires nonisometric seeds.
- **Walsh-only pass (G31):** not used as a hardness lemma.
- **Exterior completeness failures (G33–34):** exterior tags are avoided.
- **\(A_5\) bicyclic zero divisors (goal G2):** Q uses a division quaternion algebra; M/T use no group ring.
- **\(D_4\) midpoint/recombination (goal G3–5):** those coordinate-separable shells are avoided.
- **\(E_6\) affine-port no-go (goal G6–7):** ports are redundant/nonlinear, not affine shell maps.
- **Canonical quaternion grade-zero attack (goal G11):** Q starts from the redundant-signature survivor that removes that pseudosection.
- **Redundant-signature NAND survivor (goal G12):** used only as a seed; COPY and all-depth transfer remain explicitly open.

## Recommendation

Attempt **Strategy 1** first. Its **FRONTIER lemma is Q1**, specifically construction of a compatible COPY module with no false grade-zero fiber. The first experiment is the exact \(\mathcal O/P^2\) enumeration of length-\(8\)–\(12\) COPY signatures followed by depth-two Graver/valuation testing.
