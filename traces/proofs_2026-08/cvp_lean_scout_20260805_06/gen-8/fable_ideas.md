I did not consult the prohibited document or related material. The mechanisms below target U0 only; finite experiments are falsifiers, while any asymptotic promotion must be a Lean theorem.

1. **Make U0 a quantified Lean statement before testing it**

**Mechanism / move.** U0 is presently under-specified: \(C_S\), “finite refinement,” “bounded-width expansion,” and the four normal forms are not formal objects. Amend it to `U0*`: for every fixed color bound \(q\), equality-gadget width \(w\), and fixed block templates \(T\), there is \(S_0\) such that no marked expansion of \(D_S\) with parameters \((q,w)\) is \(T\)-n-fold, generalized n-fold, tree-fold, or two-stage.

**Falsification.** An admissible expansion not represented by the definitions, or a uniform template and certificate representing every tested \(D_S\).

**Smallest experiment.** Serialize \(C_8\); implement Lean predicates for markings, equality-gadget contraction, and one two-stage normal form; check a Python-produced certificate in Lean.

**Likely death.** “Bounded-width expansion” may permit arbitrary long width-two wiring, making U0* false unless locality or bounded interpretation depth is added.

**Obstruction audit.** RS slack G1, filtered quotient G6, radix kernel G7; signed/affine G2–3,G5,G9,G11,G13,G15,G19; DROP G12/Goal-G8; composition G14,G28,G31,G32,G37,G38; G30; G33–34; D4 Goal-G3–5; E6 Goal-G6–7; Goal-G1–2/G19 splices; Goal-G11–12, affine COPY, toric exchange; Gen-4 seam, Gen-5 flip, Gen-6 Beneš, Gen-7 ghosts/cycle; and carry/lumpability are metric-soundness issues, outside U0*. Markov-versus-Graver is unused. Fixed-block tractability and marking are explicitly formalized.

2. **Recursive separator profile versus detector expansion**

**Mechanism / move.** Define a marked recursive separator number: the least \(k\) such that every induced substructure has a balanced separator of at most \(k\) marked row/column vertices, recursively for the fixed tree-fold depth. Prove in Lean that each fixed-template normal form has bounded profile, while the detector incidence graph of \(D_S\) has profile \(\Omega(S)\) by an explicit vertex-expansion certificate; bounded local equality gadgets change it only by \(f(k,w)\).

**Falsification.** A separator of constant size in the serialized detector graph, or a fixed-class matrix family with unbounded profile.

**Smallest experiment.** For \(S=8,16,32\), contract equality-only vertices and solve minimum balanced vertex separator by MILP.

**Likely death.** Generalized n-fold may not satisfy the proposed recursive separator bound, requiring four separate invariants rather than one.

**Obstruction audit.** G1/G6/G7; affine-signed G2–3/G5/G9/G11/G13/G15/G19; DROP G12/Goal-G8; G14/G28/G31/G32/G37/G38; G30; G33–34; D4 Goal-G3–5; E6 Goal-G6–7; Goal-G1–2 and G19 splices; Goal-G11–12, affine COPY, toric exchange; Gen-4 seam, Gen-5 physical flip, Gen-6 Beneš exchange/marking, Gen-7 ghosts/COPY cycle; carry/lumpability are outside because this proves only structural nonmembership. Markov≠Graver is not invoked. The fixed-block obstruction is attacked directly, with signed-permutation markings preserved.

3. **Coding-theoretic tree complexity of \(\ker D_S\)**

**Mechanism / move.** Reduce modulo a fixed prime \(p\) and view  
\[
K_S=\{(C_Sz,z):z\in\mathbb F_p^m\}
\]
as a marked linear code. Fixed-block forms should admit bounded-state tree realizations: every cut exposes only \(O_{T}(1)\) syndrome dimensions. Prove a Lean lemma that puncturing/shortening bounded-width equality extensions cannot turn a code with linear branch complexity into bounded complexity; certify linear complexity from detector expansion.

**Falsification.** A low-state tree realization of \(K_{32}\), or failure of bounded complexity for one claimed fixed-block class.

**Smallest experiment.** Build \(K_8,K_{16}\) over \(p=3\); enumerate branch decompositions for \(K_8\), then use rank lower bounds for \(K_{16}\).

**Likely death.** The identity coordinates may permit unexpectedly cheap realizations, or generalized n-fold codes may themselves have growing branch complexity.

**Obstruction audit.** G1/G6/G7, G2–3/G5/G9/G11/G13/G15/G19, DROP G12/Goal-G8, G14/G28/G31/G32/G37/G38, G30, G33–34, D4 Goal-G3–5, E6 Goal-G6–7, Goal-G1–2/G19 splices, Goal-G11–12/affine-COPY/toric exchange, Gen-4 seam, Gen-5 flip, Gen-6 Beneš, Gen-7 ghosts/cycle, and carry/lumpability concern Euclidean soundness, absent here. No Markov-to-Graver inference occurs. Fixed-block tractability is tested through code complexity; markings become distinguished coordinates.

4. **A marked matroid minor obstruction**

**Mechanism / move.** Search for a canonical marked minor of the column matroid of \(D_S\) isomorphic over \(\mathbb F_p\) to the cycle matroid of the growing detector expander. Prove separately that matroids of each fixed-template class have bounded branch-depth after deleting a bounded template-dependent marked set, and that equality auxiliaries are only controlled extensions/coextensions. Unbounded expander branch-width would prove U0.

**Falsification.** The proposed detector minor does not exist, or one fixed-block class contains expander matroid minors with fixed templates.

**Smallest experiment.** For \(S=8\), use Sage/Python exact elimination to exhibit every deletion/contraction in the minor certificate; write a Lean checker for the resulting rank equalities.

**Likely death.** The identity block may collapse the desired minor, and bounded-width auxiliary equalities may be more general than controlled matroid extensions.

**Obstruction audit.** RS/quotient/radix G1/G6/G7; signed-affine G2–3/G5/G9/G11/G13/G15/G19; DROP G12/Goal-G8; composition G14/G28/G31/G32/G37/G38; G30; exterior G33–34; D4 Goal-G3–5; E6 Goal-G6–7; Goal-G1–2/G19 splices; Goal-G11–12, affine COPY, toric exchange; Gen-4 seam, Gen-5 flip, Gen-6 Beneš, Gen-7 ghosts/cycle; carry/lumpability are outside this representability claim. Markov≠Graver is irrelevant. Fixed-block tractability is precisely the bounded-minor assertion; marked elements cannot be silently permuted away.

5. **Model-theoretic obstruction via twin-width**

**Mechanism / move.** Regard \(D_S\) as a finite colored relational structure encoding nonzero coefficients, row/column sort, and markings. Fixed-template block substitution and bounded-depth equality-gadget interpretations plausibly have twin-width bounded by \(f(T,q,w)\), whereas explicit bounded-degree detector expanders have unbounded twin-width. State both closure and detector lower-bound lemmas in Lean rather than relying on recognition heuristics.

**Falsification.** A bounded-width contraction sequence for detector sizes \(8,16,32\), or an unbounded-twin-width family inside a fixed claimed normal form.

**Smallest experiment.** Encode the marked incidence graphs into an exact twin-width SAT solver; find optimum contraction width for sizes \(8\) and \(16\).

**Likely death.** Arbitrary tree-fold incidence structures or coefficient colors may already have unbounded twin-width; equality expansion may not be a bounded-depth interpretation.

**Obstruction audit.** G1/G6/G7; G2–3/G5/G9/G11/G13/G15/G19; G12/Goal-G8; G14/G28/G31/G32/G37/G38; G30; G33–34; D4 Goal-G3–5; E6 Goal-G6–7; diagonal/A5/G19 splices; Goal-G11–12, affine COPY, toric exchange; Gen-4 seam, Gen-5 physical flip, Gen-6 Beneš exchange, Gen-7 ghosts/COPY cycle; carry/lumpability all concern soundness or prior gadgets, not relational class membership. Markov-versus-Graver is unused. Fixed-block tractability is attacked through a closure invariant, and markings are relation symbols.

6. **Rigidity versus forced block symmetries**

**Mechanism / move.** Use an explicit rigid detector graph, so the marked automorphism group of \(D_S\), after contracting equality gadgets, is trivial. Prove a finite-template pigeonhole theorem: sufficiently large n-fold, two-stage, or bounded-depth tree-fold structures with finitely many colors contain two indistinguishable sibling blocks, hence a nontrivial marked automorphism. A valid representation would transfer that symmetry back to \(D_S\), contradiction.

**Falsification.** A nontrivial automorphism of the actual detector serialization, or a rigid arbitrarily large fixed-template normal form.

**Smallest experiment.** Compute color-preserving automorphism groups of contracted \(D_8,D_{16},D_{32}\) with nauty; separately generate all small two-stage templates and check the forced-swap claim.

**Likely death.** Global coupling rows can distinguish every brick without changing the nominal fixed template, or auxiliary equality gadgets can destroy symmetry. Then U0 must restrict admissible expansions more sharply.

**Obstruction audit.** G1/G6/G7, affine-signed G2–3/G5/G9/G11/G13/G15/G19, DROP G12/Goal-G8, G14/G28/G31/G32/G37/G38, G30, G33–34, D4 Goal-G3–5, E6 Goal-G6–7, Goal-G1–2/G19 splices, Goal-G11–12/affine-COPY/toric exchange, Gen-4 seam, Gen-5 flip, Gen-6 Beneš, Gen-7 ghosts/cycle, and carry/lumpability are outside this symmetry statement. Markov≠Graver is avoided. Fixed-block tractability is the asserted symmetry source; integral-isometry marking is enforced.

7. **Actively try to refute U0 with certified template synthesis**

**Mechanism / move.** Encode membership in each normal form as SAT/SMT variables for row/column partitions, template types, tree ancestry, and bounded-width equality gadgets. Search simultaneously across \(S=8,16,32\) for one shared template. A found certificate refutes U0’s intended edge; repeated UNSAT becomes useful only after proving in Lean a pumping lemma that any fixed template appearing at arbitrarily large sizes must already fit these three scales or repeat a forbidden boundary signature.

**Falsification.** A shared decomposition certificate is the desired refutation; failure of the pumping bound invalidates any promotion from finite UNSAT.

**Smallest experiment.** Start with two-stage form, \(q,w\le2\), on \(D_8,D_{16}\); emit a certificate checked by a small Lean verifier.

**Likely death.** The pumping threshold may depend enormously on the unknown template, so no finite scale set is complete.

**Obstruction audit.** G1/G6/G7; signed-affine G2–3/G5/G9/G11/G13/G15/G19; DROP G12/Goal-G8; G14/G28/G31/G32/G37/G38; G30; G33–34; D4 Goal-G3–5; E6 Goal-G6–7; Goal-G1–2/G19 splices; Goal-G11–12, affine COPY, toric exchange; Gen-4 seam, Gen-5 physical flip, Gen-6 Beneš, Gen-7 ghosts/COPY cycle; carry/lumpability do not constrain syntactic recognition. Markov-versus-Graver is not used. Fixed-block tractability is tested directly rather than inferred; all markings and permitted expansions are solver variables.
