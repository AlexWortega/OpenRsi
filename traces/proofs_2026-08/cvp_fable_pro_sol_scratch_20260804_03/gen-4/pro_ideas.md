I will use this obstruction shorthand:

- **S — slack annihilation:** free integer slack can erase amplified residuals.
- **E — exact/local limitation:** only 18 three-row gadgets are certified, and only locally; one/two rows fail.
- **P — provenance:** reconstructed survivors were not hash-compared with Generation 2 output.
- **O — overlap cancellation:** shared clauses may create global kernel directions.
- **N — non-Boolean robustness:** exact falsifying fibers do not exclude approximate or non-Boolean cheats.
- **G — gap scaling:** no sparse-unsatisfaction-to-\(n^c\) law exists.
- **V — CVP realization:** no complete basis, target, radius, and dimension accounting exists.

### 1. Private clause syndromes plus an equality forest

**Core trick.** Give every clause private copies of its variables and private certified measurement rows, preventing inter-clause cancellation. Connect occurrences of each variable by a bounded-degree equality tree; scale both clause and equality defects by \(W=n^K\), leaving Boolean anchors unscaled.

**Expected move.** Any globally consistent satisfying selection has zero expensive defect. An unsatisfiable formula must either activate a private clause obstruction or break an equality edge, suggesting distance \(\Omega(W)\) over an \(O(\sqrt n)\) completeness radius.

**Checks.** **S:** no free clause slack. **E:** uses only dumped, exact three-row survivors; no claim for fewer rows. **P:** first assert set/hash equality with Generation 2. **O:** private rows remove cancellation; equality composition remains unproved. **N:** not outside—non-Boolean occurrence values may satisfy both blocks. **G:** weighting gives a candidate gap only after exact separation. **V:** all blocks are integral linear rows, but radii remain unaudited.

**Falsification/test.** Compose the specified representative over two clauses sharing one variable, all polarities and references; decide zero-defect feasibility by Smith/Hermite form, then enumerate squared norm \(\le8\).

**Smallest experiment.** Extend the Generation-3 verifier with survivor-set equality and this two-clause block matrix.

**Likely death.** Fractional/signed selectors synchronize through non-Boolean occurrence values while every expensive row vanishes.

---

### 2. Construction-A amplification of the local defect vector

**Core trick.** Treat each private clause obstruction as a symbol \(d_i\bmod q\), then encode \(d=(d_i)\) with an explicit \(q\)-ary linear code of polynomial relative distance. Construction A realizes centered residues as Euclidean lattice coordinates: a nonzero syndrome should occupy many coordinates rather than merely one clause.

**Expected move.** If every false clause has \(d_i\not\equiv0\pmod q\), code distance converts one nonzero local defect into \(\Omega(N)\) squared penalty.

**Checks.** **S:** quotient variables can center residues but cannot erase \(d_i\) unless \(q\mid d_i\). **E:** depends on extracting an actual integral defect functional from the exact survivor. **P:** hash comparison is mandatory. **O:** coding private defect coordinates avoids literal summation, but correlated codeword cancellation remains possible. **N:** not outside—large defects divisible by \(q\) are invisible. **G:** code distance supplies scaling if completeness and dimension remain controlled. **V:** Construction A supplies a lattice block, not the full target/radius proof.

**Falsification/test.** For \(q=5\), compute all attainable defects of one survivor over coefficients \([-6,6]\); search for a harmful defect divisible by \(5\), then compose two clauses with a length-6 repetition/simplex encoder.

**Smallest experiment.** Exact enumeration plus SNF modular-feasibility checks.

**Likely death.** Integer wraparound produces zero syndromes at small anchor cost.

---

### 3. Full Walsh-spectrum selector encoding

**Core trick.** Replace three ad hoc measurements by the complete Walsh–Hadamard character table on the eight local assignments. Parseval makes every signed selector perturbation visible somewhere in the spectrum; normalization and degree-one characters are tied to global variable values, while higher characters remain clause-private.

**Expected move.** Prove a quantitative local inequality: every integer selector inconsistent with all seven satisfying one-hots has spectral cost exceeding the Boolean baseline by a fixed amount. Scale only the separating spectral subspace.

**Checks.** **S:** no OR slack variables appear. **E:** outside the one-to-three-row search assumptions, but needs a new exact unbounded audit. **P:** independent of the 18 survivors. **O:** private higher spectra prevent direct cancellation; shared degree-one characters may still enable it. **N:** full Parseval directly targets signed/non-Boolean selectors, though target offsets complicate the bound. **G:** scaling works only if legal one-hots have zero amplified component. **V:** the Hadamard block is integral, but a common target for seven legal patterns is unresolved.

**Falsification/test.** Enumerate all selector vectors in \([-5,5]^8\) with normalization one and fixed marginals; compare minimum spectral cost for legal one-hots versus harmful signed points.

**Smallest experiment.** An 8-by-8 integer matrix and exhaustive Python search, followed by exact quadratic minimization.

**Likely death.** Every common spectral target charges legal one-hots too, leaving only a constant ratio.

---

### 4. Toric-fiber gadget with a Voronoi “nonnegativity moat”

**Core trick.** Search for an integer configuration whose nonnegative affine fibers are generated exactly by satisfying local patterns—a normal affine semigroup/Hilbert-basis condition. Since lattice coefficients are signed, pair each selector with a complement and place the target at a half-integral Voronoi center, making negative or over-one coefficients cross a large geometric moat.

**Expected move.** Convert the local soundness question from excluding arbitrary signed kernel vectors to proving that every low-distance lattice point lies in the nonnegative semigroup, where toric normality classifies the fiber.

**Checks.** **S:** no residual slack. **E:** independent of the existing three-row family and requires exact Graver/Hilbert computation. **P:** not applicable. **O:** clause-private semigroup rows plus shared marginal rows still need composition. **N:** this is the principal target; no proof yet that the moat controls all signed coefficients. **G:** a scalable moat could yield \(n^c\), but only if completeness stays near its center. **V:** the moat is realizable by repeated anchor coordinates, though full accounting is absent.

**Falsification/test.** Enumerate small \(0/1\) configurations for the seven OR patterns; compute their Graver moves and search for a signed move of anchor cost at most the Boolean baseline.

**Smallest experiment.** Use Normaliz/4ti2 if available, or brute-force all 3–5-row matrices and coefficients \([-4,4]\).

**Likely death.** Group inverses defeat any purely linear attempt to enforce a nonnegative cone at polynomial cost.

---

### 5. \(p\)-adic clause tagging with penalized carries

**Core trick.** Assign clause \(i\) a mixed-radix tag \((1,B^i)\), or several prime-power tags, and aggregate integral local defects through those tags. Add explicit carry variables with their own heavily weighted coordinates, so cancelling the earliest nonzero tagged defect requires a quantitatively expensive carry.

**Expected move.** A valuation argument would identify the least-index nonzero defect and lower-bound either an aggregate row or the carry norm. Coefficients \(B^i\) still have polynomial bit length.

**Checks.** **S:** carries are penalized rather than free residual-erasing slacks. **E:** requires an integral defect functional from an exact three-row survivor; it does not improve local isolation. **P:** use only hash-verified survivors. **O:** clause tagging directly attacks cancellation. **N:** not outside—unbounded signed defects may manufacture cheap carries. **G:** valuations could give polynomial separation, but conditioning and completeness costs are unknown. **V:** weighted integer rows are immediately expressible as a CVP block; radii are not proved.

**Falsification/test.** On the eight-clause unsatisfiable three-variable core, use \(B=5\) and two tagged rows; exactly optimize selectors and carries in increasing norm balls, then use SNF to detect zero defect.

**Smallest experiment.** Start with two overlapping clauses and tags \(1,5\), enumerating carries \([-10,10]\).

**Likely death.** A large signed local deviation induces a low-norm carry chain that defeats lexicographic separation.

---

### 6. Cohomological consistency amplification

**Core trick.** Regard occurrence assignments as a \(0\)-cochain, equality violations as a coboundary, and clause defects as higher-dimensional cells. Embed the formula incidence structure into an explicit finite complex with a cosystolic inequality: a nontrivial defect class must have large support unless corrected by many consistency violations.

**Expected move.** Replace “one false clause” by a global topological dichotomy—either many clause cells are defective or many equality cells are broken—without sharing scalar measurement rows.

**Checks.** **S:** there are no free clause slacks. **E:** this is a different global mechanism, not covered by local row searches. **P:** independent of survivor identity unless local gadgets label cells. **O:** cohomology is designed to prevent cancellation into a boundary. **N:** finite-group cochains miss integer multiples and approximate Euclidean cheats. **G:** a polynomial cosystolic bound would amplify support, but may amount to forbidden PCP-style gap amplification; that must be rejected if so. **V:** a boundary matrix is integral, but converting support expansion into Euclidean CVP radii is open.

**Falsification/test.** Build the smallest complete 2-complex containing two overlapping clauses; enumerate all \(\mathbb F_2\) cochains and test whether a one-cell defect is a boundary.

**Smallest experiment.** Exhaustive bit-vector linear algebra on 6–10 vertices, followed by a Construction-A lift.

**Likely death.** Formula defects are boundaries, or the needed expansion theorem is effectively a PCP theorem rather than a PCP-free argument.

---

### 7. Nullstellensatz/moment-lattice obstruction

**Core trick.** Encode Booleanity by \(x_i^2-x_i\) and each clause by its multilinear falsity polynomial. For an unsatisfiable formula, search for a bounded-degree identity \(1=\sum_i g_i f_i\); linearize all appearing monomials as moment coordinates, turning the constant-term contradiction into an integral affine obstruction.

**Expected move.** A global algebraic certificate cannot be cancelled clause-by-clause: any exact pseudoassignment satisfying all lifted equations would imply \(1=0\). Repeating or weighting the constant-coordinate obstruction could create the gap.

**Checks.** **S:** no clause slack is used. **E:** outside the local affine-fiber assumptions. **P:** independent of the 18 survivors. **O:** the certificate is global, so cancellation is absorbed into the identity. **N:** exact pseudoassignments are excluded, but low-cost approximate moments are not. **G:** no polynomial degree/monomial bound is known for arbitrary 3SAT; this is the central obstruction. **V:** linearized equations give an integer matrix, but completeness anchors and CVP distance accounting remain open.

**Falsification/test.** Compute the minimum-degree certificate for the eight-clause three-variable unsatisfiable core, build its moment matrix, and search for low-norm integer pseudo-moments.

**Smallest experiment.** SymPy/Sage Gröbner elimination through degree three or four, then exact least-squares enumeration.

**Likely death.** Required degree is linear, producing exponentially many moment coordinates.

Classical touchstones only: MacWilliams–Sloane, *The Theory of Error-Correcting Codes* (1977); Sturmfels, *Gröbner Bases and Convex Polytopes* (1996); Cox–Little–O’Shea, *Ideals, Varieties, and Algorithms* (1992).
