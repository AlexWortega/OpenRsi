import Mathlib

namespace VerifyColumnMatroidGrammar

/-- An exact integral column dependency of a matrix.  This file deliberately
uses integral dependency vectors as its explicit grammar convention; it does
not identify this predicate with a separately formalized rational matroid. -/
def IsColumnDependency {R K : Type*} [Fintype K]
    (D : Matrix R K ℤ) (x : K → ℤ) : Prop :=
  D.mulVec x = 0

/-- A circuit vector is a nonzero dependency having inclusion-minimal support.
We retain the vector, rather than quotienting by units, because its support is
the column-matroid circuit used by the grammar. -/
def IsCircuitVector {R K : Type*} [Fintype K]
    (D : Matrix R K ℤ) (x : K → ℤ) : Prop :=
  x ≠ 0 ∧ IsColumnDependency D x ∧
    ∀ y : K → ℤ, y ≠ 0 → IsColumnDependency D y →
      Function.support y ⊆ Function.support x →
      Function.support y = Function.support x

/-- Left multiplication by an integrally left-invertible matrix preserves each
column-dependency vector, not just its support. -/
theorem row_rebase_dependency_iff
    {R K : Type*} [Fintype R] [DecidableEq R] [Fintype K]
    (D : Matrix R K ℤ) (U V : Matrix R R ℤ) (hVU : V * U = 1)
    (x : K → ℤ) :
    IsColumnDependency (U * D) x ↔ IsColumnDependency D x := by
  unfold IsColumnDependency
  constructor
  · intro h
    calc
      D.mulVec x = ((1 : Matrix R R ℤ) * D).mulVec x := by rw [Matrix.one_mul D]
      _ = ((V * U) * D).mulVec x := by rw [hVU]
      _ = (V * (U * D)).mulVec x := by rw [Matrix.mul_assoc]
      _ = V.mulVec ((U * D).mulVec x) := by rw [Matrix.mulVec_mulVec]
      _ = 0 := by rw [h, Matrix.mulVec_zero]
  · intro h
    calc
      (U * D).mulVec x = U.mulVec (D.mulVec x) := by rw [Matrix.mulVec_mulVec]
      _ = 0 := by rw [h, Matrix.mulVec_zero]

/-- Consequently the exact circuit-vector predicate is invariant under any
allowed invertible integral row rebasing. -/
theorem row_rebase_circuit_iff
    {R K : Type*} [Fintype R] [DecidableEq R] [Fintype K]
    (D : Matrix R K ℤ) (U V : Matrix R R ℤ) (hVU : V * U = 1)
    (x : K → ℤ) :
    IsCircuitVector (U * D) x ↔ IsCircuitVector D x := by
  constructor
  · rintro ⟨hx, hdep, hmin⟩
    refine ⟨hx, (row_rebase_dependency_iff D U V hVU x).mp hdep, ?_⟩
    intro y hy hdy hsub
    exact hmin y hy ((row_rebase_dependency_iff D U V hVU y).mpr hdy) hsub
  · rintro ⟨hx, hdep, hmin⟩
    refine ⟨hx, (row_rebase_dependency_iff D U V hVU x).mpr hdep, ?_⟩
    intro y hy hdy hsub
    exact hmin y hy ((row_rebase_dependency_iff D U V hVU y).mp hdy) hsub

/-- Reindex the columns by a bijection. -/
def permuteColumns {R K K' : Type*} (D : Matrix R K ℤ) (e : K' ≃ K) :
    Matrix R K' ℤ := fun r k => D r (e k)

/-- Transport coefficients in the matching direction. -/
def pushCoefficients {K K' : Type*} (e : K' ≃ K) (x : K' → ℤ) : K → ℤ :=
  fun k => x (e.symm k)

/-- Column permutation merely transports the dependency equation. -/
theorem permuteColumns_mulVec
    {R K K' : Type*} [Fintype K] [Fintype K']
    (D : Matrix R K ℤ) (e : K' ≃ K) (x : K' → ℤ) :
    (permuteColumns D e).mulVec x = D.mulVec (pushCoefficients e x) := by
  funext r
  unfold Matrix.mulVec dotProduct permuteColumns pushCoefficients
  exact Fintype.sum_equiv e (fun k => D r (e k) * x k)
    (fun k => D r k * x (e.symm k)) (by intro k; simp)

/-- Exact dependency invariance under a column permutation. -/
theorem column_permutation_dependency_iff
    {R K K' : Type*} [Fintype K] [Fintype K']
    (D : Matrix R K ℤ) (e : K' ≃ K) (x : K' → ℤ) :
    IsColumnDependency (permuteColumns D e) x ↔
      IsColumnDependency D (pushCoefficients e x) := by
  unfold IsColumnDependency
  rw [permuteColumns_mulVec]



/-- Pull coefficients back along the column bijection. -/
def pullCoefficients {K K' : Type*} (e : K' ≃ K) (y : K → ℤ) : K' → ℤ :=
  fun k => y (e k)

@[simp] theorem push_pull {K K' : Type*} (e : K' ≃ K) (y : K → ℤ) :
    pushCoefficients e (pullCoefficients e y) = y := by
  funext k
  simp [pushCoefficients, pullCoefficients]

@[simp] theorem pull_push {K K' : Type*} (e : K' ≃ K) (x : K' → ℤ) :
    pullCoefficients e (pushCoefficients e x) = x := by
  funext k
  simp [pushCoefficients, pullCoefficients]

private theorem push_ne_zero {K K' : Type*} (e : K' ≃ K) (x : K' → ℤ)
    (hx : x ≠ 0) : pushCoefficients e x ≠ 0 := by
  intro h
  apply hx
  rw [← pull_push e x, h]
  rfl

private theorem pull_ne_zero {K K' : Type*} (e : K' ≃ K) (y : K → ℤ)
    (hy : y ≠ 0) : pullCoefficients e y ≠ 0 := by
  intro h
  apply hy
  rw [← push_pull e y, h]
  rfl

private theorem pull_support_subset
    {K K' : Type*} (e : K' ≃ K) (x : K' → ℤ) (y : K → ℤ)
    (h : Function.support y ⊆ Function.support (pushCoefficients e x)) :
    Function.support (pullCoefficients e y) ⊆ Function.support x := by
  intro k hk
  have hy : y (e k) ≠ 0 := by
    simpa [Function.mem_support, pullCoefficients] using hk
  have hp := h hy
  simpa [Function.mem_support, pushCoefficients] using hp

private theorem support_eq_of_pull_support_eq
    {K K' : Type*} (e : K' ≃ K) (x : K' → ℤ) (y : K → ℤ)
    (h : Function.support (pullCoefficients e y) = Function.support x) :
    Function.support y = Function.support (pushCoefficients e x) := by
  ext k
  have hk := Set.ext_iff.mp h (e.symm k)
  simpa [Function.mem_support, pullCoefficients, pushCoefficients] using hk

/-- A column bijection sends every circuit vector to a circuit vector, with
exactly the transported coefficients and therefore exactly the transported
support. -/
theorem column_permutation_circuit_forward
    {R K K' : Type*} [Fintype K] [Fintype K']
    (D : Matrix R K ℤ) (e : K' ≃ K) (x : K' → ℤ)
    (hx : IsCircuitVector (permuteColumns D e) x) :
    IsCircuitVector D (pushCoefficients e x) := by
  rcases hx with ⟨hx0, hxdep, hxmin⟩
  refine ⟨push_ne_zero e x hx0,
    (column_permutation_dependency_iff D e x).mp hxdep, ?_⟩
  intro y hy0 hydep hsub
  have hpulldep : IsColumnDependency (permuteColumns D e) (pullCoefficients e y) :=
    (column_permutation_dependency_iff D e (pullCoefficients e y)).mpr (by
      simpa using hydep)
  have heq := hxmin (pullCoefficients e y) (pull_ne_zero e y hy0)
    hpulldep (pull_support_subset e x y hsub)
  exact support_eq_of_pull_support_eq e x y heq

/-- Hence the circuit predicate (and its support-minimal dependency system) is
invariant under arbitrary column permutation. -/
theorem column_permutation_circuit_iff
    {R K K' : Type*} [Fintype K] [Fintype K']
    (D : Matrix R K ℤ) (e : K' ≃ K) (x : K' → ℤ) :
    IsCircuitVector (permuteColumns D e) x ↔
      IsCircuitVector D (pushCoefficients e x) := by
  constructor
  · exact column_permutation_circuit_forward D e x
  · intro hx
    have hD : permuteColumns (permuteColumns D e) e.symm = D := by
      funext r k
      change D r (e (e.symm k)) = D r k
      rw [e.apply_symm_apply]
    have hx' : IsCircuitVector
        (permuteColumns (permuteColumns D e) e.symm) (pushCoefficients e x) := by
      rw [hD]
      exact hx
    have hback := column_permutation_circuit_forward
      (permuteColumns D e) e.symm (pushCoefficients e x) hx'
    have hcoeff : pushCoefficients e.symm (pushCoefficients e x) = x := by
      funext k
      change x (e.symm (e k)) = x k
      rw [e.symm_apply_apply]
    rw [hcoeff] at hback
    exact hback

end VerifyColumnMatroidGrammar
