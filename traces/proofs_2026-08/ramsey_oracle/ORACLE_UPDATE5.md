# Sixth-call focused wall: maximum separated permutation families

Five calls have now produced and tested four routes. The latest theorem rigorously shows only that the **greedy degree guarantee** for permutation orbits is fixed-base: for every triangle-free graph `H` on `n` vertices, with reflexive nonadjacency matrix `M`, `per(M)>=n!/C^n`, `C<5.38`. It does **not** bound the maximum separated permutation family.

Define `F subset S_n` to be `H`-separated if for every distinct `pi,sigma in F` there is a position `i` with `pi(i)sigma(i) in E(H)`. Coloring a pair by such a position is triangle-free, so a family of size `n^{Omega(n)}` for some explicit triangle-free `H_n` would immediately give the target using `n` colors. Equivalently, `F` is independent in the graph on `S_n` joining pairs that are coordinatewise equal-or-nonadjacent in `H`.

Small permanent diagnostics were poor, but they say nothing decisive about independence number. The exact conceptual wall is now:

1. Is there a universal upper bound `|F|<=C^n` for every triangle-free `H` and every separated `F`? If yes, prove it by a genuine clique/fractional-cover/entropy/injection argument, not merely maximum degree. A natural hope is a distribution over bad cliques/cylinders that fractionally covers `S_n` with exponential total weight.
2. If no, give one explicit classical triangle-free family `H_n` and a precise construction/probabilistic argument yielding `|F|=n^{Omega(n)}`. Hidden use of an equally strong Ramsey coloring is circular.

Please focus exclusively on resolving this permutation-family question. An honest structural reduction with one sharply stated nontrivial lemma is useful only if accompanied by a credible proof route; do not propose unrelated families or restate the original problem. The forbidden recent document and all descriptions of it remain strictly off-limits.