Below are seven independent, pre-proof mechanisms. None is promoted without unrestricted obstruction/control searches.

### 1. Log-width color-coded moment tables

**Core trick.** Use a deterministic \(k\)-perfect-hash family with \(k=\Theta(\log n)\), and for each hash store a \(2^k\)-dimensional group-algebra/Walsh table rather than enumerating all \(n^k\) moments. If a sparse signed perturbation involves at most \(k\) variables, some injective coloring exposes its top multilinear term. Classical hook: Naor–Schulman–Srinivasan splitters (1995).

**Expected move.** Convert “small anchor excess” into sparse support, then charge every sparse zero-residual pseudodistribution in polynomially many coordinates.

**Obstruction audit.** G1: no slack. G2/G3: does not assume fixed local marginals. G5: hashes are global, not private rows. G6: all tables must be emitted and searched unrestrictedly. G7: fingerprints need not vanish on its old residual kernel. G9/G11: degree grows beyond three. G12: missing-table normalization prices drops. G13/G15: the affine lift still exists, but may become expensive in the added tables—so not excluded. G14: not fixed pair bags. G19: not a flow encoding. G20/G21: scaling remains unproved. G22: no ordinary tensor decomposition is assumed.

**Falsification.** Find a \(k+1\)-parity or dense affine lift invisible/cheap under every hash.

**Smallest experiment.** For the nine-clause instance, use \(k=4\), enumerate a minimal perfect-hash family, append exact tables, and search through \(B+64\).

**Likely death.** Cheap attacks are dense, invalidating the sparse-support premise.

---

### 2. Quaternary phase lifting via \(\mathbb Z_4\)-linear codes

**Core trick.** Append quadratic phase coordinates to each legal label and place them in a Construction-\(A_4\) lattice from a \(\mathbb Z_4\)-linear Kerdock-type code. Binary-affine collisions need not remain coordinatewise cheap after the nonlinear Gray/phase lift, even though all honest labels retain equal norm. Classical hook: Hammons–Kumar–Calderbank–Sloane–Solé (1994).

**Expected move.** Make parity, clause drops, and signed selectors pay code distance in phase coordinates without relying on an old residual syndrome.

**Obstruction audit.** G1: no slack. G2/G3 and G5: no local-isolation composition claim. G6: emit the integral Construction-\(A_4\) basis and optimize unrestrictedly. G7: its zero residual does not imply zero phase cost. G9/G11: phases are quadratic over \(\mathbb Z_4\), not bounded real moments. G12: include a nonzero phase for the zero/drop label. G13: its affine combination still lifts linearly; only anchor energy, not syndrome incompatibility, can defeat it. G15: no marginal hierarchy. G14: orthogonal to pair bags. G19: flow splicing remains unaddressed unless paths receive phases. G20/G21: ordinary code distance gives no polynomial relative gap yet. G22: no tensor theorem.

**Falsification.** A lifted G13 vector or drop whose phase excess is \(O(1)\).

**Smallest experiment.** Search all length-8 \(\mathbb Z_4\) quadratic phase assignments for the eight clause labels, scoring G7, G11, G12, and G13 simultaneously.

**Likely death.** Linearity modulo four recreates an equally cheap affine lift.

---

### 3. High-girth nonabelian word fingerprints

**Core trick.** Break a branching program into \(L=\Theta(\log n)\)-layer segments and tag each segment by the endpoint of its transition word in a high-girth finite Cayley graph. Regular-representation basis vectors make distinct short words affinely independent, so signed flow splicing cannot silently exchange partial histories. Classical hook: Lubotzky–Phillips–Sarnak Cayley graphs (1988).

**Expected move.** Turn the G19 accepting splice into a nonzero segment-history discrepancy while keeping group size and dimension polynomial.

**Obstruction audit.** G1: no slack. G2/G3/G5: no marginal isolation. G6: group tags, targets, and transition rows are explicit lattice coordinates. G7 and G9/G11: selector kernels do not imply equal nonabelian words. G12: a dropped segment misses its unit tag. G13/G15: affine mixtures of complete histories still exist but cannot manufacture an absent basis endpoint cheaply unless histories collide. G14: unrelated to pair bags. G19: directly changes its assumption that conservation plus endpoint state captures history. G20/G21: segment separation alone has no recursive relative-gap theorem. G22: no decomposable-tensor assumption.

**Falsification.** Reconstruct an exact accepting signed flow whose group tag also vanishes, or find a short word collision.

**Smallest experiment.** Extract the two-negative-edge G19 witness, tag only the shortest segment containing both negative edges using a small permutation group, and solve that local fiber exactly.

**Likely death.** Splicing combines many distinct word tags with signed coefficients to synthesize the desired endpoint.

---

### 4. Iterated Lawrence lifting of the selector configuration

**Core trick.** Apply \(r\) Lawrence liftings to the complete selector/consistency matrix, pairing each coefficient with complementary copies and shared-sum rows. In algebraic statistics, Lawrence liftings can force kernel moves to decompose into conformal Graver moves whose “type” grows with the lifting depth. Classical hook: Sturmfels, *Gröbner Bases and Convex Polytopes* (1996).

**Expected move.** With \(r=\Theta(\log n)\), make every signed attack require polynomially many non-Boolean blocks before residual amplification is applied.

**Obstruction audit.** G1: no slack. G2/G3: uses global kernel geometry, not the surviving local matrices. G5: shared complement rows replace private composition. G6: every lifted coefficient is unrestricted. G7: its circuit may lift, but should acquire larger type. G9/G11: attacks are handled as Graver moves, not moments. G12: drops violate shared sums in every copy. G13 and G15: their affine lifts probably persist; only a growing norm claim could defeat them. G14: not pair-bag propagation. G19: signed flows can also be lifted, with no current exclusion. G20/G21: the required type-to-relative-gap inequality is unproved. G22: iteration may create analogous entangled moves, so not outside it.

**Falsification.** A bounded-type circuit surviving two liftings, especially a lifted G13 or G19 witness.

**Smallest experiment.** Lawrence-lift the 72-selector G7 matrix once and twice; compute short Graver/kernel moves with 4ti2 or exact MILP.

**Likely death.** Attack cost and honest baseline grow at the same rate.

---

### 5. Degree-filtered Nullstellensatz geometry

**Core trick.** Build a squarefree Macaulay module for the Boolean and clause ideals, but weight coefficient layers by proof degree and represent repeated subexpressions with algebraic branching-program states. A satisfying assignment supplies a short multiplicative evaluation functional; an unsatisfiable formula should force any approximate integral functional to fail at a high-degree layer. Classical hook: polynomial calculus of Clegg–Edmonds–Impagliazzo (1996).

**Expected move.** Replace local consistency by global incompatibility of an integral truncated ring homomorphism, potentially charging pseudodistributions only when their required degree becomes large.

**Obstruction audit.** G1: no slack. G2/G3/G5: no local overlap composition. G6: multiplicativity cannot be externally assumed; every Macaulay equation must be emitted. G7: degree-one selector kernels need not extend multiplicatively. G9/G11: filtration can exceed cubic degree. G12: the constant monomial detects missing mass. G13/G15: their affine combination extends to all linear checks; nonlinear-degree coordinates must make it expensive, so these obstructions remain live. G14: not bounded pair bags. G19: signed algebraic proofs may splice exactly like flows. G20/G21: polynomial dimension at useful degree is unresolved. G22: branching-program compression may admit entangled states.

**Falsification.** An integral truncated pseudo-homomorphism of low norm, or superpolynomial Macaulay width.

**Smallest experiment.** Build the full squarefree degree-4 Macaulay matrix for the eight-clause three-variable contradiction and compare exact CVP minima by degree weighting.

**Likely death.** Necessary degree is linear, making the representation exponential.

---

### 6. Delaunay-shell Boolean forcing

**Core trick.** Search for a rational positive-definite Gram matrix whose empty Delaunay ellipsoid has exactly the legal local or bag encodings as nearest lattice points, with all signed selectors, zero labels, and splice states on a provably later shell. Unlike residual amplification, this attacks unrestricted coefficients directly through Voronoi geometry. Classical hook: Voronoi’s reduction theory (1908).

**Expected move.** Obtain a composable “Booleanity radius”: every vector below a fixed shell is honest, after which clause residuals can safely receive polynomial weight.

**Obstruction audit.** G1: no slack. G2/G3: strengthens finite affine isolation geometrically. G5: composition is not automatic; clique-sum Delaunay preservation must be proved. G6: the Gram factor and target are emitted, with unrestricted CVP. G7 and G9/G11: their signed kernels are explicitly competing lattice points. G12: zero/drop states are included in the shell search. G13/G15: affine lifts are not annihilated; they must lie beyond the shell. G14: can start from pair-bag vertices but needs recursion. G19: splice states must also be enumerated. G20/G21: no growing shell-ratio family is known. G22: no tensor assumption unless products are introduced.

**Falsification.** SDP infeasibility or any G7/G13/G19 point forced onto the honest shell.

**Smallest experiment.** Solve an exact rational SDP/LP for one clause and then two overlapping clauses, with all coefficients in \([-2,2]\) as designated competitors.

**Likely death.** Equal-radius completeness forces a nearby affine lattice point or only a constant shell ratio.

---

### 7. Alternating, rather than tensor, composition

**Core trick.** Encode each gadget port by a small vector space and attach exterior-power coordinates recording oriented collections of ports. Honest substitutions remain decomposable wedges, whereas repeated, spliced, or affinely mixed histories often lose their top Plücker coordinate through cancellation or become nondecomposable.

**Expected move.** Establish a depth-two identity in which illegal exterior mass multiplies under substitution while honest radius grows only additively; recurse for \(O(\log n)\) depth.

**Obstruction audit.** G1: no slack. G2/G3/G5: ports and overlap require a new explicit composition contract. G6: Plücker relations cannot be imposed externally; only precomputed column wedges are legitimate. G7: its linear kernel may have nonzero wedge fingerprint. G9/G11: exterior degree can grow. G12: dropping a factor kills top-degree mass and must be priced. G13/G15: their affine lift still exists and may cancel all wedges, so not outside those obstructions. G14: could use pair bags as base gadgets but gains no theorem from the finite pass. G19: signed splices may be detected by oriented history wedges. G20/G21: multiplicative excess is precisely the unproved claim. G22: alternating powers reduce some decomposable tensors but arbitrary entangled lattice vectors remain fully live.

**Falsification.** Any depth-two entangled vector below the proposed product contract.

**Smallest experiment.** Add all \(2\times2\) minors of port fingerprints to two overlapping Generation-14 bags and exactly enumerate the unrestricted shell.

**Likely death.** Plücker coordinates linearize into new signed columns, recreating cheap entangled cancellations.
