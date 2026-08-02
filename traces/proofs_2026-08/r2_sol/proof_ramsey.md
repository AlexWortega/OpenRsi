# Rigorous constructions and reductions for multicolor triangle Ramsey numbers

**Proposition.** For every integer `k≥1`, `R_k(3)>2^k`.

**Proof.** Identify `2^k` vertices with binary words in `{0,1}^k`. For distinct words `x,y`, color edge `{x,y}` by the least index `i∈{1,...,k}` such that `x_i≠y_i`.

Suppose three vertices `x,y,z` formed a monochromatic triangle of color `i`. Then each pair differs in coordinate `i`; thus `x_i,y_i,z_i` would be three pairwise distinct members of `{0,1}`, which is impossible. Hence this `k`-coloring of `K_{2^k}` has no monochromatic triangle. By the definition of `R_k(3)`, it follows that `R_k(3)>2^k`. ∎

This is only exponential and does not establish the requested superexponential bound.

## Further checked translation-invariant seeds

There are symmetric sum-free partitions of `Z_127 minus {0}`, `Z_251 minus {0}`, `Z_509 minus {0}`, `Z_1021 minus {0}`, and `Z_2039 minus {0}` into respectively 5, 6, 7, 8, and 9 classes. Their class sizes are respectively

`(22,34,24,26,20)`, `(52,54,32,32,40,40)`,

`(62,58,78,100,52,62,96)`, `(122,110,124,192,144,132,92,104)`, and

`(120,268,224,242,154,230,228,232,340)`.

The explicit classes are stored in the corresponding `experiments/cyclic_<p>_<k>.json` files. Color an edge `xy` by the class of the difference `y-x mod p`; symmetry makes this well-defined for unordered edges, and sum-freeness excludes a monochromatic triangle. `verify_cyclic_colorings.py` checks these properties and all vertex triangles.

Thus there are triangle-free `k`-colorings of `K_p` for `(p,k)=(127,5),(251,6),(509,7),(1021,8),(2039,9)`. Their per-color bases decrease from about `2.634` toward `2.332`; they are finite algebraic seeds, not superexponential progress, and are below the classical fixed-base construction quoted in the prompt.


There are sum-free partitions of `F_2^7 minus {0}` into five classes of sizes `23,25,24,22,33`, and of `F_2^8 minus {0}` into six classes of sizes `56,31,33,58,41,36`. The explicit classes are stored in `experiments/f2_7_5.json` and `experiments/f2_8_6.json`. As in the construction below, coloring `xy` by the class of `x+y` gives triangle-free colorings of `K_128` with five colors and `K_256` with six colors. The script `verify_f2_partitions.py` checks the partitions, sum-freeness, and respectively all 341,376 and 2,763,520 vertex triangles.

These finite seeds still have no asymptotic value beyond a fixed exponential base. Their per-color bases are `128^(1/5) approximately 2.639` and `256^(1/6)=2^(4/3) approximately 2.520`; even the better first value is below the classical fixed exponential base quoted in the problem statement. They are useful only as new algebraic search data, not as progress toward superexponential growth.

A SAT search for a compressed two-block rule found no improvement: it produced a 10-color sum-free partition of `F_2^14 minus {0}` from the five-color `F_2^7` seed, exactly matching disjoint-palette composition. The rule colors each nonzero pair of seed states `(a,b)` by a lookup table; `verify_block_composition.py` directly checks all 44,731,051 projective lines in `F_2^14`. Attempts with eight and nine output colors did not yield a verified construction; no impossibility is claimed.

A previously recorded three-block 13-color state rule is **invalid**. The search and verifier incorrectly discarded realizable projective lines whenever two coarse block-state vectors coincided. Underlying vectors `x,y,x+y` can be distinct while their state vectors repeat. For example, the archived rule in `experiments/invalid/block_power_3_13.json` colors the distinct vectors `16384,196608,212992` identically. The negative audit `verify_retracted_block_power_3_13.py` verifies this explicit monochromatic witness and exits successfully; the corrected search now includes repeated-state constraints. All constructions recursively derived from that rule were also removed from the claimed results. No correlated palette compression is currently verified.

## A checked three-color base construction

**Proposition.** There is a triangle-free three-coloring of `K_16`. Consequently, if `k=3q+r` with `0<=r<3`, then

`R_k(3)>16^q 2^r`.

**Proof.** Identify the vertices with the vector space `F_2^4`, writing its nonzero vectors as the integers `1,...,15` in binary. Partition them into

`S_1={1,2,4,8,15}`,

`S_2={3,5,7,10,11}`,

`S_3={6,9,12,13,14}`.

Color an edge `xy` by the index of the set containing `x+y` (addition is bitwise XOR). Direct pairwise checking shows that each `S_i` is sum-free in `F_2^4`: for distinct `u,v in S_i`, the vector `u+v` does not belong to `S_i`. (For reproducibility, the finite check is recorded in `NOTES_ramsey.md`.) If a triangle `x,y,z` had color `i`, then the distinct vectors `u=x+y` and `v=x+z` would lie in `S_i`, as would `u+v=y+z`, contradicting sum-freeness. This proves the first claim.

Apply the lexicographic product lemma below to `q` copies of this coloring and `r` copies of the two-vertex one-color coloring. The resulting coloring uses `3q+r=k` colors on `16^q2^r` vertices. ∎

Its asymptotic base `16^(1/3) approximately 2.52` improves the binary baseline but remains merely exponential (and is weaker than the best classical exponential constructions cited in the problem statement).

A second finite vector-space seed is useful for checking the algebraic search framework.

**Proposition.** There is a triangle-free four-coloring of `K_32`.

**Proof.** In `F_2^5`, partition the nonzero vectors (written as integers in binary) into

`T_1={3,5,7,14,18,22,26,27}`,

`T_2={9,11,12,13,23,25,29}`,

`T_3={2,6,15,17,20,24,31}`,

`T_4={1,4,8,10,16,19,21,28,30}`.

Each `T_i` is sum-free: for distinct `a,b in T_i`, the XOR `a+b` does not lie in `T_i`. Color edge `xy` by the class containing `x+y`. As in the `K_16` proof, a monochromatic triangle would give `u,v,u+v` in one sum-free class, impossible. ∎

This seed has per-color base `32^{1/4} approximately 2.378`, worse than the `K_16` seed. Numerically its parameters are exactly those of the lexicographic product of the `K_16` seed with a one-color `K_2` (`32=16*2`, `4=3+1`), so it gives no improvement even for residue classes. Its value is only as an independently checkable finite construction and as a test case for automated searches. It is not the translation-invariant direct-product partition: its difference-class sizes are `8,7,7,9`, whereas that product has sizes `10,10,10,1` (up to permutation). Thus it is structurally distinct despite identical parameters.

It also cannot be extended rigidly to `F_2^6` while preserving these four color classes on the hyperplane `F_2^5 times {0}`.

**Computational lemma (fixed-layer nonextension).** There is no assignment of four colors to the 32 vectors `(y,1)` such that, together with the displayed coloring on `(x,0)`, every projective line `{u,v,u+v}` is nonmonochromatic.

**Verification method.** A line not already contained in the fixed hyperplane has exactly two vectors `(y,1),(z,1)` and their sum `(y+z,0)`. Thus assigning both layer-one vectors color `c` is forbidden exactly when `y+z in T_c`. This is a finite constraint problem on 32 variables. A complete minimum-remaining-values backtrack tried all four colors for `(0,1)` and exhausted respectively 57, 56, 64, and 64 recursive nodes without a solution. The standard-library verification script is `verify_ramsey.py`; it reproduces node counts `[57,56,64,64]` and also checks every triangle in the `K_16` and `K_32` seeds.

This is a computer-verified nonextension of one fixed seed, not an impossibility theorem for all four-colorings of `F_2^6`. Repeated unrestricted min-conflicts searches reached one monochromatic line but never zero; that heuristic observation is not part of the lemma. The algebraic-extension route is therefore banked after two failed attempts rather than pursued as evidence of impossibility.

## Checked interval-difference seeds

For `(N,k)=(128,5),(256,6),(512,7),(1024,8),(2048,9)` there are colorings `c:{1,...,N-1}->[k]` such that no triple `a,b,b-a` (`0<a<b<N`) is monochromatic. Coloring the edge `{x,y}` of the ordered vertex set `{0,...,N-1}` by `c(|x-y|)` therefore gives a triangle-free `k`-coloring of `K_N`. The explicit rules are stored in `experiments/interval_<N>_<k>.json`; `verify_interval_difference.py` checks all difference constraints.

This is a clean translation family, but again `N=2^(k+2)` in the displayed sequence, so its base decreases to two. It is not superexponential progress.

## Checked dihedral translation seeds

For dihedral groups of orders `32,64,128,256,512,1024` there are inverse-closed product-free partitions of the nonidentity elements into respectively `4,5,6,7,8,9` classes. Coloring an unordered edge `{x,y}` by the class of `x^{-1}y` is well-defined by inverse closure; a monochromatic triangle would give two same-class elements whose product is in that class. The explicit partitions are in `experiments/dihedral_<n>_<k>.json`, where `n` denotes the rotation subgroup order. `verify_dihedral_colorings.py` independently checks inverse closure, product-freeness, and every vertex triangle.

These give triangle-free colorings of `K_32,K_64,K_128,K_256,K_512,K_1024` with `4,5,6,7,8,9` colors. This is again only a doubling family, with decreasing per-color base, so it does not imply a superexponential bound.

## Checked shifted cyclic seeds

There are layer-dependent cyclic colorings of `K_62` with five colors, `K_93` with six colors, `K_254` with six colors, and `K_381` with seven colors. Vertices are `Z_31 times [r]`, and the edge color depends on the unordered layer pair and the oriented cyclic difference. The explicit lookup rules are in the corresponding `experiments/shifted_<p>x<r>_<k>.json` files; `verify_shifted_cyclic.py` checks every triangle directly (up to 9,145,270 triangles for `K_381`).

These are correlated/non-translation finite seeds, but their per-color bases are at most `254^(1/6)≈2.517`; they have no asymptotic value yet.

## Checked multi-missing cyclic subsets

The verified cyclic seeds contain induced subsets in which every vertex misses several colors. For at least two missing colors, verified parameter triples `(N,g,t)` (order, global colors, minimum missing colors) include

`(10,5,2),(15,6,2),(25,7,2),(50,7,2),(80,8,2),(130,9,2)`.

For at least three missing colors they include `(15,7,3),(25,8,3)`. The explicit subsets are stored in `experiments/multimiss_*` and `experiments/miss3_*`; `verify_multi_missing_subsets.py` and `verify_three_missing_subsets.py` check every triangle and missing palette.

These provide richer missing-color blow-up inputs, but their relevant local-seed bases `N^(1/(g-t))` remain at most about `2.19`; no growing base results.

## A checked induced cyclic local-palette seed

The verified five-color cyclic coloring of `K_127` contains an induced `K_40` in which every vertex sees exactly four colors. The verified six-, seven-, and eight-color cyclic colorings of `K_251,K_509,K_1021` contain induced `K_60,K_100,K_160` in which every vertex sees at most respectively five, six, and seven colors. The selected vertices are stored in the corresponding `experiments/cyclic<p>_local<N>.json` files; `verify_cyclic_local_subset.py` checks all induced triangles and incident palettes. These give structured local seeds larger than the ad hoc examples below. Their iteration bases are at most `40^(1/4)≈2.515`, `60^(1/5)≈2.268`, `100^(1/6)≈2.154`, and `160^(1/7)≈2.065`, hence decrease toward two rather than grow.

## Checked local-palette seeds

There are triangle-free edge-colorings of `K_20`, `K_25`, and `K_26` using five colors globally while every vertex is incident to only four colors. There are also colorings of `K_50`, `K_55`, `K_56`, and `K_57` using six colors globally while every vertex is incident to only five colors. The explicit vertex palettes and edge colors are stored in the corresponding `experiments/local_<N>_g<g>_s<s>.json` files; `verify_local_palette_seed.py` checks every edge against both endpoint palettes, every triangle, and every actual incident palette.

These seeds illustrate genuine missing-color structure, but their parameters are not numerically valuable. The local-seed iteration below gives asymptotic base at most `57^(1/5)≈2.245`, below existing fixed seeds. They are finite search guidance, not superexponential progress.

## Missing-color blow-up lemma

A possible way beyond disjoint-palette products is to reuse colors that are absent at a vertex.

**Lemma.** Let `c` be a triangle-free coloring of `K_X` with palette `P`. For every `x in X`, let

`M_x = P minus {c(xy): y in X, y!=x}`

be the colors missing at `x`. Suppose that for each `x` there is a triangle-free coloring `d_x` of a complete graph on a vertex set `Y_x`, using only colors from `M_x`. Then there is a triangle-free coloring with palette `P` on `sum_x |Y_x|` vertices.

**Proof.** Replace each `x` by the cluster `{x} times Y_x`. Color edges inside that cluster by `d_x`; color every edge from the `x`-cluster to the `x'`-cluster by `c(xx')`.

A triangle meeting three clusters projects to a monochromatic triangle under `c` if it is monochromatic, impossible. A triangle contained in one cluster is handled by `d_x`. Finally, a triangle with two vertices in the `x`-cluster and one in the `x'`-cluster has its two cross-edges colored `c(xx')`, whereas its internal edge has a color in `M_x`; these colors differ by definition. Thus no monochromatic triangle exists. ∎

**Corollary.** With the convention `R_0(3)-1=1`, any triangle-free `k`-coloring `c` on `X` yields

`R_k(3)-1 >= sum_{x in X} (R_{|M_x|}(3)-1)`.

Indeed, independently relabel an extremal `|M_x|`-coloring onto the palette `M_x` in each cluster.

This lemma identifies a concrete route by which palette reuse can outperform ordinary lexicographic multiplication: construct a large outer coloring in which many vertices miss many colors. It is not by itself a superexponential bound; standard first-difference and translation-invariant constructions generally expose every color at every vertex, making all `M_x` empty.

It is useful to isolate the resulting local parameter. Say an edge-coloring is *locally `s`-colored* if at most `s` distinct colors occur on edges incident to each vertex.

**Corollary (local-palette reduction).** If a triangle-free `k`-coloring of `K_N` is locally `s`-colored, then

`R_k(3)-1 >= N (R_{k-s}(3)-1)`.

**Proof.** Every vertex misses at least `k-s` colors. Choose any `k-s` of them and use an extremal `(k-s)`-coloring of equal cluster size in the blow-up lemma. ∎

The first nontrivial local case can be determined exactly.

Let `L_s` be the largest number of vertices in a triangle-free complete-graph coloring that is locally `s`-colored; the global palette is unrestricted. Since an ordinary `s`-coloring is locally `s`-colored, `L_s>=R_s(3)-1`.

For comparison, the standard neighborhood recurrence is

`R_s(3)<=s(R_{s-1}(3)-1)+2`.

Indeed, at a vertex of a coloring on `s(R_{s-1}(3)-1)+2` vertices, some color occurs on at least `R_{s-1}(3)` incident edges. The corresponding neighborhood contains no edge of that color and hence is an `(s-1)`-colored complete graph large enough to contain a monochromatic triangle.

**Proposition.** For every `s>=1`,

`L_s <= 1+sL_{s-1}`,

with `L_1=2`. In particular `L_s <= s! sum_{j=0}^s 1/j! < 3s!`. Moreover `L_2=5` and `L_3=16`.

**Proof.** Fix a vertex `v` in a locally `s`-colored triangle-free coloring. Partition the other vertices into at most `s` classes according to the color of their edge to `v`. Within a class corresponding to color `i`, no edge has color `i`, since that would form a monochromatic triangle with `v`. Every vertex in the class already sees color `i` on its edge to `v`, so it sees at most `s-1` colors within the class. The coloring induced on each class is therefore locally `(s-1)`-colored and triangle-free, and each class has size at most `L_{s-1}`. This proves the recurrence. Clearly `L_1=2`. Dividing the recurrence by `s!` and iterating gives the displayed factorial bound.

The recurrence gives `L_2<=5`. Equality is attained by coloring a five-cycle red and its complementary five-cycle blue; both color classes are triangle-free. It then gives `L_3<=16`, while the explicit three-coloring of `K_16` above is locally three-colored and proves equality. ∎

Starting from `R_1(3)=3`, the ordinary recurrence and the local recurrence have identical numerical upper-bound sequence shifted by one:

`R_s(3)<=1+s! sum_{j=0}^s 1/j!`, while `L_s<=s! sum_{j=0}^s 1/j!`.

This is consistent with `L_s>=R_s(3)-1`; the local argument is a genuine extension of the same neighborhood recursion, not by itself a stronger numerical upper bound for ordinary Ramsey numbers. In particular the recurrence gives `R_2(3)<=6` and `R_3(3)<=17`; the standard `C_5` coloring and the explicit `K_16` coloring above give matching lower bounds, so `R_2(3)=6` and `R_3(3)=17` are self-contained consequences of constructions in this file.

Equality in the local recurrence is rigid at the first step.

**Lemma (equality conditions).** If a locally `s`-colored triangle-free coloring has `1+sL_{s-1}` vertices, then at every vertex `v`:

1. exactly `s` colors occur at `v`;
2. each incident color class has exactly `L_{s-1}` other vertices; and
3. the coloring induced on each such class is an extremal locally `(s-1)`-colored coloring on `L_{s-1}` vertices.

**Proof.** The proof of `L_s<=1+sL_{s-1}` partitions the other vertices into at most `s` classes, each of size at most `L_{s-1}`. Equality in their total size forces equality in every one of these inequalities. ∎

In particular, any hypothetical equality `L_4=65` would require that around every vertex the other 64 vertices split into four induced locally three-colored extremal `K_16`s. These four induced colorings need not use the same three global colors: each class merely avoids its corresponding color at `v` and uses at most three colors locally.

There are additional global consequences.

**Corollary (regular color classes under equality).** Under equality `L_s=1+sL_{s-1}`, every nonempty color graph is `L_{s-1}`-regular on its support. Consequently each support has at least `2L_{s-1}` vertices, and the number `g` of globally used colors satisfies

`g <= floor((1+sL_{s-1})s/(2L_{s-1}))`.

**Proof.** If color `a` occurs at a vertex `v`, then its incident class at `v` has exactly `L_{s-1}` vertices by the equality lemma, so the degree of `v` in color graph `G_a` is `L_{s-1}`. Thus `G_a` is regular on its nonisolated support. It is triangle-free. If its support has `v_a` vertices and degree `d=L_{s-1}`, Mantel's theorem gives `v_ad/2=|E(G_a)|<=v_a^2/4`, hence `v_a>=2d`. Finally, every vertex belongs to exactly `s` supports, so `sum_a v_a=(1+sL_{s-1})s`; combine this with `v_a>=2L_{s-1}`. ∎

For hypothetical `L_4=65`, every color graph would be 16-regular, triangle-free, and supported on at least 32 vertices, while `sum_a v_a=260`. Hence at most eight colors could occur globally. If exactly four global colors occur, every vertex sees all four and the coloring is an ordinary four-coloring of `K_65`; the equality partition says each monochromatic neighborhood has size 16 and carries an extremal three-color `K_16`. This is precisely the equality configuration for the standard vertex-neighborhood recurrence `R_4(3)<=4(R_3(3)-1)+2=66` (using `R_3(3)=17`, proved above from the neighborhood recurrence and the explicit `K_16` coloring). It therefore cannot be excluded by that recurrence alone. Any color supported on exactly 32 vertices must be `K_{16,16}`: it has `32*16/2=256=32^2/4` edges, so equality holds in Mantel's theorem, whose equality case is the balanced complete bipartite graph.

The exact edge count is consistent but useful to record. Since every color graph is 16-regular on its support, it has `8v_a` edges. Therefore

`sum_a |E(G_a)|=8 sum_a v_a=8*260=2080=binom(65,2)`.

Thus the regularity and support-incidence identity already account for every edge; edge counting adds no contradiction.

Every vertex palette is a four-element subset of the global palette, and any two such palettes intersect because their joining edge has a color incident to both. Hence the distinct palettes form an intersecting 4-uniform family on at most eight colors. If exactly eight global colors occur, complement pairing bounds the number of distinct vertex palettes by `binom(8,4)/2=35`. Since there are 65 vertices, at least one exact palette type occurs at least twice.

The case of eight global colors has further forced structure. The eight support sizes are integers at least 32 and sum to 260, only four above their minimum total 256. Therefore at least four supports have size exactly 32 (if five or more supports exceeded 32, the excess would be at least five). Each corresponding color graph is `K_{16,16}` by the Mantel equality observation. Thus a hypothetical eight-color equality example contains at least four 32-vertex complete bipartite color classes.

These bipartite classes obey a compatibility constraint. If two edge-disjoint complete bipartite graphs have supports `S,T` and bipartitions `S=A union B`, `T=C union D`, then on `S cap T` the two induced bipartitions cannot cross: one cannot find `x,y in S cap T` separated by both bipartitions, because `xy` would belong to both color classes. Equivalently, on the overlap at least one of the two restricted bipartitions is constant. To prove this, encode each overlap vertex by its two side-bits. If both bits each take both values, choose vertices with first bits 0 and 1. They must have the same second bit; comparing each with a vertex having the opposite second bit then forces both first bits to be equal, a contradiction. Hence one bit is constant. Since each side of either `K_{16,16}` has size 16, it follows that any two of these minimum-support color classes have support intersection at most 16: the overlap must lie wholly in one side of at least one bipartition. (The binary compatibility assertion was also exhaustively checked for overlap sizes up to six.)

With four minimum-support classes, encode each vertex by a word in `{0,1,star}^4`, where `star` means it lies outside that support and `0,1` denote the two bipartition sides. Each coordinate contains sixteen zeros, sixteen ones, and thirty-three stars. For every coordinate pair, among vertices non-starred in both, at least one coordinate bit is constant by the compatibility lemma. This finite constraint system is a possible SAT/ILP target. A linear-program feasibility scan over its 81 word types and all four orientation choices for each coordinate pair found a feasible aggregate solution (one vertex `****` and four groups of sixteen with patterns `**00`, `*1*1`, `001*`, and `1***`, after relabeling coordinates/bits). Thus these aggregate support/cut constraints alone cannot yield a contradiction; the remaining edge-color conditions are essential. This computation is a feasibility witness, not a proof that the full coloring exists.

This remains a necessary condition, not a contradiction. For comparison, the explicit equality examples at `s=2,3` satisfy the predicted regularity: the two color classes of the `K_5` construction are 2-regular, and each of the three color classes of the `K_16` construction is 5-regular on all 16 vertices.

Thus the local upper-bound recurrence is sharp through `s=3`. It is worth recording the canonical family having exactly the upper-bound number of vertices, even though its local palette is too large.

**Example (partial-permutation tree).** Let `T_s` consist of all ordered lists of distinct symbols from `[s]`, including the empty list. Then

`|T_s|=sum_{j=0}^s s!/(s-j)! = s! sum_{j=0}^s 1/j!`.

For two lists, inspect the first position at which they differ, treating termination as a special symbol `star`, and color their edge by the unordered pair of the two symbols seen there. This coloring is triangle-free and uses `binom(s+1,2)` colors globally.

**Proof.** The count is immediate. Consider three lists and their earliest position of disagreement, treating a terminated list as displaying `star`. If the three displayed values are distinct, the three pair-colors at that position are distinct, so the triangle is not monochromatic. If exactly two values agree, the two edges to the third list receive the same pair-label there, while the agreeing pair first differs later. That later edge cannot receive the same label: a nontermination symbol displayed earlier cannot reappear in either list, and `star` has no later coordinate. Thus again the triangle is not monochromatic. The possible labels are the unordered pairs from `[s] union {star}`, and every such pair occurs (compare one-symbol lists for two ordinary symbols, or the empty list with a one-symbol list), giving the global count. ∎

The empty list is incident to only `s` colors, but a full-length permutation is incident to all `binom(s+1,2)` colors. Thus the maximum local palette is quadratic, not `s`.

Moreover, this particular labeling admits no nontrivial deterministic compression that preserves triangle-freeness: any two distinct pair-labels occur together as the only two colors on some triangle. Hence identifying any two labels would make that triangle monochromatic.

Here is a complete case check. First suppose `A={a,b}` has no `star`.

- If `B={c,d}` is disjoint from `A`, the lists `(a)`, `(b,c)`, `(b,d)` have labels `A,A,B`.
- If `B={a,c}` shares one symbol with `A` (rename `a,b` if needed), the lists `(a)`, `(b,a)`, `(b,c)` have labels `A,A,B`.
- If `B={c,star}` with `c notin A`, the lists `()`, `(c,a)`, `(c,b)` have labels `B,B,A`.
- If `B={a,star}` (rename within `A` if needed), the lists `(a)`, `(b)`, `(b,a)` have labels `A,A,B`.

The only remaining possibility is that both labels contain `star`, say `A={a,star}` and `B={b,star}`. Then `()`, `(a)`, `(a,b)` have labels `A,A,B`. Thus merging any two distinct labels creates a monochromatic triangle. (The finite statement was also exhaustively checked for `s<=5`.)

A truncated version gives a small parameter tradeoff. Keep only lists of length at most `ell<=s`. Its order is

`N(s,ell)=sum_{j=0}^ell s!/(s-j)!`,

and its maximum local palette is

`q(s,ell)=sum_{j=0}^{ell-1}(s-j)=ell(2s-ell+1)/2`.

To count the palette at a list `p` of length `d`, comparisons first diverging at position `h<d` contribute `s-h-1` labels pairing `p_h` with a symbol not used in the common prefix. Comparisons with a proper prefix of `p` contribute the `d` labels `{p_h,star}`. If `d<ell`, extensions of `p` contribute `s-d` labels `{star,b}`; if `d=ell`, there are no extensions. Hence for `d<ell` the palette size is

`sum_{h=0}^{d-1}(s-h-1)+d+(s-d)`,

while for `d=ell` it is `sum_{h=0}^{ell-1}(s-h-1)+ell`. Both expressions are maximized at `d=ell-1` or `d=ell` and equal `ell(2s-ell+1)/2` there. For every `ell<=s`, one has `N(s,ell)<=1+ell s^ell<=2s^{ell+1}` and `q(s,ell)>=ell s/2`. Hence

`log N(s,ell)/q(s,ell) <= 2(ell+1)log s/(ell s)+2log 2/(ell s)=O(log s/s)`

uniformly in `ell`. Therefore no sequence of these truncations has unbounded `N^{1/q}`. The exact palette formula was also computationally checked for all `s<=8`.

Thus this construction explains the numerical recurrence `1+sL_{s-1}` but does **not** prove `L_s` attains its factorial upper bound for `s>=4`; even optimized truncation remains quantitatively inadequate.

Nor does one application of the missing-color blow-up rescue the full tree when the inner clusters use the binary baseline. With global palette `g=binom(s+1,2)`, a vertex at depth `d` has local palette at least `s` (the root has exactly `s`), so it misses at most `g-s` colors. There are fewer than `3s!` vertices. Therefore the total blow-up order is at most

`3s! 2^{g-s}`,

whose logarithm divided by the global palette size `g` is at most

`(log(3s!)+(g-s)log 2)/g = log 2+O(log s/s)`.

Thus this specific use remains fixed-base exponential in `g`; its many missing colors do not create a superexponential seed. The local-palette reduction with `L_2=5` gives `R_k(3)-1 >= 5(R_{k-2}(3)-1)`, whose iterated base is only `sqrt(5)`. With `L_3=16` it recovers the stronger explicit-seed recurrence.

There is a basic but important comparison with the original Ramsey problem:

`L_s >= R_s(3)-1`,

because every globally `s`-colored example is locally `s`-colored. Therefore proving `L_s^{1/s}` unbounded is no easier than proving the desired superexponential Ramsey lower bound if one uses globally `s`-colored witnesses. The local-seed approach can only add leverage when the outer witness uses more than `s` colors globally but still fits into the eventual palette budget `k`. The factorial upper bound shows that local palette size alone does not rule out the desired scale, but it supplies no construction. The next proposition makes the required global-palette control precise.

The local parameter also has a classical covering reformulation that helps delimit possible constructions.

**Lemma (local-palette set system).** In a locally `s`-colored coloring, assign to each vertex `v` its incident palette `P_v`. Then `|P_v|<=s`, every pair satisfies `P_u cap P_v != empty`, and for each color `a` the graph induced by edges of color `a` on the support `{v:a in P_v}` is triangle-free. Conversely, any edge assignment choosing for each pair `uv` a color in `P_u cap P_v`, with no monochromatic triangle, gives such a coloring.

In particular, by the elementary pairwise-intersecting-family bound, the number of **distinct** local palettes is at most `2^{g-1}` when the global palette has size `g`: pair every subset of `[g]` with its complement, and a pairwise-intersecting family contains at most one member of each pair.

Multiplicity can also be bounded, although only in terms of the original Ramsey numbers. Vertices with the same local palette `P` induce a triangle-free coloring using only `|P|` colors, so there are at most `R_{|P|}(3)-1` of them. Consequently every locally `s`-colored coloring using `g` colors globally satisfies

`N <= sum_{P in F} (R_{|P|}(3)-1)
 <= min(2^{g-1}, sum_{j=1}^s binom(g,j)) (R_s(3)-1)`,

where `F` is its pairwise-intersecting family of distinct nonempty local palettes. Equivalently,

`R_s(3)-1 >= N / min(2^{g-1}, sum_{j=1}^s binom(g,j))`.

The second type-count bound simply counts all nonempty subsets of size at most `s`; unlike the complement-pairing bound, it uses the local-size restriction. Here monotonicity `R_j(3)<=R_s(3)` for `j<=s` follows by allowing unused colors.

For `g>=s`, the elementary estimate

`sum_{j=1}^s binom(g,j) <= s (eg/s)^s`

follows from `binom(g,j)<=(eg/j)^j` and the fact that `(eg/j)^j` increases for `1<=j<=g` (differentiate `j log(eg/j)`). Thus

`log(R_s(3)-1) >= log N - s log(eg/s)-log s`.

This quantifies the limitation of the local-seed strategy. If `g=O(s^d)` and `N>=s^{c s}`, then the seed already contains an ordinary lower bound roughly `s^{(c-d+1)s}` whenever `c>d-1`. Only in the complementary parameter range can the iteration mechanism conceivably add leverage not already present in one palette type.

A sharper exact type count is available by the uniform Erdős--Ko--Rado theorem. Writing `F_j={P in F:|P|=j}`, each `F_j` is intersecting, so for `j<=g/2`,

`|F_j|<=binom(g-1,j-1)`.

For `j>g/2` the trivial bound `binom(g,j)` applies. Hence

`|F|<=sum_{j=1}^{min(s,floor(g/2))} binom(g-1,j-1)
      +sum_{j=floor(g/2)+1}^s binom(g,j)`.

In the most relevant sparse regime `s<=g/2`, this simplifies to

`|F|<=binom(g-1,s-1)+...+binom(g-1,0)=sum_{i=0}^{s-1}binom(g-1,i)`.

This improves constants but not the exponent-level limitation above. We use the classical EKR theorem here only as a diagnostic bound, not as an ingredient in any claimed superexponential construction.

There is also a useful blow-up bound for a single palette type. Let `F_P` be the vertices whose exact local palette is `P`, and let `U_P` be all vertices whose local palette contains `P`. If `F_P` is nonempty, then every edge from a vertex of `F_P` has color in `P`; hence all edges inside `F_P` and from `F_P` to the rest of the graph use `P`. This observation alone does not force edges within `U_P` to use `P`, so a tempting reduction to a `|P|`-colored complete graph on `U_P` is invalid. The valid multiplicity bound applies only to `F_P` itself. We record this warning because confusing exact palettes with containing palettes would falsely strengthen the argument.

A different elementary consequence concerns vertices with small incident palettes. For `0<=t<=s`, let

`V_{<=t}={v:|P_v|<=t}`.

Then

`|V_{<=t}| <= min(2^{g-1},sum_{j=1}^t binom(g,j))(R_t(3)-1)`.

Indeed, repeat the palette-type multiplicity argument using only those vertices. Thus any local-seed construction of order exceeding this bound must place a positive number of vertices at local palette size greater than `t`. This is merely a distributional obstruction; it does not by itself improve Ramsey bounds.

**Lemma (clique-cover formulation).** A triangle-free edge-coloring of `K_N` is equivalent to a family of triangle-free graphs `{G_a}` whose edge sets partition `E(K_N)`. It is locally `s`-colored exactly when each vertex belongs to the nonisolated vertex sets of at most `s` graphs `G_a`.

**Proof.** Take `G_a` to be the graph formed by edges of color `a`; conversely, color each edge by the unique graph containing it. A monochromatic triangle is exactly a triangle in one `G_a`, and incidence with a color is exactly nonisolation in the corresponding graph. ∎

A counting consequence is

`binom(N,2) <= sum_a floor(v_a^2/4)`,

where `v_a` is the number of nonisolated vertices of `G_a`, by Mantel's theorem, while

`sum_a v_a <= Ns`

by local `s`-coloredness. These inequalities alone are too weak: since `v_a<=N`, they only recover `N-1<=Ns/2` up to rounding. Thus any factorial-order obstruction or construction must exploit overlap structure beyond edge counts.

**Lemma (composition of local seeds).** If there are triangle-free colorings with parameters `(N_1,g_1,s_1)` and `(N_2,g_2,s_2)`—order, global palette size, and maximum local palette size—then there is one with parameters

`(N_1N_2, g_1+g_2, s_1+s_2)`.

**Proof.** Use the lexicographic product construction with disjoint palettes. At `(x,y)`, the incident colors consist of at most `s_1` outer colors and at most `s_2` inner colors. Triangle-freeness was proved in the exact product lemma below. ∎

Thus achievable parameter triples form a multiplicative/additive semigroup. In particular, finitely many fixed seeds can only give bounded `log N/s`; a superexponential application requires a sequence of genuinely improving seeds, not products among a fixed library.

**Proposition (iteration of a local seed).** Suppose a triangle-free coloring of `K_N` uses at most `g` colors globally and is locally `s`-colored, where `1<=s<=g`. Then, for every `k>=g`,

`R_k(3)-1 >= N^{1+floor((k-g)/s)}`.

**Proof.** Put `F(k)=R_k(3)-1`. Relabel the seed's global palette into any chosen `g` colors among the available `k` colors. The local-palette reduction gives

`F(k)>=N F(k-s)`

whenever `k>=g`: each outer vertex misses at least `k-s` colors, and an extremal coloring using at most those colors can be placed in its cluster. Iterate while the remaining palette size is at least `g`. The number of applications is `1+floor((k-g)/s)`, and terminate with the trivial bound `F(k-ts)>=1`. ∎

Consequently, if such a seed exists for every sufficiently large integer `s`, with `log N >= c s log s` and `g <= C s^d`, then it would imply a superexponential Ramsey bound. Indeed, for large `k`, choose an available `s` comparable to `k^{1/d}` so that `g<=k`; then the proposition gives

`log R_k(3) >= (c/d+o(1)) k log k`.

(The constants require choosing `s` sufficiently below `k^{1/d}` if the inequality for `g` has a leading constant.) Thus even factorial-order local seeds with a polynomial-size global palette would suffice formally. However, the palette-type multiplicity inequality above shows that if additionally `g=o(s log s)`, then such a seed already implies

`log R_s(3) >= (c-o(1))s log s`,

which is essentially the desired superexponential construction at palette size `s`. Therefore the local-seed framework only offers a potentially different route when `g` itself is of order `s log s` or larger (while still polynomial in `s`). The exact values `L_s` alone do not ensure global palette control.

There is also a useful palette-system formulation and a cheap probabilistic baseline.

**Lemma (palette-system local-lemma construction).** Let `P_1,...,P_N` be subsets of a global palette of size `g`, each of size at most `s`, and suppose every pair satisfies `|P_i cap P_j|>=q>=1`. If

`e(3N-8)g/q^3 <= 1`,

then `K_N` has a triangle-free coloring that uses only colors in `P_i` on edges incident to vertex `i`. In particular it is locally `s`-colored.

**Proof.** Independently color edge `ij` uniformly from `P_i cap P_j`. For a fixed triangle `i,j,l`, the probability of being monochromatic equals

`sum_{a in P_i cap P_j cap P_l} 1/(|P_i cap P_j| |P_i cap P_l| |P_j cap P_l|) <= g/q^3`.

A triangle event is independent of all triangle events sharing none of its three edges; at most `3(N-3)` other triangles share an edge with it. The symmetric Lovasz local lemma therefore applies under `e(g/q^3)(3N-8)<=1`. Any resulting coloring has every edge incident to `i` colored from `P_i`. ∎

Taking every `P_i` equal to an `s`-element palette gives only `N` of order `s^2` (here the exact bad-event probability is `1/s^2`). Thus this direct local-lemma argument is far below the factorial-size seed criterion. Nonidentical highly intersecting palettes do not help through the displayed coarse bound unless one also exploits substantially more event structure.

A natural factorial-size construction illustrates why the parameter `s`, not merely `N`, matters.

**Example (permutation coloring).** On the `n!` permutations of `[n]`, color two permutations by the unordered pair of symbols appearing at their first differing position. This is a triangle-free coloring using exactly `binom(n,2)` colors, and every vertex is incident to every color.

To prove triangle-freeness, suppose three permutations had all three edges colored by `{a,b}`, and take the earliest coordinate at which they are not all equal. At that coordinate exactly two of the permutations must agree, while the third differs, and the two displayed values must be `a,b`. The agreeing pair first differs later. But both members of that pair have already used one of `a,b` at the earlier coordinate, so neither can use that symbol later; their eventual first-difference color therefore cannot be `{a,b}`, a contradiction. Every color `{a,b}` occurs at every permutation: swap the positions occupied by `a` and `b`; the first changed position displays precisely those two symbols.

Here `N=n!` but `s=g=binom(n,2)`, so `log N/s` tends to zero. The construction is therefore asymptotically worse than a fixed-base exponential seed under the iteration proposition.

The same proof gives a precise coding subproblem.

**Lemma (first-difference permutation codes).** For any family `F subset S_n`, color a pair by the unordered symbols at its first differing coordinate. The coloring is triangle-free. If

`D_pi={ {pi_i,sigma_i}: sigma in F minus {pi}, i is the first coordinate where pi and sigma differ }`,

then its local palette size is `max_pi |D_pi|`, and its global palette is `|union_pi D_pi|<=binom(n,2)`.

Thus a family with `|F|>=exp(c s log s)` and all `|D_pi|<=s`, for a suitable relation between `n` and `s`, would be a useful local seed. Merely taking independent swaps of `s` disjoint adjacent symbol pairs gives `|F|=2^s` and `|D_pi|=s`: the first differing block exposes exactly that block's symbol pair, and every block can be exposed. This is only the ordinary binary exponential baseline. The lemma is a reduction, not a construction meeting the factorial target.

For further orientation, assigning a private color to every edge of `K_N` is locally `N-1`-colored and uses `binom(N,2)` colors. It rigorously gives

`R_k(3)-1 >= N(R_{k-N+1}(3)-1)` whenever `binom(N,2)<=k`

(by adjoining unused colors if necessary). This recurrence is not enough for the target: its gain is only a factor `N` at a cost of `N-1` available inner colors, and optimizing `log N/(N-1)` keeps the iterated growth exponential. A successful use of the reduction requires outer colorings with substantially more vertices relative to their local palette size.

## Quantitative Shannon-capacity bridge

The graph-capacity formulation can be stated directly and is useful for parameter bookkeeping.

Let `G^{boxtimes m}` denote the `m`-fold strong graph power: two distinct words are adjacent when in every coordinate their entries are equal or adjacent in `G`.

**Lemma.** If `alpha(G)<=2`, then for every `m>=1`,

`R_m(3)>alpha(G^{boxtimes m})`.

(The inequality is still true but vacuous when the right side is at most one; in applications it is large.)

**Proof.** Let `S` be an independent set in `G^{boxtimes m}`. For distinct words `x,y in S`, nonadjacency in the strong power means that in at least one coordinate `i`, the entries `x_i,y_i` are distinct and nonadjacent in `G`. Color `xy` by the least such coordinate.

If three words formed a monochromatic triangle of color `i`, then their three entries in coordinate `i` would be pairwise distinct and pairwise nonadjacent in `G`. They would form an independent set of size three, contradicting `alpha(G)<=2`. ∎

The converse translation is also exact up to enlarging the graph.

**Lemma (coloring-to-capacity converse).** If `K_N` has a triangle-free `k`-coloring, then there is a graph `G` with `alpha(G)<=2` such that

`alpha(G^{boxtimes k})>=N`.

One may take `|V(G)|=kN`.

**Proof.** For each color `i`, let `H_i` be the graph on the `N` coloring vertices whose edges are precisely the pairs **not** colored `i`. Since the color-`i` graph is triangle-free, `alpha(H_i)<=2`: three independent vertices in `H_i` would have all three pairs colored `i`.

Let `G` be the join of the graphs `H_1,...,H_k`: its vertex set is the disjoint union of their vertex sets, it induces `H_i` on part `i`, and every two vertices in different parts are adjacent. Any independent set of `G` lies in one part, so `alpha(G)=max_i alpha(H_i)<=2`.

For each original coloring vertex `v`, form the word

`x(v)=((1,v),(2,v),..., (k,v)) in V(G)^k`.

If `u!=v` and their edge has color `i`, then `(i,u)` and `(i,v)` are distinct and nonadjacent in `H_i`, hence in `G`. Therefore `x(u)` and `x(v)` are nonadjacent in the strong power. The `N` words `x(v)` form an independent set in `G^{boxtimes k}`. ∎

Together the two lemmas give an exact finite-power identity:

**Theorem (universal strong-power extremum).** For every `k>=1`,

`max_{G: alpha(G)<=2} alpha(G^{boxtimes k}) = R_k(3)-1`,

where the maximum ranges over all finite graphs. Moreover the maximum can be attained by a graph on at most

`k(R_k(3)-1)`

vertices.

**Proof.** The capacity-to-coloring lemma gives `alpha(G^{boxtimes k})<=R_k(3)-1` for every admissible `G`. Conversely, take a triangle-free `k`-coloring on `R_k(3)-1` vertices and apply the coloring-to-capacity construction; its graph has independence at most two, has exactly `k(R_k(3)-1)` vertices, and its `k`th strong power has an independent set of the required size. ∎

For `k=2`, this identity gives the universal upper bound five, while the more detailed proposition below classifies exactly which graphs attain it. For `k=3`, the value `R_3(3)=17` proved above gives universal maximum 16, attained by the graph constructed from the explicit `K_16` coloring above. If `alpha(G)=2`, the product of a two-vertex independent set gives `alpha(G^{boxtimes3})>=8`, so the possible strong-cube values lie between 8 and 16. Exact atlas computations through graph order five show only `8` and `10` (besides `1` for complete graphs), with `10` supplied by `C_5`; larger values require larger graphs. An attempted exact enumeration at order six was computationally expensive; greedy scans found only 8 and 10, so no exact order-six claim is made.

Using the classical upper bound `R_k(3)<=3k!`, the maximizing graph may in particular be taken to have fewer than `3k*k!` vertices. This makes the universal optimization finite in principle, though astronomically large and circular because the sharp cutoff depends on Ramsey information.

**Generalization.** Let `R_k(r+1)` denote the diagonal `k`-color Ramsey number for `K_{r+1}`. The same first-nonedge argument gives

`max_{G:alpha(G)<=r} alpha(G^{boxtimes k})=R_k(r+1)-1`.

For the converse, given a `k`-coloring with no monochromatic `K_{r+1}`, define `H_i` by making the non-color-`i` pairs adjacent and join the `H_i`; then `alpha(H_i)<=r`, and diagonal encoding works exactly as before. Thus the graph-power identity is a general reformulation of diagonal multicolor clique Ramsey numbers, not a peculiarity of triangles.

This exact identity also shows why optimizing over a graph allowed to depend arbitrarily on `k` is literally the original Ramsey problem. The Shannon-capacity formulation gains content only by seeking a coherent graph family, a fixed graph with useful powers, or quantitative control on witness graphs/powers.

A broad class is incapable of beating the binary baseline.

**Lemma (fractional-chromatic complement bound).** For every finite graph `G`,

`Theta(G)<=chi_f(overline G)<=chi(overline G)`,

where `chi_f` denotes fractional chromatic number. In particular, for every `m`,

`alpha(G^{boxtimes m})<=chi(overline G)^m`.

**Proof.** We first prove the standard inequality `alpha(F)<=chi_f(overline F)` for every graph `F`. A fractional coloring of `overline F` assigns nonnegative weights to independent sets of `overline F`—equivalently, cliques of `F`—so that the total weight covering each vertex is at least one. If `S` is independent in `F`, every clique of `F` contains at most one vertex of `S`. Summing the covering inequalities over `S` therefore gives

`|S|<=sum_C weight(C)`.

Minimizing proves the inequality.

Next, fractional chromatic number is submultiplicative under the disjunctive (OR) product: taking products of fractional color classes gives

`chi_f(A vee B)<=chi_f(A)chi_f(B)`.

The complement of a strong product is the disjunctive product of the complements:

`overline(G boxtimes H)=overline G vee overline H`.

Therefore

`alpha(G^{boxtimes m})<=chi_f(overline(G^{boxtimes m}))
 <=chi_f(overline G)^m`.

Taking `m`th roots and the supremum gives the first inequality. The second is immediate from integral colorings.

For completeness, the final displayed integral bound also has a direct proof. Properly color `overline G`. Distinct words in a strong-power independent set must have a coordinate forming an edge of `overline G`, so their coordinatewise color words differ; this injects the code into a `chi(overline G)`-ary word space. ∎

**Corollary (bipartite complement).** If `H=overline G` is bipartite and has an edge, then `Theta(G)=2` and in fact

`alpha(G^{boxtimes m})=2^m`

for every `m`.

**Proof.** The lemma gives the upper bound. If `uv` is an edge of `H`, all words over `{u,v}` are pairwise nonadjacent in the strong power, giving the matching lower bound. ∎

Hence capacity greater than `B` requires a triangle-free complement with fractional chromatic number (and therefore chromatic number) greater than `B`. In particular, capacity greater than two requires an odd cycle. This explains why bipartite complement experiments cannot improve the binary base and connects the capacity route to high-chromatic triangle-free graphs. High chromatic number is necessary but not sufficient on the evidence here: the Mycielski and Hoffman--Singleton experiments above did not produce corresponding capacity gains at small powers. No general insufficiency theorem is claimed.

Combining the bound with the effective-capacity criterion gives another necessary feature of any successful family: if the achieved base at some power is at least `t^a`, then necessarily

`chi_f(overline G_t)>=t^a`.

Thus polynomial capacity growth demands at least polynomial fractional-chromatic growth in the triangle-free complements. Ordinary high chromatic number is not enough unless the fractional chromatic number also grows at the required rate; the challenge is then to convert that large fractional value (an upper bound on capacity) into large strong-power independent sets.

There is also a probabilistic lower bound in terms of complement density.

**Lemma (independent-coordinate random-code bound).** Let `H=overline G`. In coordinate `j`, let symbols be sampled from an arbitrary distribution `p^{(j)}` and put

`q_j=2 sum_{uv in E(H)} p_u^{(j)}p_v^{(j)}`.

For `m` coordinates, the direct no-bad-pair first moment produces a code of order at least a constant times

`product_{j=1}^m (1-q_j)^{-1/2}`.

In the iid case `p^{(j)}=p`, this gives

`Theta(G)>=(1-q(p))^{-1/2}`.

For the uniform distribution this is `(1-2e/v^2)^{-1/2}`.

**Proof.** Choose `N` words independently from the product distribution `p^{(1)} times ... times p^{(m)}`. For a fixed pair of sampled words, the probability of obtaining an ordered edge of `H` in coordinate `j` is `q_j`. Thus the probability that the pair is adjacent-or-equal in every coordinate of `G`, and hence fails the independence condition, is

`p_m=product_{j=1}^m(1-q_j)`.

The expected number of bad unordered pairs is at most `N^2p_m/2`. If this is less than one, there exists a sample with no bad pair; in particular all sampled words are distinct and form an independent set in `G^{boxtimes m}`. Taking `N=max(1,floor(p_m^{-1/2}/2))` makes the expectation less than one whenever the second term is active. This proves the finite product lower bound up to a harmless absolute constant. In the iid case, taking `m`th roots and letting `m` grow gives the capacity bound. ∎

For triangle-free `H`, one always has `q_j<=1/2` for every coordinate distribution. This is the clique-number-two case of the Motzkin--Straus theorem. For completeness, let `F(p)=sum_{uv in E(H)}p_up_v`. If two positive-weight nonadjacent vertices `a,b` have weighted-neighbor sums `A,B`, then their contribution to `F` is `p_a A+p_b B` with no `p_ap_b` term. Moving all mass `p_a+p_b` to whichever of `a,b` has larger weighted-neighbor sum does not decrease `F` and shrinks its support. Iterating leaves a clique, of size at most two because `H` is triangle-free. On two vertices the maximum is `p(1-p)<=1/4`, proving `q_j=2F(p)<=1/2`. Therefore even allowing a different independent symbol distribution in every coordinate gives geometric-mean base at most `sqrt(2)` for the direct first moment, below the universal lower bound `alpha(G)=2` when `H` has an edge. Taking the maximum with the trivial code gives

`Theta(G)>=max(alpha(G),(1-q(p))^{-1/2})`.

Thus the direct first-moment method demanding no bad sampled pair is quantitatively useless for every product distribution with independently sampled coordinates, even when the coordinate marginals vary. This does **not** rule out expurgation or more sophisticated use of the same ensemble. For general independent coordinates, sample `M` words and form the conflict graph whose edges are bad pairs. Some sample has at most

`M^2 product_j(1-q_j)/2`

conflict edges. The elementary bound `alpha>=M^2/(2E+M)` then yields

`alpha>=M/(M product_j(1-q_j)+1)`.

Choosing `M` sufficiently large makes the geometric-mean lower bound approach

`(product_j(1-q_j))^{-1/m}<=2`. Thus even this expurgation-by-edge-count variant cannot beat the trivial binary base.

The symmetric Lovasz local lemma applied directly to bad-pair events has the same ceiling. Each event has probability `product_j(1-q_j)` and depends on fewer than `2M` other pair events, so the LLL permits geometric-mean code base at most `(product_j(1-q_j))^{-1/m}<=2`. Therefore first moment, edge-count expurgation, and the basic dependency-graph LLL all fail to beat two for independently sampled product-distributed codewords, even with coordinate-dependent marginals. A successful random-code proof must exploit more structure than pair-event probabilities and their elementary dependencies.

The useful gap remains between the trivial lower bound two and the potentially large upper bound `chi_f(overline G)`. No reverse inequality in terms of `chi_f` is asserted; treating a large fractional chromatic number as a capacity lower bound would reverse the only proved implication.

The proposition completely explains the earlier exhaustive benchmark: all strong squares have independence at most five, and `C_5` is exactly the obstruction to the baseline value four. Enumeration through seven vertices was used as an independent check, not as evidence needed for the theorem.

There is an exact structural explanation of the power-two threshold.

**Proposition (complete strong-square classification at the top).** If `alpha(G)<=2`, then

`alpha(G^{boxtimes2})<=5`.

Moreover, writing `H=overline G` (which is triangle-free), equality holds if and only if `H` contains a five-cycle as a (not necessarily induced) subgraph.

**Proof.** First, suppose there were six independent codewords. For each pair, choose a coordinate in which their symbols form an edge of `H`, and color the pair by that coordinate. A monochromatic triangle would map to a triangle in `H`, impossible. This would give a red/blue coloring of `K_6` with no monochromatic triangle, impossible by the elementary proof of `R_2(3)=6`: at any vertex three incident edges share a color; an edge among their other endpoints either completes a triangle in that color or, if all three avoid it, those endpoints form a triangle in the other color. Hence the upper bound is five.

If `H` contains a `C_5`, the standard five words `(i,2i mod 5)` on that cycle form an independent set in `G^{boxtimes2}`.

Conversely, take five independent codewords `(x_v,y_v)`, indexed by the vertices of `K_5`. For each pair `uv`, at least one of `x_ux_v` and `y_uy_v` is an edge of `H`; choose one such coordinate and color `uv` red or blue accordingly. A red triangle would map its three edges through the first coordinate to a triangle of `H`. The three first-coordinate vertices are distinct because each selected edge has distinct endpoints. This contradicts triangle-freeness; similarly there is no blue triangle. Thus we have a two-coloring of `K_5` with no monochromatic triangle. Each color class must be a five-cycle. Indeed, if a vertex had three red neighbors, none of the three edges among those neighbors could be red, so all three would be blue, forming a blue triangle. Thus red degree is at most two at every vertex; symmetrically blue degree is at most two. Since the two degrees sum to four, both equal two at every vertex, and both color classes are five-cycles.

The red cycle gives a graph homomorphism from `C_5` into `H` via the first coordinates. It is injective. Adjacent cycle vertices cannot coincide. If two vertices at distance two coincided, say the cycle images satisfy `z_0=z_2`, then the edges `z_2z_3`, `z_3z_4`, and `z_4z_0` form a triangle in `H`; its vertices are distinct because each displayed edge has distinct endpoints. The distance-three case is the same after reversing the cycle. Therefore the five images form a `C_5` subgraph of `H`. ∎

**Corollary.** For every graph `G` with `alpha(G)<=2`, its strong-square independence number is:

- `1` if `alpha(G)=1`;
- at least `4` if `alpha(G)=2` (take products of a two-vertex independent set);
- exactly `5` iff `overline G` contains `C_5`;
- exactly `4` otherwise.

Thus the only possible values are `1,4,5`. In particular, if `H` is triangle-free, `C_5`-free, and has an edge, then `alpha(overline H^{boxtimes2})=4`. Hence for every odd cycle `C_{2r+1}` with `r>=3`, the power-two code size is exactly four.

This square classification does **not** imply `Theta(G)=2` in the `C_5`-free case: independence number is supermultiplicative, not submultiplicative, so higher powers may improve the base. Only the bipartite-complement theorem above controls all powers. This warning prevents extrapolating a power-two computation into a capacity theorem.

For the same graph at power three, an exact maximum-clique computation (NetworkX branch-and-bound on the 125-vertex compatibility graph) gives

`alpha(overline(C_5)^{boxtimes3})=10`.

Since `C_5` is self-complementary, this is the familiar value `alpha(C_5^{boxtimes3})=10`. It yields only base `10^{1/3}<sqrt(5)`, consistent with `Theta(C_5)=sqrt(5)`; power two remains the more efficient witness. This computation is again a benchmark, not progress toward unbounded capacity. For the 11-vertex Mycielski extension of `C_5` (the Grötzsch graph), an exact maximum-clique computation on its 121-word power-two compatibility graph also gives maximum code size five. Random greedy scans of this and several other larger triangle-free complements (including Petersen, cube, Hoffman--Singleton, and further Mycielski examples) found no base exceeding `sqrt(5)` at powers two or three; because the latter scans are heuristic, details are recorded only in the notes and no conclusion is drawn from them. Exact fractional-coloring linear programs give diagnostic upper bounds `chi_f(H)=5/2` for `C_5` and Petersen, `2` for the cube, `29/10` for the Grötzsch graph, and `10/3` for Hoffman--Singleton. These upper bounds are all constant and hence cannot support unbounded capacity within these fixed examples.

The converse construction also compares capacity directly to a given coloring:

`Theta(G)>=alpha(G^{boxtimes k})^{1/k}>=N^{1/k}`.

Thus any family with `N^{1/k}->infinity` yields a family of independence-two graphs with unbounded Shannon capacity. Conversely, if capacities are unbounded, the first bridge and the power approximation give triangle-free colorings with arbitrarily large exponential base (on graph-dependent color counts). This proves the commonly stated qualitative equivalence, while the effective criteria below address the missing uniform rate.

Writing the Shannon capacity as

`Theta(G)=sup_m alpha(G^{boxtimes m})^{1/m}`,

(the supremum is a limit by supermultiplicativity of independence numbers under strong products), we obtain the following precise consequence: for every `epsilon>0`, there are infinitely many `m` for which

`R_m(3)>(Theta(G)-epsilon)^m`.

Indeed choose one power `q` with `alpha(G^{boxtimes q})^{1/q}>Theta(G)-epsilon`. For every multiple `m=tq`, the Cartesian power of an independent set in `G^{boxtimes q}` is independent in `G^{boxtimes m}`, proving the claim.

More quantitatively, a family of graphs `G_k` with `alpha(G_k)<=2` and

`alpha(G_k^{boxtimes k})>=k^{c k}`

would directly prove the desired Ramsey lower bound. Merely proving that capacities `Theta(G)` are unbounded gives unbounded Ramsey exponential bases along arithmetic progressions of color counts: for any fixed target base `B`, choose `G` with `Theta(G)>B`, then the preceding argument gives `R_m(3)>B^m` for infinitely many multiples `m` of a graph-dependent power. Without uniform control on that power as the graph varies, this does not by itself yield a stated rate such as `k^{ck}` for every `k`. This distinction prevents a hidden quantifier error in using the capacity equivalence.

There is, however, a clean interpolation lemma once constructions are available on a sufficiently dense sequence of color counts.

**Lemma (padding/interpolation).** Suppose triangle-free colorings exist on `N_j` vertices using `k_j` colors, where `k_j` is increasing and `k_{j+1}/k_j<=C`. If

`log N_j >= c k_j log k_j`

for all sufficiently large `j`, then for every sufficiently large integer `k`,

`R_k(3) >= k^{(c/C+o(1))k}`.

**Proof.** Given `k`, choose `j` with `k_j<=k<k_{j+1}`. Regard the `k_j`-coloring as a `k`-coloring by leaving colors unused. Since `k_j>=k/C` and `log k_j=log k+O(1)`,

`log R_k(3) > log N_j >= c k_j log k_j
 >=(c/C+o(1))k log k`.

Exponentiate. ∎

Thus capacity constructions on powers `k_j` with bounded successive ratios would suffice. For one fixed graph, multiples of a single good power have ratio tending to one but only give a fixed exponential base. To obtain `k^{ck}`, the achieved bases must grow with the color count while the union of good color-count sequences remains multiplicatively dense.

A convenient sufficient condition packages the power needed to approach capacity.

**Corollary (effective-capacity criterion).** Suppose that for every sufficiently large integer `t` there is a graph `G_t` with `alpha(G_t)<=2` and an integer power `q_t` such that

`q_t<=t^D` and `alpha(G_t^{boxtimes q_t})^{1/q_t}>=t^a`

for fixed constants `a,D>0`. Then there is `c=c(a,D)>0` such that

`R_k(3)>=k^{c k}`

for all sufficiently large `k`.

**Proof.** The capacity bridge at `m=q_t` gives a `q_t`-color construction of order at least `t^{a q_t}`. This alone does not ensure dense color counts because `q_t` may vary irregularly. Instead include all multiples `m=u q_t`, obtained by Cartesian powers of the independent set; they have order at least `t^{a m}`.

Given large `k`, choose `t=floor(k^{1/(D+1)})`. Then `q_t<=t^D<=k^{D/(D+1)}=o(k)` (and for large `k`, `t` lies in the range where the assumed graph exists). Let `m=floor(k/q_t)q_t`; thus `k-q_t<m<=k` and `m=(1-o(1))k`. Pad the resulting `m`-coloring to `k` colors. Since `log t=(1/(D+1)+o(1))log k`,

`log R_k(3)>=a m log t=(a/(D+1)+o(1))k log k`.

Any fixed `c<a/(D+1)` works eventually. ∎

This criterion makes the missing quantitative task explicit: construct independence-two graphs with polynomially bounded witness power and polynomially growing achieved capacity base. A statement about the limiting capacity without a witness-power bound is insufficient.

The converse lemma shows this criterion is not merely an artifact of the graph language. If one already had a triangle-free `t`-coloring on `t^{a t}` vertices, its associated graph would satisfy the criterion with witness power `q_t=t` (so `D=1`) and achieved base `t^a`; applying the criterion would recover an all-`k` exponent only about `a/2` because of the deliberately coarse choice `t approximately sqrt(k)`. Direct padding of colorings on every `t` would retain exponent `a`. Thus the effective-capacity criterion is a sufficient tool for sparse/irregular witnesses, not an equivalence with optimal constants.

## An explicit correlated strong-cube witness

The following finite witness is a modest but genuine improvement over the previously tested `C_5`-based capacity benchmark. Let `H` be the 11-vertex Grötzsch graph with edge set

`01,04,06,09,12,15,17,23,26,28,34,37,39,45,48,5A,6A,7A,8A,9A`,

where `A` denotes vertex 10, and put `G=overline H`. Then `H` is triangle-free, so `alpha(G)<=2`. The following twelve words form an independent set in `G^{boxtimes 3}`:

`(0,3,10),(0,9,10),(1,0,3),(1,6,0),(2,9,5),(3,8,9),`

`(4,9,1),(6,2,2),(7,0,8),(8,4,6),(9,3,4),(10,10,9)`.

Indeed, direct checking shows that every pair of displayed words has some coordinate whose two entries form an edge of `H`; this is exactly nonadjacency in the corresponding coordinate of `G`, hence nonadjacency in the strong product. Consequently

`alpha(G^{boxtimes 3})>=12` and `Theta(G)>=12^(1/3)>sqrt(5)`.

The final strict inequality follows after raising to the sixth power: `12^2=144>125=5^3`. The standard-library script `verify_grotzsch_code.py` checks both triangle-freeness of `H` and all 66 word pairs. This is a fixed constant capacity improvement and therefore still yields only a fixed-base exponential Ramsey construction; it is not a superexponential lower bound.

## General first-difference amplification

The binary construction and lexicographic products are instances of one exact scheme.

**Lemma.** Suppose `K_q` has a triangle-free `r`-coloring `c`. Then the words `[q]^n` admit a triangle-free `nr`-coloring on `q^n` vertices: color two words by the pair `(i,c(x_i y_i))`, where `i` is their first differing coordinate.

**Proof.** If three words had a monochromatic triangle `(i,a)`, then all three pairs would first differ at coordinate `i` and their three symbols there would form a color-`a` monochromatic triangle under `c`. They are pairwise distinct because every pair differs at `i`. Contradiction. ∎

Taking `q=R_r(3)-1` gives

`R_{nr}(3)>(R_r(3)-1)^n`.

For arbitrary `k`, writing `k=nr+s` with `0<=s<r`, the lexicographic product with the binary `s`-color construction gives

`R_k(3)>(R_r(3)-1)^n 2^s`.

Thus increasing the alphabet size does not bypass the original problem: obtaining unbounded per-color base `q^{1/r}` is exactly obtaining unbounded Ramsey bases at the seed level. Any first-difference construction with a fixed seed remains fixed-base exponential. This formalizes why changing from binary to larger alphabets, without a new seed theorem, is circular.

## Exact lexicographic product lemma

Call a coloring *triangle-free* if none of its color classes contains a triangle.

**Lemma.** If there is a triangle-free `r`-coloring of `K_m` and a triangle-free `s`-coloring of `K_n`, then there is a triangle-free `(r+s)`-coloring of `K_{mn}`. Equivalently,

`R_{r+s}(3) > (R_r(3)-1)(R_s(3)-1)`.

**Proof.** Let `c` be the first coloring on a vertex set `X`, and `d` the second on `Y`; relabel their palettes to be disjoint. On `X times Y`, color the edge joining `(x,y)` and `(x',y')` by `c(xx')` when `x != x'`, and by `d(yy')` when `x=x'` (in which case necessarily `y != y'`).

Suppose a triangle were monochromatic in a color from the palette of `d`. Every one of its three edges would then have equal first coordinates at its endpoints, so all three vertices would lie in one fiber `{x} times Y`; their second coordinates would form a monochromatic triangle under `d`, a contradiction.

Suppose instead that a triangle were monochromatic in a color from the palette of `c`. No edge of that triangle can have equal first coordinates, because such an edge receives a color from the disjoint palette of `d`. Thus its three first coordinates are pairwise distinct and form a monochromatic triangle under `c`, again a contradiction. The displayed Ramsey inequality follows by taking colorings on `R_r(3)-1` and `R_s(3)-1` vertices. ∎

Iterating a fixed `s`-color base coloring on `q` vertices gives an `st`-coloring on `q^t` vertices. Hence it gives only

`R_k(3) > (q^{1/s})^k`

(for multiples `k=st`), a fixed-base exponential. Thus lexicographic tensoring is a valid amplification mechanism but cannot turn any single fixed base coloring into the requested superexponential bound; one needs base colorings whose quantity `q^{1/s}` is itself unbounded with `s`, which is essentially the original difficulty.
