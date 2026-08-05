import Mathlib

/-!
Universal algebraic kernel for the Generation-5 multi-channel transfer proposal.

A vector of product-transfer symbols can detect a defect exactly when its
syndrome map is injective on the defect space.  Once detected, componentwise
left/right multiplication by nonzero elements of a division ring cannot erase
all channels.  For residue symbols modeled as the two-dimensional
`𝔽₁₇`-space, `r` channels have exact capacity `2 * r`: an injective linear
syndrome forces the defect-space dimension to be at most `2 * r`, and above
that ambient-dimension bound every linear syndrome has a nonzero kernel element.

These statements are conditional algebra.  They do not construct rank-one
product labels, serialize a NAND/COPY tile, prove a shell-energy bound, or
establish Q1/Q2.
-/

namespace VerifyMultichannelTransfer

/-- Componentwise two-sided transport of a direct sum of transfer symbols. -/
def transport {ι D : Type*} [DivisionRing D]
    (u v x : ι → D) : ι → D :=
  fun i => u i * x i * v i

/-- Nonzero componentwise division-ring factors preserve, and reflect, whether
an entire vector-valued transfer is zero. -/
theorem transport_eq_zero_iff
    {ι D : Type*} [DivisionRing D]
    (u v x : ι → D)
    (hu : ∀ i, u i ≠ 0) (hv : ∀ i, v i ≠ 0) :
    transport u v x = 0 ↔ x = 0 := by
  constructor
  · intro h
    funext i
    have hi : u i * x i * v i = 0 := congrFun h i
    rcases mul_eq_zero.mp hi with hux | hvi
    · exact (mul_eq_zero.mp hux).resolve_left (hu i)
    · exact (hv i hvi).elim
  · rintro rfl
    funext i
    simp [transport]

/-- If a direct-sum syndrome is injective on the defect group, componentwise
transport by nonzero division-ring factors detects exactly the nonzero defects.
This is the precise conditional implication needed before a multi-channel
candidate may use componentwise graded transport. -/
theorem injective_syndrome_survives_transport_iff
    {ι D G : Type*} [DivisionRing D] [AddCommGroup G]
    (T : G →+ (ι → D)) (hT : Function.Injective T)
    (u v : ι → D) (hu : ∀ i, u i ≠ 0) (hv : ∀ i, v i ≠ 0)
    (g : G) :
    transport u v (T g) ≠ 0 ↔ g ≠ 0 := by
  constructor
  · intro htransport hg
    apply htransport
    apply (transport_eq_zero_iff u v (T g) hu hv).2
    rw [hg]
    exact T.map_zero
  · intro hg htransport
    apply hg
    apply hT
    have hsyndrome : T g = 0 :=
      (transport_eq_zero_iff u v (T g) hu hv).1 htransport
    exact hsyndrome.trans T.map_zero.symm

abbrev F := ZMod 17

local instance : Fact (Nat.Prime 17) := ⟨by norm_num⟩

/-- One `F_289` leading symbol represented as a two-dimensional `F_17` space. -/
abbrev ResidueSymbol := Fin 2 → F

/-- A direct sum of `r` residue-symbol channels. -/
abbrev Channels (r : ℕ) := Fin r → ResidueSymbol

/-- `r` residue channels have exact `F_17` dimension `2r`. -/
theorem channels_finrank (r : ℕ) :
    Module.finrank F (Channels r) = 2 * r := by
  change Module.finrank F (Fin r → Fin 2 → F) = 2 * r
  rw [Module.finrank_pi_fintype]
  simp [Nat.mul_comm]

/-- Necessary capacity bound: an injective `r`-channel linear syndrome can
exist only when the defect-space dimension is at most `2r`. -/
theorem injective_multichannel_rank_bound
    {V : Type*} [AddCommGroup V] [Module F V] [FiniteDimensional F V]
    (r : ℕ) (T : V →ₗ[F] Channels r) (hT : Function.Injective T) :
    Module.finrank F V ≤ 2 * r := by
  rw [← channels_finrank r]
  exact LinearMap.finrank_le_finrank_of_injective hT

/-- Complementary obstruction: if the defect-space dimension exceeds `2r`,
every `r`-channel linear syndrome misses a genuine nonzero defect. -/
theorem exists_nonzero_multichannel_kernel
    {V : Type*} [AddCommGroup V] [Module F V] [FiniteDimensional F V]
    (r : ℕ) (T : V →ₗ[F] Channels r)
    (tooLarge : 2 * r < Module.finrank F V) :
    ∃ g : V, g ≠ 0 ∧ T g = 0 := by
  have hdim : Module.finrank F (Channels r) < Module.finrank F V := by
    rwa [channels_finrank r]
  have hker : LinearMap.ker T ≠ ⊥ :=
    LinearMap.ker_ne_bot_of_finrank_lt hdim
  obtain ⟨g, hg_mem, hg_ne⟩ := (Submodule.ne_bot_iff _).mp hker
  exact ⟨g, hg_ne, (LinearMap.mem_ker).mp hg_mem⟩

end VerifyMultichannelTransfer
