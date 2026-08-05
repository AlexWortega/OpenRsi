No present chain is complete; each hinges on one explicit new soundness lemma. The routes below avoid PCP composition and use only deterministic combinatorial/algebraic constructions. Classical ingredients allowed here include Cook–Levin tableau encodings, deterministic splitters/perfect hash families (Naor–Schulman–Srinivasan, 1995), expander-code ideas (Sipser–Spielman, 1996), and standard Smith/Graver-basis algorithms.

## Strategy 1 — Asymmetric finite-state min-plus amplifier

### Lemma chain

**A1. Constant-alphabet computation tiles.**  
Given a 3CNF \(F\) of size \(M\), deterministically construct \(O(M)\) constant-size tiles with finite boundary alphabet \(\Sigma\), such that globally legal boundary states correspond exactly to Boolean assignments and the distinguished terminal port is ACCEPT iff the assignment satisfies \(F\).

**A2. Exact integral transfer representation.**  
For each tile, emit an integral CVP factor and target whose transfer table
\[
E_T(p,q)=\min_{z\in\mathbb Z^{r_T}}\|C_Tz-y_T\|_2^2
\]
is finite-state complete: every unrestricted integral vector belongs to a recorded port class—LEGAL, ILLEGAL, DROP, or MALFORMED—and gluing tiles corresponds exactly to min-plus convolution of these tables.

**A3. Asymmetric amplifier tile.**  
Exhibit one fixed tile \(A\), constants \(a,\mu,\lambda\), and a complete unrestricted transfer table such that:

1. composing with \(A\) multiplies every legal cost by at most \(\mu\);
2. every state carrying an ILLEGAL, DROP, or MALFORMED marker costs at least \(\lambda\) times its previous adverse cost;
3. \(\lambda>\mu\);
4. the composed rank grows by at most factor \(a\);
5. the terminal marker prevents any coefficient/row permutation from exchanging legal and illegal seeds.

**A4. Iterated gap lemma.**  
At depth \(k\), YES distance squared is at most \(B\mu^k\), while NO distance squared is at least \(B\lambda^k\). Taking \(k=\lceil\log_a M\rceil\) gives final dimension \(n=O(M^2)\) and distance ratio at least
\[
n^{c_A},\qquad c_A=\frac{\log(\lambda/\mu)}{4\log a}>0.
\]

**A5. CVP emission.**  
Clear denominators and output the recursively glued basis and target directly. All entries have polynomial bit length, so this is a deterministic polynomial-time many-one reduction.

### Why this suffices
A1–A2 encode SAT with no external restrictions; A3 supplies the missing multiplicative asymmetry; A4 yields a polynomial factor; A5 gives an ordinary Euclidean GapCVP instance.

### Crux
A3: finding a fixed amplifier whose inequality holds for the **complete unrestricted integer transfer table**, not merely selected attacks.

### First experiment
Enumerate asymmetric rank-\(\le 12\) tiles with two-bit ports and one distinguished terminal coordinate. For each candidate, compute exact depth-one and depth-two min-plus tables over the full coefficient shell implied by the anchor eigenvalue. Reject unless closure holds and
\[
\lambda/\mu>1
\]
for every nonlegal class. Also run canonical colored-graph isomorphism to exclude a G30-type seed isometry.

### Obstruction-map check
- **G1 RS residual spreading** and **G7 multi-order radix:** no residual-only amplification or free slack.
- **G2/G3 affine isolation** and **G5 private-row overlap:** A2 records all freed boundary states; it does not assume fixed marginals.
- **G6 quotient gate:** no external filters or changed references.
- **G9 degree-two PSD, G11 cubic moments, G12 spherical fingerprint, G13 affine collision:** affine/parity vectors are explicit adverse port classes, not presumed detectable by moments or compatible hashes.
- **G14 pair bags, G15 laminar hierarchy, G38 splitter bags:** no fixed-level bag argument.
- **G19 Barrington flow:** no signed-flow encoding.
- **G28 frozen pair-tile recursion:** A3 requires the opposite strict inequality and a complete-state certificate.
- **G30 literal tensor:** composition is asymmetric min-plus gluing, not Kronecker tensoring.
- **G31 Walsh Gram, G32 cross-copy moments, G37 two-level metric:** no additive orthogonal-copy metric.
- **G33 exterior bivectors/G34 metric repair:** no exterior tags or cosphericity requirement.

---

## Strategy 2 — Logarithmic bags with an integral cosystolic inequality

### Lemma chain

**B1. Deterministic logarithmic bag complex.**  
For every 3CNF \(F\) with \(M\) clauses, construct \(O(M^d)\) bags, each containing at most \(q=K\log M\) variables/clauses, using deterministic splitters and a constant-degree overlap graph. Each bag has coordinates only for assignments satisfying all clauses in that bag. Total selector count is \(M^{O(K)}\).

**B2. Exact completeness.**  
Every satisfying assignment induces one-hot selectors in every bag, satisfying all normalization and complete-overlap marginal equations, at a common squared anchor radius \(B\).

**B3. Integral cosystolic soundness.**  
For explicit \(\delta>0\) and polynomial row weight \(W\), every unrestricted integral selector family for an unsatisfiable \(F\) obeys
\[
\operatorname{Anchor}(z)+W\|Az-b\|_2^2\ge B\,M^{2\delta}.
\]
The theorem must cover zero-residual affine pseudodistributions, clause drops, and arbitrary signed coefficients—not only bounded-support deviations. Its proof should use a direct expansion/unique-continuation argument over \(\mathbb Z\), not a PCP or gap-CSP theorem.

**B4. Lattice realization and exponent.**  
Use factor \([\,2I;\sqrt W A\,]\), replicating rows if necessary to keep it integral. If \(n\le M^D\), B2–B3 give approximation factor
\[
M^\delta\ge n^{\delta/D}.
\]

### Why this suffices
B2 supplies a universal YES radius, while B3 directly establishes the NO radius for all lattice vectors. B1 and B4 ensure deterministic polynomial size.

### Crux
B3: proving that a sparse nonlaminar logarithmic-bag complex has polynomial **integral** cosystole, rather than merely local consistency or real/rational agreement.

### First experiment
Take the G38 nine-clause obstruction and form two and three overlapping copies on an explicit 3-regular clause-overlap graph. Build \(q=4,5,6\) splitter bags and solve the exact MIQP
\[
\min_{z\in\mathbb Z^N}\|2z-1\|^2+W\|Az-b\|^2
\]
using certified coefficient bounds. Measure whether normalized excess grows superadditively and extract every zero-residual affine kernel by Smith normal form.

### Obstruction-map check
- **G1/G7:** no slack or radix residual spreading.
- **G2/G3/G5:** no private local hash; full overlaps enter one global complex.
- **G6:** normalization and consistency are emitted coordinates.
- **G9/G11/G12/G13:** B3 explicitly quantifies over parity and honest-affine-span collisions.
- **G14:** logarithmic bags replace fixed pair bags.
- **G15:** overlap graph is nonlaminar, and B3 must exclude affine lifts through all levels.
- **G19:** no flow linearization.
- **G28/G30:** no frozen recursion or tensor seed.
- **G31/G32/G37:** soundness is a global integral cosystole, not additive Walsh/moment energy.
- **G33/G34:** no exterior geometry.
- **G38:** this is its intended escape: asymptotic logarithmic bags plus a proved scaling inequality, not a finite \(B+64\) shell.

---

## Strategy 3 — Graver-growth lift for signed pseudoproofs

### Lemma chain

**C1. One-hot Tanner tableau.**  
Convert \(F\) into a constant-degree factor graph whose local coordinates are legal gate/clause configurations. Honest satisfying tableaux are globally consistent one-hot vectors of squared radius \(B_0=\Theta(M)\).

**C2. Fixed integral lift with Graver expansion.**  
Construct an explicit constant-size lift \(L\) with coordinate growth \(a\) and constant \(\rho>\sqrt a\) such that, after \(k\) lifts, every normalized exact-consistency integer vector that is not a Boolean tableau has anchor excess at least
\[
B_0\rho^{2k}.
\]
The statement must include all integer kernel vectors and must remain true under arbitrary factor-graph overlaps.

**C3. Nonzero-residual branch.**  
Replicate every emitted consistency row \(R=\Theta(B_0\rho^{2k})\) times. Thus any nonzero integral residual costs at least the C2 lower bound, while YES vectors retain zero residual.

**C4. Polynomial gap.**  
With \(k=\lceil\log_a M\rceil\), dimension is \(n=O(Ma^k)=O(M^2)\), while the distance ratio is at least
\[
M^{\log_a(\rho/\sqrt a)}
 \ge n^{c_C},\qquad
c_C=\tfrac12\log_a(\rho/\sqrt a)>0.
\]

### Crux and first experiment
The frontier is C2. Enumerate small non-unimodular two-lifts of the 18 G3 local survivors, compose them on every one- and two-variable overlap, and compute exact Graver bases through depth three. Accept only if the minimum harmful \(\ell_2\)-norm grows by factor \(\rho>\sqrt a\) at every depth and no zero-cost affine lift appears.

### Obstruction-map check
C2 explicitly repairs **G2/G3/G5** by requiring overlap-stable Graver growth. Anchored carries avoid **G1**, and complete kernel enumeration avoids **G7**. All rows are emitted, avoiding **G6**. The theorem quantifies over **G9/G11 parity**, **G12 drops**, **G13 affine collisions**, **G15 lifts**, and **G19 signed splicing**. It uses neither **G14/G38 bags**, **G28 min-plus recursion**, **G30 tensors**, **G31/G32/G37 additive metrics**, nor **G33/G34 exterior tags**.

## Recommendation

Attempt **Strategy 1 first**: it has the cleanest finite falsification gate and, if successful, the shortest path to an explicit exponent.

**FRONTIER lemma:** A3, the asymmetric complete-state amplifier with \(\lambda>\mu\).

**First experiment:** exhaustive exact search of asymmetric rank-\(\le12\) tiles, computing complete depth-one/depth-two transfer tables and rejecting any candidate with nonclosure, \(\lambda\le\mu\), or a legal/illegal seed isometry.
