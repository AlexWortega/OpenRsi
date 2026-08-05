Classical ingredients only: Construction-A lattices and expander codes (Conway–Sloane; Sipser–Spielman, 1996), signed-digit arithmetic (Avizienis, 1961), Graver bases (Graver, 1975), treewidth methods, and Sherali–Adams lifts (1990). No off-limits material was consulted.

1. **Voronoi deep-hole Boolean alphabet**

**Mechanism.** Replace coordinatewise half-integral anchors by a lattice gadget whose target is a deep hole and whose complete nearest-point shell is exactly a legal assignment alphabet. Couple clause evaluations to linear projections of those nearest points, then heavily scale only clause residuals.

**Expected move.** Exact-zero cheats must either remain legal assignments or cross a next-shell gap; a polynomial shell ratio would yield the desired CVP gap.

**Obstruction audit.** G1 slack: no slack variables. G2–3 isolation: not a fixed-marginal affine selector fiber. G5 overlap: shared deep-hole coordinates replace private rows, but clause-supported circuits may still survive. G6 gate: basis, target, and coupling coordinates are all emitted. G7 radix kernel: amplification is geometric, not applied after a residual map. G9 parity/G11 unique cubic: parity combinations should leave the nearest shell. G12 clause drop: zero blocks are not nearest points. The finite-only obstruction remains: a uniform shell/composition theorem is required.

**Falsification.** Any illegal lattice point in or near the legal shell, especially one satisfying all clause projections.

**Experiment.** Search dimensions 4–12 over small Construction-A lattices; enumerate complete nearest and next shells, then couple the best gadget to the nine-clause instance.

**Likely death.** Known shell gaps stay constant, or coupling creates new near points.

---

2. **Construction-A expander syndrome barrier**

**Mechanism.** Encode replicated variable/selector deviations with an explicit linear code of relative distance \(\delta\), and realize its syndrome modulo \(p\) directly as a Construction-A lattice block. Natural \(p\mathbb Z\) “carry” columns only reduce a coordinate to its residue; they cannot erase a nonzero syndrome.

**Expected move.** Every exact kernel cheat becomes a codeword of weight \(\Omega(N)\), while every non-codeword pays many syndrome coordinates; large syndrome scaling then amplifies one false clause.

**Obstruction audit.** G1 slack: modular carries cannot annihilate nonzero residues. G2–3 isolation: this is global coding, not local fixed marginals. G5 overlap: expander checks cross clauses, although a harmful global codeword remains possible. G6: no external filters. G7: no radix transform; exact kernels are attacked by code distance. G9 parity and G11 unique cubic are low-support deviations and should have nonzero syndrome. G12 deletion violates many checks. Asymptotics would follow only from an explicit distance theorem compatible with all honest assignments.

**Falsification.** A low-weight harmful codeword or a code invariant forced by honest-assignment differences.

**Experiment.** Put BCH or small-expander checks on the 72 selector coordinates and rerun exact shell DP through squared radius 108 for several primes.

**Likely death.** Required honest assignment differences force low-distance codewords into the kernel.

---

3. **Canonical signed-digit carry avalanche**

**Mechanism.** Replace each selector coefficient by a length-\(L\) canonical signed-digit chain with emitted recurrence rows and anchored carry states. Honest \(0/1\) coefficients terminate immediately, whereas \(-1,2\), a missing normalization, or an inconsistent residual should launch a nonzero carry through \(\Theta(L)\) levels.

**Expected move.** Set \(L=N^\alpha\) so every signed-selector repair accumulates polynomial energy without introducing free slack.

**Obstruction audit.** G1 slack: every carry is charged at every level, unlike the free residual slack. G2–3: Booleanity comes from canonical representation, not local affine isolation. G5: chains can share variable digits globally, but clause-local carry cycles are not excluded. G6: all digits, carries, rows, and targets are inside CVP. G7: radix is applied to coefficients themselves, so an \(Az=b\) signed kernel is not automatically invisible. G9 parity and G11 cubic parity contain negative coefficients and should avalanche. G12 clause drop starts a normalization carry. A uniform gap still needs baseline accounting in the output dimension.

**Falsification.** A periodic carry cycle, alternative expansion of \(-1\), or honest baseline growing as fast as the penalty.

**Experiment.** Implement bases \(3,4\), lengths \(2\)–\(6\), first for one OR clause and then the nine-clause shell.

**Likely death.** Redundant signed-digit representations absorb defects cheaply, or every dormant carry contributes baseline cost.

---

4. **High-girth toric/Graver fiber**

**Mechanism.** Treat harmful signed selectors as circuits of an integer configuration. Build the configuration from Vandermonde or cyclic-polytope columns, plus an occurrence-expander, aiming for a Graver dichotomy: every kernel vector is either a difference of honest global assignments or has norm at least \(N^{1/2+c}\).

**Expected move.** Huge weights enforce the exact fiber; the Graver lower bound makes every non-honest fiber point polynomially farther than completeness.

**Obstruction audit.** G1: no slack. G2–3: replaces constant local isolation by a uniform global circuit theorem. G5: not private-row composition, though its clause-supported circuit could reappear and must be excluded. G6: the full integer matrix defines the lattice. G7: exact residual kernels are the object being bounded, not ignored. G9 parity and G11 unique cubic are explicit short circuits the construction must destroy. G12 deletion is a nonkernel defect or a long circuit. The asymptotic obstruction is precisely the missing Graver-distance theorem.

**Falsification.** Any non-honest Graver element of subpolynomial norm.

**Experiment.** Generate small Vandermonde/expander configurations for the nine-clause incidence pattern; use MILP plus exact kernel enumeration to find the shortest harmful circuit.

**Likely death.** The affine span of all honest assignments necessarily creates short exchange circuits.

---

5. **Treewidth–well-linked structural dichotomy**

**Mechanism.** Exploit that the reduction may solve easy source instances. If incidence treewidth is \(O(\log N)\), solve 3SAT by dynamic programming and emit a fixed yes/no CVP instance; otherwise extract a large well-linked set and route consistency checks through many disjoint paths.

**Expected move.** Low-treewidth formulas require no gadget soundness. In the high-treewidth case, changing one local selector should force many routed disagreements, potentially supplying a polynomial gap.

**Obstruction audit.** G1: no slack. G2–3: local isolation is used only inside a globally routed network. G5: private overlap is replaced by many crossing routes, but its kernel might lift along cycles. G6: routes and checks are emitted coordinates. G7: no radix. G9 parity and G11 unique-occurrence parity should cross many separators. G12 deletion should break all routes incident to that clause. The finite-only obstruction would be addressed by quantitative well-linkedness, if it applies to the relevant unsatisfiable core.

**Falsification.** A high-treewidth formula whose contradiction lies in a constant-size appendage while all width comes from an irrelevant satisfiable component.

**Experiment.** Enumerate small formulas, compute exact treewidth and minimum routed-selector attack cost, including deliberately padded tiny unsatisfiable cores.

**Likely death.** High treewidth says nothing about where unsatisfiability resides.

---

6. **Affine tensor spherical code**

**Mechanism.** Give each legal clause label a rational codeword \(u_a\) and use a nonzero tag target \(t\), chosen so all legal labels have equal radius while zero and bounded signed combinations are farther. Tensor \((u_a,t)\) to depth \(O(\log N)\); constant-factor separation per level would become polynomial while dimension remains polynomial.

**Expected move.** Simultaneously amplify clause deletion and cube parity without relying on degree-occurrence comparisons.

**Obstruction audit.** G1: no slack. G2–3: separation is metric rather than affine-fiber inconsistency. G5: tags may be globally coupled, but local affine circuits remain possible. G6: rational factor and nonzero target are explicit CVP data. G7: no post-residual radix. G9 parity is directly included among forbidden signed combinations. G11 unique cubic is irrelevant because tags do not require another occurrence. G12 clause drop is outside the killed homogeneous-tag assumption: deletion pays \(\|t\|^2\) rather than merely losing one unit. Asymptotic tensor accounting remains unproved.

**Falsification.** An affine signed combination having tensor correlation at least that of a legal label.

**Experiment.** Grid-search rational \(u_a,t\) in dimensions 3–8; exhaust all \(z\in[-2,3]^8\) through anchor excess 36, including zero and seven-term parity, then test tensor depth two.

**Likely death.** Equidistance forces a dangerous affine combination, or legal radius tensorizes just as quickly.

---

7. **Clause-subset direct-product lift**

**Mechanism.** Introduce selectors for every pair, or fixed-size \(k\)-tuple, of clauses, labelled by assignments to their combined variables. Enforce all intersection marginals, so one false clause contaminates \(\Theta(m^{k-1})\) tuple checks rather than one local row.

**Expected move.** For constant \(k\), the lift is polynomial; sharing original variable anchors while multiplying zero-baseline checks could create a power-law soundness gain.

**Obstruction audit.** G1: no residual slack. G2–3: fibers use higher-order overlaps, not fixed local marginals. G5: all intersections are checked rather than keeping private rows, but signed overlap cocycles may still exist. G6: every normalization and marginal is a CVP coordinate. G7: no radix. G9 parity should be exposed in tuples containing the attacked clause and another witness clause. G11 unique cubic gains many tuple comparisons. G12 deleting one clause block violates every tuple containing it. The asymptotic obstruction remains: fixed-level lifts may have pseudo-distributions and their baseline dimension may cancel amplification.

**Falsification.** A signed Möbius cocycle satisfying every tuple marginal, or no improvement after normalizing by output dimension.

**Experiment.** Build the \(k=2\) lift of the nine-clause instance—at most six variables per pair—and use exact MILP/shell DP to compare obstruction and control minima.

**Likely death.** Fixed-level Sherali–Adams-type integrality gaps reproduce the same cheats globally.
