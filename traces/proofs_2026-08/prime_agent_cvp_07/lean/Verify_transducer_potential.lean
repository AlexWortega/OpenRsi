import Mathlib

namespace VerifyTransducerPotential

variable {State : Type*}

/-- The final state reached from `start` by the listed successor states. -/
def endpoint (start : State) : List State → State
  | [] => start
  | next :: rest => endpoint next rest

/-- Total integer gain along a walk represented by its start and successor list. -/
def walkGain (weight : State → State → ℤ) (start : State) : List State → ℤ
  | [] => 0
  | next :: rest => weight start next + walkGain weight next rest

/-- Every consecutive pair in the represented walk is an allowed transition. -/
def IsWalk (edge : State → State → Prop) (start : State) : List State → Prop
  | [] => True
  | next :: rest => edge start next ∧ IsWalk edge next rest

/--
A local integer potential certificate telescopes exactly along every finite walk.
The parameters `p/q` encode the certified gain per transition without division.
-/
theorem potential_certificate_telescope
    (edge : State → State → Prop)
    (weight : State → State → ℤ)
    (potential : State → ℤ)
    (p q : ℤ)
    (certificate : ∀ x y, edge x y →
      p ≤ q * weight x y + potential y - potential x)
    (start : State) (successors : List State)
    (walk : IsWalk edge start successors) :
    p * (successors.length : ℤ) + potential start -
        potential (endpoint start successors) ≤
      q * walkGain weight start successors := by
  induction successors generalizing start with
  | nil => simp [endpoint, walkGain]
  | cons next rest ih =>
      rcases walk with ⟨firstEdge, remainingWalk⟩
      have firstBound := certificate start next firstEdge
      have remainingBound := ih next remainingWalk
      simp only [List.length_cons, Nat.cast_add, Nat.cast_one, walkGain, endpoint]
      nlinarith

/--
If all potentials lie in `[lo, hi]`, the same certificate gives a uniform
all-length lower bound, losing only the fixed potential width.
-/
theorem potential_certificate_bounded
    (edge : State → State → Prop)
    (weight : State → State → ℤ)
    (potential : State → ℤ)
    (p q lo hi : ℤ)
    (certificate : ∀ x y, edge x y →
      p ≤ q * weight x y + potential y - potential x)
    (lower : ∀ x, lo ≤ potential x)
    (upper : ∀ x, potential x ≤ hi)
    (start : State) (successors : List State)
    (walk : IsWalk edge start successors) :
    p * (successors.length : ℤ) - (hi - lo) ≤
      q * walkGain weight start successors := by
  have telescoped := potential_certificate_telescope edge weight potential p q
    certificate start successors walk
  have startLower := lower start
  have endUpper := upper (endpoint start successors)
  linarith

/--
The threshold relevant to the ramified-prime proposal is exact: one unit of
valuation gain per four binary levels beats the binary scale because 17 > 2^4.
-/
theorem ramified_seventeen_beats_four_binary_levels
    {depth gain : ℕ} (gain_pos : 0 < gain) (enoughGain : depth ≤ 4 * gain) :
    2 ^ depth < 17 ^ gain := by
  calc
    2 ^ depth ≤ 2 ^ (4 * gain) :=
      Nat.pow_le_pow_right (by decide) enoughGain
    _ = (2 ^ 4) ^ gain := by rw [pow_mul]
    _ = 16 ^ gain := by norm_num
    _ < 17 ^ gain :=
      Nat.pow_lt_pow_left (by decide) (Nat.ne_of_gt gain_pos)

end VerifyTransducerPotential
