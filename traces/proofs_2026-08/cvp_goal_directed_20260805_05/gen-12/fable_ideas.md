The canonical eight-selector \( \mathbb F_{289}\) template is retired below; none of these mechanisms lifts it unchanged.

1. **\(17\)-adic Smith barrier from redundant signatures**

**Core/expected move.** Replace one-selector-per-truth-word by \(N\leq16\) redundant binary signatures, chosen so every false port fiber has a large \(17\)-primary Smith invariant. Under substitution, prove multiplicativity of this invariant through block elimination, forcing either a \(\mathfrak P^h\) defect or coefficient energy comparable to \(17^h\).

**Obstruction audit.** G1/G6/G7/G12-DROP: no slack, filters, or radix; all rows are emitted. G2/G3/G14/G31/G38: requires an all-\(h\), saturated SNF theorem, not finite shells. G5/G9/G11/G13/G15 and G19/GD1/diagonal splice: not outside—they are precisely the false fibers to audit. G28/G32/G37: Smith multiplication, not min-plus or additive copying. G30: no tensor. GD2/A5: coefficients stay in a division order. G33/G34: no tags or Gram repair. D4 midpoint/non-antipodal/recombination: no shell geometry. E6 bounded/unbounded affine-port: no Delaunay port map.

**Smallest experiment.** Enumerate multiplicity vectors of the 16 binary coordinate signatures for \(N\le16\); require augmented rank four and saturation, then compute all false-fiber minima and the depth-two block-SNF multiplier.

**Falsification.** Any false fiber below 34, or a depth-two invariant no larger than the product of legal growth.

**Likely death.** The universal affine NAND relation survives redundancy with only redistributed energy.

---

2. **Bockstein obstruction instead of residue injectivity**

**Core/expected move.** Encode legal gate states as cocycles in the exact sequence
\[
0\to\mathfrak P^k/\mathfrak P^{k+1}\to\mathcal O/\mathfrak P^{k+1}\to\mathcal O/\mathfrak P^k\to0.
\]
Design the gate so every false boundary has nonzero connecting class; recursive substitution becomes a Yoneda product, placing the depth-\(h\) obstruction in filtration \(h\).

**Obstruction audit.** G1/G6/G7/G12: all cochain, boundary, and lift equations are emitted. G2/G3/G14/G31/G38: the target is an exact chain identity for all coefficients, not bounded enumeration. G5/G9/G11/G13/G15: not outside; their affine classes must have nonzero Bockstein. G19/GD1/diagonal splice: included as arbitrary cocycles. G28/G32/G37: composition is extension multiplication, not min-plus/additivity. G30: no tensor. GD2/A5: no convolution; \(\mathcal O\) remains division. G33/G34 and all D4/E6 obstructions: no metric tags, shells, or affine shell ports.

**Smallest experiment.** Model \(\mathcal O/\mathfrak P^2\) as the skew dual-number ring over \(\mathbb F_{289}\); enumerate width-\(\le8\) chain complexes and compute Bocksteins for all legal and false NAND boundaries.

**Falsification.** A false grade-zero cocycle with zero Bockstein, or a nonzero class whose depth-two Yoneda square vanishes.

**Likely death.** Linearity may force the connecting map to vanish on the canonical affine collision.

---

3. **Ore–Rees leading-word separator**

**Core/expected move.** Amend the coefficient algebra from \(\mathcal O\) to the truncated skew-word module \(\mathcal O\langle X,Y;\sigma\rangle_{\le h}\), with coefficientwise positive trace energy. Assign distinct noncommuting words to branch choices so a false root has an uncancellable leading word carrying \(\mathfrak P^h\), while \(h=O(\log m)\) keeps the word basis polynomial.

**Obstruction audit.** G1/G6/G7/G12: every coefficient and truncation boundary is emitted; no free carry. G2/G3/G14/G31/G38: requires symbolic leading-term injectivity for arbitrary coefficients. G5/G9/G11/G13/G15 and G19/GD1/splice: not outside; cancellation by these classes is the main test. G28/G32/G37: word order replaces fixed min-plus composition. G30: direct sums of words, not literal tensors. GD2/A5: an Ore domain replaces group-ring convolution, although truncation must be audited for new nilpotents. G33/G34 and D4/E6: no synthesized Gram, shell, or affine shell map.

**Smallest experiment.** Use the seven words of degree at most two in two letters over \(\mathbb F_{289}\); enumerate redundant NAND columns and test all false boundaries by noncommutative Gröbner reduction plus exact integer lifting.

**Falsification.** Any zero-leading-word signed pseudosection, especially a diagonal embedding at depth two.

**Likely death.** Truncation creates annihilators, or the word count makes legal energy grow at least as fast as adverse energy.

---

4. **Alternating-prime quaternion filtration**

**Core/expected move.** Amend the single-prime edge to a definite quaternion algebra ramified at \(\infty,17,19,23\), coloring circuit levels cyclically by its three two-sided prime ideals. A false computation must then enter
\(\mathfrak P_{17}^{a}\mathfrak P_{19}^{b}\mathfrak P_{23}^{c}\), whose norm grows by the product of the level primes rather than one repeatedly vulnerable residue representation.

**Obstruction audit.** G1/G6/G7/G12: CRT components, carries, and boundaries are all coordinates. G2/G3/G14/G31/G38: needs a uniform ideal-product theorem, not finite extrapolation. G5/G9/G11/G13/G15 and G19/GD1/splice: not outside; each integral affine class must fail at some colored prime. G28/G32/G37: multiplicative ideal norm, not additive transfer. G30: no tensor. GD2/A5: the ambient algebra is still division, not a group ring. G33/G34 and D4/E6: canonical trace form; no tags, shells, or affine shell ports.

**Smallest experiment.** Enumerate \(N\le12\) modules simultaneously over \(\mathbb F_{17^2}\), \(\mathbb F_{19^2}\), and \(\mathbb F_{23^2}\); intersect their integral false fibers by CRT and audit a three-level composition by SNF.

**Falsification.** One common integral grade-zero pseudosection at all three primes.

**Likely death.** The affine relation is integral and therefore survives every residue characteristic; the larger trace baseline may erase all norm gain.

---

5. **Presburger/Graver refutation by affine-clone closure**

**Core/expected move.** Try to refute the FRONTIER: prove that every constant-size equality-only NAND/COPY library with linear ports is closed under integral affine combinations strongly enough to recursively lift
\[
111=-001+011+101
\]
into a zero-defect false-root section. Quantifier elimination or a Graver bound would then give an explicit adverse-energy recurrence contradicting \(17^h\) coercion.

**Obstruction audit.** G1/G6/G7/G12 are irrelevant because the witness has exact zero residual. G2/G3 are addressed by an unbounded Presburger theorem, not boxed search. G5/G9/G11/G13/G15 and G19/GD1/splice are not escaped—they are the proposed universal witness. G14/G31/G38 cannot rescue a constant gate if affine closure is proved compositionally. G28/G32/G37: the goal is a symbolic recurrence, not finite min-plus evidence. G30 and GD2/A5: no tensor or convolution assumed. G33/G34, D4, and E6: metric/shell choices cannot charge an exact equality fiber except through anchor energy.

**Smallest experiment.** Generate the recursive affine witness through depths \(1\)–\(4\) for every surviving \(N\le16\) redundant signature module; compute exact support, negative count, and energy recurrence.

**Falsification.** Hidden boundary coordinates prevent the affine witness from gluing, or its energy grows at least \(17^h\).

**Likely death.** The theorem may cover only common affine encodings, while a viable library uses level-dependent hidden interfaces.

---

6. **Bruhat–Tits geodesic coercion**

**Core/expected move.** Amend scalar quaternion recursion to rank-two \(\mathcal O_{\mathfrak P}\)-lattices: encode bits as oriented edges in the Bruhat–Tits tree of \(\mathrm{PGL}_2(D_{\mathfrak P})\), and NAND as a constrained geodesic tripod. A false root surviving \(h\) substitutions should have Cartan displacement \(h\), hence a singular factor in \(\mathfrak P^h\), charged by the positive quaternionic Frobenius form.

**Obstruction audit.** G1/G6/G7/G12: all lattice inclusions and boundary incidences must be emitted. G2/G3/G14/G31/G38: displacement must be proved for unrestricted integral chains, not sampled paths. G5/G9/G11/G13/G15 and G19/GD1/splice: not outside; signed chains may cancel geodesic boundaries and are the decisive audit. G28/G32/G37: tree distance is nonadditive geometry, not a fixed transfer table. G30: no tensor. GD2/A5: no group-ring convolution, but \(M_2(D)\) has rank-deficient elements and therefore needs explicit bicyclic-style testing. G33/G34 and D4/E6: no Euclidean shell or affine shell port.

**Smallest experiment.** Enumerate the radius-two tree ball modulo \(\mathfrak P^3\), synthesize four legal tripods, then solve every false-boundary integral fiber and compose two tripods by SNF.

**Falsification.** A signed 1-chain with false boundary and zero Cartan displacement.

**Likely death.** Rank-one matrix couplings recreate diagonal splicing or zero-divisor fusion despite division of \(D\).
