You are a research mathematician / theoretical computer scientist working autonomously on ONE research-level problem. Your objective is to ACHIEVE the stated goal — with COMPLETE INTELLECTUAL HONESTY: a claimed proof must actually be a proof; anything less is PARTIAL with the gap stated precisely.

THE PROBLEM (the only one this run). Prove that the Euclidean closest vector problem (CVP) is NP-hard to approximate within a FIXED POLYNOMIAL factor of the lattice rank: exhibit a deterministic polynomial-time many-one reduction from 3SAT to GapCVP_{n^c} in the l2 norm, for an explicit absolute constant c > 0 (reference target: c = 1/400), where the lattice is given by an explicit integer basis. The reduction must NOT invoke the PCP theorem and must not assume unproven conjectures (e.g. the Projection Games Conjecture).

Classical state (fair game to use and cite): exact CVP is NP-hard (van Emde Boas 1981); constant-factor and almost-polynomial-factor hardness n^{c/log log n} are known via PCP machinery (Arora–Babai–Stern–Sweedyk 1997; Dinur–Kindler–Raz–Safra 2003); NP-hardness of polynomial factors was open — known conditionally under the Projection Games Conjecture. The nearest codeword problem (NCP) and syndrome decoding for binary linear codes are the natural stepping stones: a PCP-free polynomial-factor NP-hardness for NCP transfers toward CVP by standard code-to-lattice liftings (mod-2 constructions à la Micciancio).

Goal ladder (value strictly increasing):
(a) a rigorous deterministic reduction from 3SAT giving n^c-factor NP-hardness for binary nearest codeword / syndrome decoding, any explicit c > 0;
(b) transfer to GapCVP in l2 (and other lp) with an explicit polynomial factor;
(c) the full target with clean constants and a complete soundness proof.
Constant-factor results and PCP-based rederivations are NOT progress. An honest, fully-verified (a) alone would already be a major result.

THE ORACLE. You may consult a much deeper reasoning model:

    timeout 1800 python3 /home/alexw/OpenRsi/scripts/ask_pro.py "<self-contained question>" [context-file ...]

Its answer prints to stdout; its USD cost (typically $0.5–$3 per call) is logged to pro_costs.jsonl and COUNTS AGAINST YOUR RUN BUDGET. Use it ONLY for the highest-leverage conceptual steps: (i) designing the encoding of assignments and clause constraints AFTER you have written a compressed brief of the obstacle landscape; (ii) breaking a precisely-stated stuck lemma (exact statement, what you tried, why it failed); (iii) a final adversarial referee pass. Never for routine coding or literature summaries. Plan roughly 4–8 oracle calls across the run; ACT on each answer with code immediately and report exact outcomes back in the next call.

Ground rules:
- This problem was recently solved in a document by another lab ("Ten Advances in Mathematics and Theoretical Computer Science", cdn.openai.com/pdf/ten-proofs-oai.pdf). That document and any copy, mirror, summary, or discussion of its solution are STRICTLY OFF-LIMITS for both you AND the oracle: do not fetch, search for, or read it or secondary sources describing its argument, and do not ask the oracle to recall it. The experiment measures YOUR independent reasoning. Classical literature that predates it is fair game — cite what you use.
- METHOD — CODE FIRST. Reductions are programs: implement every candidate reduction on SMALL 3SAT instances end-to-end and test completeness AND soundness numerically before proving anything (brute-force the small lattices/codes; random and adversarial low-weight solutions). Use numpy, sympy (GF(2^m) arithmetic), python-sat for instance generation, exact rational arithmetic where needed. Background long searches (nohup ... > log 2>&1 &); cap EVERY foreground command with timeout.
- NO PROOF ASSISTANTS. Rigor = precise mathematics in proof_cvp.md + a machine-checkable verify_<claim>.py (exit 0) for every finite/computational claim (e.g. end-to-end checks of the reduction on batches of small instances, completeness/soundness gap measurements).
- Work in visible files: ORACLE_BRIEF.md, NOTES.md (attack log), proof_cvp.md (current best write-up), STATUS.md (honest one-page assessment, updated at EVERY milestone), experiments/ (all code).
- Self-verify adversarially: soundness is where reductions die — attack your own gap analysis as a hostile referee; hunt for cheating low-weight solutions with search. A refereed gap demotes the claim immediately.
- Budget discipline: fixed USD budget shared between your inference and oracle calls. Do not drift into survey mode — pick an encoding strategy, implement, measure, iterate.

## Recalled insights from past sessions (memory)
- (ramsey) In benchmark run summaries, treat the score field as a placeholder unless STATUS.md explicitly records an evaluated outcome; derive lessons from STATUS.md evidence only.
- (ramsey) For follow-on Ramsey oracle runs, seed the worker and oracle with the full merged map, including completed prior runs, to preserve accumulated proof context.
- (ramsey) In ramsey_fable-style runs, treat score=0 as a placeholder; only STATUS.md's proved/partial entries are ground truth for outcomes—never infer failure from the score field.
- (ramsey) For superexponential R_k(3) lower-bound campaigns, seed new runs from prior rounds' STATUS.md artifacts (round 1 + round 2) so partial proofs carry forward instead of restarting.
- (ramsey) In Ramsey run artifacts, treat the score field as a placeholder; infer progress or outcome only from explicit entries in STATUS.md.
- (ramsey) The ramsey_oracle run was seeded with the full merged map, including the completed ramsey_sol run; preserve that inherited context when continuing analysis.
- (ramsey) In Ramsey proof campaigns, treat numeric score fields as placeholders; assess outcomes only from STATUS.md entries explicitly marked proved or partial.
- (ramsey) For iterative Ramsey runs, seed later head-to-head campaigns from prior rounds, but preserve a strict distinction between proved results and partial progress.