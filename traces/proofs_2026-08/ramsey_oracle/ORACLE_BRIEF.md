# Oracle brief: superexponential multicolor triangle Ramsey lower bound

## Objective and integrity constraint
For `R_k(3)`, prove either

`R_k(3) >= (c k^{1/3}/log k)^k`

for an absolute `c>0`, or any bound `R_k(3)>=k^{c k}`. Equivalently, construct triangle-free `k`-edge-colorings of complete graphs with per-color base `N^{1/k}` unbounded. Goal ladder: (a) explicit verified base above classical `3.199`; (b) a coherent family with provably growing base; (c) the full bound. Fixed bases below 3.199 are not progress.

The recent OpenAI “Ten Advances...” document and every copy, summary, or discussion of its proof are forbidden. Do not recall, reconstruct, cite, search for, or use it. Classical pre-existing ideas are allowed.

## Exact formulations and positive tools
1. If `alpha(G)<=2`, then an independent code `C subset V(G)^m` in the strong power gives a triangle-free `m`-coloring of `K_|C|` by the first coordinate containing a distinct nonedge. Conversely any triangle-free `k`-coloring on `N` vertices yields a graph with `alpha<=2` and a size-`N` independent set in its `k`th strong power. Hence exactly

`max_{alpha(G)<=2} alpha(G^{boxtimes k}) = R_k(3)-1`.

The capacity language is useful only with coherent/effective families, since arbitrary `G_k` restates Ramsey.

2. Effective-capacity criterion: if for every large `t` there is `G_t`, `alpha(G_t)<=2`, and `q_t<=t^D` with

`alpha(G_t^{boxtimes q_t})^{1/q_t} >= t^a`,

then multiplication of codes and padding imply `R_k(3)>=k^{c k}`. Thus polynomially growing achieved base at polynomial witness power suffices.

3. Missing-color/local-palette lemma: a triangle-free outer coloring on `N` vertices, using `g` global colors but at most `s` colors at each vertex, gives

`R_k(3)-1 >= N(R_{k-s}(3)-1)` for `k>=g`,

and hence `R_k(3)-1 >= N^{1+floor((k-g)/s)}`. Therefore seeds with `log N >= c s log s` and `g<=s^{O(1)}` suffice. The extremal locally-`s` order obeys `L_s<=1+sL_{s-1}<3s!`, with equality known for `L_1=2,L_2=5,L_3=16`; this leaves the right factorial scale possible but no construction with controlled global palette.

4. Exact lexicographic product uses disjoint palettes: `(N_1,k_1)*(N_2,k_2)=(N_1N_2,k_1+k_2)`. Fixed seeds cannot make a growing base. Universal color-only palette compression cannot save colors: mixed triangles force outer and inner image palettes disjoint.

5. Finite positive benchmark: complement of the 11-vertex Groetzsch graph has a verified 12-word independent code in power 3, base `12^{1/3}`. Translation partitions include `F_2^7/5` and `F_2^8/6`. All are fixed-base and below 3.199. The unrestricted partition of `F_2^6\{0}` into four sum-free classes is unresolved, but even success is only a finite seed.

## Proved obstructions / routes not to repeat
- Independently sampled product codewords: direct first moment, edge-count expurgation, and basic dependency-graph LLL cannot beat base 2. This remains true with coordinate-dependent marginals, via Motzkin--Straus for triangle-free complements.
- `Theta(G)<=chi_f(overline G)`. Bipartite complements have capacity exactly 2. Shift-graph complements have capacity at most 4 via random cuts. Generalized shift complements have capacity at most 10 via binary de Bruijn patterns. Triangle-free Kneser complements have `chi_f<3`.
- Fixed seeds plus ordinary products/amplification stay fixed-base. First-difference polynomial evaluation is just this. Partial-permutation trees have factorially many vertices but quadratic local palette, and their raw pair-labels are compression-rigid; truncation remains fixed-base.
- Translation/group difference partitions require inverse-closed product-free classes. Any group with 3-torsion is impossible (`g,g^{-1}=g^2`). Tested 2-groups (dihedral, unitriangular, wreath), odd Heisenberg, affine/metacyclic families have fixed/decreasing bases. `UT(n,2)` highest-coordinate coloring has `binom(n,2)` classes; observed compression is constant only.
- Extensive tested/banked finite families: cyclic/shifted/interval rules, Mycielski and random/circulant Cayley cubes, permutation quotients and node-dependent permutation trees, local palettes, wreath towers, polynomial/projective/bilinear rules, constant-weight/Kneser variants. None exceeds base 2.63 except inherited classical constructions; no growing mechanism.
- A large fractional chromatic number is only an upper bound on capacity, not a lower bound. High chromatic triangle-free graphs alone do not give codes.
- Local-palette type obstruction: palettes are pairwise-intersecting subsets of `[g]`; each exact palette type of size <=s has multiplicity at most `R_s(3)-1`, and there are at most `sum_{i=0}^{s-1} binom(g-1,i)` types when `s<=g/2`. Any proposed local seed must survive this accounting.

## Precise open gap
Design a genuinely correlated, scalable object—not a fixed seed or iid product—of one of these equivalent forms:

(A) triangle-free colorings with `k` colors on `k^{Omega(k)}` vertices;
(B) independence-two graphs with polynomial witness power and polynomially growing achieved strong-power code base;
(C) local-palette seeds `(N,g,s)` with `N>=s^{c s}`, `g<=s^{O(1)}`.

We need concrete candidates precise enough for immediate small-parameter implementation: explicit vertex set, edge-color/code rule (or finite CSP), parameter prediction, and the exact lemma whose proof would establish growing base. Prefer structural correlation across coordinates and explain why it evades the obstructions above. Please propose only 1–2 highest-leverage candidates, with small tests that can quickly falsify them. Adversarially flag circular steps (especially any hidden appeal to a Ramsey construction of the same strength).

## Current-run oracle proposals and exact failure modes (do not repeat)

### Stationary closed-walk automata
The first proposal took *all* length-q closed walks of a Boolean transition matrix A and imposed exact pair synchronization via `tr(B^q)=tr(A^q)`. This condition is sufficient, but the proposed pivotal lemma was the original zero-error correlation problem in new notation; no transition family was given. Exact tests:
- all `2^15=32768` symmetric Boolean 5x5 matrices over `H=C5`, q=2..6: optimum exactly `2^q`;
- all `16^5=1,048,576` directed matrices whose five rows are arbitrary subsets of size at most two, q=2..8: optimum `2^q`.
- unrestricted heuristic on Groetzsch found W=11 at q=3, below inherited unrestricted code 12; q=4,5 gave 16,32.
Thus C5 branching specifically creates off-diagonal bad cycles. No universal automaton upper bound is claimed. Bounded-period layered programs are phase lifts of stationary ones, while unbounded layers risk encoding an arbitrary code tautologically.

### Anchored palettes
The second proposal used every vertex `(a,B)`, `a in {1,2}`, `|B|=r-1`, with palette `{0,a} union B`, at `g~r^2`, and greedily kept each color graph triangle-free. It fails structurally, not merely algorithmically: when `g-2>=6(r-1)`, six disjoint B's under one anchor have every pair-list exactly `{0,a}`, forcing a forbidden two-colored K6. Small greedy retention was only 8/20, 7/112, 22/990 at suggested early parameters.

For any retained family F, the proved general necessary condition is
`nu(L_F(C)) <= R_{|C|+2}(3)-1`
for every core C: disjoint petals over C give a clique whose edge lists are the fixed `|C|+2` colors `{0,a} union C`. This kills the natural Erdos-matching extremizer (sets meeting a fixed 5-set): its one-point link contains 17 disjoint petals and forces a 3-colored K17. But the condition does not itself reduce entropy enough: all sets containing a fixed core of size O(log r) still number `exp((1-o(1))r log r)` and evade these simple link tests. The unsolved step is an actual correlated edge rule using common/petal colors. Do not propose further set-family pruning without such a rule.

Every finite claim above now has the unified passing verifier `experiments/verify_current_finite_claims.py`.

### Varying-domain partial assignments
A post-failure rule labeled each incidence `x in B` by a state of a triangle-free graph `H_x`; pairs must share an x with adjacent states and are colored by x. This is always triangle-free. The oracle supplied, and the write-up now proves, the sharp fractional-cylinder bound
`sum_(f in F) product_(x in B_f) 1/chi_f(H_x[S_x]) <= 1`.
Consequently bounded-`chi_f` states give at most `Q^r` objects regardless of how many domains exist; binary/bipartite states cap at `2^r`. Domain variation supplies no factorial entropy. High-`chi_f` polynomial-size triangle-free states formally permit `r^{Theta(r)}`, but constructing assignments near the bound is exactly the missing correlated OR-power code problem. Small exact tests agree: K2 gives maxima 4 and 8 at r=2,3 despite increasing universe; C5 gives only 5 at r=2 for universes 3,4,5. Passing checker: `experiments/verify_fractional_cylinder.py`.

### Permutation-orbit code attempt
A fresh explicit idea takes all permutations of `V(H)` and selects a large orbit-code greedily: two permutations are separated if some coordinate images form an H-edge. By vertex transitivity under coordinate permutation, a greedy independent set in the bad-pair graph has size at least `n!/D`, where `D=per(M)` and `M_uv=1` iff `u=v` or `uv` is a nonedge of triangle-free H. This yields an n-coordinate triangle-free coloring of size `n!/D`. Exact subset-DP permanents show the achieved bases are only 1.560, 1.468, 1.370 for C5 and its 11/23-vertex Mycielski extensions; 30 random maximal triangle-free graphs at n=20 peaked at 1.592. The failure is now rigorous and universal for this greedy guarantee: a neighborhood-peeling argument plus a dense bipartite factor lemma and van der Waerden proves `per(M)>=n!/C^n` for `C=(5/2)(5/3)^(3/2)<5.38`. Hence `(n!/D)^(1/n)<5.38` for every triangle-free H. This does not upper-bound the maximum separated permutation subset, only the permanent/degree lower-bound mechanism. Verifiers: `experiments/verify_permutation_orbit.py`, `experiments/verify_permanent_bound.py`.
