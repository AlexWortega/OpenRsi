I treat the hash-locked G19 splice and its surviving diagonal embedding as mandatory seed attacks. These mechanisms either replace the killed linear pair lift or delimit the roadmap class in which FRONTIER could still hold.

### 1. Equivariant-diagonal no-go theorem — refute/amend

**Core trick.** Formalize a “linear coherent lift” as an additive, transition-relabeling-equivariant functor on layered flow modules. Try to prove that unary marginals plus honest-basis completeness force a chain map \(\Delta_k(s)\) carrying every integral accepting flow—including G19—into the lifted accepting fiber with only polynomial anchor excess.

**Expected move.** Refute FRONTIER for this whole natural class, amending Strategy 1 to require a demonstrably non-additive coefficient coercifier.

**Experiment.** On the smallest two-layer G19 support, symbolically enumerate equivariant row orbits for \(k=2\), solve for every admissible lift, and test whether \(\Delta_2\) necessarily exists. **Falsification:** one equivariant equal-radius lift with no such map.

**Obstruction audit.** G1: no slack. G2/G3: theorem covers all integers. G5: assumes complete tuple ports. G6: all rows emitted. G7: exact kernels are the subject. G9/G11/G12/G13/G15/G19: arbitrary parity, drop, affine, laminar, and splice flows are covered. G14/G38: no bag extrapolation. G28: no min-plus claim. G30: strictly broader than literal tensoring. G31: structural theorem, not finite extrapolation. G32/G37: additive parity is included. G33/G34: no exterior metric.  

**Likely death.** Naturality may be too strong; an asymmetric enlarged gadget can evade the theorem.

---

### 2. Coprime carry-branching coercifier — prove an amended FRONTIER

**Core trick.** Replace every transition coefficient \(x\) by simultaneous radix-2 and radix-3 decompositions, recursively encoding both carries. Canonical \(x\in\{0,1\}\) receives equal-radius complemented digits, while any other integer must create either an illegal residue or two nonzero descendant carries, potentially doubling defect mass per depth.

**Expected move.** Attach this tree before tuple coherence so each negative G19 coefficient incurs \((1+\epsilon)^k\) energy independently of residual kernels.

**Experiment.** Build the depth-3 scalar gadget and exactly minimize conditioned on \(x=-2,-1,0,1,2\); then attach it to the six non-Boolean coordinates of `diag(s)` and run unrestricted MILP. **Falsification:** a carry assignment whose bad/legal ratio fails to increase with depth.

**Obstruction audit.** G1: every residue and carry is norm-charged. G2/G3: scalar DP ranges over all \(\mathbb Z\). G5/G6: all carry ports/equalities are emitted. G7: zero residual still pays digit energy. G9/G11/G13/G15/G19: their non-Boolean coefficients are directly encoded. G12: zero/drop gets its canonical charged tree. G14/G38: no bag shell. G28: not the killed tile. G30: not tensoring. G31: requires a proved scalar induction. G32/G37 remain live—independent parity copies may preserve the ratio. G33/G34: no tag metric.

**Likely death.** Bad carries may terminate cheaply, or honest baseline may branch equally fast.

---

### 3. Nonabelian Fourier fusion over \(S_5\) — prove or refute

**Core trick.** At each balanced program segment, represent its endpoint product as an integral signed measure on \(S_5\). Glue children using complete \((g,h,gh)\) fusion selectors and measure energy in all irreducible Fourier blocks; honest delta measures have identical Plancherel radius.

**Expected move.** Find a rational potential proving that a virtual measure falsely concentrated on ACCEPT gains Fourier energy at each fusion, while an honest path remains a delta.

**Experiment.** Extract the smallest G19 splice-bearing subprogram, enumerate fusion coefficients in \([-2,2]\), compute exact rational \(S_5\) Fourier blocks, and LP-search for a \(>1\) adverse potential. **Falsification:** a bounded virtual measure fusing to ACCEPT at legal energy.

**Obstruction audit.** G1: fusion variables are charged, not free slack. G2/G3: eventual theorem must cover all integral measures; the box is only a falsifier. G5/G6: complete fusion ports are emitted. G7: Fourier-zero virtual measures remain a danger. G9/G11: parity measures are enumerated. G12: zero mass violates charged normalization. G13/G15/G19: affine and splice measures may still fuse—explicitly tested. G14/G38: no bag scaling. G28: different state algebra and potential. G30: fusion, not rank-one tensoring. G31: promotion requires a spectral theorem. G32/G37: compatible additive measures remain live. G33/G34: regular-representation geometry gives completeness directly.

**Likely death.** The representation ring may contain low-energy virtual units closed under fusion.

---

### 4. Integral cosystolic expansion — prove via topology

**Core trick.** Regard transition flows as relative integral \(1\)-chains and the G19 splice as a cycle. Replace each recursive layer by a bounded-degree \(2\)-complex whose emitted edge–face incidences force every non-honest relative cycle either to contain an honest accepting path or to have expanding integral coboundary norm.

**Expected move.** Turn FRONTIER into an integral cosystolic inequality iterated through \(k\) levels.

**Experiment.** Attach the smallest complete or computer-searched \(2\)-complex to the compressed G19 splice support; use Smith normal form to classify relative homology and MILP to find the shortest accepting cycle. **Falsification:** a zero-coboundary splice with cost below \(4R_2^2/3\).

**Obstruction audit.** G1: face coefficients are charged. G2/G3: SNF treats the full integer chain group. G5/G6: every incidence and boundary port is emitted. G7: residual kernels become explicit homology classes. G9/G11/G13/G15/G19: all are integral chains, not excluded by sign assumptions. G12: drops create boundary defects. G14/G38: no finite bag inference. G28: no min-plus tile. G30: no tensor rank assumption. G31: needs a uniform cosystolic theorem. G32/G37: disjoint parity cycles are a live threat. G33/G34: no exterior tags or repaired Gram.  

**Likely death.** Known expansion may hold only mod \(2\), while the integral splice is a cheap boundary with a small filling.

---

### 5. Graver-circuit fanout — prove using integer programming structure

**Core trick.** Compute primitive Graver circuits of the flow/query matrix and route every circuit through a bounded-degree expander of circuit ports. Seek a conformal-decomposition theorem forcing any non-honest accepting vector to activate many routed primitive circuits at the next level.

**Expected move.** Derive multiplicative energy from circuit fanout rather than tensor moments; an honest path has no circuit component.

**Experiment.** Orbit-compress the smallest G19 matrix, enumerate its Graver basis with `4ti2`, and MILP-synthesize a two-level routing matrix and rational potential. **Falsification:** G19 itself remains one primitive circuit with a one-port lift.

**Obstruction audit.** G1: decomposition/routing variables must all be norm-charged. G2/G3: Graver decomposition is unbounded and integral. G5/G6: complete circuit ports and equalities are emitted. G7: kernel vectors are precisely decomposed. G9/G11/G13/G15/G19: each harmful affine vector receives a circuit decomposition. G12: drops are additional primitive directions. G14/G38: no bag shell. G28: recurrence is circuit-theoretic, not the killed transfer table. G30: no literal tensor. G31: requires an all-level fanout proof. G32/G37: additive circuit copies may defeat strict growth and must be included. G33/G34: no metric synthesis.

**Likely death.** Graver decompositions are nonunique; unrestricted auxiliary variables may cancel, recreating G1, or G19 may already be indecomposable.

---

### 6. Noncommutative identity-testing fingerprints — prove or expose an identity

**Core trick.** Associate each transition word with a basis element of a truncated free algebra and propagate segment products through a balanced multiplication table. A deterministic noncommutative-ABP hitting family should detect any virtual accepting word polynomial that is not identically zero; regular-representation blocks give honest words equal norm.

**Expected move.** Show that the diagonal G19 splice has a nonzero polynomial fingerprint at every level, then amplify direct feature energy recursively.

**Experiment.** Reconstruct the splice’s signed path polynomial, evaluate it on all \(2\times2\) matrices with entries in \(\{-1,0,1\}\), and find the smallest separating family before compiling one depth-two multiplication gadget. **Falsification:** the splice polynomial is identically zero, or an unrestricted multiplication-table lift restores it at legal cost.

**Obstruction audit.** G1: fingerprints are direct coordinates, without slack. G2/G3: full soundness still needs all-integer multiplication selectors. G5/G6: complete product ports are emitted. G7: polynomial identities are the exact surviving kernel. G9/G11/G13/G15/G19: their signed path polynomials are explicitly tested. G12: drops alter the constant/normalization coefficient. G14/G38: no bags. G28: different algebraic recursion. G30: no rank-one premise. G31: requires a hitting theorem, not a finite pass. G32/G37: additive identities remain live. G33/G34: regular blocks avoid exterior completeness repair.

**Likely death.** The relevant virtual polynomial may be identically zero, or the truncated algebra may require exponential rank.

---

### 7. Proof-complexity pseudoexpectation attack — refute/amend

**Core trick.** Interpret ordered-\(k\) flow coordinates as degree-\(k\) linearized moments. Use high-girth unsatisfiable Tseitin/3XOR instances to seek normalized integral pseudoexpectations that satisfy every emitted tuple equation and claim ACCEPT, showing that bounded-degree coherence cannot imply amplification.

**Expected move.** Refute FRONTIER for all lifts whose rows are degree-\(k\) moment consequences, forcing the roadmap toward a nonlocal coercive gadget.

**Experiment.** Encode the smallest odd-charge cubic Tseitin graph of girth \(>4\), build the orbit-compressed \(k=2\) accepting system, use SNF to test integral solvability, then minimize anchor cost exactly. **Falsification:** the accepting fiber is empty over \(\mathbb Q\), or every integral point already exceeds \(16R_2^2/9\).

**Obstruction audit.** G1: no slack is introduced. G2/G3: SNF audits the entire fiber. G5/G6: all tuple ports and constraints are emitted. G7: exact kernels are the intended witness. G9/G11/G13/G15: parity/affine pseudodistributions are the mechanism, not ignored. G12: normalization forbids silent drops. G14/G38: asymptotics come from girth, not finite bags. G19: seeks an accepting signed flow directly. G28/G30: neither min-plus nor seed tensoring. G31: requires a family theorem. G32/G37: additive parity supports the attack. G33/G34: no geometric tags.

**Likely death.** Rational pseudoexpectations may not admit normalization-one integral lifts, or Barrington endpoint equations may exceed the claimed degree model.
