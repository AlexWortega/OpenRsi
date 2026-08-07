import Mathlib

namespace VerifyRowRebasingSupportFailure

/-- Extend a finite row vector by zero. -/
def extendRows {n : ℕ} {K : Type*} (A : Fin n → K → ℤ) (r : ℕ) (k : K) : ℤ :=
  if h : r < n then A ⟨r, h⟩ k else 0

/-- The integral first-difference row operation. -/
def rowDiff {n : ℕ} {K : Type*} (A : Fin n → K → ℤ) (i : Fin n) (k : K) : ℤ :=
  if i.val = 0 then A i k
  else A i k - A ⟨i.val - 1, by omega⟩ k

/-- The inverse prefix-sum row operation. -/
def rowPrefix {n : ℕ} {K : Type*} (A : Fin n → K → ℤ) (i : Fin n) (k : K) : ℤ :=
  ∑ r ∈ Finset.range (i.val + 1), extendRows A r k

private def natDiff (f : ℕ → ℤ) : ℕ → ℤ
  | 0 => f 0
  | r + 1 => f (r + 1) - f r

private theorem sum_natDiff (f : ℕ → ℤ) (q : ℕ) :
    ∑ r ∈ Finset.range (q + 1), natDiff f r = f q := by
  induction q with
  | zero => simp [natDiff]
  | succ q ih =>
      rw [Finset.sum_range_succ, ih]
      simp only [natDiff]
      omega

private theorem natDiff_sum (f : ℕ → ℤ) (q : ℕ) :
    natDiff (fun s => ∑ r ∈ Finset.range (s + 1), f r) q = f q := by
  cases q with
  | zero => simp [natDiff]
  | succ q =>
      simp only [natDiff, Finset.sum_range_succ]
      omega

private theorem extend_rowDiff {n : ℕ} {K : Type*} (A : Fin n → K → ℤ)
    (r : ℕ) (hr : r < n) (k : K) :
    extendRows (rowDiff A) r k = natDiff (fun s => extendRows A s k) r := by
  cases r with
  | zero => simp [extendRows, rowDiff, natDiff, hr]
  | succ r =>
      have hr' : r < n := by omega
      simp [extendRows, rowDiff, natDiff, hr, hr']

/-- First differences are an invertible integral row rebasing: prefix sums recover every row. -/
theorem rowPrefix_rowDiff {n : ℕ} {K : Type*} (A : Fin n → K → ℤ) :
    rowPrefix (rowDiff A) = A := by
  funext i k
  rw [show rowPrefix (rowDiff A) i k =
      ∑ r ∈ Finset.range (i.val + 1), natDiff (fun s => extendRows A s k) r by
    apply Finset.sum_congr rfl
    intro r hr
    apply extend_rowDiff
    have := Finset.mem_range.mp hr
    omega]
  rw [sum_natDiff]
  simp [extendRows, i.isLt]

private theorem prefix_at {n : ℕ} {K : Type*} (A : Fin n → K → ℤ)
    (r : ℕ) (hr : r < n) (k : K) :
    extendRows (rowPrefix A) r k =
      ∑ s ∈ Finset.range (r + 1), extendRows A s k := by
  simp [extendRows, rowPrefix, hr]

/-- Conversely, first differences recover every row from prefix sums. -/
theorem rowDiff_rowPrefix {n : ℕ} {K : Type*} (A : Fin n → K → ℤ) :
    rowDiff (rowPrefix A) = A := by
  funext i k
  have hi : i.val < n := i.isLt
  rcases i with ⟨(_|r), hi⟩
  · change rowPrefix A ⟨0, hi⟩ k = A ⟨0, hi⟩ k
    simp [rowPrefix, extendRows, hi]
  · have hr : r < n := by omega
    rw [show rowDiff (rowPrefix A) ⟨r + 1, hi⟩ k =
        rowPrefix A ⟨r + 1, hi⟩ k - rowPrefix A ⟨r, hr⟩ k by
      simp [rowDiff]]
    rw [show rowPrefix A ⟨r + 1, hi⟩ k =
        ∑ s ∈ Finset.range (r + 2), extendRows A s k by rfl]
    rw [show rowPrefix A ⟨r, hr⟩ k =
        ∑ s ∈ Finset.range (r + 1), extendRows A s k by rfl]
    rw [show r + 2 = (r + 1) + 1 by omega, Finset.sum_range_succ]
    simp [extendRows, hi]

/-- A lower-triangular cumulative matrix. -/
def cumulativeMatrix {n : ℕ} (i j : Fin n) : ℤ :=
  if j.val ≤ i.val then 1 else 0

/-- First differences turn the cumulative matrix into the identity matrix, at every size. -/
theorem rowDiff_cumulative {n : ℕ} (i j : Fin n) :
    rowDiff (cumulativeMatrix (n := n)) i j = if i = j then 1 else 0 := by
  by_cases h0 : i.val = 0
  · have hji : j.val = i.val ↔ i = j := by
      constructor
      · intro h; apply Fin.ext; omega
      · intro h; omega
    simp [rowDiff, cumulativeMatrix, h0, ← hji]
  · by_cases hij : i = j
    · subst j
      simp [rowDiff, cumulativeMatrix, h0]
      omega
    · have hval : j.val ≠ i.val := by
        intro h
        apply hij
        apply Fin.ext
        exact h.symm
      simp [rowDiff, cumulativeMatrix, h0, hij]
      omega

/-- The identity block before row rebasing. -/
def identityMatrix {n : ℕ} (i s : Fin n) : ℤ := if i = s then 1 else 0

/-- First differences turn the identity block into a lower bidiagonal block. -/
theorem rowDiff_identity {n : ℕ} (i s : Fin n) :
    rowDiff (identityMatrix (n := n)) i s =
      if i = s then 1 else if i.val = s.val + 1 then -1 else 0 := by
  by_cases h0 : i.val = 0
  · unfold rowDiff
    rw [if_pos h0]
    by_cases his : i = s
    · simp [identityMatrix, his]
    · have hsuc : i.val ≠ s.val + 1 := by omega
      simp [identityMatrix, his, hsuc]
  · have hpredlt : i.val - 1 < n := by omega
    let p : Fin n := ⟨i.val - 1, hpredlt⟩
    unfold rowDiff
    rw [if_neg h0]
    change identityMatrix i s - identityMatrix p s = _
    by_cases his : i = s
    · have hpne : p ≠ s := by
        subst s
        intro h
        have := congrArg Fin.val h
        simp [p] at this
        omega
      simp [identityMatrix, his, hpne]
    · by_cases hsuc : i.val = s.val + 1
      · have hps : p = s := by
          apply Fin.ext
          simp [p]
          omega
        simp [identityMatrix, his, hsuc, hps]
      · have hps : p ≠ s := by
          intro h
          apply hsuc
          have := congrArg Fin.val h
          simp [p] at this
          omega
        simp [identityMatrix, his, hsuc, hps]

/-- `[I|-C]`, with the identity columns tagged by `inl`. -/
def augmented {n : ℕ} (i : Fin n) : Sum (Fin n) (Fin n) → ℤ
  | .inl s => if i = s then 1 else 0
  | .inr j => - cumulativeMatrix i j

/-- The exact support after rebasing `[I|-C]`: a bidiagonal block plus `-I`. -/
theorem rowDiff_augmented {n : ℕ} (i : Fin n) (k : Sum (Fin n) (Fin n)) :
    rowDiff (augmented (n := n)) i k =
      match k with
      | .inl s => if i = s then 1 else if i.val = s.val + 1 then -1 else 0
      | .inr j => if i = j then -1 else 0 := by
  cases k with
  | inl s =>
      change rowDiff (identityMatrix (n := n)) i s = _
      exact rowDiff_identity i s
  | inr j =>
      change rowDiff (fun i j => -cumulativeMatrix i j) i j = _
      rw [show rowDiff (fun i j => -cumulativeMatrix i j) i j =
          - rowDiff (cumulativeMatrix (n := n)) i j by
        unfold rowDiff
        split_ifs <;> ring]
      rw [rowDiff_cumulative]
      split_ifs <;> simp_all

/-- Hence every row of the rebased augmented matrix has support at most three. -/
theorem rebased_row_support_shape {n : ℕ} (i : Fin n)
    (k : Sum (Fin n) (Fin n)) (h : rowDiff (augmented (n := n)) i k ≠ 0) :
    k = Sum.inl i ∨
    (∃ s : Fin n, i.val = s.val + 1 ∧ k = Sum.inl s) ∨
    k = Sum.inr i := by
  cases k with
  | inl s =>
      simp only [rowDiff_augmented] at h
      split_ifs at h with his hsuc
      · exact Or.inl (congrArg Sum.inl his.symm)
      · exact Or.inr (Or.inl ⟨s, hsuc, rfl⟩)
      · simp at h
  | inr j =>
      simp only [rowDiff_augmented] at h
      split_ifs at h with hij
      · exact Or.inr (Or.inr (congrArg Sum.inr hij.symm))
      · simp at h


/-- Each rebased identity column meets only its matching row and its successor. -/
theorem rebased_left_column_support_shape {n : ℕ} (i s : Fin n)
    (h : rowDiff (augmented (n := n)) i (.inl s) ≠ 0) :
    i = s ∨ i.val = s.val + 1 := by
  simp only [rowDiff_augmented] at h
  split_ifs at h with his hsuc
  · exact Or.inl his
  · exact Or.inr hsuc
  · simp at h

/-- Each rebased cumulative-block column is a leaf: it meets exactly its matching row. -/
theorem rebased_right_column_support_shape {n : ℕ} (i j : Fin n)
    (h : rowDiff (augmented (n := n)) i (.inr j) ≠ 0) :
    i = j := by
  simp only [rowDiff_augmented] at h
  split_ifs at h with hij
  · exact hij
  · simp at h

/-- Row injection for the lower half of a `2m` by `2m` cumulative matrix. -/
def lowerRow (m : ℕ) (r : Fin m) : Fin (2 * m) := ⟨m + r.val, by omega⟩

/-- Column injection for the first half. -/
def firstColumn (m : ℕ) (c : Fin m) : Fin (2 * m) := ⟨c.val, by omega⟩

/-- Before rebasing, the cumulative support contains an explicit `K_{m,m}` biclique. -/
theorem cumulative_big_biclique (m : ℕ) (r c : Fin m) :
    cumulativeMatrix (lowerRow m r) (firstColumn m c) = 1 := by
  simp [cumulativeMatrix, lowerRow, firstColumn]
  omega

end VerifyRowRebasingSupportFailure
