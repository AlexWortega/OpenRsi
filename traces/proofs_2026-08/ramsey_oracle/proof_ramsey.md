# Current Ramsey write-up

## Main target

The requested superexponential lower bound is **not proved** in this run. The inherited rigorous reductions and constructions remain in `prior/final/proof_ramsey.md`. This file records only new claims from the current run.

## Obstruction to the anchored-palette proposal

The second oracle proposal fixes integers `r,g`, vertices

`V={(a,B): a in {1,2}, B subset {3,...,g}, |B|=r-1}`,

and vertex palettes

`P_(a,B)={0,a} union B`.

Edges are required to receive a color in the intersection of their endpoint palettes. Such a coloring is automatically locally `(r+1)`-colored, but the following obstruction shows that the proposed full vertex family is not colorable at its intended scale, regardless of the greedy algorithm.

**Proposition.** If `g-2 >= 6(r-1)`, no edge-coloring of the complete graph on `V` can both (i) color every edge `uv` from `P_u cap P_v` and (ii) avoid monochromatic triangles.

**Proof.** Choose six pairwise disjoint `(r-1)`-subsets `B_1,...,B_6` of `{3,...,g}`; the numerical hypothesis permits this. Restrict to the six vertices `v_i=(1,B_i)`. For distinct `i,j`,

`P_(v_i) cap P_(v_j) = {0,1}`.

Thus the induced `K_6` is edge-colored using only two colors. But every two-coloring of `K_6` has a monochromatic triangle: at any vertex, at least three incident edges have one common color, say red. If any edge among their three other endpoints is red, it completes a red triangle; otherwise all three such edges are blue and form a blue triangle. Contradiction. ∎

For the suggested asymptotic choice `g=floor(r^2)`, the hypothesis holds for every integer `r>=6`, since `r^2-2>=6(r-1)`. Hence the full anchored-palette family is asymptotically impossible. More generally, any surviving induced subfamily can contain at most five pairwise-disjoint `B` sets within either anchor class.

There is a hierarchy strengthening this matching obstruction. For a retained uniform family `F` under one anchor and a set `C`, define its link

`L_F(C)={B minus C: B in F, C subset B}`.

**Lemma (link-Ramsey obstruction).** If the palette lists admit a triangle-free coloring, then

`nu(L_F(C)) <= R_(|C|+2)(3)-1`

for every `C`, where `nu` is matching number.

**Proof.** Otherwise choose `R_(|C|+2)(3)` pairwise-disjoint link members `Q_i` and put `B_i=C union Q_i`. Distinct `B_i,B_j` intersect exactly in `C`, so every edge among their vertices has its color in the same set `{0,a} union C` of `|C|+2` colors. The definition of the Ramsey number forces a monochromatic triangle. ∎

The matching-number restriction by itself is quantitatively harmless. For a fixed five-set `S`, the family of all `(r-1)`-sets meeting `S` has matching number at most five and cardinality

`binom(r^2-2,r-1)-binom(r^2-7,r-1)`,

whose logarithm is `r log r+O(r)`. However this natural large family violates the next link constraint. Fix `x in S`; if `r^2-7>=17(r-2)` (in particular `r>=16`), choose 17 disjoint `(r-2)`-sets outside `S`. The corresponding sets `{x} union Q_i` intersect pairwise exactly in `{x}`, so their edges have only colors `{0,a,x}`. Since `R_3(3)=17`, no triangle-free coloring exists.

Conversely, these link obstructions alone do not prove that every factorial-size family is impossible. A family of all `(r-1)`-sets containing a fixed logarithmic-size core still has logarithmic order `(1-o(1))r log r` and trivially suppresses most link matchings. No edge-coloring of such a family is supplied. Thus the route reaches the original correlated-coloring difficulty rather than solving it.

`experiments/verify_anchored_obstruction.py` checks the palette intersections for explicit disjoint blocks and exhausts all `2^15` two-colorings of `K_6`, confirming the finite core of the first proposition.

## Exact finite automaton searches

The first oracle proposal considered all closed walks of length `q` in a finite transition digraph as codewords. A transfer-product trace identity exactly checks pairwise coordinate separation. Two exhaustive searches found no improvement over binary in specified classes:

1. For `H=C_5`, among every symmetric Boolean `5x5` transition matrix (loops allowed), the largest feasible closed-walk code has size `2^q` for each `2<=q<=6`.
2. For `H=C_5`, among every directed Boolean `5x5` transition matrix with every row of outdegree at most two, the largest feasible code has size `2^q` for each `2<=q<=8`.

These are finite enumeration results only, implemented in `experiments/search_stationary_c5.py` and `experiments/search_stationary_c5_directed.cpp`. They do not imply an asymptotic obstruction to stationary automata and do not advance the goal ladder.

## Varying-domain partial assignments do not supply domain entropy

A possible repair of anchored palettes is to label every incidence `x in B` by a state in a triangle-free graph `H_x`, and require every pair of partial assignments to share a coordinate at which their states are adjacent. Coloring a pair by such a coordinate is triangle-free. The following packing bound shows that varying the domains contributes no extra multiplicative factor.

**Lemma (fractional-cylinder packing).** Let `F` be a family of partial assignments `f=(B_f,h_f)`, where `B_f subset U`, `|B_f|=r`, and `h_f(x) in V(H_x)`. Suppose every distinct `f,g` have some `x in B_f cap B_g` for which `h_f(x)h_g(x)` is an edge of `H_x`. Let `S_x` be the states actually used at `x` and put `q_x=chi_f(H_x[S_x])`. Then

`sum_(f in F) product_(x in B_f) q_x^(-1) <= 1`.

In particular, if every `q_x<=Q`, then `|F|<=Q^r`.

**Proof.** For each `x`, take a fractional coloring of `H_x[S_x]` of total weight `q_x`. Independently sample an independent set `I_x`, choosing each fractional color class with probability equal to its weight divided by `q_x`. Every used state `v` then belongs to `I_x` with probability at least `1/q_x`.

For `f`, let `E_f` be the event that `h_f(x) in I_x` for every `x in B_f`. Coordinate independence gives

`Pr(E_f)>=product_(x in B_f)q_x^(-1)`.

The events `E_f` are pairwise disjoint: if `f,g` are separated at `x`, then the independent set `I_x` cannot contain both adjacent states. Summing their probabilities proves the claim. ∎

**Corollary.** Binary or bipartite state graphs give at most `2^r` partial assignments, regardless of the size of `U` or number of possible domains. More generally, a family of size `r^{c r}` forces `max_x chi_f(H_x[S_x])>=r^c`.

Thus the binary partial-assignment proposal is rigorously banked. Allowing high-fractional-chromatic triangle-free state graphs leaves formal room, but constructing a family near the packing bound is already the strong-power correlated-code problem; fractional chromatic number is only an upper bound and supplies no construction.

## The permutation-orbit permanent guarantee has bounded base

Let `H` be triangle-free on `n` vertices and let `M` be its reflexive nonadjacency matrix: `M_uv=1` exactly when `u=v` or `uv` is not an edge of `H`. On all `n!` permutations of `V(H)`, call two words bad if they are coordinatewise nonadjacent-or-equal. Each word has exactly `D=per(M)` bad partners. The usual greedy bound therefore selects at least `n!/D` pairwise-separated permutations; coloring a pair by a coordinate whose images form an `H`-edge is triangle-free.

The next theorem proves that this particular guarantee can never have growing base.

**Theorem.** For every triangle-free `H`,

`per(M) >= n!/C^n`, where `C=(5/2)(5/3)^(3/2)=25 sqrt(15)/18<5.38`.

Consequently `(n!/per(M))^(1/n)<5.38` uniformly.

**Proof.** We first need a dense-matrix lemma. Suppose an `m x m` zero-one matrix `A` has at most `a<=4m/9` zeros in each row and column. Its bipartite support contains an `(m-2a)`-regular spanning subgraph. Indeed, the integral max-flow criterion asks that, for all row sets `X` and column sets `Y`,

`e(X,[m] minus Y) >= (m-2a)(|X|-|Y|)`

when `|X|>|Y|`. Put `x=|X|,y=|Y|`. The left side is at least

`x(m-y)-min(ax,a(m-y))`.

If `x<=m-y`, subtracting the desired right side gives `x(a-y)+(m-2a)y`. This is nonnegative directly for `y<=a`; for `y>a`, use `x<=m-y` to lower-bound it by `y^2-3ay+am>=0`, whose discriminant is nonpositive because `9a<=4m`. If `x>=m-y`, the corresponding difference is `x(2a-y)+(m-a)y-am`. For `y<=2a`, minimize at `x=m-y` and obtain the same quadratic; for `y>=2a`, minimize at `x=m` and obtain `a(m-y)>=0`. This proves the factor claim. Applying van der Waerden to its normalized adjacency matrix gives

`per(A)>=m!(1-2a/m)^m`.                                                   (1)

Now recursively process the current induced subgraph of `H`, of order `m`. While it has a vertex of degree greater than `2m/5`, remove that vertex's neighborhood as a block of size `b`. Every removed block is independent because `H` is triangle-free, so the corresponding principal block of `M` is all ones. At termination the residual set `T`, of size `t`, has integer maximum degree `a_0<=2t/5`; its principal matrix has at most `a_0` zeros per row and column. Equation (1), with `a=a_0`, gives

`per(M[T])>=t!(1-2a_0/t)^t>=t!/5^t`.

Restricting to permutations preserving every removed block and `T`,

`per(M)>= (product_i b_i!) t!/5^t`.                                      (2)

Put `p_i=b_i/n`, `p_*=t/n`, and `x_i=b_i/m_i`, where `m_i` is the residual size before block `i` is removed. Then `x_i>2/5`. The multinomial/entropy bound and entropy chain rule give

`log(n!/(product_i b_i! t!)) <= n H(p_1,...,p_*)`
`= sum_i m_i h(x_i)`.

Since `h(x)/x` is decreasing and its derivative is `log(1-x)/x^2`,

`sum_i m_i h(x_i) <= [h(2/5)/(2/5)] sum_i b_i`
`= n(1-p_*) log C`.

Finally `C>5`. Combining this with (2),

`log(n!/per(M)) <= n(1-p_*)log C + np_* log 5 <= n log C`.

This proves the theorem. ∎

This obstruction applies only to the elementary transitive greedy guarantee `n!/per(M)`, not to the maximum separated permutation family. The next result shows why optimizing that maximum is not a useful simplification of the original problem.

## Balanced permutation codes are asymptotically universal

For a triangle-free graph `H`, call `C subset V(H)^m` *H-separated* if every distinct `x,y in C` have some coordinate `i` with `x_i y_i in E(H)`. Let `s_H(m)` be the maximum size of such a code. If `J` is triangle-free on `n` vertices, call `F subset S_n` a separated permutation family when every pair is separated coordinatewise by an edge of `J`, and let `P(n)` be the maximum size over all such `J,F`.

**Lemma (constant-composition lift).** If `H` has `q` vertices and `C subset V(H)^m` is H-separated, then some triangle-free graph `J` on exactly `m` vertices has a separated permutation family of size at least

`|C|/binom(m+q-1,q-1) >= |C|/(m+1)^q`.

**Proof.** Partition `C` according to the composition vector `(r_v)_(v in V(H))`, where `r_v` counts occurrences of `v`. There are `binom(m+q-1,q-1)` compositions, so a class `C'` has at least the asserted size. Blow up each vertex `v` of `H` into `r_v` independent clones `(v,1),...,(v,r_v)`, joining clones precisely when their original vertices are adjacent in `H`. The resulting `J` is triangle-free and has `m` vertices.

For `x in C'`, replace its `a`-th occurrence of symbol `v` by clone `(v,a)`. The resulting word `pi_x` uses every vertex of `J` exactly once, hence is a permutation. If `x,y` are separated at coordinate `i`, their corresponding clones at `i` are adjacent in `J`; therefore `pi_x,pi_y` are separated. ∎

**Theorem.**

`limsup_(n to infinity) P(n)^(1/n) = sup_(H triangle-free) Theta_sep(H)`,

where `Theta_sep(H)=sup_m s_H(m)^(1/m)`. Moreover

`sup_H Theta_sep(H) = sup_(k>=1) (R_k(3)-1)^(1/k)`.

**Proof.** A separated permutation family is in particular a separated word code, giving `P(n)^(1/n)<=sup_H Theta_sep(H)`. Conversely, for fixed finite `H`, apply the lemma to an optimal length-`m` code. Its loss `(m+1)^q` has `m`-th root tending to one, so `limsup_m P(m)^(1/m)>=Theta_sep(H)`. Take the supremum over `H`.

For the second identity, the exact capacity/Ramsey bridge gives `s_H(k)<=R_k(3)-1`, proving one direction. For each `k`, a graph attaining the finite extremum `R_k(3)-1` has separated capacity at least `(R_k(3)-1)^(1/k)`, proving the reverse direction. ∎

Thus a universal exponential bound for separated permutation families would be equivalent to a universal exponential upper bound for `R_k(3)`, while a superexponential permutation family would solve the present problem. Balance of symbol frequencies does not simplify the asymptotic zero-error question: arbitrary codes can be balanced by a triangle-free blow-up with only polynomial loss for fixed `H`.

There is also a direct obstruction to one tempting proof method. A clique `Q` in the bad-pair graph (every pair coordinatewise equal or nonadjacent in `H`) uses at each coordinate an independent set of `H`, and hence `|Q|<=alpha(H)^n`. Any fractional cover of all `n!` permutations by such bad cliques must consequently have total weight at least `n!/alpha(H)^n`, by summing the covering inequalities.

For completeness, triangle-free graphs with sublinear independence number follow by an elementary alteration. Take `G(N,p)` with `p=cN^(-2/3)` for a sufficiently small constant `c`. Its expected number of triangles is `binom(N,3)p^3<c^3N/6`; with positive probability there are fewer than `N/2` triangles. Also, for `t=CN^(2/3)log N` and sufficiently large fixed `C`,

`binom(N,t)(1-p)^(binom(t,2)) <= exp(t log(eN/t)-p t(t-1)/2)=o(1)`.

Thus with positive probability both properties hold. Delete one vertex from every triangle. The remaining triangle-free graph has `n>=N/2` vertices and independence number below `t=O(n^(2/3)log n)`. For these graphs the cover lower bound is at least `(c'n^(1/3)/log n)^n` by `n!>=(n/e)^n`, which is superexponential. Therefore a universal exponential-weight cover by bad cliques or bad coordinate cylinders cannot prove a universal exponential bound for `P(n)`.

## Finite obstruction to the proposed generalized-quadrangle Tanner family

The oracle-proposed `q=2` instance has a transparent exact reduction. Model the doily `GQ(2,2)` with its 15 points as the duads (two-subsets) of `[6]` and its 15 lines as the synthemes (partitions of `[6]` into three duads). Its incidence graph `X` is the cubic Tutte--Coxeter graph. A balanced Tanner configuration labels each of the 45 edges of `X` by a duad, requires the three labels at every vertex to form a syntheme, and uses every duad exactly three times.

**Lemma.** Such a configuration exists if and only if `X` has six perfect matchings `M_1,...,M_6` satisfying `|M_i cap M_j|=3` for every `i!=j`.

**Proof.** Given a configuration `f`, let `M_i` contain the edges whose duad label contains `i`. At each vertex the three labels partition `[6]`, so exactly one incident edge belongs to `M_i`; thus it is a perfect matching. Moreover `M_i cap M_j` consists precisely of the three edges labeled `{i,j}`.

Conversely, put `r_e=|{i:e in M_i}|`. The six matchings have total size 90, while their 15 pairwise intersections have total size 45. Therefore

`sum_e (r_e-2)^2 = [2 sum_e binom(r_e,2)+sum_e r_e]-4 sum_e r_e+4*45 = 0`.

Every edge lies in exactly two matchings and receives their index-pair as label. At a vertex the six matchings choose its three incident edges, each exactly twice, so those three pairs partition `[6]`. Each pair `{i,j}` occurs exactly `|M_i cap M_j|=3` times. ∎

**Computational lemma.** The Tutte--Coxeter graph has exactly 288 perfect matchings. In the graph joining two when their intersection has size three, there are 5,040 edges and clique number exactly three. In particular no balanced `q=2` configuration exists.

The independent standard-library verifier `experiments/verify_gq_tanner_q2_obstruction.py` enumerates all perfect matchings by exact cover, constructs the compatibility graph, and computes its clique number by exhaustive branch-and-bound. It exits zero. This is a finite obstruction only; it does not prove nonexistence for larger generalized quadrangles.

There is a second exact failure of the originally proposed rigidity quotient. The verifier deterministically selects the first involutory doily polarity produced by its incidence-graph isomorphism enumeration and constructs its triangle-free polarity graph. Exhaustion of all 720 doily collineations finds exactly 30 collineations outside that polarity's centralizer that move every point to a nonneighbor. Thus, if a legal configuration existed, postcomposing it by any such map would preserve the line constraints and equitability while producing a coordinatewise bad mate not identified by the polarity-preserving quotient. The script `experiments/verify_gq_polarity_bad_maps.py` verifies this count for the selected polarity. Quotienting by the full doily collineation group absorbs these maps, but the preceding computational lemma says that the balanced `q=2` configuration space is empty.

## Tensor fitting-rank obstruction for correlated coordinate codes

The following bound applies without any product or independence assumption on the code.

**Lemma.** For `1<=i<=m`, let `H_i=(V_i,E_i)` be graphs, and let `phi_i:X->V_i` be arbitrary maps such that every distinct `x,y in X` have some `i` with `phi_i(x)phi_i(y) in E_i`. Suppose that over a field `F` there is a matrix `B_i` indexed by `V_i` with nonzero diagonal and `B_i(u,v)=0` whenever `uv in E_i`. Then

`|X| <= product_i rank_F(B_i)`.

**Proof.** Pull back each matrix to `M_i(x,y)=B_i(phi_i(x),phi_i(y))` and form their entrywise product `M=Hadamard_i M_i`. Separation makes every off-diagonal entry zero, while the diagonal is nonzero; hence `rank(M)=|X|`. If `rank(B_i)=r_i`, a rank factorization writes its pullback as a sum of `r_i` rank-one matrices. Expanding the entrywise product writes `M` as a sum of at most `product_i r_i` rank-one matrices. Thus `rank(M)<=product_i r_i`. ∎

This gives a direct algebraic kill criterion. If `V_i subset F_q^d` and a polynomial `P_i(U,V)` is nonzero on the diagonal and vanishes on graph edges, its evaluation matrix has rank at most the rank of its coefficient matrix between `U`-monomials and `V`-monomials. In particular, if edges imply `R(u,v)!=0`, diagonals satisfy `R(v,v)=0`, and `R` is bilinear, then

`P(u,v)=1-R(u,v)^(q-1)`

is a fitting polynomial by Fermat's identity. Its rank is at most

`1+binom(d+q-2,q-1)`.

For `q=2`, `P=1+R` and its rank is at most `d+1`. Therefore arbitrary global correlation cannot make an `m`-coordinate code larger than `(d+1)^m` when every coordinate uses such a binary bilinear predicate. The finite checker `experiments/verify_tensor_fitting_rank.py` verifies tightness for the binary `K_2` code through six coordinates and checks rank five for a nondegenerate alternating bilinear form on `F_2^4`.

## Symmetric perfect-matching partner codes cannot scale

For even `n`, encode each perfect matching `M` of `K_n` by its partner word `p_M in [n]^n`, where `p_M(i)` is matched to `i`. There are `(n-1)!!` words, whose `n`-th root grows like `sqrt(n/e)`. A natural symmetric separation rule chooses a 3-uniform hypergraph `T` on `[n]` and joins symbols `a,b` in coordinate graph `H_i` exactly when `{i,a,b} in T`. Every `H_i` is triangle-free exactly when every link of `T` is triangle-free.

**Proposition.** There is an absolute constant `N_0` such that no such symmetric rule separates all perfect-matching partner words for even `n>=N_0`.

**Proof.** Fix any four-set `{a,b,c,d}` and extend a pairing of the other `n-4` vertices to a perfect matching. Compare the two matchings obtained by using `{ab,cd}` and `{ac,bd}` on the four-set. They agree outside it. At the four changed coordinates, separation is possible only through one of the triples

`{a,b,c}, {a,b,d}, {a,c,d}, {b,c,d}`.

Therefore every four-set contains at least one edge of `T`; equivalently, the complement of `T` has no complete 3-uniform hypergraph on four vertices.

On the other hand `T` itself has no complete 3-uniform hypergraph on four vertices: if all four triples on `{a,b,c,d}` belonged to `T`, then the link at `a` would contain the triangle `bc,bd,cd`, contrary to triangle-freeness. Thus coloring triples red when they belong to `T` and blue otherwise produces a two-coloring with no monochromatic four-vertex complete 3-graph. By the finite 3-uniform Ramsey theorem, this is impossible once `n>=R_3(4,4)`. Take `N_0=R_3(4,4)`. ∎

In fact the unrestricted coordinate version is also bounded.

**Theorem.** There is an absolute `N_1` such that, for even `n>=N_1`, no collection of triangle-free graphs `H_i` on `[n] minus {i}` separates every pair of perfect-matching partner words by the rule `p_M(i)p_N(i) in E(H_i)`.

**Proof.** For each increasing triple `a<b<c`, record its three-bit color

`(1_[bc in H_a], 1_[ac in H_b], 1_[ab in H_c])`.

This is an eight-coloring of the triples of `[n]`. By the finite 3-uniform Ramsey theorem with eight colors, for all sufficiently large `n` there is a seven-element set `S` on which this color is constant, say `(A,B,C)`.

We must have `A=0`: otherwise choose `i` in `S` with three larger elements `x,y,z`; homogeneity puts all three edges `xy,xz,yz` in `H_i`, a triangle. Similarly `C=0`, using an `i` with three smaller elements.

Choose four elements `a<b<c<d` of `S`, fix an arbitrary perfect matching on the vertices outside them, and compare the two extensions

`M={{a,c},{b,d}}`,  `N={{a,d},{b,c}}`.

They agree outside the four-set. At coordinate `a`, their partners `c,d` form an edge of `H_a` exactly when `A=1`; at `b`, partners `d,c` again correspond to the first bit `A` because `b<c<d`; at `c`, partners `a,b` correspond to the third bit `C`; and at `d`, partners `b,a` again correspond to `C`. Since `A=C=0`, no coordinate separates `M,N`, a contradiction. ∎

Thus even completely coordinate-dependent triangle-free partner graphs cannot separate *all* perfect matchings asymptotically. Importantly, this does not remove factorial entropy.

**Lemma (factorial switch-free subfamily).** The perfect matchings of `K_n` contain a family `F_n` of size at least

`(n-1)!! / (1+2 binom(n/2,2))`

such that no two members differ only on four vertices.

**Proof.** Form the conflict graph on perfect matchings, joining two when their symmetric difference is one alternating four-cycle. From a fixed matching, choose two of its `n/2` edges and one of the two alternative pairings of their four endpoints. Hence this graph is regular of degree `2 binom(n/2,2)`. The elementary greedy independent-set bound `alpha>=|V|/(Delta+1)` gives the result. ∎

The `n`-th root of this lower bound is asymptotic to `sqrt(n/e)`, since the polynomial denominator has negligible `n`-th root. Thus pruning all immediate four-switch obstructions preserves exactly the desired growing entropy. The unresolved issue is constructing triangle-free coordinate graphs that separate such a family; finite SAT examples below do not reveal a scalable rule.

At `n=6`, an 8-triple hypergraph does separate all 15 matchings and has triangle-free links. `experiments/verify_matching_hypergraph_n6.py` independently checks this finite construction. Its base is only `15^(1/6)<2`, so it has no goal-ladder value.

For completeness, pruning does evade the theorem at small orders but currently performs poorly. Saved coordinate-dependent examples contain 28, 159, and 300 matching words at lengths 8, 10, and 12. The independent verifier `experiments/verify_pruned_matching_codes.py` reconstructs every matching, checks every coordinate graph for triangles, and checks every codeword pair for separation. Their bases are respectively about 1.517, 1.660, and 1.609, all below two. These finite examples provide no asymptotic construction or benchmark progress.