import Mathlib

namespace VerifyIntegralEuclideanIsometry

open scoped BigOperators

def sqNorm {ι : Type*} [Fintype ι] (v : ι → ℤ) : ℤ :=
  ∑ i, (v i) ^ 2

lemma integer_unit_vector
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (v : ι → ℤ) (h : sqNorm v = 1) :
    ∃ p : ι, (v p = 1 ∨ v p = -1) ∧
      ∀ i, i ≠ p → v i = 0 := by
  have hbound : ∀ i, -1 ≤ v i ∧ v i ≤ 1 := by
    intro i
    have hsquare : (v i) ^ 2 ≤ 1 := by
      calc
        (v i) ^ 2 ≤ ∑ j ∈ (Finset.univ : Finset ι), (v j) ^ 2 := by
          simpa only using
            (Finset.single_le_sum (s := (Finset.univ : Finset ι))
              (fun j _ ↦ sq_nonneg (v j)) (Finset.mem_univ i))
        _ = sqNorm v := by simp [sqNorm]
        _ = 1 := h
    constructor
    · by_contra hn
      have hx : v i ≤ -2 := by omega
      nlinarith
    · by_contra hn
      have hx : 2 ≤ v i := by omega
      nlinarith
  have hnonzero : ∃ p, v p ≠ 0 := by
    by_contra hn
    simp only [not_exists, not_not] at hn
    have hv : v = 0 := funext hn
    simp [hv, sqNorm] at h
  obtain ⟨p, hp⟩ := hnonzero
  have hpsign : v p = 1 ∨ v p = -1 := by
    rcases hbound p with ⟨hlo, hhi⟩
    omega
  refine ⟨p, hpsign, ?_⟩
  intro i hip
  have hpair : (v p) ^ 2 + (v i) ^ 2 ≤ sqNorm v := by
    calc
      (v p) ^ 2 + (v i) ^ 2 = ∑ j ∈ ({p, i} : Finset ι), (v j) ^ 2 := by
        simp [Ne.symm hip]
      _ ≤ ∑ j ∈ (Finset.univ : Finset ι), (v j) ^ 2 := by
        apply Finset.sum_le_sum_of_subset_of_nonneg
        · exact Finset.subset_univ _
        · intro j _ _
          exact sq_nonneg (v j)
      _ = sqNorm v := by simp [sqNorm]
  rcases hpsign with hpone | hpneg
  · rw [hpone, h] at hpair
    nlinarith [sq_nonneg (v i)]
  · rw [hpneg, h] at hpair
    nlinarith [sq_nonneg (v i)]

/--
A square integer matrix with orthonormal columns is a signed permutation
matrix.  This is the exact marking restriction needed before a compiler
normal form can be used for Euclidean energy or selector-support claims.
-/
theorem integer_orthonormal_columns_are_signed_permutation
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A : ι → ι → ℤ)
    (unit : ∀ j, ∑ i, (A i j) ^ 2 = 1)
    (orthogonal : ∀ j k, j ≠ k → ∑ i, A i j * A i k = 0) :
    ∃ σ : ι ≃ ι, ∃ ε : ι → ℤ,
      (∀ j, ε j = 1 ∨ ε j = -1) ∧
      ∀ i j, A i j = if i = σ j then ε j else 0 := by
  classical
  have hunit : ∀ j, ∃ p : ι, (A p j = 1 ∨ A p j = -1) ∧
      ∀ i, i ≠ p → A i j = 0 := by
    intro j
    exact integer_unit_vector (fun i ↦ A i j) (unit j)
  let p : ι → ι := fun j ↦ (hunit j).choose
  let ε : ι → ℤ := fun j ↦ A (p j) j
  have hsign : ∀ j, ε j = 1 ∨ ε j = -1 := by
    intro j
    exact (hunit j).choose_spec.1
  have hcolumn : ∀ i j, A i j = if i = p j then ε j else 0 := by
    intro i j
    by_cases hi : i = p j
    · subst i
      simp [ε]
    · simp [hi, (hunit j).choose_spec.2 i hi]
  have pinjective : Function.Injective p := by
    intro j k hpk
    by_contra hjk
    have hdot := orthogonal j k hjk
    have heps : ε j * ε k = 0 := by
      calc
        ε j * ε k = ∑ i, A i j * A i k := by
          simp_rw [hcolumn]
          simp [hpk]
        _ = 0 := hdot
    rcases hsign j with hj | hj <;>
      rcases hsign k with hk | hk <;>
      simp [hj, hk] at heps
  let σ : ι ≃ ι := Equiv.ofBijective p
    ⟨pinjective, Finite.injective_iff_surjective.mp pinjective⟩
  refine ⟨σ, ε, hsign, ?_⟩
  intro i j
  simpa [σ] using hcolumn i j

/-- The same result stated directly as the integer Gram identity `AᵀA = I`. -/
theorem integer_gram_identity_forces_signed_permutation
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A : ι → ι → ℤ)
    (gram : ∀ j k, ∑ i, A i j * A i k = if j = k then 1 else 0) :
    ∃ σ : ι ≃ ι, ∃ ε : ι → ℤ,
      (∀ j, ε j = 1 ∨ ε j = -1) ∧
      ∀ i j, A i j = if i = σ j then ε j else 0 := by
  apply integer_orthonormal_columns_are_signed_permutation A
  · intro j
    simpa [pow_two] using gram j j
  · intro j k hjk
    simpa [hjk] using gram j k

end VerifyIntegralEuclideanIsometry
