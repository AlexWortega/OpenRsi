# STATUS (this run)

## Problem — superexponential lower bound for R_k(3): **PARTIAL**

Main statement OPEN. No superexponential bound; no base > 3.19963 achieved.

## Proved this run (each with a passing verifier)

1. **Cyclic ⇒ Schur ceiling lemma** (`proof_ramsey.md` §2,
   `verify_cyclic_ceiling.py` exit 0): a symmetric sum-free k-partition of Z_n
   restricts to an integer sum-free k-partition of [1, floor((n-1)/2)]; hence
   n <= 2·S(k)+2.
   - With S(5)=160 (Heule 2017, cited): the cyclic 5-color route is capped at
     base 322^{1/5} ≈ 3.1735 < 3.19963. Route provably closed.
   - For k=6 (7): beating 3.19963 cyclically is EQUIVALENT to improving the
     Schur records S(6) >= 536 / S(7) >= 1680 to >= 537 / >= 1717.
2. **Rigidity theorem: every triangle-free locally-3 coloring of K_16 uses
   exactly 3 global colors** (`proof_ramsey.md` §4, `verify_local3_rigidity.py`
   exit 0: profile completeness + exhaustive C backtracker ~4.3e9 nodes,
   cross-checked by CaDiCaL UNSAT on an independent encoding).
3. **L_4 <= 64** (`proof_ramsey.md` §5, `verify_L4_64.py` exit 0): there is NO
   triangle-free locally-4 coloring of K_65. Proof = equality lemma (round1) +
   rigidity theorem + full palette-system enumeration (304 canonical cases) +
   kissat UNSAT with DRAT certificates verified by drat-trim on 303 cases +
   published R_4(3) <= 62 (FKR 2004) for the ordinary-4-coloring case.
   FIRST STRICT FAILURE of the recursion L_s <= 1+sL_{s-1} (sharp at s=2,3):
   L_1,L_2,L_3 = 2,5,16, now 50 <= L_4 <= 64. The extremal-tower route to
   factorial local seeds is dead at its first open level.
4. **New verified dilation-invariant partitions** (`verify_cyclic_partition.py`
   exit 0): Z_43/4 (base 2.5607), Z_41/4, Z_37/4, Z_13/3. Machinery tests only.
5. **Locally-4 seed K_27, g=5** (`verify_local4.py` exit 0). L_4 >= 27 within a
   5-group ansatz (not extendable one-vertex within the ansatz).

## Negative/banked this run
- Z_5 x Z_b locally-4 ansatz: UNSAT b ∈ {3,6,8..13}. Banked.
- Coset/dilation-invariant partitions at Schur-record scale: all UNSAT/
  impossible (k=6 p∈[900,1450], k=7 p∈[3434,4000], idx<=96). Banked.
- Cyclic k=4: no symmetric sum-free 4-partition of Z_n for 46<=n<=61.
- Min-conflicts at record scale (Z_1073/1076/1079 k=6, Z_3434 k=7): stalled
  (best 27-33 / 95 conflicts). Killed; consistent with record-hardness.
- F_2^d routes for record bases: closed a priori (max base ~3.03 < 3.19963).

## Still running
- kissat+DRAT on the final (ordinary 4-coloring) L_4 case — optional, covered
  by FKR citation.
- sat_cyclic full/blocks n=1073 k=6 (record rediscovery lottery; low value).

## Honest assessment
Goal (a) unmet; goals (b),(c) unmet. Contributions: two structural theorems
(rigidity of extremal locally-3 colorings; L_4 <= 64 killing the factorial
tower at its first level) and a reduction lemma placing the entire cyclic
family under Schur-number ceilings. Net effect on the problem: the two most
tractable-looking routes to a growing per-color base (cyclic scaling; rigid
extremal local towers) are now PROVABLY dead or record-hard, so future budget
must go to genuinely correlated, non-difference, non-extremal constructions.
All claims above are backed by verifiers that exit 0 in this run, or explicit
literature citations predating the excluded document.
