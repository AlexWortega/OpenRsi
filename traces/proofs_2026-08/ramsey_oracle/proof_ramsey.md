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

This obstruction applies only to the elementary transitive greedy guarantee `n!/per(M)`, not to the maximum separated permutation family, which could conceivably be larger.