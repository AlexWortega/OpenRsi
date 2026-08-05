Compliance note: nothing below draws on the prohibited document or any coverage of it; all citations are classical (pre-2024) literature. No searches were run against it.

**Obstruction map used for all checks** (from STATUS/NOTES/GATE):
- **O1 — slack annihilation (Gen-1 kill):** free integer slack directions zero out amplified residuals at unamplified anchor cost.
- **O2 — locality (Gen-2/3):** isolation is a constant-size fact; no overlap/composition lemma; shared rows may permit cross-clause cancellation.
- **O3 — no CVP accounting:** no basis/target/radii or dimension-dependent gap law exists.
- **O4 — survivor identity:** the 18 matrices were reconstructed by symmetry, never hash-checked against Gen-2 output.
- **O5 — exact-only isolation:** only zero-defect fibers are excluded; low-cost approximate cheats are unbounded.

---

**1. Whole-instance tensor amplification (Haviv–Regev style, ℓ₂)**

*Trick:* Start from exact CVP hardness (van Emde Boas 1981): integer Gram means deciding dist² ≤ d vs ≥ d+1 already carries gap √(1+1/d). Amplify by tensoring the instance with itself: if distances multiply on the yes side and are lower-bounded multiplicatively on the no side, k-fold tensoring gives gap growth in explicit Kronecker bases.

*Expected move:* a radii law dist(L⊗L, t⊗t) ≥ dist(L,t)² for a designed gadget class (e.g., Gram a projection scalar multiple).

*Obstruction check:* **O1** — outside: no residual/anchor split, no slack bits; tensoring acts on every direction uniformly. **O2** — outside: global operation, no shared local rows. **O3** — this sketch *is* an O3 attack; basis/target explicit via Kronecker products. **O4** — vacuous: 18 matrices unused. **O5** — honestly inside: non-product short vectors are exactly approximate cheats; unresolved.

*Smallest experiment:* brute-force dist(L⊗L, t⊗t) vs dist(L,t)² for all 3-dim integer lattices with entries in [-2,2]; log every sub-multiplicative counterexample.

*Likely death:* base gap is 1+1/poly, so reaching a constant needs superpolynomial tensor depth; plus non-product vectors break soundness.

---

**2. ℓ∞ amplification then one-shot norm transfer**

*Trick:* In ℓ∞, tensors behave perfectly: ‖u⊗v‖∞ = ‖u‖∞‖v‖∞, and CVP∞-adjacent problems (simultaneous Diophantine approximation, Lagarias 1985) have classical PCP-free hardness. Amplify polynomially in ℓ∞ by k-wise coordinate products, then transfer ℓ∞→ℓ₂ once, paying √dim, surviving if the ℓ∞ exponent exceeds 1/2.

*Expected move:* reduce campaign to a PCP-free CVP∞ gap theorem, where soundness = "one very violated coordinate," a different combinatorial target.

*Obstruction check:* **O1** — outside in form (max-norm cost isn't a sum of residual+anchor), but a slack-like escape could still zero the max coordinate; honest partial exposure. **O2** — outside: amplification is global coordinate products, not gadget overlap. **O3** — transfer step forces explicit radii accounting; addressed by construction. **O4** — vacuous. **O5** — inside: approximate cheats = coordinates all slightly violated; ℓ∞ tensoring amplifies these too, which is the hope, unproven.

*Smallest experiment:* 3-variable unsat formula as CVP∞ gadget; compute exact ℓ∞ yes/no optima by enumeration; then the coordinate-product square; check gap squares.

*Likely death:* an unsat formula falsifies only one clause, so the ℓ∞ "one big coordinate" never materializes without weight tricks that reintroduce the additive accounting problem.

---

**3. Graver/conformal-circuit composition lemma**

*Trick:* Any integer cheat vector decomposes into sign-conformal circuits of the global measurement matrix (Graver basis theory; Sebő, Onn). Conformality forbids cancellation between summands — precisely the failure mode O2 fears. If every circuit touching a falsified clause block pays ≥1 by the local certificates, costs add.

*Expected move:* superadditive law: ‖cheat‖² ≥ #(falsified local fibers crossed).

*Obstruction check:* **O1** — slack directions become circuits and get charged if the matrix has no measurement-free circuit; the 18 survivors certify exactly this locally; honest: must re-verify globally. **O2** — not outside: this is the direct assault on O2, using the no-cancellation structure conformality provides. **O3** — gives an accounting scaffold, no radii yet; partially inside. **O4** — inside: depends on the 18 matrices, so the hash check is mandatory step zero. **O5** — inside unless combined with sketch 4's margins; alone, exact-only.

*Smallest experiment:* (a) rerun `verify_affine_isolation_core.py`, hash survivors, assert set-equality (closes O4); (b) the gate-mandated two-clause shared-variable composition; enumerate Graver basis of the composed matrix (small enough for direct enumeration) and check every conformal circuit through the falsified clause costs ≥1.

*Likely death:* a global circuit threading two satisfied clauses and one falsified clause with zero net measurement — cancellation inside a single circuit, which conformality does not forbid.

---

**4. Farkas margins: from emptiness to quantitative robustness**

*Trick:* Each Gen-3 certificate w with wᵀA=0, |wᵀb|=β≥1 proves more than emptiness: for every real z, ‖Az−b‖₂ ≥ β/‖w‖₂. Convert all 126 certificates into explicit margin constants; design the CVP instance so falsified-clause residual blocks have disjoint coordinate supports, making margins add in squares.

*Expected move:* kill O5 for this gadget class — a uniform lower bound on approximate cheats, not just exact ones.

*Obstruction check:* **O1** — inside if any unmeasured slack column exists; must verify each certificate's w covers slack columns (checkable). **O2** — only handles disjoint supports; overlap composition delegated to sketch 3; honest. **O3** — margins are exactly the soundness-radius ingredient; partial progress. **O4** — inside: uses the 18 matrices; requires the hash check first. **O5** — this sketch is the O5 attack; by LP duality the bound is tight and unconditional.

*Smallest experiment:* compute β/‖w‖₂ for all 126 systems; for one representative, brute-force min over a fine rational grid of ‖Az−b‖ and confirm it matches the duality bound.

*Likely death:* margins are tiny (β=1, ‖w‖ large), so the per-clause cost is o(1) and unsat instances with one falsified clause gain nothing — the amplification gap remains untouched.

---

**5. Homological rigidity: coset distance of explicit qLDPC/cosystolic expanders**

*Trick:* Let the lattice be Construction-A over the boundary map of an explicit linear-distance quantum LDPC code (Panteleev–Kalachev 2021) or cosystolic expander (Kaufman–Kazhdan–Lubotzky). A cheat is a chain in a fixed homology class; "slack moves" are boundaries, which cannot change the class, and the *entire coset* has minimum weight ≥ code distance — polynomial rigidity by construction, deterministically.

*Expected move:* soundness = nontrivial class ⇒ Euclidean distance ≥ √(linear distance); completeness = satisfying assignment ⇒ trivial class with short representative.

*Obstruction check:* **O1** — outside: the escape directions (boundaries) are exactly what the coset bound quantifies over; no unamplified anchor exists. **O2** — outside: expansion is a global spectral property, not gadget composition. **O3** — basis/target explicit from parity checks; radii from code distance; addressed if completeness works. **O4** — vacuous. **O5** — favorable: coset minimum distance bounds *all* integer cheats, approximate included.

*Smallest experiment:* toric code on a 5×5 torus; encode a two-clause toy constraint as a homology class; brute-force coset minimum weights for trivial vs nontrivial classes; verify the Euclidean lift preserves the gap.

*Likely death:* completeness — deterministically mapping SAT structure into "trivial class with short witness" is where PCP-like local testability usually sneaks in.

---

**6. CRT prime-weight rigidity on slack channels**

*Trick:* Gen-1 died because slack (a,b)=(−1,0) is a legal integer escape. Route every slack bit through coordinates weighted by residues modulo many distinct primes, so a slack value outside {0,1} produces nonzero entries in all but O(log H) of the prime coordinates (an integer of height H vanishes modulo at most log H primes) — the slack itself becomes amplified.

*Expected move:* re-run of the Gen-1 attack fails; false clause forced to pay across ~all prime coordinates.

*Obstruction check:* **O1** — this is the direct O1 counter; but honesty: the cheat value −1 must be distinguished from legitimate 0/1 by *linear* coordinates, which is exactly the classical difficulty; only mod-p separation is claimed. **O2** — untouched; inside, deferred. **O3** — weights explicit; radii accounting must be redone; inside. **O4** — vacuous. **O5** — partially outside: nonzero-mod-p coordinates give quantitative cost, covering approximate cheats near the fiber.

*Smallest experiment:* modify `verify_rs_slack_cheat.py`: append prime-weighted slack coordinates for primes {2,3,5,7,11,13}; recompute the exact optimum on the all-eight-clauses formula; check whether 27 rises substantially versus baseline (which must be re-audited too).

*Likely death:* legitimate slack values also hit prime coordinates unless residues are centered exactly, and completeness cost inflates in lockstep — ratio collapses toward 1.

---

**7. Deterministic locally dense CVP gadget from bent-function deep holes**

*Trick:* Classical SVP/CVP gap machinery (Micciancio 2000) needs a locally dense lattice with a random center; derandomize using explicit deep holes of first-order Reed–Muller codes — bent functions sit at distance 2^{m−1}−2^{m/2−1} with exponentially many nearest codewords, fully explicit. Construction-A lift gives a deterministic dense gadget; direct-sum with the exact CVP instance and project.

*Expected move:* a fully explicit, deterministic constant-factor GapCVP hardness — the missing verified base for sketches 1–2.

*Obstruction check:* **O1** — outside the letter (no slack bits), but the mixing cheat (intermediate vectors straddling gadget and instance blocks) is the moral analog; must test. **O2** — outside: no local overlap structure. **O3** — this sketch is pure O3 work: explicit basis, target, and radii computed from RM parameters. **O4** — vacuous. **O5** — inside: local density controls approximate cheats only via the projection argument's robustness; partially unresolved.

*Smallest experiment:* RM(1,4), bent function of 4 variables; enumerate all 32 codewords; verify deep-hole distance 6 and count nearest codewords; build the Construction-A lattice and brute-force the coset/close-point statistics.

*Likely death:* the known ceiling — this machinery yields constant factors; the polynomial climb still needs sketch 1's unproven tensor soundness.

---

**8. Parametric Presburger uniformization of the certificates**

*Trick:* The 126 infeasibility certificates look like instances of one parametric family. Encode "for all polarities, references, and shared-variable identifications, the harmful fiber is empty with margin ≥ β" as a parametric Presburger sentence and get a *uniform* lemma via quantifier elimination, replacing per-instance audits with one symbolic proof that scales over clause arrangements.

*Expected move:* a machine-checked uniform local-soundness lemma — the reusable brick both sketches 3 and 4 need.

*Obstruction check:* **O1** — inherits whatever the underlying gadget does; not an independent O1 answer; honest. **O2** — partially outside: uniformity over arrangements is a step toward composition, though unbounded dimension is not expressible in a single Presburger sentence — only bounded-overlap templates. **O3** — no; purely a lemma-factory. **O4** — outside after step zero: QE would re-derive the survivors symbolically, independently confirming identity. **O5** — outside if margins are quantified in the sentence (∀z: ‖Az−b‖² ≥ 1).

*Smallest experiment:* encode one two-clause composed system with a symbolic polarity parameter in Z3/`LIA`; ask for unsat of the harmful fiber for *all* parameter values; extract the proof.

*Likely death:* QE blowup beyond two clauses, and the bounded-template ceiling means it never becomes a scaling law by itself.

---

**Cross-sketch note for the agent:** sketches 3+4 are complementary (composition × margins) but share the O4 debt — the survivor hash check is a 20-minute task that unblocks both and should run first regardless of which sketch is selected. Sketches 1, 5, 7 are mutually independent global routes with disjoint failure modes; do not let one kill demoralize the others.
