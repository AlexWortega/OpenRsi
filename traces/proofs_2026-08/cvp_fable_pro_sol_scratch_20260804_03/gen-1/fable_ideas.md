# Generation 1 — Divergent mechanism sketches

**Compliance note:** The off-limits document and anything derived from it were not consulted. Per ORACLE_BRIEF, no prior campaign obstruction map exists; the attached map is **empty**. So that "check against every obstruction" is meaningful, I check each sketch against the five *classically proved* obstructions any route must clear:

- **O1 (limits on c):** GapCVP_√n ∈ coNP (Aharonov–Regev 2004); GapCVP_√(n/log n) ∈ coAM (Goldreich–Goldwasser 1998). NP-hardness at c ≥ 1/2 collapses PH — claim only small explicit c.
- **O2 (integer-cheating):** In any linear/lattice encoding, non-Boolean integer coefficients can satisfy clause equations at O(1) ℓ₂ cost; exact reductions (van Emde Boas 1981) gapify to O(1) only. Provable by brute force on small instances.
- **O3 (campaign rules):** deterministic, many-one, no PCP theorem (nor covert reproof), no conjectures.
- **O4 (tensor soundness):** distance of a shifted lattice/coset need not multiply under tensoring; only homogeneous minimum distance multiplies exactly.
- **O5 (repetition wall):** k-fold tensoring of a constant gap g on base size n₀ gives gap N^(log g/log n₀) in dimension N = n₀^k — exponent vanishes as n₀ grows. Polynomial gap with **absolute** c needs a base gap already polynomial in base dimension, or a one-shot amplifier.

---

## Sketch 1 — Vandermonde rigidity against integer cheating (number theory)

**Mechanism:** Two-tier coordinates. Light coordinates give honest cost √n. Heavy coordinates are rows of a Vandermonde/geometric-progression matrix scaled by W: any *nonzero* integer combination with coefficients bounded by B has magnitude ≥ 1 (determinant/Liouville-type lower bound), so any cheat that perturbs heavy rows pays ≥ W. Coefficient boundedness enforced by light penalty coordinates carrying identity.
**Expected move:** gap W/√n with W = n^(0.4+1/2), i.e., explicit c ≈ 0.4, single-shot.
**Obstruction check:** O1: c < 1/2 by construction ✓. O2: this is a *direct attack* on O2 — but the coefficient-bounding gadget is itself linear, so O2 is only partially escaped; honestly flagged. O3: deterministic, no PCP ✓. O4/O5: no tensoring, no repetition ✓.
**Falsification test:** find a no-instance vector with cost o(W) mixing moderate coefficients across many Vandermonde rows.
**Smallest experiment (today):** n = 8 variables, 3–4 clauses; build the lattice, brute-force CVP (enumerate coefficients in [−10,10]); compare yes/no distances.
**Likely death:** Liouville-type bounds decay exponentially in the number of combined rows; a spread-out cheat cancels the heavy rows cheaply.

## Sketch 2 — NCP-first: expander distance amplification, then embed (coding theory)

**Mechanism:** 3SAT → exact Nearest Codeword (Berlekamp–McEliece–van Tilborg 1978). Amplify the *relative* distance gap deterministically via ABNNR (Alon–Bruck–Naor–Naor–Roth 1992) expander distance amplification — a PCP-free combinatorial amplifier. Embed binary NCP into CVP by the standard scaled-lattice embedding.
**Expected move:** constant-factor PCP-free NCP hardness; then push toward polynomial via structured tensoring.
**Obstruction check:** O1: fine, tiny c targeted. O2: NCP quotients out integer cheating over F₂ (cheats are wrong codewords, not non-Boolean integers) — genuinely outside O2's assumptions until the final lattice embedding, where mod-2 lattices (x ≡ codeword mod 2) re-block it; flagged. O3 ✓ (ABNNR is explicit/deterministic). O4: tensoring cosets is exactly where O4 bites — this sketch's open crux. O5: even if tensoring works, exponent vanishes; a growing-gap amplifier is still needed. Honest: O4/O5 not cleared.
**Falsification test:** exhibit a tensored no-instance whose coset minimum weight collapses below the product bound.
**Smallest experiment:** 8-vertex explicit expander, ABNNR on a 16-bit code; brute-force NCP distances before/after amplification and after one tensor step.
**Likely death:** completeness distortion in ABNNR (yes-target drifts) or O4 coset collapse.

## Sketch 3 — Barnes–Wall one-shot amplifier (lattice geometry)

**Mechanism:** Barnes–Wall lattices BW_k (dim 4^k) are explicit, tensor-structured, with minimum distance 2^k and covering-radius/packing-radius ratio ~ N^(1/4). Embed the exact 3SAT lattice so honest targets sit at a deep hole (distance r), while any cheating vector must traverse to another BW point at cost ≈ N^(1/4)·r. The polynomial gap comes from a *fixed rigid family*, not repetition — evading O5.
**Expected move:** one-shot gap N^(1/4−ε), explicit c.
**Obstruction check:** O1: 1/4 < 1/2 ✓. O2: cheating is "move to another BW point," priced by minimum distance — but the 3SAT-gadget coordinates glued on re-open O2 (cheap escape directions); that gluing is the entire problem, flagged honestly. O3 ✓ (BW explicit; deterministic). O4: no instance tensoring; BW's own tensor structure is provable classical fact ✓. O5: explicitly avoided (amplifier gap grows with dimension) ✓.
**Falsification test:** find hybrid vectors (part gadget, part BW) at cost O(r) in no-instances.
**Smallest experiment:** BW₂ (dim 16) + 3-variable formula gadget; brute-force CVP; measure yes/no ratio.
**Likely death:** the seam between formula gadget and BW admits O(1)-cost hybrids; gap collapses at the interface.

## Sketch 4 — Cosystolic expansion (topology / high-dimensional expanders)

**Mechanism:** Encode assignments as Z₂ 1-cochains on an explicit Ramanujan complex. Cosystolic expansion (Evra–Kaufman 2016; Kaufman–Kazhdan–Lubotzky 2014) is a *deterministic, PCP-free theorem*: any cochain far from the cocycle space violates proportionally many faces. Realize the coboundary operator as a mod-2 lattice; unsatisfiability ⇒ far from cocycles ⇒ many violated faces ⇒ large ℓ₂ distance.
**Expected move:** constant-gap CVP hardness from topology instead of PCP; then hand off to a one-shot amplifier (Sketch 3).
**Obstruction check:** O1 ✓ (modest c). O2: expansion converts one logical violation into Ω(fraction) geometric violations over F₂; lifting to Z re-admits even-integer cheats — needs the mod-2 lattice gadget, cost analysis open, flagged. O3 ✓: expansion of a fixed explicit complex, not a proof-composition argument. O4/O5: constant gap only; boosting hits the same wall as everyone — honestly not cleared.
**Falsification test:** small complex where a far-from-cocycle target has an integer (non-F₂) lattice vector nearby.
**Smallest experiment:** complete 2-complex on 8 vertices (known coboundary expander); build coboundary lattice over Z; brute-force distances.
**Likely death:** stalls at constant gap; contributes soundness technology, not the polynomial exponent.

## Sketch 5 — Simplex-embedded Reed–Solomon + Johnson bound (list decoding)

**Mechanism:** Assignments → RS codewords over F_q; embed each symbol as a vertex of a regular simplex in R^q, so ℓ₂ distance ↔ Hamming agreement *and* the simplex geometry makes fractional/large-integer symbol values expensive in norm — a genuinely **nonlinear** Booleanness constraint, which is exactly what O2 says linear encodings lack. Johnson bound: any target within the decoding radius is near only a short list of codewords; clause coordinates penalize each listed non-satisfying assignment.
**Expected move:** one-shot polynomial gap ~ q^Ω(1) from list-decoding radius vs. distance.
**Obstruction check:** O1: tune c < 1/2 ✓. O2: attacked via nonlinear simplex geometry — but vectors *outside* the simplex hull may still be cheap; partially inside O2, flagged. O3: Johnson bound is combinatorial, not PCP — but clause checks touching 3 symbols risk sliding into composition/alphabet-reduction, i.e., covert PCP; must be watched ✓/⚠. O4/O5: single-shot ✓.
**Falsification test:** cheap off-simplex vector satisfying clause coordinates in a no-instance.
**Smallest experiment:** RS over F₅, length 5, simplex embedding in R²⁵; brute-force CVP for a 2-variable formula.
**Likely death:** consistency between clause coordinates and codeword coordinates reintroduces PCP-style composition.

## Sketch 6 — Dinur-style powering natively in ℓ₂ (flagged as PCP-adjacent)

**Mechanism:** Treat the CVP instance as a constraint graph on coordinate blocks; define graph powering directly on the lattice and prove an ℓ₂ amplification lemma: gap (1+1/poly) → constant in O(log n) deterministic powering steps. Hope: ℓ₂ averaging replaces Dinur's alphabet-reduction/composition step (norms average; alphabets don't), so no proof composition is needed.
**Expected move:** 1/poly → constant gap; combine with Sketch 3 for polynomial.
**Obstruction check:** O1 ✓. O2: powering multiplies violation count statistically — a frontal O2 attack. O3: ⚠ honest flag — if a composition/alphabet-reduction step turns out necessary, this is reproving PCP and violates the campaign rule; abort criterion built in. O4: powering ≠ tensoring; dimension grows linearly per step ✓. O5: avoided if per-step gap growth is multiplicative ✓.
**Falsification test:** one powering step on an exact instance fails to increase the yes/no distance ratio.
**Smallest experiment:** 20-dim exact-CVP instance from a 4-variable formula; implement one powering step; brute-force ratio before/after.
**Likely death:** coefficient growth per step forces a composition step ⇒ O3 violation ⇒ route must be killed by its own rule.

## Sketch 7 — Birkhoff-polytope integrality (combinatorial rigidity)

**Mechanism:** Encode assignments as permutation matrices. Birkhoff–von Neumann: the *only* integer points of the doubly-stochastic polytope are permutations — so "non-Boolean integer cheating" is annihilated by polyhedral integrality, not by penalties. Clauses become linear functionals on permutation entries; soundness for "wrong permutation" cheats from spectral gaps of Cayley graphs on S_n (Diaconis–Shahshahani-type bounds).
**Expected move:** an encoding where O2 is *structurally impossible*, leaving only combinatorial cheats to price.
**Obstruction check:** O1 ✓. O2: uniquely, fully outside O2's assumptions for non-permutation cheats — the strongest O2 answer in this generation; but wrong-permutation cheats remain and are priced only O(1) so far, flagged. O3 ✓ deterministic, no PCP. O4/O5: single-shot ✓, though the achievable gap is unproven.
**Falsification test:** wrong permutation at distance O(1) from target in a no-instance (expected!) — then test whether Cayley-graph spectral penalties lift it.
**Smallest experiment:** S₄ (16-dim), 3-variable formula; brute-force CVP over the Birkhoff lattice slice.
**Likely death:** gap stuck at O(1) because adjacent transpositions are cheap; spectral penalty terms are again linear and re-admit O2.

## Sketch 8 — Homogenize: deterministic MDP hardness → CVP via GMSS transfer

**Mechanism:** Minimum Distance Problem hardness has a *deterministic, PCP-free* proof at constant factor (Cheng–Wan 2009, via Reed–Solomon deep holes and character sums). Minimum distance multiplies **exactly** under code tensoring — the homogeneous problem evades O4 entirely. Transfer hardness to inhomogeneous CVP via Goldreich–Micciancio–Safra–Seifert (1999)-style factor-preserving reductions.
**Expected move:** clean PCP-free superconstant MDP gap; then attempt a growing base gap via algebraic-geometry codes (character-sum bounds strengthening with q) to beat O5.
**Obstruction check:** O1 ✓. O2: homogeneous F_q setting — integer cheating not defined until the final transfer; the transfer step must be re-audited, flagged. O3 ✓ (Cheng–Wan is deterministic, PCP-free). O4: *cleared* — the one sketch where tensoring is provably sound (d(C₁⊗C₂)=d₁d₂). O5: ⚠ the honest wall: constant base gap tensored gives vanishing exponent; needs base gap q^Ω(1) — open, this sketch's whole bet.
**Falsification test:** show character-sum slack cannot grow the base gap beyond a constant.
**Smallest experiment:** RS deep-hole gadget over F₁₆; verify gap numerically; one tensor step; confirm exact multiplication.
**Likely death:** O5 — the exponent c comes out as o(1), reproducing the classical quasipolynomial wall.

---

**Portfolio logic (no favorite):** Sketches 1, 5, 7 attack O2 by three different nonlinearities (Diophantine, simplex geometry, polytope integrality); 2, 8 route through codes where O2/O4 weaken; 3 is the only one-shot polynomial amplifier candidate; 4 and 6 are constant-gap engines from topology and graph powering that only matter combined with 3 or 8. First executable batch: experiments for 1, 3, 7 (all brute-forceable in dimension ≤ 20 today).
