## 1. Bilateral rank-condenser fold

**Mechanism / expected move.** For a reduced tensor word \(W\in D\otimes D\), replace coordinate puncturing by  
\[
\Phi(W)=\bigoplus_{s=1}^S A_sWB_s^\top ,
\]
where the binary-expanded \(A_s,B_s\) come from a canonical rank-condenser family seeded by the parity-check matroid of \(D\). The hope is that sparse YES words activate few entries while every NO mixed matrix survives in many blocks, using \(Sr^2\ll n^2\) outputs.

**Obstruction check.** O1 bounded signatures: global dense maps, not local-view signatures. O2 marginals/tableaus: no wire interfaces. O3 scopes: blocks see all coordinates. O4 phases: no phases. O5 integer fibers: binary construction. O6 fingerprints: no assignment columns. O7 tensor amplification: directly addresses arbitrary mixed words and is neither coordinate sampling nor type merging; no theorem guarantees success. O8 exact transfer applies if a binary gap survives.

**Smallest experiment.** On the existing \(q=3,m=8\) suite, freeze \(r=2,3\) Vandermonde/subspace-design maps, enumerate every mixed square, plus all-eight and holonomy cases; report active rank and YES/NO minima.

**Falsification / likely death.** Kill if best NO \(\le\) worst YES or output-adjusted exponent fails to beat \(25/9\). Dense condensers likely flatten every nonzero word to similar weight.

---

## 2. Explicit noncommutative ordered-pair fold

**Mechanism / expected move.** Replace the killed commutative algebra by \(M_5(\mathbb F_2)\). Canonically label triple \(i\) by left and right matrices \(L_i,R_i\), and map ordered tensor coordinate \((i,j)\) to \(\operatorname{vec}(L_iR_j)\); noncommutativity removes the automatic \((i,j)\leftrightarrow(j,i)\) kernel. Expected move: compress 64 moving coordinates to 25 while retaining the \(9\) versus \(25\) square gap.

**Obstruction check.** O1: not a bounded local Boolean signature, although all-eight may still expose a relation. O2–O3: no marginals or scope hierarchy. O4: no phase consistency. O5: binary, not an integer repair gadget. O6: polynomial triple dictionary, not assignments. O7: a dense structured fold attacking all mixed words, outside fixed sampling; square-length accounting remains mandatory. O8 applies conditionally.

**Smallest experiment.** Freeze  
\(L_i=P^i(I+E_{0,h_i})\), \(R_j=(I+E_{h_j,0})P^{2j}\), \(h_i\) from canonical incidence columns, in \(M_5(\mathbb F_2)\). Enumerate the existing 10 YES, 200 NO, all-eight, affine-closure, and holonomy families.

**Falsification / likely death.** Kill on any pointed kernel or ratio \(\le1\). Most likely, the 25-dimensional bilinear image has a large mixed-tensor kernel unrelated to commutativity.

---

## 3. Möbius connected-collision lift

**Mechanism / expected move.** Mutate Schur walks by indexing each *connected vertex set* \(S\) in the triple-incompatibility graph once, rather than replicating a collision through many walks. Add the squarefree feature \(\prod_{i\in S}x_i\), transformed to the Möbius basis of connected induced subgraphs; matchings activate none, while a spread-out illegal cover should activate many genuinely different collision clusters.

**Obstruction check.** O1 honestly applies at degree \(r\): a cube relation of size \(2^{r+1}-1\) remains; growing \(r=\Theta(\log q)\) is not ruled out but may itself supply a polynomial cheat. O2: no affine marginals. O3 partially applies because these are proper connected scopes; global-cycle counterexamples are a direct threat. O4: no phases. O5: binary. O6: features index polynomially many graph subsets, not assignments, assuming bounded incompatibility degree. O7: no tensoring, but every mixed lifted word must be checked. O8 applies if successful.

**Smallest experiment.** Extend the Schur-walk verifier with all connected sets of sizes \(2,3,4\), deduplicated by vertex set, and enumerate every mixed word on the same hostile suite.

**Falsification / likely death.** Kill if all-eight or three-matching holonomy again cancels every feature. Likely death: connected-set monomials retain the same affine XOR cancellation without walk multiplicity.

---

## 4. Nonlinear low-rank legal variety

**Mechanism / expected move.** Assign each triple \(j\) a small matrix \(M_j\), and attach the global linear state \(M(x)=\sum_jx_jM_j\). Search for labels making every perfect matching land in the nonlinear determinantal variety \(\operatorname{rank}M(x)\le r\), while every illegal odd cover has rank at least \(R\gg r\); convert rank into Hamming cost using a fixed family of left/right condensers. Unlike a quotient, three legal states can sum to rank \(3r\), so affine-closure cheats need not remain cheap.

**Obstruction check.** O1: outside only if low rank follows from a genuinely global determinant identity, not affine local labels. O2–O3: no marginals/scopes. O4: no phases. O5: binary rank, not integer exact fibers. O6: matrices label polynomially many triples. O7: no pure tensor multiplier; condensers must handle every matrix in the affine span. O8 applies after binary realization.

**Smallest experiment.** For all \(q=2\) dictionaries, use SAT/SMT to search \(3\times3\) binary \(M_j\) with legal rank \(\le1\) and illegal rank \(\ge2\); freeze any rule and test \(q=3\), all-eight, and odd holonomy.

**Falsification / likely death.** Falsify if no labels exist already at \(q=2\), or labels fail relabeling transfer. Most likely universal completeness forces the \(M_j\) into an affine structure admitting low-rank illegal sums.

---

## 5. Formula-dependent nonabelian holonomy coordinates

**Mechanism / expected move.** Choose a canonical spanning tree of the formula-incidence graph and assign non-tree edges generators of a free group. For each fundamental cycle, add truncated Magnus coefficients of the ordered constraint product; a consistent witness should be gauge-trivial, while odd permutation holonomy yields a noncommuting word with a detectable lowest-degree coefficient. There are only linearly many fundamental cycles, even when each coordinate depends globally on a long cycle.

**Obstruction check.** O1: high-degree cycle products lie outside bounded-degree signatures. O2: no proper marginals. O3: fundamental-cycle coordinates include the entire missed dependency. O4: explicitly uses the stated exception—formula-dependent global selectors—not copy-stable local phases. O5: binary/noncommutative rather than integer slack. O6: intended dictionary is cycle-based, not assignment-based; succinct construction is unresolved. O7: not tensoring, though mixed lifted words remain essential. O8 applies conditionally.

**Smallest experiment.** On twisted 3-color cycles of lengths \(3,5,7\), truncate Magnus words at degrees \(2,3\), build the span of all lifted legal local configurations, and search for minimum pointed illegal combinations; then run all-eight.

**Falsification / likely death.** Kill if a support-three mixed word has zero Magnus signature. Likely death: constructing the nonlinear lift without enumerating assignments either explodes in dimension or reintroduces a bounded-fan-in tableau.

---

## 6. Global Macaulay border-basis syndrome

**Mechanism / expected move.** Form the Boolean polynomial ideal of the 3CNF, compute a truncated Macaulay matrix, and globally row-reduce it before choosing columns. Use only pivot and border monomials reachable from clause supports; the hoped-for invariant is that SAT quotients possess a sparse character-like representative, whereas UNSAT quotients require a large support representation of the affine target. Dense elimination could expose global dependencies without complete-assignment columns.

**Obstruction check.** O1 honestly threatens any fixed-degree truncation; only elimination-generated high-degree rows escape. O2: no gate tableau or unary interfaces. O3: not a scope hierarchy after global row reduction, though low truncation may behave like one. O4: no phases. O5: binary polynomial algebra, not scaled integer fibers. O6: monomials rather than complete assignments, provided the border remains polynomial. O7: independent of tensoring and therefore still needs a direct polynomial gap. O8 transfers any resulting binary distance gap.

**Smallest experiment.** For all 3CNFs on at most five variables, build degree-\(3,4,5\) Macaulay border matrices, turn candidate affine targets into syndrome instances, and exhaustively compare SAT/UNSAT coset weights, including all-eight.

**Falsification / likely death.** Kill if completeness is not uniformly sparse or degree five already has virtual UNSAT leaders as cheap as SAT. Most likely the border becomes exponential before global consistency appears.
