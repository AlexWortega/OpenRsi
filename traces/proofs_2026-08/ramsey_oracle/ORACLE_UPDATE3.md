# A concrete post-failure mechanism to referee or generalize

After recording both failures in ORACLE_BRIEF.md, I derived this explicit local-palette rule.

Vertices carry `(z,B,h)`, where `z in {0,1}^t`, `B` is an r-subset of a polynomial universe U, and `h:B->{0,1}`. Global colors are t core colors plus U; local palette size at most t+r. For a pair:
1. if z differs, use its first differing coordinate (standard triangle-free rule);
2. if z agrees, require an x in B∩B' with h(x)≠h'(x), and color by such an x.
A monochromatic core triangle is impossible by first difference. A monochromatic x triangle would require three binary h(x) values pairwise different, impossible. Thus it is valid provided each fixed-z family consists of pairwise-conflicting partial Boolean assignments.

But this binary version cannot grow: each partial assignment on r coordinates defines a codimension-r subcube of `{0,1}^U`; pairwise conflict means these subcubes are disjoint, so each z-class has size at most 2^r. With t=O(r), total order is only exp(O(r)), not factorial.

A natural generalization assigns each incidence x a state in a triangle-free graph H_x and colors a same-z pair by x when their states are adjacent in H_x. Monochromatic x triangles remain impossible. However, on a common fixed domain this is exactly an OR-power clique / strong-complement code, risking circularity with the original problem. Varying domains might conceivably add factorial entropy, but the binary cylinder packing shows the simplest case does not.

Please adversarially determine whether varying-domain partial H-assignments can provably yield `exp(Omega(r log r))` pairwise separated objects with: domain size r, universe/poly state size polynomial in r, and an explicit triangle-free H; or prove a general packing obstruction for this whole mechanism. If neither, propose at most one genuinely explicit alternative with a proved nontrivial ingredient. Do not offer an existence CSP or desired lemma. Forbidden-document constraint remains absolute.
