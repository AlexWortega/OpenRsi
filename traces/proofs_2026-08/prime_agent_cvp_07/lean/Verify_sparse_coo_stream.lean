import Mathlib

/-!
Universal semantics for a streamed sparse COO matrix emitter.

The statement is deliberately independent of any particular U0a row family:
a finite stream may contain duplicate coordinates and zero or negative integer
coefficients.  Folding records directly into an output vector is proved equal
to materializing the corresponding dense integer matrix and applying
`Matrix.mulVec`.  Thus an eager matrix and a stream retaining only its output
vector have identical mathematical semantics.  This is not a running-time theorem for the
current Python serializer and proves no CVP soundness claim.
-/

namespace VerifySparseCooStream

/-- One coordinate-list record for an `m` by `n` integer matrix. -/
structure Entry (m n : ℕ) where
  row : Fin m
  col : Fin n
  coeff : ℤ
  deriving DecidableEq, Repr

/-- Dense materialization.  Repeated coordinates are added, as required by
COO semantics rather than silently overwritten. -/
def dense {m n : ℕ} (entries : List (Entry m n)) :
    Matrix (Fin m) (Fin n) ℤ :=
  fun i j => (entries.map fun e =>
    if e.row = i ∧ e.col = j then e.coeff else 0).sum

/-- Contribution of one record to one selected output row. -/
def contribution {m n : ℕ} (x : Fin n → ℤ) (i : Fin m)
    (e : Entry m n) : ℤ :=
  if e.row = i then e.coeff * x e.col else 0

/-- Extensional (order-independent) sparse matrix-vector semantics. -/
def sparseMatVec {m n : ℕ} (entries : List (Entry m n))
    (x : Fin n → ℤ) : Fin m → ℤ :=
  fun i => (entries.map (contribution x i)).sum

/-- Online update performed when a COO record is emitted. -/
def streamStep {m n : ℕ} (x : Fin n → ℤ) (acc : Fin m → ℤ)
    (e : Entry m n) : Fin m → ℤ :=
  Function.update acc e.row (acc e.row + e.coeff * x e.col)

/-- Left fold of the emitted record stream, starting from the zero vector. -/
def streamMatVec {m n : ℕ} (entries : List (Entry m n))
    (x : Fin n → ℤ) : Fin m → ℤ :=
  entries.foldl (streamStep x) 0

lemma foldl_streamStep_apply {m n : ℕ} (entries : List (Entry m n))
    (x : Fin n → ℤ) (acc : Fin m → ℤ) (i : Fin m) :
    entries.foldl (streamStep x) acc i =
      acc i + (entries.map (contribution x i)).sum := by
  induction entries generalizing acc with
  | nil => simp
  | cons e entries ih =>
      rw [List.foldl_cons, ih]
      simp only [List.map_cons, List.sum_cons]
      unfold streamStep contribution
      by_cases h : e.row = i
      · subst i
        simp [Function.update_self]
        ring
      · have h' : i ≠ e.row := Ne.symm h
        simp [Function.update, h', h]

/-- Streaming the records is exactly their extensional sparse semantics. -/
theorem streamMatVec_eq_sparseMatVec {m n : ℕ}
    (entries : List (Entry m n)) (x : Fin n → ℤ) :
    streamMatVec entries x = sparseMatVec entries x := by
  funext i
  rw [streamMatVec, sparseMatVec, foldl_streamStep_apply]
  simp

lemma sum_dense_row {m n : ℕ} (entries : List (Entry m n))
    (x : Fin n → ℤ) (i : Fin m) :
    ∑ j, dense entries i j * x j =
      (entries.map (contribution x i)).sum := by
  induction entries with
  | nil => simp [dense]
  | cons e entries ih =>
      simp only [dense, List.map_cons, List.sum_cons]
      simp_rw [add_mul]
      rw [Finset.sum_add_distrib]
      unfold dense at ih
      rw [ih]
      unfold contribution
      by_cases hr : e.row = i
      · subst i
        simp
      · simp [hr]

/-- Main COO theorem: online folding equals dense materialization followed by
ordinary matrix-vector multiplication, for every size, stream, and vector. -/
theorem streamMatVec_eq_dense_mulVec {m n : ℕ}
    (entries : List (Entry m n)) (x : Fin n → ℤ) :
    streamMatVec entries x = (dense entries).mulVec x := by
  rw [streamMatVec_eq_sparseMatVec]
  funext i
  simp only [sparseMatVec, Matrix.mulVec, dotProduct]
  symm
  exact sum_dense_row entries x i

/-- Appending two output chunks and then interpreting them adds their sparse
linear maps.  This is the semantic basis for emitting row families in chunks. -/
theorem sparseMatVec_append {m n : ℕ}
    (first second : List (Entry m n)) (x : Fin n → ℤ) :
    sparseMatVec (first ++ second) x =
      sparseMatVec first x + sparseMatVec second x := by
  funext i
  simp [sparseMatVec, List.map_append]

/-- Dense materialization has the same chunk law. -/
theorem dense_append {m n : ℕ} (first second : List (Entry m n)) :
    dense (first ++ second) = dense first + dense second := by
  funext i j
  simp [dense, List.map_append]

/-- Permuting the emission order cannot change the represented matrix. -/
theorem dense_perm {m n : ℕ} {first second : List (Entry m n)}
    (h : first.Perm second) : dense first = dense second := by
  funext i j
  unfold dense
  exact (h.map _).sum_eq

/-- Consequently emission order cannot change streamed matrix-vector
semantics, even when coordinates repeat. -/
theorem streamMatVec_perm {m n : ℕ} {first second : List (Entry m n)}
    (h : first.Perm second) (x : Fin n → ℤ) :
    streamMatVec first x = streamMatVec second x := by
  rw [streamMatVec_eq_dense_mulVec, streamMatVec_eq_dense_mulVec,
    dense_perm h]

/-- Flattening a list of row-family chunks has exactly the sum of their record
counts.  This is a generic enumeration bridge for serializer manifests. -/
theorem flatten_length {α : Type*} (families : List (List α)) :
    families.flatten.length = (families.map List.length).sum := by
  induction families with
  | nil => rfl
  | cons family families ih => simp [ih]

end VerifySparseCooStream
