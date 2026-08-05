import Mathlib

namespace VerifyProductTagRectangle

/--
Every tag that is only a sum of a left-selector label and a right-selector
label annihilates the alternating `2 × 2` toric exchange.
-/
theorem affine_marginal_tag_annihilates_rectangle
    {A : Type*} [AddCommGroup A] (a₀ a₁ b₀ b₁ : A) :
    (a₀ + b₀) + (a₁ + b₁) - (a₀ + b₁) - (a₁ + b₀) = 0 := by
  abel

/--
An ordered product tag turns the same rectangular exchange into the product
of the two selector differences.  No commutativity of multiplication is used.
-/
theorem product_tag_rectangle_factorization
    {R : Type*} [Ring R] (a₀ a₁ b₀ b₁ : R) :
    a₀ * b₀ + a₁ * b₁ - a₀ * b₁ - a₁ * b₀ =
      (a₀ - a₁) * (b₀ - b₁) := by
  noncomm_ring

/--
Over a division ring, the ordered-product transfer of the rectangular move is
nonzero exactly when both the left labels and the right labels are distinct.
This is the exact local separation criterion used by a product-tag Q1 search.
-/
theorem product_tag_rectangle_ne_zero_iff
    {D : Type*} [DivisionRing D] (a₀ a₁ b₀ b₁ : D) :
    a₀ * b₀ + a₁ * b₁ - a₀ * b₁ - a₁ * b₀ ≠ 0 ↔
      a₀ ≠ a₁ ∧ b₀ ≠ b₁ := by
  rw [product_tag_rectangle_factorization]
  simp only [mul_ne_zero_iff, sub_ne_zero]

/--
The criterion is unchanged when every right label is transported through a
ring automorphism, as in a fixed skew-product residue class.
-/
theorem skew_product_tag_rectangle_ne_zero_iff
    {D : Type*} [DivisionRing D] (σ : D ≃+* D) (a₀ a₁ b₀ b₁ : D) :
    a₀ * σ b₀ + a₁ * σ b₁ - a₀ * σ b₁ - a₁ * σ b₀ ≠ 0 ↔
      a₀ ≠ a₁ ∧ b₀ ≠ b₁ := by
  rw [product_tag_rectangle_factorization]
  simp only [mul_ne_zero_iff, sub_ne_zero]
  constructor
  · rintro ⟨ha, hσb⟩
    refine ⟨ha, ?_⟩
    intro hb
    exact hσb (congrArg σ hb)
  · rintro ⟨ha, hb⟩
    exact ⟨ha, σ.injective.ne hb⟩

end VerifyProductTagRectangle
