import Mathlib

/-!
A universal obstruction behind the surviving Generation-4 lift-or-kill proposal.

If three integral seam directions survive every emitted non-transfer row, while
one leading transfer coordinate takes values in the two-dimensional
`𝔽₁₇`-space, then an integral combination of those directions also survives
all those rows and has zero leading transfer.  Its three coefficients can be
chosen in `[-8, 8]`, hence with squared coefficient weight at most `192`.
If the original directions are integrally independent, the resulting seam
movement is nonzero.

This theorem does not assert that three such directions survive the omitted
rows of the campaign's full NAND/COPY matrix, nor that the resulting movement
has CVP energy below `17E`; those are exactly the pending serialized-matrix
and exact-minimization checks.
-/

namespace VerifySingleTransferLiftObstruction

abbrev F := ZMod 17

local instance : Fact (Nat.Prime 17) := ⟨by norm_num⟩

abbrev Symbol := Fin 2 → F
abbrev ResidueCoeffs := Fin 3 → F

noncomputable def transferMap (x : Fin 3 → Symbol) :
    ResidueCoeffs →ₗ[F] Symbol where
  toFun c q := ∑ i, c i * x i q
  map_add' c d := by
    ext q
    simp only [Pi.add_apply, add_mul, Finset.sum_add_distrib]
  map_smul' a c := by
    ext q
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, mul_assoc,
      Finset.mul_sum]

/-- Three symbols in the two-dimensional leading residue space always have a
nontrivial residue dependency. -/
theorem exists_nonzero_residue_dependency (x : Fin 3 → Symbol) :
    ∃ d : ResidueCoeffs, d ≠ 0 ∧ ∀ q : Fin 2, ∑ i, d i * x i q = 0 := by
  have hdim : Module.finrank F Symbol < Module.finrank F ResidueCoeffs := by
    change Module.finrank F (Fin 2 → F) < Module.finrank F (Fin 3 → F)
    rw [Module.finrank_fin_fun, Module.finrank_fin_fun]
    norm_num
  have hker : LinearMap.ker (transferMap x) ≠ ⊥ :=
    LinearMap.ker_ne_bot_of_finrank_lt hdim
  obtain ⟨d, hd_mem, hd_ne⟩ := (Submodule.ne_bot_iff _).mp hker
  refine ⟨d, hd_ne, ?_⟩
  have hz : transferMap x d = 0 := (LinearMap.mem_ker).mp hd_mem
  intro q
  exact congrFun hz q

/-- The centered integer representative of a residue modulo `17`. -/
def balancedLift (a : F) : ℤ :=
  if a.val ≤ 8 then (a.val : ℤ) else (a.val : ℤ) - 17

lemma balancedLift_bounds (a : F) : -8 ≤ balancedLift a ∧ balancedLift a ≤ 8 := by
  have hval : a.val < 17 := a.val_lt
  by_cases h : a.val ≤ 8
  · simp only [balancedLift, if_pos h]
    omega
  · simp only [balancedLift, if_neg h]
    omega

lemma balancedLift_cast (a : F) : (balancedLift a : F) = a := by
  by_cases h : a.val ≤ 8
  · simp [balancedLift, h]
  · rw [balancedLift, if_neg h, Int.cast_sub, Int.cast_natCast,
      ZMod.natCast_zmod_val]
    have h17 : ((17 : ℤ) : F) = 0 := by
      change ((17 : ℕ) : ZMod 17) = 0
      exact ZMod.natCast_self 17
    rw [h17, sub_zero]

/--
Sharp lift-or-kill obstruction for one `𝔽₁₇²` transfer coordinate.

`g i` are three candidate integral seam directions. `row` can be the entire
family of emitted non-transfer equations: each row is represented as an
integer linear functional. If every `g i` survives every row, their certified
combination `v` does too. Integral independence ensures that `v` is a genuine
nonzero movement rather than a zero presentation.
-/
theorem single_transfer_lift_obstruction
    {Cell Row : Type*}
    (row : Row → (Cell → ℤ) →ₗ[ℤ] ℤ)
    (g : Fin 3 → Cell → ℤ)
    (x : Fin 3 → Symbol)
    (survives : ∀ r i, row r (g i) = 0)
    (independent : ∀ c : Fin 3 → ℤ,
      (∑ i, c i • g i) = 0 → c = 0) :
    ∃ c : Fin 3 → ℤ, ∃ v : Cell → ℤ,
      c ≠ 0 ∧
      v ≠ 0 ∧
      (∀ i, -8 ≤ c i ∧ c i ≤ 8) ∧
      (∑ i, c i ^ 2) ≤ 192 ∧
      v = ∑ i, c i • g i ∧
      (∀ r, row r v = 0) ∧
      (∀ q : Fin 2, ∑ i, (c i : F) * x i q = 0) := by
  obtain ⟨d, hd_ne, hd_transfer⟩ := exists_nonzero_residue_dependency x
  let c : Fin 3 → ℤ := fun i => balancedLift (d i)
  let v : Cell → ℤ := ∑ i, c i • g i
  have hc_cast : ∀ i, (c i : F) = d i := by
    intro i
    exact balancedLift_cast (d i)
  have hc_ne : c ≠ 0 := by
    intro hc
    apply hd_ne
    funext i
    rw [← hc_cast i, congrFun hc i]
    simp
  have hv_ne : v ≠ 0 := by
    intro hv
    exact hc_ne (independent c hv)
  have hc_bounds : ∀ i, -8 ≤ c i ∧ c i ≤ 8 := by
    intro i
    exact balancedLift_bounds (d i)
  have hc_square : ∀ i, c i ^ 2 ≤ 64 := by
    intro i
    have h := hc_bounds i
    nlinarith [sq_nonneg (c i + 8), sq_nonneg (8 - c i)]
  have hc_weight : (∑ i, c i ^ 2) ≤ 192 := by
    calc
      (∑ i, c i ^ 2) ≤ ∑ _i : Fin 3, (64 : ℤ) :=
        Finset.sum_le_sum fun i _hi => hc_square i
      _ = 192 := by norm_num
  refine ⟨c, v, hc_ne, hv_ne, hc_bounds, hc_weight, rfl, ?_, ?_⟩
  · intro r
    simp only [v, map_sum, LinearMap.map_smul, survives, smul_zero,
      Finset.sum_const_zero]
  · intro q
    simpa only [hc_cast] using hd_transfer q

end VerifySingleTransferLiftObstruction
