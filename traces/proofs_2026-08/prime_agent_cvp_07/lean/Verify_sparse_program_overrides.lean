import Mathlib

/-!
Universal semantics for a default program with sparse event overrides.

A program of `n` cells is represented by one default value and a finite list
of `(cell,value)` overrides.  Lookup is deliberately defined without any
routing or NAND semantics.  We prove that lookup agrees with dense
materialization, that the induced program-row target is one-hot, and that a
strictly key-sorted override stream has unique keys and returns the recorded
value at every emitted override.  These are serializer semantic facts only;
they prove no butterfly placement, CVP completeness, or soundness statement.
-/

namespace VerifySparseProgramOverrides

/-- First-match lookup in a sparse override stream.  Canonical streams below
have unique keys, so the first/last match convention is immaterial there. -/
def lookup {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) : List (Fin n × α) → Fin n → α
  | [], _ => default
  | (key, value) :: rest, i =>
      if key = i then value else lookup default rest i

/-- The function denoted by the sparse representation. -/
def denseFunction {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) (overrides : List (Fin n × α)) : Fin n → α :=
  lookup default overrides

/-- Ordinary dense list materialization, used by an eager implementation. -/
def denseList {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) (overrides : List (Fin n × α)) : List α :=
  List.ofFn (denseFunction default overrides)

@[simp] theorem denseList_length {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) (overrides : List (Fin n × α)) :
    (denseList default overrides).length = n := by
  simp [denseList]

/-- Pointwise lookup in the eager dense list is exactly sparse lookup. -/
theorem denseList_get_eq_lookup {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) (overrides : List (Fin n × α)) (i : Fin n) :
    (denseList default overrides).get
        ⟨i.1, by simp⟩ = lookup default overrides i := by
  simp [denseList, denseFunction]

/-- Extensional version of the sparse/dense equivalence. -/
theorem denseFunction_eq_lookup {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) (overrides : List (Fin n × α)) :
    denseFunction default overrides = lookup default overrides := rfl

@[simp] theorem lookup_nil {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) (i : Fin n) : lookup default [] i = default := rfl

@[simp] theorem lookup_cons_self {n : ℕ} {α : Type*} [DecidableEq α]
    (default value : α) (key : Fin n) (rest : List (Fin n × α)) :
    lookup default ((key, value) :: rest) key = value := by
  simp [lookup]

/-- If no override has the requested key, lookup returns the default. -/
theorem lookup_eq_default_of_not_mem {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) (overrides : List (Fin n × α)) (i : Fin n)
    (h : i ∉ overrides.map Prod.fst) :
    lookup default overrides i = default := by
  induction overrides with
  | nil => rfl
  | cons entry rest ih =>
      rcases entry with ⟨key, value⟩
      simp only [List.map_cons, List.mem_cons, not_or] at h
      have hki : key ≠ i := Ne.symm h.1
      simp [lookup, hki, ih h.2]

/-- Canonical ordering condition for a stream of finite-index overrides. -/
def SortedOverrides {n : ℕ} {α : Type*}
    (overrides : List (Fin n × α)) : Prop :=
  overrides.Pairwise (fun a b => a.1 < b.1)

/-- Strict key ordering implies that keys do not repeat. -/
theorem sortedOverrides_keys_nodup {n : ℕ} {α : Type*}
    {overrides : List (Fin n × α)} (h : SortedOverrides overrides) :
    (overrides.map Prod.fst).Nodup := by
  rw [List.nodup_iff_pairwise_ne, List.pairwise_map]
  exact h.imp (fun hab => ne_of_lt hab)

/-- In a canonical sorted stream, lookup at every recorded pair returns that
pair's value.  Thus the sparse stream has no ambiguous duplicate updates. -/
theorem lookup_eq_of_mem_sorted {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) {overrides : List (Fin n × α)}
    (hsorted : SortedOverrides overrides) {key : Fin n} {value : α}
    (hmem : (key, value) ∈ overrides) :
    lookup default overrides key = value := by
  induction overrides with
  | nil => simp at hmem
  | cons entry rest ih =>
      rcases entry with ⟨headKey, headValue⟩
      unfold SortedOverrides at hsorted
      rw [List.pairwise_cons] at hsorted
      rcases hsorted with ⟨hhead, htail⟩
      simp only [List.mem_cons] at hmem
      rcases hmem with hfirst | hrest
      · cases hfirst
        simp [lookup]
      · have hlt : headKey < key := hhead (key, value) hrest
        have hne : headKey ≠ key := ne_of_lt hlt
        simp [lookup, hne, ih htail hrest]

/-- A program row is targeted at one exactly when its row label is the chosen
mode for that cell. -/
def programTarget {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) (overrides : List (Fin n × α))
    (cell : Fin n) (rowMode : α) : ℕ :=
  if lookup default overrides cell = rowMode then 1 else 0

@[simp] theorem programTarget_selected {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) (overrides : List (Fin n × α)) (cell : Fin n) :
    programTarget default overrides cell (lookup default overrides cell) = 1 := by
  simp [programTarget]

@[simp] theorem programTarget_other {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) (overrides : List (Fin n × α)) (cell : Fin n) (mode : α)
    (h : mode ≠ lookup default overrides cell) :
    programTarget default overrides cell mode = 0 := by
  simp [programTarget, Ne.symm h]

/-- The rows belonging to every cell form a one-hot vector. -/
theorem programTarget_sum_one {n : ℕ} {α : Type*}
    [Fintype α] [DecidableEq α]
    (default : α) (overrides : List (Fin n × α)) (cell : Fin n) :
    ∑ mode : α, programTarget default overrides cell mode = 1 := by
  simp [programTarget]

/-- Across the whole program there is exactly one targeted mode row per
cell, hence exactly `n` targeted program rows. -/
theorem programTarget_total {n : ℕ} {α : Type*}
    [Fintype α] [DecidableEq α]
    (default : α) (overrides : List (Fin n × α)) :
    ∑ cell : Fin n, ∑ mode : α, programTarget default overrides cell mode = n := by
  simp [programTarget_sum_one]

/-- One-hot targets computed from sparse lookup agree pointwise with targets
computed after eager dense-list materialization. -/
theorem sparseTarget_eq_denseTarget {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) (overrides : List (Fin n × α))
    (cell : Fin n) (rowMode : α) :
    programTarget default overrides cell rowMode =
      (if (denseList default overrides).get ⟨cell.1, by simp⟩ = rowMode
       then 1 else 0) := by
  rw [denseList_get_eq_lookup]
  rfl

/-- A recorded canonical override selects precisely its recorded mode row. -/
theorem override_target_selected {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) {overrides : List (Fin n × α)}
    (hsorted : SortedOverrides overrides) {key : Fin n} {value : α}
    (hmem : (key, value) ∈ overrides) :
    programTarget default overrides key value = 1 := by
  simp [programTarget, lookup_eq_of_mem_sorted default hsorted hmem]

/-- Every other mode row at a recorded canonical override is zero. -/
theorem override_target_other {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) {overrides : List (Fin n × α)}
    (hsorted : SortedOverrides overrides) {key : Fin n} {value other : α}
    (hmem : (key, value) ∈ overrides) (hne : other ≠ value) :
    programTarget default overrides key other = 0 := by
  apply programTarget_other
  simpa [lookup_eq_of_mem_sorted default hsorted hmem] using hne

/-- A cell absent from the override keys selects the default mode row. -/
theorem absent_target_selects_default {n : ℕ} {α : Type*} [DecidableEq α]
    (default : α) (overrides : List (Fin n × α)) (key : Fin n)
    (h : key ∉ overrides.map Prod.fst) :
    programTarget default overrides key default = 1 := by
  simp [programTarget, lookup_eq_default_of_not_mem default overrides key h]

end VerifySparseProgramOverrides
