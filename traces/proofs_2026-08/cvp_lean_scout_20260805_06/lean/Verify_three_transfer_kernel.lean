import Mathlib

/-!
A single leading transfer symbol in `𝔽₁₇²` cannot separate three
independent rectangle directions: three vectors in a two-dimensional space
have a nontrivial linear relation.  This is the fixed-size linear kernel used
by `experiments/verify_product_tag_rectangle_kernel.py`.
-/

namespace VerifyThreeTransferKernel

abbrev F := ZMod 17

local instance : Fact (Nat.Prime 17) := ⟨by norm_num⟩

abbrev K := Fin 2 → F
abbrev C := Fin 3 → F

noncomputable def transferMap (x : Fin 3 → K) : C →ₗ[F] K where
  toFun c q := ∑ i, c i * x i q
  map_add' c d := by
    ext q
    simp only [Pi.add_apply, add_mul, Finset.sum_add_distrib]
  map_smul' a c := by
    ext q
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, mul_assoc,
      Finset.mul_sum]

/-- Every three proposed `𝔽₁₇²` leading symbols have a nonzero coefficient
combination whose leading symbol is zero. -/
theorem exists_nonzero_three_transfer_kernel (x : Fin 3 → K) :
    ∃ c : C, c ≠ 0 ∧ ∀ q : Fin 2, ∑ i, c i * x i q = 0 := by
  have hdim : Module.finrank F K < Module.finrank F C := by
    change Module.finrank F (Fin 2 → F) < Module.finrank F (Fin 3 → F)
    rw [Module.finrank_fin_fun, Module.finrank_fin_fun]
    norm_num
  have hker : LinearMap.ker (transferMap x) ≠ ⊥ :=
    LinearMap.ker_ne_bot_of_finrank_lt hdim
  obtain ⟨c, hc_mem, hc_ne⟩ := (Submodule.ne_bot_iff _).mp hker
  refine ⟨c, hc_ne, ?_⟩
  have hz : transferMap x c = 0 := (LinearMap.mem_ker).mp hc_mem
  intro q
  exact congrFun hz q

end VerifyThreeTransferKernel
