Compliance note: I have not consulted, recalled, or searched for the prohibited document ("Ten Advances…") or any coverage of it. Everything below is built only from the attached campaign files and pre-existing classical literature.

**Obstruction map (labels used in every sketch):**
- **O1 — slack-cheat kill (Gen 1):** any gadget with integer degrees of freedom that escape amplification is dead; algebraic-number/multi-prime variants *with the same unamplified slack* inherit the kill.
- **O2 — locality of the survivor (Gen 2/3):** the 18-matrix isolation fact is constant-size, one clause, fixed marginals; no mechanism may assume it scales.
- **O3 — overlap composition (live, untested):** shared variables create integer kernel directions absent from local systems.
- **O4 — no finite→asymptotic promotion:** all-n claims require proof (a theorem or decision procedure), never extrapolation from finite experiments.
- **O5 — Q ≠ Z certification:** rational consistency/inconsistency does not settle integer feasibility; need exact integer certificates or complete bounded enumeration.

---

**1. n-fold integer programming / Graver-basis lifting (IP theory)**

*Trick:* Arrange clause measurements as an n-fold product of a fixed bimatrix. By the Graver-basis structure theorem for n-fold IPs (Santos–Sturmfels; De Loera–Hemmecke–Onn), every integer kernel element of the composed system is a conformal (non-cancelling) sum of lifts of a *finite, computable* set. Global soundness then reduces to a finite check on that set — by theorem, not extrapolation.

*Expected move:* a proved all-n lower bound on the norm of any harmful integer move.

*Obstruction check:* **O1** — slack columns sit inside the block; every slack move is a Graver element and is checked, or the route dies visibly. **O2** — uses the 18 survivors only as candidate blocks, assumes no scaling. **O3** — overlap must be encoded in the n-fold linking rows; if 3SAT's sharing pattern doesn't fit fixed-width linking, honest failure. **O4** — the finite→all-n step is a published theorem. **O5** — Graver computation (4ti2) is exact over Z.

*Falsification / experiment:* compute the Graver basis of one certified 3-row block with 2-fold linking (4ti2, today); any harmful conformal element of squared norm ≤ 4 kills it.

*Likely death:* arbitrary 3SAT incidence isn't fixed-block n-fold; encoding it inflates the block with n.

---

**2. Unique-neighbor expander parity matrix (coding theory)**

*Trick:* Take the 0/1 measurement matrix H from an explicit unbalanced bipartite unique-neighbor expander. Over Z (not just GF(2)): any nonzero v with Hv = 0 has support ≥ δn, since a unique neighbor row sees exactly one nonzero entry and can't vanish. So every kernel (cheat) direction has ℓ₂-norm ≥ √(δn), while completeness stays O(1) per row.

*Expected move:* a global, dimension-growing lower bound on all linear cheat directions.

*Obstruction check:* **O1** — slack columns are vertices of the expander, hence covered; no unamplified direction exists *for linear cheats*. **O2** — fresh family; no reliance on the 18 matrices. **O3** — expansion is a property of the whole matrix, so overlap directions are automatically kernel vectors of H and inherit the bound. **O4** — explicit expanders (e.g., Ramanujan-based) give proved all-n statements. **O5** — the unique-neighbor argument is native to Z.

*Falsification / experiment:* build a 24-column, degree-3 expander-like matrix today; ILP-search for integer kernel vectors of support < δn (exact, bounded box plus LLL).

*Likely death:* Booleanity is nonlinear; cheats that change the *affine* part (choose non-Boolean values consistently) aren't kernel vectors of H, so expansion protects the wrong object.

---

**3. Farkas dual-witness soundness (LP duality / proof complexity)**

*Trick:* Gen-3's certificates already imply an unconditional real bound: w with wᵀA = 0, wᵀb ≠ 0 forces ‖Ax − b‖ ≥ |wᵀb|/‖w‖ for *every real* x. Design the reduction so that unsatisfiability implies existence of many near-orthogonal witnesses wᵢ with mismatches ≥ pᵢ, giving dist² ≥ Σ(wᵢᵀb)²/‖wᵢ‖² — soundness as explicit linear algebra, no PCP.

*Expected move:* quantitative distance lower bounds from dual certificates instead of fiber-emptiness.

*Obstruction check:* **O1** — witnesses annihilate *all* columns including slack, or the witness doesn't exist and the design fails visibly. **O2** — generalizes the *form* of the Gen-3 certificates, not their scaling. **O3** — witnesses are computed on the composed system; overlap is the first test. **O4** — needs a proved existence lemma (e.g., closed-form Vandermonde/character witnesses) for all unsat instances. **O5** — bound holds over R, so Z-vs-Q is moot; this sidesteps O5 entirely.

*Falsification / experiment:* today: two overlapping OR clauses; exactly compute the best dual witness (rational LP) and check whether |wᵀb|/‖w‖ exceeds the completeness cost.

*Likely death:* proof-complexity analogue — some unsat formulas may admit only exponentially long/heavy Farkas certificates, so the soundness lemma is false or unprovable.

---

**4. Presburger / automatic-structure uniformization (model theory)**

*Trick:* Restrict to a structured NP-hard 3SAT fragment (e.g., bounded-pathwidth incidence chains). Then "for every length n, the composed harmful fiber is empty over Z and every violating integer point pays ≥ f(n)" becomes a sentence about a *regular family* of ILPs — decidable via Presburger arithmetic / automatic-sequence tools (Walnut, TaPAS). One decision-procedure run yields a legal all-n lemma.

*Expected move:* machine-checked conversion of local isolation into a uniform scaling law.

*Obstruction check:* **O1** — slack variables are existentially quantified inside the sentence, so cheats are searched over Z exhaustively by the decision procedure. **O2** — the tool *proves or refutes* scaling of the Gen-2/3 structure; nothing assumed. **O3** — overlap is exactly what the parametric chain encodes; this is the first target. **O4** — decidability is the promotion mechanism, which is legitimate. **O5** — Presburger is natively over Z.

*Falsification / experiment:* today: encode the pending 2-clause overlap audit (1 and 2 shared variables, all one-hot references) as quantified Presburger formulas in Z3; extend to a 3-clause chain.

*Likely death:* the needed norm bound f(n) is quadratic (norms aren't Presburger-definable), or the family isn't regular, or solver blowup at 3 clauses.

---

**5. Cyclotomic trace-norm Booleanity (algebraic number theory)**

*Trick:* Embed each Boolean value as (−1)^x ∈ Z[ζ_p] via the Minkowski embedding. Any nonzero algebraic integer α satisfies ‖σ(α)‖₂ ≥ √p·|N(α)|^{1/p} ≥ √p by AM–GM, so *every* nonzero deviation — including would-be slack — is amplified by arithmetic itself; there is no residual/slack coordinate split.

*Expected move:* Booleanity amplification for free, with amplification factor √p from a norm theorem.

*Obstruction check:* **O1** — the Gen-1 kill explicitly covers algebraic variants *with the same unamplified slack mechanism*; here the design rule is that no separate slack columns exist — every degree of freedom is an algebraic integer paying √p. Honestly: if clause products must be linearized, auxiliaries reappear and O1 applies in full. **O2** — independent of the 18 survivors. **O3** — overlap = shared field elements; must be tested exactly on two clauses. **O4** — the norm/AM–GM bound is a theorem for all p. **O5** — algebraic integers are a Z-lattice; native to Z.

*Falsification / experiment:* today: p = 5, one clause; enumerate all lattice points within squared radius 2p (exact, via Gram matrix + Fincke–Pohst) and check the non-Boolean minimum.

*Likely death:* linearizing the clause constraint reintroduces free auxiliary columns → exactly the Gen-1 cheat.

---

**6. Tensor-product gap amplification (geometry of lattices, Haviv–Regev style)**

*Trick:* If any slack-free constant-gap γ instance emerges (e.g., from a survived overlap audit), amplify by tensoring: completeness multiplies always (dist(t⊗t′, L⊗L′) ≤ dist·dist); soundness multiplication is the hard direction but holds for structured instances (integer-valued Gram, orthogonal-completion tricks, as in classical SVP tensoring literature).

*Expected move:* γ → γᵏ at dimension nᵏ.

*Obstruction check:* **O1** — inherits whatever base instance exists; tensoring adds no new slack, but doesn't fix O1 either — honest: this is a *post-processor*, contingent on a base. **O2** — needs the survivor upgraded to an actual constant-gap instance first; assumes nothing about scaling. **O3** — untouched; overlap must be solved at the base level. **O4** — soundness-under-tensoring must be a proved lemma for the specific base structure. **O5** — tensor soundness failures are integer phenomena; test with exact CVP.

*Falsification / experiment:* today: take any small exact CVP instance from the Gen-2 matrices; compute exact dist of the tensor square vs (dist)² by enumeration; strict inequality collapse kills it.

*Likely death:* arithmetic: γᵏ vs nᵏ gives gap N^{log γ/log n} → constant, not n^c, unless the base gap already grows with a parameter; tensoring alone cannot cross that line.

---

**7. Coboundary-expansion overlap control (topology / HDX)**

*Trick:* Model assignments as 0-cochains on an explicit high-dimensional expander whose triangles are clauses; cheat moves are cochains with vanishing coboundary on the constraint complex, and cosystolic/coboundary expansion (Gromov; Kaufman–Kazhdan–Lubotzky; LSV complexes) forces any such nonzero cochain to have weight ≥ εn. Clause overlap *is* the gluing data of the complex — composition is intrinsic, not bolted on.

*Expected move:* overlap obstruction dissolved by making it the load-bearing structure.

*Obstruction check:* **O1** — auxiliaries must themselves be faces of the complex to be covered by expansion; if they can't be, O1 applies and the route dies honestly. **O2** — no use of the 18 matrices. **O3** — this is the direct attack on O3. **O4** — expansion of explicit complexes is proved for all n; but mostly with F₂ coefficients — Z-coefficient statements must be sourced or proved, else no promotion. **O5** — F₂ expansion does *not* certify Z: ±2-valued cochains escape; a Z-coefficient argument is mandatory.

*Falsification / experiment:* today: smallest complete 3-partite triangle complex; exact ILP for the minimum-norm integer 1-cochain with zero coboundary but nonzero pairing against one triangle.

*Likely death:* no usable Z-coefficient expansion theorem; even-valued cochains cheat below the F₂ bound.

---

**Cross-cutting note:** sketches 1 and 4 are the only two that legally manufacture all-n statements (theorem-based and decidability-based promotion respectively); sketches 2, 5, 7 are new soundness *sources*; 3 is a new soundness *format*; 6 is a contingent post-processor. The mandatory Gen-4 overlap audit (Fable's specified experiment) should still run first — sketches 1, 3, and 4 each consume its output directly.
