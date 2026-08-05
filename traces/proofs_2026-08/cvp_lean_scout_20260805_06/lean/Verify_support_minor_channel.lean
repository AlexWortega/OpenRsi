import Mathlib

namespace VerifySupportMinorChannel

/-- The bipartite support graph of a matrix. -/
def incidenceGraph {R K : Type*} (C : R → K → ℤ) : SimpleGraph (Sum R K) where
  Adj
    | .inl r, .inr k => C r k ≠ 0
    | .inr k, .inl r => C r k ≠ 0
    | _, _ => False
  symm := ⟨by
    intro u v
    cases u <;> cases v <;> simp_all⟩
  loopless := ⟨by
    intro u
    cases u <;> simp⟩

/-- The matrix `[I | -C]` used in U0. -/
def augmentedMatrix {R K : Type*} [DecidableEq R] (C : R → K → ℤ) :
    R → Sum R K → ℤ
  | r, .inl s => if r = s then 1 else 0
  | r, .inr k => -C r k

/-- The support graph of `[I | -C]`. -/
def augmentedSupport {R K : Type*} [DecidableEq R] (C : R → K → ℤ) :
    SimpleGraph (Sum R (Sum R K)) :=
  incidenceGraph (augmentedMatrix C)

/-- Include the rows and the original `C` columns, omitting identity columns. -/
def originalVertex {R K : Type*} : Sum R K → Sum R (Sum R K)
  | .inl r => .inl r
  | .inr k => .inr (.inr k)

/-- The inclusion of original support vertices is injective. -/
theorem originalVertex_injective {R K : Type*} :
    Function.Injective (originalVertex : Sum R K → Sum R (Sum R K)) := by
  intro u v h
  cases u <;> cases v <;> simp_all [originalVertex]

/--
The support graph of `C` is an induced copy inside the support graph of
`[I | -C]`. Thus the identity block cannot erase any support-graph minor or
separator obstruction already certified in `C`.
-/
theorem original_support_induced {R K : Type*} [DecidableEq R]
    (C : R → K → ℤ) (u v : Sum R K) :
    (augmentedSupport C).Adj (originalVertex u) (originalVertex v) ↔
      (incidenceGraph C).Adj u v := by
  cases u <;> cases v <;>
    simp [augmentedSupport, augmentedMatrix, incidenceGraph, originalVertex]

/-- Every added identity-column vertex is a leaf attached only to its row. -/
theorem identity_column_neighborhood {R K : Type*} [DecidableEq R]
    (C : R → K → ℤ) (r : R) (v : Sum R (Sum R K)) :
    (augmentedSupport C).Adj (.inr (.inl r)) v ↔ v = .inl r := by
  cases v with
  | inl s =>
      simp [augmentedSupport, augmentedMatrix, incidenceGraph, eq_comm]
  | inr k =>
      cases k <;> simp [augmentedSupport, augmentedMatrix, incidenceGraph]

/-- Internal connectivity of a branch set, expressed without leaving the set. -/
def InternallyConnected {W : Type*} (H : SimpleGraph W) (S : W → Prop) : Prop :=
  ∀ ⦃x y⦄, S x → S y →
    Relation.ReflTransGen (fun a b => H.Adj a b ∧ S a ∧ S b) x y

/--
A branch-set certificate that `G` is obtained as a graph minor of `H`.
This is the exact certificate consumed by a minor-monotone invariant.
-/
structure MinorModel {V W : Type*} (G : SimpleGraph V) (H : SimpleGraph W) where
  branch : V → W → Prop
  nonempty : ∀ v, ∃ x, branch v x
  disjoint : ∀ ⦃u v x⦄, branch u x → branch v x → u = v
  connected : ∀ v, InternallyConnected H (branch v)
  lift_edge : ∀ ⦃u v⦄, G.Adj u v →
    ∃ x y, branch u x ∧ branch v y ∧ H.Adj x y

/--
A precise, checkable meaning of a faithful equality expansion: contraction is
onto, every contraction fiber is internally connected, and every old edge has
an edge between the corresponding fibers.
-/
structure FaithfulEqualityExpansion {V W : Type*}
    (G : SimpleGraph V) (H : SimpleGraph W) where
  collapse : W → V
  onto : Function.Surjective collapse
  fiber_connected : ∀ v, InternallyConnected H (fun x => collapse x = v)
  lift_edge : ∀ ⦃u v⦄, G.Adj u v →
    ∃ x y, collapse x = u ∧ collapse y = v ∧ H.Adj x y

/--
Every faithful equality expansion is minor-preserving. Consequently, once an
allowed gadget has such a contraction certificate, no minor-monotone support
invariant can decrease under that expansion.
-/
def FaithfulEqualityExpansion.minorModel {V W : Type*}
    {G : SimpleGraph V} {H : SimpleGraph W}
    (E : FaithfulEqualityExpansion G H) : MinorModel G H where
  branch v x := E.collapse x = v
  nonempty v := by
    obtain ⟨x, hx⟩ := E.onto v
    exact ⟨x, hx⟩
  disjoint := by
    intro u v x hxu hxv
    exact hxu.symm.trans hxv
  connected v := E.fiber_connected v
  lift_edge := by
    intro u v huv
    obtain ⟨x, y, hx, hy, hxy⟩ := E.lift_edge huv
    exact ⟨x, y, hx, hy, hxy⟩

/-- Existence form of the minor-preservation theorem. -/
theorem faithful_equality_expansion_is_minor {V W : Type*}
    {G : SimpleGraph V} {H : SimpleGraph W}
    (E : FaithfulEqualityExpansion G H) : Nonempty (MinorModel G H) :=
  ⟨E.minorModel⟩

/-- The induced original support gives an explicit singleton-branch minor model. -/
theorem augmented_support_contains_original_minor
    {R K : Type*} [DecidableEq R] (C : R → K → ℤ) :
    Nonempty (MinorModel (incidenceGraph C) (augmentedSupport C)) := by
  refine ⟨{
    branch := fun v x => x = originalVertex v
    nonempty := ?_
    disjoint := ?_
    connected := ?_
    lift_edge := ?_
  }⟩
  · intro v
    exact ⟨originalVertex v, rfl⟩
  · intro u v x hxu hxv
    apply originalVertex_injective
    exact hxu.symm.trans hxv
  · intro v x y hx hy
    subst x
    subst y
    exact Relation.ReflTransGen.refl
  · intro u v huv
    exact ⟨originalVertex u, originalVertex v, rfl, rfl,
      (original_support_induced C u v).2 huv⟩

end VerifySupportMinorChannel
