I use **O1–O8** for: bounded signatures; marginal/tableau encodings; local-view hierarchies; phase lifts; integer exact fibers; complete-assignment fingerprints; tensor amplification; exact syndrome-to-CVP transfer. Every experiment below should enumerate the entire pointed image code, not merely pure witnesses.

1. **Congruence-tower nonabelian holonomy lift**

**Core.** Build a formula-specific constraint complex and map its cycle words into \(\mathrm{PSL}_2(\mathbb F_p)\), choosing \(p\) so every nontrivial word up to a prescribed length survives. Lift each triple to whole-cycle columns on the resulting cover; consistent assignments select a coherent sheet, while inconsistent covers should accumulate nontrivial monodromy support.

**Obstruction audit.** O1: outside—signatures are whole unbounded-degree cycle words. O2: outside—no proper marginals or gates. O3: outside only if all cycle-basis relations are represented. O4: outside its theorem because the selector is formula-dependent and multivalued. O5: binary. O6: polynomially many lifted triples, not assignment columns. O7: no tensoring, though every mixed lift word remains relevant. O8 applies directly.

**Expected move.** Convert odd holonomy into support proportional to group displacement or conjugacy-orbit size.

**Falsification.** Any pointed kernel, or hostile cost not exceeding worst YES cost.

**Experiment.** Use \(p=5\); lift the \(q=2\) all-eight core and smallest \(q=3\) twisted cycle, then enumerate all image words and exact rank.

**Likely death.** Nonidentity monodromy guarantees nonzeroness, not Hamming spread; affine legal XORs may still remain cheap.

2. **Whole-route expander dictionary for permutation targets**

**Core.** Replace I18’s variable permutation tables by columns representing complete input-to-output routes through a fixed rearrangeable network, not local switch states. Attach unique-neighbor checks to route intersections and long path labels, so a legal permutation uses \(q\) disjoint routes while a signed virtual table should create many globally witnessed collisions.

**Obstruction audit.** O1: outside if each column contains its entire logarithmic route; local switch columns would remain inside. O2: outside only in the whole-route formulation—switch tableaus are killed. O3: paths are global, although missing route intersections would re-enter it. O4: no phases. O5: binary, avoiding affine integer slacks. O6: \(O(q^3)\) route columns, no assignment enumeration. O7: no tensor product; arbitrary route superpositions must be checked. O8 applies.

**Expected move.** Replace the \(3q\) table baseline by \(q\) routes while making each defect hit \(\Omega(\log q)\) expander checks.

**Falsification.** A signed/odd route cover with only \(O(1)\) excess, or a legal baseline \(\Omega(q\log q)\).

**Experiment.** Pad \(q=3\) to a four-input Beneš network; enumerate all route covers for tiny YES/NO, all-eight, and holonomy instances.

**Likely death.** Rectangle splices may exchange whole routes at constant cost.

3. **Deterministic isolation menu with BCH-protected sectors**

**Core.** Construct a polynomial menu of formula-derived weight/hash functions; each sector claims one checksum-isolated perfect matching and protects its center with a BCH shell. Unlike I10, legal witnesses are never quotiented together: they occupy separately coded sectors, and a global selector code is meant to charge cross-sector XORs.

**Obstruction audit.** O1: hashes inspect complete matchings globally. O2: outside only if sector selection is one global codeword, not bounded-fan-in routing. O3: no scope hierarchy. O4: formula-dependent selector, outside the coboundary theorem. O5: binary. O6: triples-times-hashes are polynomial; enumerating checksum centers would violate O6. O7: no tensoring; mixed sector words are the central attack. O8 applies.

**Expected move.** Remove the three-legal-witness affine-closure cheat by ensuring one sector contains only one cheap legal center.

**Falsification.** Some satisfiable instance has no isolated sector, or an odd XOR crosses sectors below the BCH distance.

**Experiment.** Freeze all affine hashes into \(\mathbb F_2^2\) for \(q=3\); build block-diagonal sectors plus a \([7,4,3]\) selector and exhaust all words on affine-closure examples.

**Likely death.** A polynomial deterministic isolation family for exponentially many witnesses is unlikely; selector superpositions may recreate the weight-nine splice.

4. **Noncommutative residual-state/Hankel code**

**Core.** Order triples canonically and regard a selected cover as a word in a free algebra. Encode it by left/right residual evaluations of the exact-cover language—equivalently, selected blocks of its Hankel matrix—so legal words have a sparse accepting residual while malformed superpositions should excite many inequivalent residual states.

**Obstruction audit.** O1: direct residuals are global, high-degree word functions. O2: a transition-by-transition ABP is inside the tableau obstruction; only direct Hankel blocks are outside. O3: no local scopes if residuals span the entire word. O4: no phases. O5: binary expansion only. O6: residual states, not complete assignments, but exponential Hankel rank would recreate O6’s size wall. O7: no tensoring; all linear combinations of residual words must be sound. O8 applies after binary expansion.

**Expected move.** Use noncommutative order sensitivity to prevent the commutative cancellations that killed I28 and affine matching quotients.

**Falsification.** Polynomial residual truncation has a pointed kernel or fails to separate all-eight/holonomy; exponential residual rank also falsifies the route.

**Experiment.** For \(q=3,m=8\), retain residuals through word length four using upper-triangular matrices over \(\mathbb F_4\), then enumerate the full image code.

**Likely death.** Exact-cover language likely has exponential Hankel rank; low-rank truncations will admit short polynomial identities.

5. **Full-pattern Möbius charts on splitter scopes**

**Core.** Mutate I27 by recording every restriction pattern on each logarithmic splitter scope, rather than features that vanish on legal matchings. In a chart separating three legal witnesses, their odd XOR occupies three pattern cells instead of disappearing; recursively encoded chart labels could turn affine-closure depth into support.

**Obstruction audit.** O1: degree \(r\) evades the all-eight cube only for \(r\ge3\); larger independently flippable cubes still trigger O1. O2: full patterns do not factor through proper marginals. O3: growing disconnected logarithmic scopes are not fully covered, though fixed/proper scopes are. O4: no phases. O5: binary. O6: coordinates are polynomially many charts, not assignments, but symbolic span construction may reproduce the fingerprint dimension wall. O7: no ordinary tensor; every mixed Schur word must be enumerated. O8 applies.

**Expected move.** Preserve YES cost at one cell per chart while forcing hostile affine combinations into many cells on many splitters.

**Falsification.** Any hostile word occupies one cell per chart, or the ANF generator rank becomes superpolynomial.

**Experiment.** Use all 3- and 4-subsets of the eight triple coordinates; compare against length-four Schur walks on the existing all-eight, holonomy, and 200-NO suite.

**Likely death.** Logarithmic charts may require \(n^{\Theta(\log n)}\) ANF rank, while constant charts retain cube trades.

6. **Code-dependent CRT–Hasse multiplication sieve**

**Core.** Represent tensor coordinates as products of formula-derived polynomials, then reduce simultaneously modulo several coprime irreducibles and their Hasse-jet powers. Choose the moduli deterministically from the reduced tensor code’s annihilator ideal, aiming for a polynomial-size hitting family whose combined multiplication maps avoid every low-support pointed secant.

**Obstruction audit.** O1: products are global and growing-degree. O2: no local wire interfaces. O3: no scope system. O4: no phase selector. O5: final maps are binary, not integer slacks. O6: polynomial algebra coordinates, not assignment columns. O7: directly targets its surviving code-dependent dense-fold opening; unlike fixed puncturing, the map depends on the code, but mixed-word soundness is wholly unproved. O8 applies to the concatenated binary image.

**Expected move.** Compress an \(n^2\) reduced tensor to \(\tilde O(n)\) residue/jet coordinates while retaining the squared YES/NO ratio.

**Falsification.** A pointed kernel, failure to beat unfurled rank exponent, or modulus selection requiring nearest-word computation.

**Experiment.** On \(q=3,m=8\), enumerate irreducibles of degrees \(2\)–\(5\), jet orders \(1,2\), greedily select using only star-zero-code invariants, freeze, then attack held-out families exhaustively.

**Likely death.** Bilinear multiplication has a huge secant kernel; enough moduli to remove it may restore quadratic rank.

7. **Communication-complexity pointer lift**

**Core.** Replace every triple coordinate by an explicit logarithmic-size index/inner-product gadget and retain the gadget’s complete character table. A legal matching chooses one consistent pointer per vertex; the hoped-for lemma is that an inconsistent odd cover induces many nonzero character blocks by low discrepancy or high partition rank.

**Obstruction audit.** O1: gadget degree is \(O(\log n)\); cubes of larger dimension still satisfy O1 relations. O2: outside only when the complete character table is retained—proper projections are killed. O3: gadgets couple distant endpoints, but a bounded collection of scopes may still miss holonomy. O4: no phases. O5: binary. O6: triple-pointer dictionary is polynomial because the gadget has \(O(\log n)\) bits; no assignment columns. O7: not tensor amplification, though all mixed gadget words matter. O8 applies.

**Expected move.** Turn one exact-cover collision into \(n^\varepsilon\) nonzero character coordinates while keeping each legal pointer choice polylogarithmically sparse.

**Falsification.** Worst YES character support exceeds best NO support, or discrepancy yields only average correlation rather than minimum Hamming support.

**Experiment.** Use a three-bit inner-product gadget on each \(q=3,m=8\) triple; retain all eight characters and enumerate exact images for YES/NO, affine-closure, all-eight, and holonomy cases.

**Likely death.** Fourier spread is not a minimum-support guarantee; affine XORs may concentrate in one character block.
