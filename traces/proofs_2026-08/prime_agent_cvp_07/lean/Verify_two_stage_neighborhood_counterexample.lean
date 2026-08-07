import Mathlib

namespace VerifyTwoStageNeighborhoodCounterexample

/-- The support graph of an integer matrix. -/
def incidenceGraph {R K : Type*} (A : R → K → ℤ) : SimpleGraph (Sum R K) where
  Adj
    | .inl r, .inr k => A r k ≠ 0
    | .inr k, .inl r => A r k ≠ 0
    | _, _ => False
  symm := ⟨by
    intro u v
    cases u <;> cases v <;> simp_all⟩
  loopless := ⟨by
    intro u
    cases u <;> simp⟩

/--
The canonical two-stage matrix with the fixed one-by-one blocks `A = [1]`
and `B = [1]`: scenario row `i` sees one common first-stage column and its
one private second-stage column.
-/
def twoStageOne (n : ℕ) : Fin n → Sum Unit (Fin n) → ℤ
  | _, .inl _ => 1
  | i, .inr j => if i = j then 1 else 0

/-- Equality of open neighborhoods (the twin relation used by neighborhood diversity). -/
def SameOpenNeighborhood {V : Type*} (G : SimpleGraph V) (u v : V) : Prop :=
  ∀ w, G.Adj u w ↔ G.Adj v w

/-- Every scenario row is adjacent to the common first-stage column. -/
theorem row_adjacent_global (n : ℕ) (i : Fin n) :
    (incidenceGraph (twoStageOne n)).Adj (.inl i) (.inr (.inl ())) := by
  simp [incidenceGraph, twoStageOne]

/-- A scenario row is adjacent to private column `j` exactly in scenario `j`. -/
theorem row_adjacent_private_iff (n : ℕ) (i j : Fin n) :
    (incidenceGraph (twoStageOne n)).Adj (.inl i) (.inr (.inr j)) ↔ i = j := by
  simp [incidenceGraph, twoStageOne]

/--
Distinct scenario rows of this fixed-template two-stage family have distinct
open neighborhoods.  Hence the number of (even unmarked) neighborhood types
among row vertices is at least `n`; neighborhood diversity is not bounded by
the fixed two-stage blocks.
-/
theorem same_row_neighborhood_iff (n : ℕ) (i j : Fin n) :
    SameOpenNeighborhood (incidenceGraph (twoStageOne n)) (.inl i) (.inl j) ↔ i = j := by
  constructor
  · intro h
    have hij := h (.inr (.inr i))
    have hi : (incidenceGraph (twoStageOne n)).Adj (.inl i) (.inr (.inr i)) :=
      (row_adjacent_private_iff n i i).2 rfl
    have hj : (incidenceGraph (twoStageOne n)).Adj (.inl j) (.inr (.inr i)) :=
      hij.mp hi
    exact (row_adjacent_private_iff n j i).1 hj |>.symm
  · intro h
    subst j
    exact fun _ => Iff.rfl

/-- Explicit injectivity formulation of the unbounded row-neighborhood witness. -/
theorem row_neighborhood_map_injective (n : ℕ) :
    Function.Injective (fun i : Fin n =>
      {w | (incidenceGraph (twoStageOne n)).Adj (.inl i) w}) := by
  intro i j h
  apply (same_row_neighborhood_iff n i j).1
  intro w
  have hw := Set.ext_iff.mp h w
  simpa using hw

end VerifyTwoStageNeighborhoodCounterexample
