# OpenRSI on ALE-Bench **Full** (all 40 problems, Full seeds, Opus 4.8)

Config: Opus 4.8 inner solver, dynamic eval budget (cap 50, patience 6), **Full seeds**
(`lite_version=False`, proper AtCoder performance), best-of-1 over all 40, then a best-of-3 retry
pass on the sub-1500 problems. Data: local `ALE_BENCH_DATA` snapshot.

## Result: mean = **1432.9** over 40 problems

Reference: ALE-Agent (SOTA) 1879 · human avg 1260. So OpenRSI on the full set lands **above the human
average but well below SOTA** — and notably below our own **Lite-subset** number (1625, or higher with
best-of-k). Why the gap is explained below.

| problem | best | | problem | best |
|---------|------|-|---------|------|
| ahc001 | 1826 | | ahc025 | 1214 |
| ahc002 | **2593** | | ahc026 | 223 ⚠ |
| ahc003 | 2380 | | ahc027 | **0** ✗ |
| ahc004 | 1888 | | ahc028 | 2218 |
| ahc005 | 2533 | | ahc030 | **0** ✗ |
| ahc006 | **3218** | | ahc031 | 1277 |
| ahc007 | 2165 | | ahc032 | 1664 |
| ahc008 | 1252 | | ahc033 | **0** ✗ |
| ahc009 | 2411 | | ahc034 | 1745 |
| ahc010 | 1347 | | ahc035 | 1369 |
| ahc011 | **0** ✗ | | ahc038 | 1538 |
| ahc012 | 2614 | | ahc039 | 2292 |
| ahc014 | **0** ✗ | | ahc040 | 1191 |
| ahc015 | 1740 | | ahc041 | **2783** |
| ahc016 | 1468 | | ahc042 | 1333 |
| ahc017 | **0** ✗ | | ahc044 | 1861 |
| ahc019 | **0** ✗ | | ahc045 | 1456 |
| ahc020 | −70 ⚠ | | ahc046 | 1119 |
| ahc021 | 2124 | | future-contest-2022-qual | 1055 |
| ahc024 | 1921 | | toyota2023summer-final | 1568 |

## Honest analysis — where the gap comes from

- **On most problems the agent is strong:** 11 problems scored **2100–3218** (ahc006 3218, ahc041
  2783, ahc012 2614, ahc002 2593, ahc005 2533…). On these it is competitive with or above SOTA.
- **~8 problems fail on Full seeds** (7 hard zeros + ahc020=−70, ahc026=223). These are **not**
  transient: e.g. **ahc011 scores 1878 on the Lite subset but 0 on Full**. The Full private cases are
  more numerous / harder, so a solution that is valid & fast enough on Lite **TLEs or produces invalid
  output on Full**, or the agent can't reach a valid solution inside the wall-clock budget. Repeated
  sampling (best-of-3) recovered some (ahc002 1324→2593) but not the systematic TLE failures.
- **Implication:** closing the last gap to ALE-Agent's 1879 on the *full* set is **not just a
  sampling problem** — it needs per-problem tuning for the tighter Full time limits (faster inner
  loops, problem-specific heuristics, longer/looser per-eval limits), which is exactly the
  hand-crafted specialization ALE-Agent brings.

## Summary vs our other numbers

| setting | mean | note |
|---------|------|------|
| ALE Lite (Opus, deep budget) | 1625 | 10 curated problems |
| ALE Lite (best-of-k, partial) | ~1800+ trend | repeated sampling on the 10 |
| **ALE Full (Opus, 40 problems)** | **1432.9** | full set; ~8 Full-seed failures drag it down |
| ALE-Agent (SOTA) | 1879 | 15× sampling + per-problem domain knowledge |

Cost: ≈ $84 (first pass) + the retry pass (~$50, killed before its final tally) ≈ **~$135**.
