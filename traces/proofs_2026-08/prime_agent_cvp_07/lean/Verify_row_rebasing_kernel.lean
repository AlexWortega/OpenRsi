import Mathlib

namespace VerifyRowRebasingKernel

/--
Left multiplication by an invertible row matrix preserves exactly the integer
kernel.  This is a semantic preprocessing of equality constraints and does not
touch coefficient variables or their Euclidean objective.
-/
theorem invertible_row_rebase_preserves_kernel
    {R K : Type*} [Fintype R] [DecidableEq R] [Fintype K]
    (D : Matrix R K ℤ) (U V : Matrix R R ℤ) (hVU : V * U = 1)
    (x : K → ℤ) :
    (U * D).mulVec x = 0 ↔ D.mulVec x = 0 := by
  constructor
  · intro h
    calc
      D.mulVec x = ((1 : Matrix R R ℤ) * D).mulVec x := by rw [Matrix.one_mul D]
      _ = ((V * U) * D).mulVec x := by rw [hVU]
      _ = (V * (U * D)).mulVec x := by rw [Matrix.mul_assoc]
      _ = V.mulVec ((U * D).mulVec x) := by
        rw [Matrix.mulVec_mulVec]
      _ = 0 := by rw [h, Matrix.mulVec_zero]
  · intro h
    calc
      (U * D).mulVec x = U.mulVec (D.mulVec x) := by
        rw [Matrix.mulVec_mulVec]
      _ = 0 := by rw [h, Matrix.mulVec_zero]

/-- The same statement as equality of kernel predicates. -/
theorem invertible_row_rebase_kernel_set
    {R K : Type*} [Fintype R] [DecidableEq R] [Fintype K]
    (D : Matrix R K ℤ) (U V : Matrix R R ℤ) (hVU : V * U = 1) :
    {x | (U * D).mulVec x = 0} = {x | D.mulVec x = 0} := by
  ext x
  exact invertible_row_rebase_preserves_kernel D U V hVU x

end VerifyRowRebasingKernel
