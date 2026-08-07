import Mathlib

namespace VerifyU0aSerializerDimensions

/-!
This file formalizes the all-parameter arithmetic behind the U0a
butterfly NAND/COPY serializer.  It deliberately proves only dimension and
layer-capacity facts; it makes no CVP soundness or universality claim.
-/

/-- Four legal source-selector columns per lane: two FREE states and one state
for each of FIX0 and FIX1. -/
def sourceSelectorColumns (w : ℕ) : ℕ := 4 * w

/-- Five gate modes, each with four Boolean input pairs, per gate location. -/
def gateSelectorColumns (w d : ℕ) : ℕ := 20 * w * d

/-- Total number of selector (lattice-basis) columns. -/
def selectorColumns (w d : ℕ) : ℕ :=
  sourceSelectorColumns w + gateSelectorColumns w d

/-- One normalization/DROP-guard row for every source or gate node. -/
def normalizationRows (w d : ℕ) : ℕ := w * (d + 1)

/-- Three source-program modes per input lane. -/
def sourceProgramRows (w : ℕ) : ℕ := 3 * w

/-- Five gate-program modes per gate location. -/
def gateProgramRows (w d : ℕ) : ℕ := 5 * w * d

/-- Two input-edge consistency equations per gate location. -/
def edgeRows (w d : ℕ) : ℕ := 2 * w * d

/-- For power-of-two width `w`, the dyadic blocks at all nontrivial scales
number `w - 1` per port and stage; there are two ports. -/
def separatorRows (w d : ℕ) : ℕ := 2 * d * (w - 1)

/-- One output-interface row per lane. -/
def outputRows (w : ℕ) : ℕ := w

/-- The serializer adds one physical identity row for every selector column. -/
def physicalRows (w d : ℕ) : ℕ := selectorColumns w d

/-- Total ambient/output dimension, presented as the sum of the actual row
families in the serializer. -/
def rowCount (w d : ℕ) : ℕ :=
  normalizationRows w d + sourceProgramRows w + gateProgramRows w d +
  edgeRows w d + separatorRows w d + outputRows w + physicalRows w d

/-- The systematic constraint matrix is `[I | -C]`, hence has `m+k` columns. -/
def systematicColumns (w d : ℕ) : ℕ := rowCount w d + selectorColumns w d

@[simp] theorem selectorColumns_closed (w d : ℕ) :
    selectorColumns w d = 4 * w + 20 * w * d := by
  rfl

/-- A subtraction-free exact formula, convenient for polynomial estimates. -/
theorem rowCount_expanded (w d : ℕ) :
    rowCount w d = 28 * w * d + 9 * w + 2 * d * (w - 1) := by
  unfold rowCount normalizationRows sourceProgramRows gateProgramRows edgeRows
    separatorRows outputRows physicalRows selectorColumns sourceSelectorColumns
    gateSelectorColumns
  ring

/-- Closed row formula.  The mild condition `1 ≤ w` is satisfied by every
legal serializer width (in fact the implementation requires `w ≥ 2`). -/
theorem rowCount_closed (w d : ℕ) (hw : 1 ≤ w) :
    rowCount w d = 30 * w * d + 9 * w - 2 * d := by
  have hsub : w - 1 + 1 = w := by omega
  have hsep : 2 * d * (w - 1) + 2 * d = 2 * d * w := by
    calc
      2 * d * (w - 1) + 2 * d = 2 * d * ((w - 1) + 1) := by ring
      _ = 2 * d * w := by rw [hsub]
  apply Nat.eq_sub_of_add_eq
  rw [rowCount_expanded]
  calc
    28 * w * d + 9 * w + 2 * d * (w - 1) + 2 * d =
        28 * w * d + 9 * w + (2 * d * (w - 1) + 2 * d) := by ring
    _ = 28 * w * d + 9 * w + 2 * d * w := by rw [hsep]
    _ = 30 * w * d + 9 * w := by ring

/-- Closed formula for the number of columns of `[I | -C]`. -/
theorem systematicColumns_closed (w d : ℕ) (hw : 1 ≤ w) :
    systematicColumns w d = 50 * w * d + 13 * w - 2 * d := by
  unfold systematicColumns
  rw [rowCount_closed w d hw, selectorColumns_closed]
  have hle : 2 * d ≤ 30 * w * d + 9 * w := by nlinarith
  apply Nat.eq_sub_of_add_eq
  calc
    (30 * w * d + 9 * w - 2 * d + (4 * w + 20 * w * d)) + 2 * d =
        (30 * w * d + 9 * w - 2 * d + 2 * d) + (4 * w + 20 * w * d) := by ring
    _ = (30 * w * d + 9 * w) + (4 * w + 20 * w * d) := by
      rw [Nat.sub_add_cancel hle]
    _ = 50 * w * d + 13 * w := by ring

/-- The selector count is bounded by an explicit quadratic polynomial in the
binary-independent parameters `w,d`. -/
theorem selectorColumns_polynomial (w d : ℕ) :
    selectorColumns w d ≤ 24 * (w + d + 1) ^ 2 := by
  unfold selectorColumns sourceSelectorColumns gateSelectorColumns
  nlinarith [Nat.zero_le w, Nat.zero_le d]

/-- The ambient dimension is bounded by an explicit quadratic polynomial. -/
theorem rowCount_polynomial (w d : ℕ) :
    rowCount w d ≤ 39 * (w + d + 1) ^ 2 := by
  rw [rowCount_expanded]
  have hs : w - 1 ≤ w := Nat.sub_le w 1
  have hmul : 2 * d * (w - 1) ≤ 2 * d * w :=
    Nat.mul_le_mul_left (2 * d) hs
  nlinarith [Nat.zero_le w, Nat.zero_le d]

/-- Consequently the complete systematic matrix has polynomially many
columns.  This is a dimension bound, not a bound on its CVP gap. -/
theorem systematicColumns_polynomial (w d : ℕ) :
    systematicColumns w d ≤ 63 * (w + d + 1) ^ 2 := by
  unfold systematicColumns
  calc
    rowCount w d + selectorColumns w d ≤
        39 * (w + d + 1) ^ 2 + 24 * (w + d + 1) ^ 2 :=
      Nat.add_le_add (rowCount_polynomial w d) (selectorColumns_polynomial w d)
    _ = 63 * (w + d + 1) ^ 2 := by ring

/-- A strict chain of `h` gates has nodes numbered `0,...,h`.  It fits into a
`d`-gate-stage layered topology exactly when these node numbers can be used as
stage numbers.  This predicate isolates the order-preserving shallow-depth
blocker found in the finite frozen artifacts. -/
def ChainFits (h d : ℕ) : Prop :=
  ∃ stage : Fin (h + 1) → Fin (d + 1),
    ∀ i, (stage i).val = i.val

/-- Choosing at least as many gate stages as the chain depth gives the
canonical order-preserving stage placement. -/
theorem chainFits_of_le (h d : ℕ) (hd : h ≤ d) : ChainFits h d := by
  refine ⟨fun i => ⟨i.val, by omega⟩, ?_⟩
  intro i
  rfl

/-- Conversely, a placement that preserves the stage numbers forces enough
physical depth. -/
theorem le_of_chainFits (h d : ℕ) (fit : ChainFits h d) : h ≤ d := by
  rcases fit with ⟨stage, hstage⟩
  let last : Fin (h + 1) := ⟨h, by omega⟩
  have hv : (stage last).val = h := hstage last
  have hb := (stage last).isLt
  omega

/-- Exact characterization of the former shallow-chain obstruction. -/
theorem chainFits_iff (h d : ℕ) : ChainFits h d ↔ h ≤ d := by
  constructor
  · exact le_of_chainFits h d
  · exact chainFits_of_le h d

/-- The canonical placement advances every chain edge by exactly one layer. -/
theorem canonical_chain_advances (h d : ℕ) (hd : h ≤ d) :
    ∃ stage : Fin (h + 1) → Fin (d + 1),
      (∀ i, (stage i).val = i.val) ∧
      ∀ i : Fin h,
        (stage ⟨i.val + 1, by omega⟩).val =
          (stage ⟨i.val, by omega⟩).val + 1 := by
  refine ⟨fun i => ⟨i.val, by omega⟩, ?_, ?_⟩
  · intro i
    rfl
  · intro i
    rfl

end VerifyU0aSerializerDimensions
