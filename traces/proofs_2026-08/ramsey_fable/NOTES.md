# Attack log (this run)

## Setup
- Re-ran prior verifiers: round1 verify_ramsey.py, sol verify_grotzsch_code.py,
  sol verify_f2_partitions.py — all exit 0. pysat + Cadical195 available. 24 cores.

## Referee kill of route: F_2^6 / 4 colors
SAT would give a triangle-free 4-coloring of K_64, i.e. R_4(3) >= 65. But
R(3,3,3,3) <= 62 is published (Fettes–Kramer–Radziszowski 2004). So the instance
is UNSAT (assuming literature), and deciding it is worthless for lower bounds.
Route dropped without spend.

## Main route: L_4 separation (locally-4 colorings beyond 61)
- L_3 = 16 proved in round1. Equality rigidity (round1): an extremal locally-s
  coloring on 1+sL_{s-1} vertices has, at EVERY vertex, exactly s incident color
  classes of size L_{s-1}, each inducing an extremal locally-(s-1) coloring.
- For L_4 = 65: 1 + 4 blocks of 16, each block an extremal locally-3 K_16.
  Question: are all extremal locally-3 16-vertex colorings globally 3-colored
  (i.e. the two Kalbfleisch–Stanton R(3,3,3)-critical colorings)? Sub-experiment:
  SAT for locally-3 K_16 with >= 4 global colors effectively used.
- Discriminating targets, in order of value:
  (i) locally-4 K_62 (any g): proves L_4 > R_4(3)-1 (strict separation);
  (ii) locally-4 K_N for N=51..61: beats all prior local-search plateaus (27);
  (iii) N=65 structured SAT with fixed KS blocks: could FIND extremal L_4.
- Prior art: sol found locally-4 only up to K_26 (g=5) by unstructured search.

## Experiments launched
(see below, appended chronologically)

## Referee analysis: what "beating 3.1996" actually requires (cyclic route)
- Classical base 3.1996 = 1073^(1/6) from Fredricksen–Sweet symmetric sum-free
  6-partition of Z_1073 (equivalently S(6) >= 536).
- KEY OBSERVATION: a symmetric sum-free k-partition of Z_n restricts on orbit
  reps [1..(n-1)/2] to an INTEGER sum-free k-partition (if a+b<=(n-1)/2 then the
  mod-n line constraint is the integer constraint). Hence such a partition
  implies S(k) >= (n-1)/2. Consequences:
  * k=5: Heule proved S(5)=160, so cyclic symmetric 5-partitions cap at n=321
    (base 3.1723). Route closed by known theorem — do not search n>321, k=5.
  * k=6: n >= 1075 would improve the 25-year-old record S(6) >= 536. Open.
  * k=7: n >= 3435 needed for base > 3.1996 (needs S(7) >= 1717 vs known >= 1680).
- F_2^d partitions are hopeless for the record: base 2^(d/k), and d/k <= log2(3.2)
  = 1.678 needs k >= 0.6d, but sum-free classes in F_2^d have size <= 2^(d-1)
  (perfect difference-cover issue) — empirically k ~ d - O(1) achievable only
  with base < 3. Killed the (8,5),(9,6) SAT runs: even SAT gives base 3.03/2.83.
- Killed sat_local4 z5zb ansatz: UNSAT for b in {6,8,9,10,11,12,13}; K_25 max
  for that ansatz. Groupwise SAT at N=30 too slow; min-conflicts stalls (62:
  best 686). L_4 route parked.

## New route: dilation-invariant (coset) Schur partitions
Classes = unions of cosets of a subgroup H <= Z_p^* (with -1 in H for symmetry).
Few variables ((p-1)/|H| cosets), SAT decides fast. Novel vs F-S templates.
Scan: k=6, primes p in [1075,1400]; k=7, primes p in [3435,4300]; various |H|.
Any SAT => verified new record base > 3.1996 => goal (a).

## Rigorous ceiling for the cyclic route (proved this session)
LEMMA (cyclic->Schur restriction): if Z_n\{0} partitions into k symmetric
sum-free classes (a+b=c mod n forbidden within a class, a=b allowed), then
restricting each class to [1, floor((n-1)/2)] gives an integer sum-free
k-partition of [1, floor((n-1)/2)] (for a,b,a+b all <= (n-1)/2 the mod-n sum
is the integer sum). Hence floor((n-1)/2) <= S(k) (Schur number), i.e.
n <= 2S(k)+2.
CONSEQUENCES:
- k=5: S(5)=160 (Heule 2017, proved) => cyclic n <= 322; base <= 322^(1/5)=3.174.
  The cyclic 5-color route can NEVER reach 3.1996. Search space closed.
- k=6: cyclic n >= 1076 would give S(6) >= 537, a new Schur record (known
  S(6) >= 536, Fredricksen–Sweet 2000). So goal (a) via cyclic k=6 is
  exactly a Schur-record improvement. Same for k=7 (n >= 3434 => S(7) >= 1716,
  vs known >= 1680): weaker than record only in range [3362..3434)?? check:
  known S(7) >= 1680 => cyclic k=7 could a priori reach n = 3362 (base 3.1898);
  beating 3.1996 needs n >= 3435 => S(7) >= 1717 — again beyond the record.
- Realism: Heule-scale SAT efforts define these records; our mc/SAT lottery
  tickets (n=1076 k=6, n=3434 k=7) continue in background but expectations low.
- Non-cyclic k=6, N >= 1076 colorings are NOT ruled out by the lemma (the
  restriction argument needs difference structure). But direct search at
  K_1076 is far beyond local-search reach; and one-vertex extension of a
  difference coloring is blocked by independence-number counting (α of each
  356-regular triangle-free circulant ~ n log d/d ≈ 18, sum over 6 colors
  ≈ 107 << 1073) — heuristic estimate, not a theorem.

## Harvest ~1.5h mark
- k=6 cyclic min-conflicts (1073/1076/1079): stalled at 27-33 conflicts across
  5 seeds. Consistent with Schur-record-hardness. Killed all but SAT full/blocks
  n=1073 (kept as the only lottery — record REDISCOVERY, not improvement, so
  actually also low value; keep blocks1073+full1073 only).
- k=7 n=3434: stalled at 95 conflicts. Killed.
- Dilation scan g of small order mod 1073: orders 2,3,4,6 all selfbad
  (since some orbit contains {x,2x} or forms self-triple). Route dead: -1 in
  <g> forces large orbits; small-order g mostly selfbad. Banked.
- local3_g4 SAT (is L_3=16 extremal coloring forced to be globally 3-colored?)
  still running >40min. Keep — this is the structurally informative one.

## Structure of locally-3 triangle-free K_16 (derived, to be SAT-checked)
- Exhaustive check (this session): every locally-2 triangle-free K_5 is globally
  2-colored (two complementary C_5s). [code inline, rechecked below in verifier]
- Rigidity at N=16=1+3*5: at any vertex v, exactly 3 incident colors, classes
  exactly 5, each class an extremal locally-2 K_5 => globally 2-colored C_5+C_5.
- Hence all 5 vertices of a class share one palette {a} u {x,y} (a = edge color
  to v, x,y = class-internal colors).
- Counting: every vertex is 5-regular in each of its 3 colors; sum of support
  sizes = 48; Mantel => each support >= 10 => AT MOST 4 global colors (g<=4).
  So L_3-extremal colorings have g=3 or g=4; SAT question is only g=4.
- g=4 case: each vertex misses exactly 1 color; m_c = #missing color c, sum
  m_c=16, each m_c even (support 16-m_c must be even for 5-regularity).

## Derived structure for extremal locally-4 K_65 (all steps proved)
Fix v0. 65 = 1 + 4*L_3 extremal => equality lemma: every vertex sees exactly 4
colors, each on exactly 16 edges. Classes C_0..C_3 (by v0-edge color i), each an
extremal locally-3 K_16 => (rigidity thm) exactly 3 internal colors pal_i, and
every vertex of C_i sees all 3 internally + color i to v0. Hence ALL vertices
of C_i share the palette P_i = {i} ∪ pal_i (|P_i| = 4), and:
- internal edges of C_i: colored from pal_i, each vertex 5-regular in each
  (rigidity/equality within the class);
- cross edges C_i-C_j: colored from P_i ∩ P_j;
- per-vertex cross-degrees: u in C_i has 48 cross edges: exactly 15 colored i
  and exactly 11 colored c for each c in pal_i (16-regularity: color i gets
  1(v0)+15 cross; c in pal_i gets 5 internal + 11 cross).
Symmetry: may permute colors {1,2,3} (with classes) and {4..15}; canonicalize
pal_0 to one of {1,2,3},{1,2,4},{1,4,5},{4,5,6} via double prefix-closure.
This yields sat_L4_65_struct.py; SAT <=> L_4 = 65 (conditional only on the
proved equality lemma + rigidity theorem).

## MAJOR HARVEST: all 303 non-classical palette cases for L_4=65 are UNSAT
Driver ran 304 canonical palette systems; 303 UNSAT (median ~60s); the single
pending case pal_i = {0,1,2,3}\{i} is an ordinary 4-coloring of K_65, i.e.
would give R_4(3) >= 66, contradicting R_4(3) <= 62 (FKR 2004). Hence
(conditional on the enumeration's completeness — refereed below — and on
solver correctness) NO extremal locally-4 K_65 exists: **L_4 <= 64**.
Referee checklist of derivation:
 1. equality lemma at s=4 (round1, proved): classes of exactly 16, every vertex
    sees exactly 4 colors each 16-regular. OK.
 2. rigidity theorem (this run, verified): class internal palette exactly 3
    colors; every class vertex sees all 3 internally (equality lemma at s=3).
    OK => vertex palettes constant per class, P_i = {i} u pal_i.
 3. degree split: color i: 1 (v0) + 15 cross; c in pal_i: 5 internal + 11
    cross. OK (5-regularity from equality lemma at s=3).
 4. capacity filters and extras <= 4 (each extra in >= 2 palettes; 16 slots,
    colors 0-3 take >= 8). OK.
 5. canonicalization group: S_4 on classes acting on colors 0-3 + renaming of
    extras. Valid symmetry of the constraint system. OK.
TODO for promotion to theorem: (i) rerun all 303 with DRAT proof logging +
drat-trim verification (drat-trim compiled at /tmp/drat-trim/drat-trim);
(ii) for the g=4 case, either cite FKR or obtain UNSAT+DRAT directly;
(iii) write verify_L4_64.py that checks the enumeration and the certificates.

## L_4 <= 64 pipeline complete
- 304 canonical palette systems; 303 kissat-UNSAT with drat-trim-verified DRAT
  proofs (results in experiments/L4cert/*.result); the ordinary-4-coloring case
  covered by R_4(3) <= 62 (FKR 2004) citation; direct DRAT run continuing.
- verify_L4_64.py re-enumerates cases from scratch, checks results, and
  re-solves 3 random cases end-to-end. Exit 0.
- Consequence recorded in proof_ramsey.md §5. The "local-seed factorial tower"
  route is dead at s=4: L_4 <= 64 < 65. Note L_4 >= R_4(3)-1 >= 50.
- Adversarial self-check performed: equality-lemma dependence is legitimate
  (65 = 1+4·16 forces extremality of every neighborhood class); degree
  accounting re-derived twice; capacity filters proven necessary before use;
  canonicalization is a symmetry of the constraint system (classes+colors 0-3
  relabeled jointly; extras renamed); the sanity encoding at s=3 correctly
  returned SAT for the realizable g=3 palette system.

## Session close-out
- All background lotteries killed (cyclic record rediscovery, coset scans).
- The straggler DRAT for the ordinary-4-coloring case exceeded 20GB/2h and was
  abandoned; that case rests on the FKR 2004 citation (R_4(3) <= 62), which is
  strictly stronger than what is needed (no triangle-free 4-coloring of K_65).
- Final verifier suite (all exit 0): verify_cyclic_ceiling.py,
  verify_local3_rigidity.py, verify_L4_64.py, verify_local4.py,
  verify_cyclic_partition.py.
- Next-step recommendations for future runs, given this run's theorems:
  1. L_4 exact value: extend rigidity analysis to non-extremal locally-4
     colorings of K_51..K_64 (the equality lemma no longer applies below 65;
     new structure needed, or incremental SAT at N=51 with 6-7 global colors).
  2. Growing-base mechanisms must avoid (i) difference/cyclic structure
     (Schur-capped), (ii) extremal local towers (rigidity-killed). Remaining
     live directions: correlated strong-power codes over growing graph
     families with growing fractional chromatic number of the complement,
     and non-difference algebraic colorings (e.g. norm/trace-based over
     growing fields) — untouched by this run's negative results.
