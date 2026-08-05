# Generation 3: Divergent Mechanism Sketches

**Prohibition compliance:** Nothing below draws on the off-limits document or coverage of it; all inspirations are classical (coding theory, additive combinatorics, electrical networks, geometry of numbers).

**Obstruction map used for checks (from IDEAS/STATUS/NOTES/GATE):**
- **O1** — slack-cheat kill: free integer slack directions zero amplified residuals, paying only unamplified anchor cost (gen-1 exact counterexample, 27 vs 19).
- **O2** — box artifact: finite-box "isolation" is uncertified; harmful fibers with ≥5 free integer dimensions generically contain short points outside [-3,3].
- **O3** — no instance: no basis, target, completeness radius, soundness threshold, or dimension-vs-gap law has ever been written down.
- **O4** — single-violated-clause bottleneck: constant per-clause penalty gives constant gap; unsat instances may violate exactly one clause, and naive amplification raises completeness equally.
- **O5** — overlap composition: cross-clause correlated kernel moves through shared variables are untested and may restore cheats.
- **O6** — brief constraints: deterministic, no PCP, no conjectures, executable soundness attacks before promotion.

---

## Sketch 1 — Congruence-obstruction isolation (p-adic certification)

**Trick.** Replace "no harmful move in a box" by "harmful fiber is empty modulo p." Design measurement rows so the affine system defining harmful signed selectors (sum = 1, marginals preserved, rows cancelled) is infeasible mod 2 or mod 3. Arithmetic infeasibility certifies emptiness of the *unbounded* integer fiber — no enumeration radius needed.

**Obstruction check.** O1: no slack variables; the selector formulation from gen-2 is retained, and congruence constraints are invariant under all integer moves, so no slack direction can restore feasibility. O2: directly targeted — a mod-p certificate is exactly the congruence obstruction the Fable review said was missing. O3: not addressed; still a local gadget (honest). O4: not addressed; per-clause exclusion only. O5: congruences compose additively over shared variables, so composition is *testable* by the same certificate; unverified until run. O6: fully executable via Smith normal form.

**Smallest test today.** For each of the 18 gen-2 isolating matrices, compute the Smith normal form of the harmful constraint system and check infeasibility mod 2, 3, 4. If all feasible, search 3-row matrices with entries {1,2} for a mod-p-infeasible design.

**Likely death.** The canonical cheat 001+010−011 differs from an honest one-hot by an *even* vector, so every residue class containing honest points may contain cheats; no congruence separates them.

---

## Sketch 2 — Effective-resistance demand gadget (electrical networks)

**Trick.** Make the unavoidable correction a *unit integer flow* between two terminals joined only by a path of length L. Any integer unit s–t flow has squared L2 norm ≥ effective resistance ≈ L. A false clause creates the demand; the only "slack" is flow, and flow pays geometry.

**Obstruction check.** O1: the gen-1 slack was a free coordinate; here every slack direction is an edge variable inside the resistor network, so it is amplified by construction — outside gen-1's assumptions, *provided* demand creation itself is inescapable (the weak point). O2: effective-resistance lower bounds hold over unbounded integers (flow decomposition), not boxes. O3: this sketch forces writing an actual basis/target (node-edge incidence lattice, weighted demand row) — progress on O3. O4: partially addressed — one violated clause forces cost √L with L = poly(n), while completeness pays O(√n) anchors; gap ≈ √(L/n), tunable to n^c if soundness holds. O5: shared variables become shared terminals; untested. O6: exact enumeration feasible at small L.

**Smallest test.** One clause, seven selectors, terminals joined by a path with L = 10; exact search over all integer moves with norm² ≤ 12 for a demand-free cheat.

**Likely death.** Non-Boolean/signed selector values evade demand creation entirely (the demand equation is itself linear), reproducing gen-1's defect one level up.

---

## Sketch 3 — Sidon/B_h-weighted measurements (additive combinatorics)

**Trick.** Gen-2 used 0/1 measurement rows; harmful selectors killed them by *exact* cancellation with coefficients in [-3,3]. Choose row coefficients from a B_h (Sidon-type) set: any signed integer combination with coefficients bounded by h that sums to zero is trivial. Then every harmful cancellation needs some coefficient > h, and an echo coordinate charges that coefficient linearly — provable, unbounded lower bound of h per false clause.

**Obstruction check.** O1: honest selectors satisfy rows exactly at coefficient ≤ 1; slack-type moves are combination coefficients, which the B_h property forces to be large — outside gen-1's "unamplified slack" assumption. O2: directly targeted — B_h is a theorem about *all* integers, replacing box search. O3: partially — weights are explicit, so completeness/soundness radii can be computed. O4: not addressed; h per clause is still per-clause (though h can be poly(n), which would beat O4 if completeness stays O(√n) — must verify honest cost doesn't scale with weights). O5: B_h must hold for the *union* difference-space of overlapping clauses; harder, testable. O6: fully executable.

**Smallest test.** Rebuild the gen-2 core with row coefficients {1, 2, 5, 11, 22, 57, 114} (Sidon-like), rerun the exact harmful-move search with box widened until minima certifiably stabilize.

**Likely death.** Honest one-hot selectors must satisfy the weighted rows exactly, forcing target entries that reintroduce small honest–harmful differences the B_h property doesn't cover.

---

## Sketch 4 — Barnes–Wall coset forcing (coding/lattice theory)

**Trick.** Route clause parity residuals into cosets of a Barnes–Wall / Construction-D lattice, whose minimum distance grows polynomially (∼N^{1/4}) in its dimension. A false clause forces the target into a provably deep nonzero coset; corrections are BW lattice moves, all long.

**Obstruction check.** O1: no free slack — the correction space *is* the BW lattice, whose shortest vector is N^{1/4}, so the gen-1 cheat class (short unamplified escape) is excluded by the lattice's proven minimum distance. O2: BW minimum-distance bounds are classical theorems over unbounded integers. O3: forces explicit basis/target; coset distance gives explicit soundness threshold — progress. O4: potentially addressed: one violated clause lands in a deep coset of distance N^{1/4} with N free to be poly(n); must check completeness stays O(√n). O5: untested; linear coset maps may cancel across clauses. O6: BW_16/BW_32 are small enough for exact experiments.

**Smallest test.** BW_16: map the 8 clause patterns of the gen-1 unsatisfiable formula to cosets; exact CVP enumeration to compare satisfied-vs-violated coset distances and hunt for a fractional-parity cheat.

**Likely death.** Cosets only encode *linear* (parity) information; 3SAT satisfaction is not parity, so the encoding either loses soundness (some unsat assignment maps to the trivial coset) or needs nonlinear preprocessing that reintroduces slack.

---

## Sketch 5 — Dual-certificate-first design (lattice duality / SDP)

**Trick.** Invert the workflow: pick the *soundness certificates* first. For dual vectors w, dist(t, L) ≥ dist(⟨w,t⟩, ℤ)/‖w‖; more strongly, a PSD matrix certificate lower-bounds distance quadratically. Design gadget columns so that every clause-violating assignment activates a pre-chosen certificate of value n^δ, from a combinatorial design over certificates.

**Obstruction check.** O1: certificates bound *all* integer points, including slack directions — if a certificate exists, gen-1-type cheats are impossible by proof, not search. O2: same — dual/SDP certificates are unbounded-valid, the exact fix Fable demanded. O3: certificate values *are* the soundness threshold; forces explicit instance. O4: single-vector certificates cap at ½/‖w‖ per constraint — honest admission: needs many certificates summed (SDP), and whether the sum scales polynomially is the open core. O5: certificate additivity over shared variables is precisely what the design must arrange; testable. O6: LLL/SDP on 12 columns runs today.

**Smallest test.** For the 18 gen-2 matrices, compute the best dual-vector and best diagonal-SDP certificate for the harmful fiber; compare against the enumerated minima to see whether certificates are tight.

**Likely death.** Certificate values for local gadgets plateau at O(1), and no design makes them add up faster than completeness cost — reducing to O4 in dual language.

---

## Sketch 6 — Expressible-penalty characterization (Voronoi/zonotope meta-mechanism)

**Trick.** Every gadget so far implicitly assumes a lattice can charge "distance to {0,1}" superlinearly. Characterize exactly which penalty functions ℤ→ℝ are realizable as x ↦ dist(t + xv, L): they are minima over lattice translates of quadratics. Prove either (a) a two-point set {0,1} can be charged with ratio ω(1) at fixed honest cost, giving a universal amplifier, or (b) it cannot — a new proved obstruction that prunes half the search space.

**Obstruction check.** O1: gen-1 explicitly left "amplifying Booleanity itself" open; this attacks that door directly. O2: characterization theorems are box-free. O3: not addressed; this is a lemma-level move (honest). O4: if (a) holds, the amplifier feeds every other sketch's O4 problem; if (b), O4 hardens into a theorem and redirects the campaign toward geometric (Sketch 2/4) routes. O5: orthogonal. O6: both directions have executable finite probes.

**Smallest test.** Exhaustively search all 2-dimensional and 3-dimensional lattices with entries in [-5,5] and one free coefficient x for the maximum of penalty(−1)/penalty-at-{0,1}-normalized-honest-cost; conjecture the supremum from data, then attempt proof.

**Likely death.** The supremum is a small constant (likely 3, matching |2x−1|), confirming (b) — which is still publishable negative infrastructure, not a reduction.

---

## Sketch 7 — Explicit instance + tensor amplification audit (multilinear algebra)

**Trick.** Convert the best surviving local gadget (gen-2 representative matrix, or Sketch 3's weighted version) into an *actual* GapCVP instance — basis, target, radii — then test whether its structure is "annulled" under tensoring so that gap g becomes g² in dimension N² (classically studied for SVP by Haviv–Regev; CVP behavior is instance-dependent).

**Obstruction check.** O1: inherits whatever the base gadget proves; tensoring adds no new slack directions but may *create* mixed-tensor cheats — must be searched. O2: tensored minima must be certified by enumeration, not boxes; feasible at dimension ≤ 144. O3: directly targeted — this sketch's primary deliverable is the missing basis/target/threshold artifact. O4: honestly *not* solved: constant base gap g gives exponent c = log g/log n → 0; tensoring only preserves an exponent already achieved, so this is infrastructure plus a diagnostic, not the polynomial jump. O5: tensor squares a single clause block; overlap still separate. O6: fully executable.

**Smallest test.** Build the 12-column CVP instance from the representative gen-2 matrix (rows [0,0,1,0,1,1,2]), compute its exact gap by enumeration, tensor once, recompute; report whether gap squares, stalls, or collapses.

**Likely death.** Mixed tensors (honest ⊗ cheat) realize sub-multiplicative distances, the classical failure mode of CVP tensoring, collapsing the gap to g.

---

**Portfolio note.** S1/S3/S5 attack O2 by three unrelated certification technologies (p-adic, additive-combinatorial, convex-duality); S2/S4 attack O4 geometrically (resistance, coset depth); S6 may convert O4 into a theorem; S7 discharges O3 regardless. Recommended parallel starts: S1 and S3 (hours of compute, decisive either way), S7 (pure infrastructure, cannot be wasted).
