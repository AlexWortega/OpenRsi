import Mathlib

namespace VerifyQuadraticCharacterSwitch

open scoped BigOperators

/-- The integral sign character of one Boolean wire. -/
def bitSign (b : Bool) : ℤ := if b then -1 else 1

/--
The four-coordinate switch word `(1, (-1)^a, (-1)^b, (-1)^(a*b))`.
The last coordinate is quadratic rather than an additive wire character.
-/
def qchar (a b : Bool) : Fin 4 → ℤ :=
  ![1, bitSign a, bitSign b, bitSign (a && b)]

/-- Every honest quadratic-character switch word has squared radius four. -/
theorem qchar_squared_radius (a b : Bool) :
    ∑ i : Fin 4, (qchar a b i) ^ 2 = 4 := by
  cases a <;> cases b <;> native_decide

/--
The old four-state affine exchange is visible in exactly the quadratic
coordinate: its mixed derivative is `-2 e₃`, rather than zero.
-/
theorem qchar_mixed_derivative (i : Fin 4) :
    qchar false false i - qchar false true i - qchar true false i +
        qchar true true i =
      if i = (3 : Fin 4) then -2 else 0 := by
  fin_cases i <;> native_decide

/--
Stronger local statement: the four honest words have no nontrivial integer
linear relation. In particular, no higher-support integer exchange among
these four local state columns can replace the killed rectangle exchange.
-/
theorem qchar_integer_linear_independent
    (c00 c01 c10 c11 : ℤ)
    (h : ∀ i : Fin 4,
      c00 * qchar false false i + c01 * qchar false true i +
      c10 * qchar true false i + c11 * qchar true true i = 0) :
    c00 = 0 ∧ c01 = 0 ∧ c10 = 0 ∧ c11 = 0 := by
  have h0 := h (0 : Fin 4)
  have h1 := h (1 : Fin 4)
  have h2 := h (2 : Fin 4)
  have h3 := h (3 : Fin 4)
  have e002 : qchar false false (2 : Fin 4) = 1 := by native_decide
  have e012 : qchar false true (2 : Fin 4) = -1 := by native_decide
  have e102 : qchar true false (2 : Fin 4) = 1 := by native_decide
  have e112 : qchar true true (2 : Fin 4) = -1 := by native_decide
  have e003 : qchar false false (3 : Fin 4) = 1 := by native_decide
  have e013 : qchar false true (3 : Fin 4) = 1 := by native_decide
  have e103 : qchar true false (3 : Fin 4) = 1 := by native_decide
  have e113 : qchar true true (3 : Fin 4) = -1 := by native_decide
  norm_num [qchar, bitSign] at h0 h1
  rw [e002, e012, e102, e112] at h2
  rw [e003, e013, e103, e113] at h3
  omega

/-- Swapping the two wires is the marked coordinate permutation `(1 2)`. -/
def wireSwap : Equiv.Perm (Fin 4) :=
  Equiv.swap (1 : Fin 4) (2 : Fin 4)

theorem qchar_wire_swap (a b : Bool) (i : Fin 4) :
    qchar b a i = qchar a b (wireSwap i) := by
  cases a <;> cases b <;> fin_cases i <;> native_decide

end VerifyQuadraticCharacterSwitch
