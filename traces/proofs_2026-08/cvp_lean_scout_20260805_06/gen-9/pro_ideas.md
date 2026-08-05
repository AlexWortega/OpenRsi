I use this exhaustive obstruction grouping in every sketch:

- **S — soundness/gadget map:** G1 RS slack; G2–3 affine isolation; G5 private overlap; G6 filtered quotient; G7 radix; G9/G11/G13 parity–affine collisions; G12 and Goal G8 DROP; G14–15 bags/laminar lift; G19 signed flow; G28 recurrence; G30 isometry; G31–32/G37 Walsh additivity; G33–34 exterior failure; G38 splitter bags; Goal G1–2 splice/\(A_5\); Goal G3–5 \(D_4\); Goal G6–7 \(E_6\); Goal G11–12 grade-zero/redundant NAND; affine COPY; toric exchange; and Generations 4–7 seam, physical flip, Beneš, ghosts/COPY-cycle.
- **R — recurrence/classification map:** carry/lumpability and Markov-versus-Graver.
- **T — frontier map:** fixed-block tractability and Generation-8 support-only/row-basis sensitivity.

## 1. Finite-field code branch-width

**Mechanism.** Regard \(D_S=[I\mid-C_S]\bmod p\) as a linear code/matroid and measure its marked branch-width. Unimodular row rebasing preserves this object, while faithful equality expansion retains the old matroid as a minor.

**Expected move.** Prove in Lean: each fixed-template \(n\)-fold, generalized \(n\)-fold, tree-fold, or two-stage family has template-bounded branch-width, but the actual serializer has width \(\Omega(S^\alpha)\). This would prove U0 basis-robustly.

**Smallest experiment.** Serialize the complete actual \(C_8\), then compute exact branch decompositions and tangle-style lower certificates over \(p=2,3\); compare against generated instances of all four grammars.

**Falsification/death.** A constant-width decomposition of \(D_8,D_{16},D_{32}\), or a fixed-template family with unbounded branch-width. Identity augmentation may also collapse the intended lower bound.

**Audit.** S is outside: this asserts only U0, not distance, DROP, signed soundness, or amplification. R is outside: no recurrence or Markov inference. T is directly addressed through a row-basis invariant and minor-monotone equality-expansion argument.

## 2. Smith interface modules

**Mechanism.** For a column cut \(A\sqcup B\), let \(L=\operatorname{row}_{\mathbb Z}(D_S)\) and study
\[
J_D(A)=L/\big((L\cap\mathbb Z^A)+(L\cap\mathbb Z^B)\big).
\]
Its generator rank and Smith invariant factors measure genuinely integral information crossing the cut and are unchanged by row rebasing.

**Expected move.** Prove that every decomposition tree for the actual serializer contains a cut with growing \(J_D(A)\), whereas each of the four fixed-template classes has a template-bounded interface module. Formal progress is a Lean theorem covering bounded-width equality elimination.

**Smallest experiment.** On actual \(C_8\), enumerate balanced cuts or branch-and-bound over decomposition trees, computing exact SNFs and explicit quotient generators.

**Falsification/death.** The identity block may force all torsion trivial and leave bounded generator rank. Alternatively, generalized/tree-fold interfaces may already have unbounded \(J_D\), invalidating the class-side theorem.

**Audit.** S is outside because no CVP soundness claim is made. R is outside because no state recurrence or primitive generation is used. T is directly addressed: SNF data are row-basis robust, and equality gadgets must receive a proved interface-module closure bound.

## 3. Row-lattice automorphism rigidity

**Mechanism.** Define the marked automorphism group by column permutations \(P\) satisfying
\[
\operatorname{row}_{\mathbb Z}(D_S)P=\operatorname{row}_{\mathbb Z}(D_S).
\]
Fixed finite-type block templates should force large repeated-brick orbits, while an asymmetric universal detector may have only bounded automorphism orbits.

**Expected move.** Prove a Lean dichotomy: sufficiently large instances of each fixed-template grammar possess a same-colored orbit of size \(\Omega(S)\), but the actual \(D_S\) has no such orbit. Also prove that permitted finite refinements and faithful bounded-width equality gadgets cannot erase the forced orbit structure.

**Smallest experiment.** Compute exact marked row-lattice automorphism groups for actual \(C_8,C_{16}\), verifying candidate permutations by integer row-lattice equality rather than support alone.

**Falsification/death.** Fixed tree-fold templates can be built on asymmetric trees, or legal markings may destroy all large automorphism groups. Equality expansions may also break syntactic symmetries without changing tractability.

**Audit.** S is outside: symmetry says nothing about adverse vectors or distances. R is outside. T is directly confronted with a row-lattice, not displayed-support, invariant; the main unresolved obligation is a separate theorem for each of the four classes.

## 4. Proof-carrying grammar recognition

**Mechanism.** Avoid guessing an invariant: formalize the four target classes and permitted color/equality transformations as inductive Lean datatypes. A recognizer must return either a decomposition proof object or a checkable bounded-width obstruction certificate.

**Expected move.** A found reusable decomposition refutes U0; otherwise finite certificates should suggest a parametric obstruction from which Lean can prove that no grammar derivation exists for any \(S\). The four classes are tested separately, preventing one vague “treewidth” argument from standing in for U0.

**Smallest experiment.** For actual \(D_8\), search widths \(1\)–\(4\), including bounded equality gadgets and bounded row rebasings with \(U,U^{-1}\in\{-1,0,1\}\). Replay every successful parse or local no-parse certificate in Lean.

**Falsification/death.** The exact literature grammars may not admit a complete practical recognizer; finite no-parses do not imply an asymptotic theorem. State explosion is likely even at \(S=16\).

**Audit.** S and R are outside because this is pure representation recognition. T is addressed literally rather than through support proxies, including the Generation-8 rebasing attack. Beyond-FINITE progress occurs only when a parametric Lean no-derivation theorem compiles.

## 5. Preprocessing-closed canonical-row-space amendment

**Mechanism.** Replace U0 by \(U0^\ast\): exclusion must survive polynomial-time row-lattice preprocessing, since \(Dx=0\) and \(UDx=0\) are identical for unimodular \(U\). Use a canonical row-Hermite representative, with marked column order handled explicitly, as the first test object.

**Expected move.** If canonical representatives admit bounded fixed-template decompositions, refute the roadmap edge as algorithmically irrelevant. Otherwise prove in Lean both kernel equivalence and a class-side closure theorem showing that canonicalized fixed-template systems retain bounded structural complexity.

**Smallest experiment.** Compute exact row-HNF representatives of actual \(D_8,D_{16},D_{32}\), run all four recognizers, and compare recursive separators before and after canonicalization.

**Falsification/death.** HNF may densify even easy fixed-template systems, so canonical support could fail to characterize tractability in either direction. Coefficient growth may also make the proposed closure false.

**Audit.** S and R are outside. T directly forces this amendment: the Generation-8 cumulative control demonstrates that support complexity can vanish under row rebasing, while current U0 quantifies only permutations/refinements/equality expansions. Thus strengthening the edge is explicitly obstruction-driven.

## 6. Network-matrix tractability ambush

**Mechanism.** Test whether the actual row lattice is regular, graphic, cographic, or network-matrix representable after objective-preserving variable transformations. If so, the separable quadratic objective may reduce to convex min-cost flow even when all four named fixed-block recognizers reject it.

**Expected move.** Either construct a parametric network representation, refuting U0 as an adequate tractability gate, or prove a parametric excluded-minor/nonregularity certificate in Lean and add network matrices as a fifth explicitly closed class.

**Smallest experiment.** On actual \(D_8\), test total unimodularity exactly, search for small determinant-\(\ge2\) minors, and run graphic/cographic/network recognition while tracking which columns carry the Euclidean objective.

**Falsification/death.** A tiny nonunimodular minor may kill the network hypothesis immediately, leaving only a modest extra exclusion lemma. Conversely, a network representation may fail because the transformation does not preserve the marked separable objective.

**Audit.** S is outside: no hardness or soundness is claimed, and the full objective is retained rather than filtered, so G1/G6/G7 are not evaded. R is outside. T motivates the amendment because U0 expressly excludes only four classes and Generation 8 already exhibited row-equivalent tree incidence.
