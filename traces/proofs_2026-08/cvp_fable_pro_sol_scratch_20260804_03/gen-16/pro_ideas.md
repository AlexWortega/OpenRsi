## Generation 16 — Divergent mechanism sketches

### 1. Delaunay-cell gluing
**Mechanism.** Synthesize a rational positive-definite form whose empty Delaunay sphere contains exactly the legal one-hot states of a clause gadget; every signed local mixture lies strictly outside. Glue constant-size cells over a bounded-degree expander using shared Schur-complement cross-terms rather than private equality rows.

**Expected move.** Obtain a uniform forbidden-shell margin surviving overlap, which could later support amplification.

**Obstruction audit.** G1 RS slack: no slack polynomial. G2/3 affine isolation: quadratic separation, not fiber inconsistency. G5 private-row overlap: cross-terms are global. G6 gate: emit one unrestricted Gram matrix and target. G7 radix: zero residual may still lie outside the sphere. G9 fixed PSD and G11 moments: search unrestricted perfect forms, with parity included adversarially. G12 fingerprint/drop: all drops become explicit sphere constraints. G13 affine collision: no same-target syndrome, though mixtures could still move inward. G14 pair bags: constant cells, not a complete pair mesh. G15 hierarchy: no growing assignment scopes; affine lifts are tested directly.

**Falsification.** Parity lies on/inside every feasible sphere, or overlap destroys the margin.

**Smallest experiment.** SDP-synthesize \(Q\) on the nine-clause obstruction and control, rationalize it, then exactly enumerate through \(4B/3\).

**Likely death.** Convexity makes an honest affine combination closer to the center.

---

### 2. Constant-scope arithmetic-circuit/toric lift
**Mechanism.** Compile Booleanity, clause violation, and aggregation into fan-in-two gates, representing each gate by one-hot truth-table selectors with linear marginal gluing. Apply algebraic-number evaluations to the final nonzero aggregate; this uses the classical toric-ideal viewpoint (Sturmfels, 1996) but keeps all scopes constant.

**Expected move.** Prove that every zero-output integral gate pseudowitness has polynomial anchor excess; otherwise scale the nonzero output coordinates.

**Obstruction audit.** G1 slack: Boolean and gate selectors are charged, not free slack. G2/3: enlarged circuit fibers replace local isolation. G5: gates share actual wires globally. G6: all selectors and checks enter CVP. G7: evaluations follow the computed output, not raw residuals. G9/G11: not bounded-degree global moments. G12: dropped gates violate normalization and fan-out checks. G13: nonlinear enlarged encoding, although linear pseudocircuits may still realize its affine collision. G14: no pair mesh. G15: constant fan-in gives polynomial size, with no root assignment table.

**Falsification.** A cheap signed local-marginal pseudocircuit computes output zero.

**Smallest experiment.** Build the all-eight-clauses three-variable circuit; exact-search coefficients in \([-2,2]\), seeding G7/G11/G13 witnesses.

**Likely death.** Local truth-table consistency admits precisely the pseudodistributions already threading hierarchies.

---

### 3. Twisted cohomological defect amplification
**Mechanism.** Convert assignments into \(0\)-cochains on a bounded-dimensional complex and clause defects into a twisted cocycle. Arrange that satisfiable formulas give a coboundary, while unsatisfiability creates a nontrivial class; cosystolic expansion would force every representative to have large support. Classical candidate complexes include explicit high-dimensional expanders of Lubotzky–Samuels–Vishne (2005).

**Expected move.** Turn one unavoidable clause defect into \(\Omega(N)\) nonzero lattice coordinates, then scale those zero-on-completeness coordinates.

**Obstruction audit.** G1: no slack. G2/3 and G5: soundness is global homology, not local fibers/private rows. G6: emit the full boundary matrices and Construction-A blocks. G7: exact local cancellation does not erase a nontrivial class. G9/G11: no moment truncation. G12: drops create boundary. G13: not automatically escaped—linear affine lifts may still become cocycles; twisting must block them. G14: constant-dimensional faces replace pair bags. G15: polynomially many bounded faces, no exponential root scope.

**Falsification.** An unsatisfiable instance has a zero or \(O(1)\)-support twisted cocycle representative.

**Smallest experiment.** Attach triangles to the nine-clause incidence graph, enumerate twists over \(\mathbb F_2,\mathbb F_3\), and compute minimum cocycle support plus short integral lifts.

**Likely death.** Constructing the required robust complex from arbitrary 3SAT secretly requires a PCP-style gap transformation.

---

### 4. Canonical balanced-digit barrier
**Mechanism.** Give each selector redundant balanced-base representations for several primes, with every digit and carry explicitly anchored. Legal \(0/1\) values receive equal-radius canonical codewords; negative or multi-unit coefficients should require a long carry chain in at least one base.

**Expected move.** Establish that every vector near completeness projects to genuine \(0/1\) selectors; ordinary clause consistency can then be scaled heavily.

**Obstruction audit.** G1 slack: carries are anchored and cross-checked, not free. G2/3: legality comes from redundant digit uniqueness. G5: representations are shared per global wire. G6: no external range filters. G7 radix: digits encode selectors themselves, not a linear image of residuals, so zero raw residual is insufficient. G9/G11: no moments. G12: drops lose digit normalization. G13: enlarged nonlinear codewords, although the affine witness may admit a cheap digit lift. G14: no pair bags. G15: \(O(\log n)\) digits per selector, constant scopes, polynomial size.

**Falsification.** Lift `011+100−111` or the G13 parity with all carry equations exact and only constant excess.

**Smallest experiment.** Use bases \(3\) and \(5\), three digit levels, on the G7 nine-clause lattice; enumerate all digit/carry states through baseline \(+32\).

**Likely death.** Linear carry equations permit noncanonical signed representations whose anchor cost remains constant.

---

### 5. Mutually-unbiased Fourier-frame metric
**Mechanism.** Color clause occurrences and map each eight-label selector through different Walsh or finite-field Fourier projections. Legal one-hots have identical total energy, while uncertainty principles should make a vector concentrated as parity in one frame diffuse in another; drops excite every frame’s DC component. The relevant classical template is finite Fourier uncertainty (Donoho–Stark, 1989).

**Expected move.** Find a uniform frame schedule separating all low-anchor signed deviations; investigate tensor schedules for multiplicative separation.

**Obstruction audit.** G1: no slack. G2/3 and G5: overlap is coupled through noncommuting global frames. G6: the metric is an explicit rational PSD Gram form. G7: zero consistency residual can retain Fourier energy. G9: not the fixed two-parameter moment metric. G11: degree is irrelevant. G12: full frame families replace one top-Walsh tag and include drop constraints. G13: not fully outside—every zero-on-honest linear row still misses the affine collision; separation must come from equal-radius quadratic energy. G14: sparse occurrence frames, no complete pair mesh. G15: constant local dimension and polynomial schedule.

**Falsification.** Any G7/G11/G13/drop vector remains below the desired shell for every admissible frame coloring.

**Smallest experiment.** Enumerate occurrence colorings from three \(8\times8\) Walsh conjugates, optimize projection weights by SDP, then exact-shell search.

**Likely death.** Parseval conservation merely redistributes, rather than increases, the harmful energy.

---

### 6. Nonlinear Sidon/Reed–Solomon assignment lift
**Mechanism.** Encode the global variable string as one-hot symbols of a systematic Reed–Solomon code, then append a nonlinear constant-weight Sidon/superimposed-code fingerprint of each symbol block. Clause selectors read systematic coordinates; short signed combinations should either violate decoding consistency or acquire large fingerprint weight. Classical ingredients are Reed–Solomon codes (1960) and Kautz–Singleton superimposed codes (1964).

**Expected move.** Force every bounded-coefficient affine pseudowitness to occupy polynomially many auxiliary coordinates, while honest assignments retain equal radius.

**Obstruction audit.** G1: no slack. G2/3: distance replaces local affine isolation. G5: all clauses share one global codeword. G6: symbol selectors and checks are unrestricted CVP coordinates. G7: residual-zero local attacks need a global code lift. G9/G11: not moment consistency. G12: constant-weight decoding checks charge drops. G13: raw linear compatibility no longer applies to the nonlinear enlarged encoding, though a lifted affine collision may remain. G14: no quadratic pair mesh. G15: code length and alphabet are polynomial; no union-assignment nodes.

**Falsification.** A low-weight Tanner pseudocodeword projects to the G13 selector while satisfying all code checks.

**Smallest experiment.** Encode the four variables over \(\mathbb F_5\) using a length-five RS code, add one-hot symbols and pairwise Sidon features, then MILP-search through baseline \(+32\).

**Likely death.** Local one-hot decoding constraints recreate cheap integral pseudocodewords, or honest code coordinates dominate the radius and erase the gap.
