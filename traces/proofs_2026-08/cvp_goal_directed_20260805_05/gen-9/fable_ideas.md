Below are six independent frontier attacks. None reuses a killed route unchanged.

### 1. Disjoint-union dilution no-go

**Mechanism.** Test whether the FRONTIER statement is impossible for any local, additive lift. Pad one unsatisfiable sheaf \(U\) by \(k\) independent satisfiable controls \(S\); then
\[
\rho(U\sqcup S^k)=\frac{d_U^2+kR_S^2}{R_U^2+kR_S^2}\to1.
\]
A bounded-locality lift preserving disjoint unions has the same limit, contradicting multiplication by \(257/256\).

**Expected move.** Refute the lemma under its natural functorial interpretation, or force an amendment: amplify excess \(\rho-1\), require connected robustly-unsatisfiable inputs, or explicitly permit global nonlocal coupling.

**Obstruction audit.** This uses no slack/drop (G1/G6/G12/DROP), bounded-fiber inference (G2/G3/G14/G31), private overlap (G5), radix (G7), parity/affine lift (G9/G11/G13/G15), signed flow/diagonal closure (G19/GD1), min-plus/additive/splitter composition (G28/G32/G37/G38), tensoring (G30), exterior metrics (G33/G34), D4 triality/non-antipodal/recombination, E6 ports, or GD2 convolution. It is structural padding, independent of those assumptions.

**Experiment.** Form \(U=\) G38 obstruction and \(k=0,\dots,32\) copies of its control; apply each candidate depth-one lift and compare exact rational ratios.

**Likely death.** The intended lift may be globally coupled and not disjoint-union preserving; then the roadmap must state that missing property.

---

### 2. Totally-unimodular Hodge lift

**Mechanism.** Choose replacement complexes whose cut/cycle boundary matrices are totally unimodular. Prove that every integral disagreement has a conformal decomposition into primitive cut, cycle, and stalk-supported circuits; route each primitive circuit through enough expander edges that its charged norm grows while legal anchor energy grows by only \(\mu\).

**Expected move.** Prove the stated \(257/256\) inequality by an all-coefficient integral Hodge theorem, rather than extrapolating from a shell.

**Obstruction audit.** G1/G6/G12/DROP are emitted coordinates; G2/G3/G14/G31 are covered by conformal decomposition, not enumeration; G5 uses complete overlaps; G7 kernels become saturated cycle components. G9/G11/G13/G15 and G19/GD1 are explicit primitive circuits. G28/G32/G37/G38 supply no composition inference; G38 is only input data. There is no G30 tensor, G33/G34 exterior metric, D4 shell, E6 port, or GD2 convolution.

**Experiment.** Enumerate connected bipartite degree-\(\le4\) replacements on at most eight vertices; retain those with TU boundary matrices. For each, compute SNF, Graver circuits, and exact G38 depth-two energies circuit-by-circuit.

**Falsification.** One primitive saturated cycle has growth at most legal growth, or the needed boundary matrix is not TU.

**Likely death.** Harmonic signed cycles may remain invisible to every cut charge.

---

### 3. Multiscale residue-and-carry lift

**Mechanism.** First embed complete bag labels into degree-two Teichmüller-style coordinates, then measure the saturated disagreement quotient modulo several small primes. Every carry is itself emitted at the next scale: a defect either has a distant nonzero residue codeword or is divisible by the prime product, forcing large ordinary integer norm.

**Expected move.** Prove \(257/256\) growth through a finite residue-distance inequality plus an archimedean divisibility bound.

**Obstruction audit.** Emitted carries handle G1/G6/G12/DROP. SNF quotient coordinates address G2/G3/G14/G31 and complete overlaps avoid G5. Unlike G7, carries are charged recursively rather than discarded. G9/G11/G13/G15 are **not outside the assumptions**: the nonlinear degree-two embedding must separate them, and failure does kill the route. G19/GD1 are tested as signed quotient classes. No G28/G32/G37 additive inference, G30 tensor, G33/G34 exterior repair, D4/E6 shell, or GD2 convolution is used; G38 is only the seed.

**Experiment.** On the twelve G38 bags, use primes \(2,3,5\), enumerate quadratic label embeddings of dimension at most 32, and compute depth-two minima plus SNF at every carry level.

**Falsification.** Any G13/G15 affine pseudosection remains zero in every residue layer.

**Likely death.** Exact integral affine collisions may survive every finite-prime checksum.

---

### 4. Signed log-Sobolev amplifier

**Mechanism.** Regard each unrestricted stalk vector as a signed measure; its centered anchor norm is a \(\chi^2\)-type energy. Apply an explicit two-step expander noise operator to complete overlap marginals and prove a log-Sobolev/Poincaré inequality directly on the saturated signed augmentation module, not merely on probability distributions.

**Expected move.** Show that nonconstant signed mass contracts by a factor below \(256/257\), while constants are exactly the canonical honest lifts.

**Obstruction audit.** G1/G6/G12/DROP are separate charged mass sectors; the Hilbert-space inequality is unbounded, covering G2/G3/G14/G31. Complete conditional marginals avoid G5; G7 is included as the zero-residual augmentation kernel. G9/G11/G13/G15 and G19/GD1 are not excluded—they must satisfy the signed inequality. No finite min-plus or additive claim (G28/G32/G37/G38), tensor (G30), exterior metric (G33/G34), D4/E6 shell, or GD2 multiplication occurs.

**Experiment.** Construct the exact quadratic forms for each degree-\(\le4\), eight-vertex replacement of G38. On the SNF-saturated augmentation quotient, compute the smallest generalized eigenvalue and separately enumerate its integral equality cases.

**Falsification.** A parity or signed-cycle vector lies in a zero/no-growth eigenspace.

**Likely death.** Real spectral expansion may coexist with an integral harmonic submodule carrying the minimum.

---

### 5. Toric normalization and Markov-basis charging

**Mechanism.** Model compatible bag marginals as an affine semigroup. Replace each stalk by a constant-size normal toric extension and compute its primitive binomial/Graver moves; add emitted coordinates charging every move, so any integral pseudosection is reduced conformally to honest sections or pays on an expander-density set.

**Expected move.** Convert the FRONTIER lemma into normality plus a quantitative lower bound for primitive Markov moves under lifting.

**Obstruction audit.** Normalization/drop generators explicitly cover G1/G6/G12/DROP. A complete Markov basis is an all-fiber statement, addressing G2/G3/G14/G31; full marginal semigroups avoid G5. G7 kernels and G9/G11/G13/G15 affine attacks become named binomial moves, not assumed absent. G19/GD1 require signed conformal decomposition. No G28/G32/G37 recurrence, G30 tensor, G33/G34 exterior metric, D4 shell, E6 port, or GD2 group ring appears; G38 only supplies the semigroup.

**Experiment.** Build the incidence semigroup of the twelve G38 bags; use Normaliz/4ti2 or a small custom enumeration to find holes and primitive moves through degree eight. Add one coordinate orbit per move and recompute depth-two minima.

**Falsification.** A semigroup hole or Markov cycle lifts with zero charge, or the Markov degree is unbounded.

**Likely death.** Marginal semigroups are often nonnormal, and completing them may exceed the \(4096\) rank factor.

---

### 6. Finite-cover monodromy lift

**Mechanism.** Put a finite-group voltage on each label-compatible overlap and replace every selector by a regular-representation fiber. Honest sections have trivial holonomy and canonical lifts; inconsistent cycles acquire nontrivial monodromy, whose augmentation representation has an exactly computable spectral gap.

**Expected move.** Prove the cycle-space part of FRONTIER via finite-cover holonomy, while cuts and drops are charged conventionally.

**Obstruction audit.** G1/G6/G12/DROP remain emitted scalar sectors; representation decomposition handles all coefficients, addressing G2/G3/G14/G31. Voltages use complete overlaps, not G5 private rows; G7 kernels become holonomy cycles. G9/G11/G13/G15 and G19/GD1 must have nontrivial action and are explicit tests. This is neither G28/G32/G37 composition nor G30 tensor, G33/G34 exterior geometry, or D4/E6 shell geometry. GD2 remains relevant as an attack, but there is no convolution/fusion product—only permutation action. G38 is the seed.

**Experiment.** Enumerate voltage assignments into \(S_3,A_4,A_5\) on the G38 overlap graph, quotienting by gauge equivalence. Compute exact augmentation spectra, SNF, and depth-two minima for DROP, affine, signed-cycle, and unrestricted low-energy states.

**Falsification.** A harmful cycle has trivial holonomy or supports an invariant signed vector.

**Likely death.** Different bad cycles may cancel their voltages, while constant-on-orbit signed coefficients bypass the spectral charge.
