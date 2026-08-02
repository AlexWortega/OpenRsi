# STATUS

Updated: fifth and final focused oracle advice implemented; permutation-orbit guarantee rigorously banked.

## Main result: **PARTIAL**

No superexponential lower bound, coherent growing-base family, or explicit base above 3.199 has been proved in this run.

## Milestone

Read the definitive `prior/final/STATUS.md` and `prior/final/proof_ramsey.md`, plus the prior campaign status/attack logs. Distilled the exact problem, positive reductions, proved obstructions, banked families, and open gap into `ORACLE_BRIEF.md`.

The current precise gap is a scalable correlated construction: equivalently (i) `k`-color triangle-free complete-graph colorings of order `k^{Omega(k)}`; (ii) independence-two graphs with polynomial witness power and polynomially growing achieved strong-power base; or (iii) local-palette seeds `(N,g,s)` with `log N=Omega(s log s)` and `g=s^{O(1)}`.

## Oracle proposal 1: stationary automata — finite tests negative

The oracle's transfer-matrix condition is mathematically sufficient, but no asymptotic automaton was supplied. Immediate exact tests found only the binary baseline:

- all 32,768 symmetric Boolean transitions on `C5`, powers 2–6: maximum feasible closed-path count `2^q`;
- all 1,048,576 directed transitions on `C5` with row outdegree at most two, powers 2–8: maximum `2^q`.

Heuristic unrestricted-transition searches on the Groetzsch template found 11 paths at power 3 (below the inherited unrestricted 12-word code) and only binary counts at powers 4–5. These are non-results, not impossibility claims.

## Oracle proposal 2: anchored palettes — rigorously rejected in proposed form

For palettes `P_(a,B)={0,a} union B` on all `(r-1)`-subsets `B subset {3,...,g}`, if `g-2>=6(r-1)` then six disjoint `B_i` under one anchor induce a `K_6` whose every edge list is exactly `{0,a}`. Ramsey's elementary `R_2(3)=6` argument forces a monochromatic triangle. Thus the full family is impossible at the proposed `g~r^2` scale (in particular for `r>=6`), independently of its greedy algorithm. A verifier exhausts the finite two-color core.

Small greedy tests also retained only 8/20, 7/112, and 22/990 vertices at `(r,g)=(3,7),(4,10),(5,14)` in the best tested variants. These are diagnostics only.

A stronger proved necessary condition is the link-Ramsey bound `nu(L_F(C))<=R_(|C|+2)(3)-1` for every core `C`. It kills the natural maximum matching-number family, but logarithmic-core families show that this hierarchy alone does not remove factorial cardinality. No edge-coloring mechanism for those families is known.

## Varying-domain partial assignments — rigorously banked at bounded fractional complexity

A general partial-assignment rule is triangle-free when each coordinate's state graph is triangle-free and every object pair is separated by adjacent states at a shared coordinate. The proved fractional-cylinder lemma gives

`sum_f product_(x in B_f) chi_f(H_x[S_x])^(-1) <= 1`.

Hence if all used state graphs have fractional chromatic number at most `Q`, the family has at most `Q^r` objects, regardless of the number of possible domains. Binary/bipartite labels cap at `2^r`; domain variation cannot supply factorial entropy. Polynomially growing `chi_f` formally leaves room, but realizing the bound is precisely the unresolved correlated strong-power code problem.

## Background harvest

No relevant completed positive background job exists. Two cyclic `Z_1073` SAT rediscovery jobs in the sibling campaign remain unresolved after hours and cannot beat the classical base. Its L4 campaign has 303 certified negative palette cases with the final ordinary four-color case still running; this is negative evidence, not a growing-base route, and is not promoted here.

## Permutation-orbit permanent mechanism — rigorously banked

For triangle-free `H` on `n` vertices, the transitive greedy construction on all permutations guarantees `n!/per(M)` codewords, where `M` is the reflexive nonadjacency matrix. A new proved universal bound is

`per(M)>=n!/C^n`, `C=(5/2)(5/3)^(3/2)<5.38`.

It follows by peeling large independent neighborhoods, applying a dense bipartite factor criterion and van der Waerden on the residual matrix, and controlling the factorial block loss by entropy. Therefore this guarantee has uniformly bounded base. Exact permanent diagnostics on C5/Mycielski and random maximal triangle-free graphs were substantially worse. This does not bound the maximum separated permutation family, only the permanent/degree guarantee.

## Final assessment

**PARTIAL, below goal-ladder item (a).** No superexponential lower bound, growing-base family, or verified base above 3.199 is obtained. The durable new information consists of exact negative finite searches and rigorous obstructions to four plausible correlated mechanisms: stationary automata in tested classes, anchored palettes, varying-domain assignments of bounded fractional complexity, and the permutation permanent quotient. Every current finite claim has a passing `verify_*.py`. These are negative structural results, not progress on the requested lower bound.

## Integrity

No forbidden document, copy, summary, or discussion was accessed or searched. No proof assistant is used. Prior partial results remain explicitly partial.
