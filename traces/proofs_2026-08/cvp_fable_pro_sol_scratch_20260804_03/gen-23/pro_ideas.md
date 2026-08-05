Fresh mechanisms only; none is promoted beyond executable falsification.

### 1. Objective-aware Chvátal–Gomory closure
**Mechanism.** Replace free clause slack by bounded-value one-hot slack, then append every rank-\(r\), coefficient-\(\le L\) Chvátal–Gomory cut valid for each clause/overlap Boolean polytope. Emit each cut as an equality with a bounded slack selector, targeting a polynomial-size closure whose exact integer fiber equals the Boolean fiber.

**Expected move.** If the exact unsatisfiable fiber disappears, polynomially scale residual coordinates to obtain the gap.

**Obstruction audit.** G1 slack-RS: no free slack or evaluations. G2 bounded isolation/G3 unbounded audit: not reused. G5 overlap circuits: cuts include overlaps. G6 external filters: every row/selector is emitted. G7 radix, G9 quadratic moments, G11 cubic moments: absent. G12 drop: drop faces are included. G13 affine collision/G15 hierarchy lift: **not escaped automatically**; primary test. G14 pair bags and G19 flow: absent. G20/G21 baseline scaling: conditional on polynomial rank. G22 underspecification: \(r,L\), slack ranges, and rows are frozen.

**Falsification.** Any \(B+O(1)\) zero-residual affine pseudosection.

**Experiment.** On the eight-clause obstruction, enumerate rank-\(\le2\) cuts on one- and two-clause polytopes; exact-search through \(B+32\).

**Likely death.** Required rank becomes linear, or signed slack selectors recreate G13.

---

### 2. Quadratic discriminant-form gluing
**Mechanism.** Assign each legal local label a shortest representative of a coset in the discriminant group \(K^*/K\) of an even lattice; glue occurrences through isotropic subgroups. Unlike a linear syndrome, the discriminant quadratic form \(q(x)=\|x\|^2\bmod 2\mathbb Z\) can charge two representatives having the same additive boundary.

**Expected move.** Find a block whose legal cosets have equal minima while every inconsistent glued coset has a multiplicatively larger minimum; recurse by orthogonal gluing.

**Obstruction audit.** G1: no slack/RS. G2/G3: no local affine-isolation claim. G5: gluing is via discriminant cosets, not private rows. G6: full lattice and target are emitted. G7: no radix. G9/G11: no moment equalities. G12: zero/drop is an audited coset. G13/G15: linear affine cancellation need not preserve \(q\), but may still yield a short representative—unresolved. G14: no pair-bag lift. G19: no flow. G20/G21: requires a gluing ratio exceeding baseline growth. G22: nonlinear quadratic refinement is the proposed new rigidity.

**Falsification.** The G13 combination occupies a legal-minimum coset, or a drop coset is shorter.

**Experiment.** Search \(A_1^k,D_4\), and small Construction-A lattices for eight equal-radius legal cosets; glue two overlapping clauses and enumerate every coset minimum.

**Likely death.** Isotropic affine combinations remain short under every feasible gluing.

---

### 3. Hurwitz-quaternion norm composition
**Mechanism.** Compile the formula into a balanced reversible gate tree and encode legal wire states by Hurwitz units. Gate tables select products \(uv=w\); the four-square identity \(\|uv\|^2=\|u\|^2\|v\|^2\) is intended to turn a local illegal correction into multiplicative norm growth across depth.

**Expected move.** Depth \(\Theta(\log n)\) with illegal multiplier \(C\) larger than honest gate-size growth \(S\) would yield \(n^{\log(C/S)}\) separation.

**Obstruction audit.** G1: no residual slack. G2/G3: unrelated. G5: composition is multiplicative, not private-row overlap. G6: all product selectors and rows are emitted. G7: no radix. G9/G11: no moments. G12: include zero and omitted-gate states in the table. G13/G15: affine combinations of complete lifted computations can still thread linear table rows; norm composition applies only to decomposable products, so this is **not yet escaped**. G14: no pair bags. G19: signed gate splicing remains possible. G20/G21: explicitly tested by \(C>S\). G22: the decomposability objection remains the central gate.

**Falsification.** A nondecomposable signed product selector of constant excess.

**Experiment.** Emit two quaternion product gates over the 24 Hurwitz units; enumerate all zero-residual states through honest baseline \(+32\), then compose two copies.

**Likely death.** Linearized multiplication admits cheap signed tensors where the norm identity is irrelevant.

---

### 4. Redundant \(p\)-adic carry cascade
**Mechanism.** Encode one assignment simultaneously as signed-digit streams in bases \(2,3,5\), sharing carries across clause-checking automata and between forward and reversed scans. Exact acceptance in an unsatisfiable instance should force a nonzero carry divisible by \(30^d\), whose ordinary Euclidean coordinate is exponentially large.

**Expected move.** With \(d=\Theta(\log n)\), carry magnitude supplies a polynomial distance gap while the honest digits remain \(0/1\).

**Obstruction audit.** G1 slack-RS: carries are shared and norm-penalized, not free clause slack, though the same failure is possible. G2/G3: unused. G5: scans are global. G6: carries and automata are emitted. G7: this enforces digit dynamics rather than radix-encoding residuals; exact zero kernels remain a threat. G9/G11: no moments. G12: dropped scans violate boundary rows. G13/G15: affine lifts may carry-combine exactly—unresolved. G14: no pair bags. G19: signed automaton splicing is directly relevant. G20/G21: \(30^d\) versus \(O(d)\) is the proposed scaling law. G22: every base, carry range, row, and weight must be frozen.

**Falsification.** Any accepting zero-residual trajectory with all carries in \(\{-1,0,1\}\).

**Experiment.** Build a 24-step repeated-variable checker for the eight-clause obstruction in bases \(2,3\); exact-search depths \(d=1,2,3\) through excess 32.

**Likely death.** Opposite-base carries cancel, reproducing a G19-style signed splice.

---

### 5. Native Voronoi amplifier gadget
**Mechanism.** Search directly for a small lattice with designated port cosets: every legal port has distance \(R\), while every unrestricted lattice point realizing an illegal boundary has distance at least \(\alpha R\). Glue gadgets by lattice fiber products and demand a finite transformer contract \(\alpha/\sqrt S>1\), where \(S\) is the honest squared-radius blowup.

**Expected move.** Recursive substitution then gives a polynomial gap without selector residual amplification.

**Obstruction audit.** G1: no slack. G2/G3: no affine-isolation assumption. G5: all boundary classes, not fixed marginals, enter the contract. G6: lattice, target, and gluing are explicit. G7: no residual kernel/radix. G9/G11: not a moment metric. G12: drops are illegal port classes. G13/G15: a proved contract quantifies over their unrestricted affine lifts rather than trying to hash them. G14: not fixed pair bags. G19: no flow. G20/G21: \(\alpha/\sqrt S>1\) is exactly the missing scaling test. G22: supplies the previously missing legal/illegal ports and composition contract.

**Falsification.** Two individually valid gadgets glue to a short illegal vector, or necessarily \(\alpha\le\sqrt S\).

**Experiment.** Enumerate positive-definite integral Gram matrices of dimension \(4\!-\!7\) with entries \([-2,2]\); compute port-coset minima and all two-gadget gluings exactly.

**Likely death.** Convexity or transference bounds forbid an amplifying ratio.

---

### 6. Uncentered Magnus-signature flow
**Mechanism.** Replace G19’s half-integral anchor on every edge by uncentered cost \(\|z\|^2+M\|Az-b\|^2\), so an honest path costs its length rather than the total number of columns. Refine each branching-program state by a degree-\(d\) truncated noncommutative Magnus signature of its transition word; signed splicing should require support across many refined states.

**Expected move.** For constant transition alphabet and \(d=\Theta(\log n)\), obtain polynomial signature dimension and prove every accepting signed flow has support \(L n^{2c}\), versus honest cost \(L\).

**Obstruction audit.** G1: no slack. G2/G3/G5: no local isolation or private overlap. G6: source, sink, repeated-query, and signature rows are emitted. G7: no radix. G9/G11: no moments. G12: dropping flow pays the scaled source/sink residual. G13/G15: affine combinations may still thread the refinement. G14: no bags. G19 signed flow: **not outside it**; changed norm and refined state are the precise mutation. G20/G21: uncentered cost removes total-column baseline inflation. G22: full truncated signatures replace the rejected exterior-square sketch, but transport remains linear and must be searched.

**Falsification.** A degree-\(d\) accepting splice with \(O(1)\) extra support.

**Experiment.** Modify the 24-layer repeated-query obstruction; compare exact minima for \(d=0,1,2,3\) through honest cost \(+32\).

**Likely death.** Signed flow lifts coherently to every finite signature degree.

Classical ingredients: Schrijver, *Theory of Linear and Integer Programming* (1986); Conway–Sloane, *Sphere Packings, Lattices and Groups*, 3rd ed. (1999); Magnus–Karrass–Solitar, *Combinatorial Group Theory* (1966); Hurwitz’s four-square norm composition.
