The supplied obstruction map is empty: `IDEAS.md` and `STATUS.md` contain no killed routes or proved obstructions. The checks below therefore address the stated campaign constraints directly.

### 1. Reed–Solomon spreading of integral residuals

**Mechanism.** Build an affine integer gadget whose residual vector \(r=(r_0,\ldots,r_{m-1})\) vanishes on a satisfying Boolean assignment. Replace \(r\) by evaluations of \(R(T)=\sum r_iT^i\) at \(N\) distinct integers; if \(r\neq0\), at least \(N-m+1\) coordinates are nonzero integers.

**Expected move.** Soundness norm becomes \(\Omega(\sqrt N)\) while Boolean anchoring costs \(O(\sqrt{n_0})\). With \(N=n_0^K\) and final dimension \(D=\Theta(N)\), this suggests a \(D^{(K-1)/(2K)}\) gap.

**Obstruction check.** No named proved obstructions or killed routes exist. Evaluation is deterministic, polynomial-sized for constant \(K\), unconditional, and not a PCP. It does assume a residual gadget robust against all non-Boolean integer vectors; that assumption is currently unproved.

**Falsification test.** Search for an integer vector that nearly satisfies the amplified equations by exploiting slack variables or non-Boolean values.

**Smallest experiment.** For padded 3-CNF \(F=(x)\land(\neg x)\), use \(r=(x-1,x)\), evaluate \(R\) at \(1,\ldots,8\), and enumerate \(x\in[-20,20]\), including a \(|x-\tfrac12|\) anchor.

**Likely death.** Non-Boolean lattice vectors satisfy the affine clause equations while paying only small anchoring cost.

*Ingredient: Reed–Solomon, 1960.*

---

### 2. Algebraic-number norm amplification

**Mechanism.** Pack residuals into an algebraic integer \(\alpha=\sum_i r_i\theta^i\) in a degree-\(d\) number field and include all archimedean embeddings. If \(\alpha\neq0\), its norm is a nonzero integer, so AM–GM gives \(\|\sigma(\alpha)\|_2\ge\sqrt d\).

**Expected move.** Choose \(d=n_0^K\); a satisfying assignment makes the entire embedding block zero, whereas any genuine integral residual contributes \(\sqrt d\). This again targets a polynomial gap in final dimension \(D\asymp d\).

**Obstruction check.** The map contains no proved obstruction. The construction is deterministic and unconditional once an explicit irreducible polynomial and certified rational approximation to its embeddings are supplied; it uses no verifier or PCP. It remains inside the vulnerable assumption that every unsatisfiable candidate produces \(\alpha\neq0\).

**Falsification test.** Measure whether embedding conditioning, approximation error, or large conjugates inflate completeness as fast as soundness.

**Smallest experiment.** In Sage, take \(\theta^4-\theta-1=0\), \(\alpha=(x-1)+x\theta\), enumerate \(x\in[-10,10]\), and compute the canonical-embedding norm with rigorous intervals.

**Likely death.** Converting irrational embeddings to a rational Euclidean lattice may require precision or coefficient size that destroys the promised gap; Boolean cheating remains.

*Ingredient: standard field norm/canonical embedding; e.g. Neukirch, 1999.*

---

### 3. Plücker rigidity instead of coordinatewise Boolean tests

**Mechanism.** Lift an assignment to its square-free monomial vector \(y_S=\prod_{i\in S}x_i\), making every 3-CNF clause residual linear in degree-\(\le3\) coordinates. Enforce that \(y\) is a genuine rank-one Boolean moment vector globally through vanishing \(2\times2\) minors—equivalently, Plücker/Segre relations—rather than weak independent anchors.

**Expected move.** Integer rank rigidity could force any fake lifted assignment to violate many minors; a subsequent deterministic code could turn that violation density into a polynomial Euclidean gap.

**Obstruction check.** There are no named obstructions or killed versions. The algebraic relations are explicit, deterministic, and PCP-free. However, minors are quadratic, while CVP supplies only linear lattice combinations and a quadratic norm; no valid linear realization is currently known.

**Falsification test.** Find low-norm integer pseudo-moment vectors satisfying all clause-linear equations but far from every Boolean rank-one vector while violating only one or two minors.

**Smallest experiment.** For three variables, enumerate \(y_S\in[-2,2]\) for \(|S|\le3\), impose the linearized clauses of a minimal unsatisfiable formula, and record the number and magnitude of failed identities \(y_Ay_B=y_{A\cap B}y_{A\cup B}\).

**Likely death.** Linearizing multiplication introduces new unconstrained variables recursively, recreating the original consistency problem.

*Ingredient: Segre varieties and Plücker relations; Harris, 1992.*

---

### 4. Homological obstruction with systolic product amplification

**Mechanism.** Encode variable choices as alternative integral chains and clauses as attached cells, arranging that a satisfying assignment gives a small filling of a target chain. For an unsatisfiable formula, the target should retain a nontrivial integral homology or torsion class; product the complex with explicit high-systole complexes so every representative of that class has large support.

**Expected move.** A \(K\)-fold product could raise a constant topological obstruction to support \(n_0^{\Omega(K)}\), while the boundary lattice and target remain polynomial-sized for constant \(K\).

**Obstruction check.** No topological route is killed in the supplied map. Boundary matrices are deterministic integer lattices, and Künneth/systolic arguments are unconditional and non-PCP. Exact boundary membership over a field is polynomial-time, so NP-hardness must reside in integrality, torsion, or nearest-chain geometry—not ordinary homology.

**Falsification test.** Check whether unsatisfiability actually survives as a homology class, rather than disappearing through unintended integer fillings.

**Smallest experiment.** Replace each variable by a 4-cycle with opposite truth chains, attach triangular clause faces, construct the face-edge boundary matrix for \((x)\land(\neg x)\), and brute-force coefficients in \(\{-1,0,1\}\). Then tensor with a cycle \(C_3\) and compare distances.

**Likely death.** Topology linearizes the choice constraints so thoroughly that the resulting obstruction becomes polynomial-time computable and cannot encode SAT.

*Ingredient: Künneth formula and cellular homology; Hatcher, 2002.*

---

### 5. Compressed Nullstellensatz duality

**Mechanism.** View Booleanity and clause satisfaction as an integer polynomial system. Unsatisfiability yields a Nullstellensatz identity \(1=\sum_i A_i f_i\); build a convolution/Hankel lattice in which a too-close vector would annihilate every \(f_i\), contradicting the identity without explicitly outputting its multipliers.

**Expected move.** Compress monomial multiplication using arithmetic-circuit or structured Toeplitz representations, hoping to retain the force of degree-\(n\) certificates in only polynomial dimension. The certificate then serves solely in the soundness proof.

**Obstruction check.** No proof-complexity route appears in the map. The mechanism is deterministic, unconditional, and not PCP-based. Known effective Nullstellensatz bounds permit exponential degree/size, so polynomial compression is an additional—and highly suspect—requirement.

**Falsification test.** Determine whether any proposed compressed multiplication operator admits pseudo-solutions that satisfy the represented moments but not the full polynomial identity.

**Smallest experiment.** Use Sage/Singular on unsatisfiable formulas with \(n=3,4\); compute Gröbner/Nullstellensatz certificates, form their multiplication matrices, and compare full rank with Kronecker, Toeplitz, and modular compressions.

**Likely death.** Uniform polynomial compression would amount to an unexpectedly strong proof-system simulation; collisions between omitted monomials probably create short cheating vectors.

*Ingredient: effective Nullstellensatz; Brownawell, 1987.*

---

### 6. Tensor-network realization of the clause partition function

**Mechanism.** Regard each clause as a constant-size Boolean tensor and contract shared variable indices. The resulting tensor network has a nonzero basis contribution exactly when a satisfying assignment exists; seek a lattice gadget whose short vectors are rank-one integral boundary conditions and whose distance measures the contraction defect.

**Expected move.** Use direct powers or singular-value amplification of the local tensors: a zero contraction remains zero, while a surviving rank-one contribution becomes spectrally isolated. Constant bond dimension plus a balanced contraction tree might yield polynomial dimension.

**Obstruction check.** No tensor-network obstruction is listed. All tensors can be explicit integers, so the route is deterministic and unconditional; it is not inherently a PCP. General formula incidence graphs have unbounded treewidth, however, and exact polynomial-size contraction would already solve the hard part.

**Falsification test.** Search for low-rank or signed tensor combinations that mimic a rank-one assignment and cancel all clause defects despite no satisfying basis state.

**Smallest experiment.** Construct clause tensors for a two-variable contradictory formula, flatten the network across every cut, compute exact singular values, and enumerate integer rank-two boundary tensors with coefficients in \(\{-1,0,1\}\).

**Likely death.** Bond dimension grows exponentially with treewidth, while allowing signed superpositions introduces cancellations unavailable to actual assignments.

*Ingredient: tensor contraction and matrix-product representations; Fannes–Nachtergaele–Werner, 1992.*

---

### 7. Multi-prime \(p\)-adic rigidity compiled into Euclidean blocks

**Mechanism.** Test each integral constraint modulo many explicit small primes, representing balanced residues through Construction-A-style lattice blocks. A bounded nonzero integer is divisible by only a limited number of those primes, so it is detected in most blocks; geometric weighting can also identify its first nonzero \(p\)-adic scale.

**Expected move.** With \(L=n_0^K\) prime blocks, every genuine bounded residual contributes \(\Omega(\sqrt L)\), while zero residual contributes nothing. A closeness hypothesis would first bound all candidate coefficients, making the product-of-primes argument applicable.

**Obstruction check.** The map contains no modular or divisibility obstruction. Prime generation and residue lattices are deterministic, polynomial-time, unconditional, and PCP-free. The unresolved assumption is that closeness bounds the relevant hidden residuals before modular wraparound is analyzed.

**Falsification test.** Search for large lattice coefficients that are inexpensive in the anchoring coordinates but make every residual divisible by the selected prime product.

**Smallest experiment.** For \(r=(x-1,x)\), use primes \(2,3,5,7\); compute balanced residues and the Boolean anchor for \(x\in[-10^4,10^4]\). Repeat with explicit slack variables and enumerate them jointly.

**Likely death.** Chinese-remainder multiples or correlated slack directions may hide all modular defects without incurring comparable Euclidean cost; preventing that may require exponentially large weights.

*Ingredient: Chinese remainder theorem and Construction A; Conway–Sloane, 1988.*
