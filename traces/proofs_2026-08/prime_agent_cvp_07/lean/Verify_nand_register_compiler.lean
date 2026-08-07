import Mathlib

/-!
An abstract fresh-register bridge for the NAND formula compiler.

This file deliberately stops before butterfly routing or CVP serialization.  It
proves a machine-independent SSA trace: every syntax node is assigned one
fresh consecutive register, operands are older than their destination, and
execution computes the recursive Boolean semantics without changing registers
outside the allocated interval.  A COPY instruction and its fresh-register
extension theorem are included because physical routing replaces logical
fanout by copies.
-/

namespace VerifyNandRegisterCompiler

/-- Binary NAND formulas; repeated variable names share one assignment. -/
inductive Formula (Var : Type*) where
  | var : Var → Formula Var
  | nand : Formula Var → Formula Var → Formula Var
  deriving Repr, DecidableEq

def nandBit (a b : Bool) : Bool := !(a && b)

def Formula.eval {Var : Type*} (assignment : Var → Bool) : Formula Var → Bool
  | .var x => assignment x
  | .nand left right => nandBit (left.eval assignment) (right.eval assignment)

def Formula.nodes {Var : Type*} : Formula Var → ℕ
  | .var _ => 1
  | .nand left right => left.nodes + right.nodes + 1

/-- Abstract register instructions.  `load` reads the one global assignment;
`copy` is the logical token-fanout primitive; and `nand` is the gate primitive. -/
inductive RegInstr (Var : Type*) where
  | load : (dst : ℕ) → Var → RegInstr Var
  | copy : (dst src : ℕ) → RegInstr Var
  | nand : (dst left right : ℕ) → RegInstr Var
  deriving Repr, DecidableEq

/-- The uniquely written register of an instruction. -/
def RegInstr.dst {Var : Type*} : RegInstr Var → ℕ
  | .load dst _ => dst
  | .copy dst _ => dst
  | .nand dst _ _ => dst

/-- Registers read from the current register file. -/
def RegInstr.inputs {Var : Type*} : RegInstr Var → List ℕ
  | .load _ _ => []
  | .copy _ src => [src]
  | .nand _ left right => [left, right]

abbrev RegFile := ℕ → Bool

/-- Total semantics of one abstract register instruction. -/
def regStep {Var : Type*} (assignment : Var → Bool)
    (regs : RegFile) : RegInstr Var → RegFile
  | .load dst x => Function.update regs dst (assignment x)
  | .copy dst src => Function.update regs dst (regs src)
  | .nand dst left right =>
      Function.update regs dst (nandBit (regs left) (regs right))

/-- Straight-line execution. -/
def regRun {Var : Type*} (assignment : Var → Bool)
    (code : List (RegInstr Var)) (regs : RegFile) : RegFile :=
  code.foldl (regStep assignment) regs

lemma regRun_append {Var : Type*} (assignment : Var → Bool)
    (first second : List (RegInstr Var)) (regs : RegFile) :
    regRun assignment (first ++ second) regs =
      regRun assignment second (regRun assignment first regs) := by
  simp [regRun, List.foldl_append]

/-- Canonical postorder SSA compilation beginning at register `base`.
The root is always the last allocated register. -/
def compileRegsAt {Var : Type*} : Formula Var → ℕ → List (RegInstr Var)
  | .var x, base => [.load base x]
  | .nand left right, base =>
      compileRegsAt left base ++
      compileRegsAt right (base + left.nodes) ++
      [.nand (base + left.nodes + right.nodes)
        (base + left.nodes - 1)
        (base + left.nodes + right.nodes - 1)]

/-- Register containing the result of a nonempty compiled formula interval. -/
def rootReg {Var : Type*} (formula : Formula Var) (base : ℕ) : ℕ :=
  base + formula.nodes - 1

/-- The compiler emits one abstract operation per syntax node. -/
theorem compileRegsAt_length {Var : Type*} (formula : Formula Var) (base : ℕ) :
    (compileRegsAt formula base).length = formula.nodes := by
  induction formula generalizing base with
  | var x => rfl
  | nand left right ihLeft ihRight =>
      simp [compileRegsAt, Formula.nodes, ihLeft, ihRight, Nat.add_assoc]

lemma map_add_range (base m n : ℕ) :
    (List.range (m + n)).map (base + ·) =
      (List.range m).map (base + ·) ++
      (List.range n).map (base + m + ·) := by
  rw [List.range_add, List.map_append, List.map_map]
  apply congrArg₂ (· ++ ·) rfl
  apply List.map_congr_left
  intro x hx
  dsimp
  omega

/-- Exact postorder destination trace: consecutive fresh registers. -/
theorem compileRegsAt_dsts {Var : Type*} (formula : Formula Var) (base : ℕ) :
    (compileRegsAt formula base).map RegInstr.dst =
      (List.range formula.nodes).map (base + ·) := by
  induction formula generalizing base with
  | var x => simp [compileRegsAt, Formula.nodes, RegInstr.dst]
  | nand left right ihLeft ihRight =>
      rw [compileRegsAt, List.map_append, List.map_append, ihLeft, ihRight]
      simp only [List.map_singleton, RegInstr.dst, Formula.nodes]
      rw [show left.nodes + right.nodes + 1 =
          (left.nodes + right.nodes) + 1 by omega,
        map_add_range base (left.nodes + right.nodes) 1,
        map_add_range base left.nodes right.nodes]
      simp
      omega

/-- Destination registers are pairwise distinct. -/
theorem compileRegsAt_dsts_nodup {Var : Type*}
    (formula : Formula Var) (base : ℕ) :
    ((compileRegsAt formula base).map RegInstr.dst).Nodup := by
  rw [compileRegsAt_dsts]
  exact List.Nodup.map (by
    intro a b h
    change base + a = base + b at h
    omega) List.nodup_range

/-- Every write lies in the half-open allocation interval. -/
theorem dst_mem_interval {Var : Type*} {formula : Formula Var} {base d : ℕ}
    (hd : d ∈ (compileRegsAt formula base).map RegInstr.dst) :
    base ≤ d ∧ d < base + formula.nodes := by
  rw [compileRegsAt_dsts] at hd
  simp only [List.mem_map, List.mem_range] at hd
  obtain ⟨i, hi, rfl⟩ := hd
  omega

/-- One instruction preserves every register except its destination. -/
lemma regStep_of_ne_dst {Var : Type*} (assignment : Var → Bool)
    (regs : RegFile) (instr : RegInstr Var) {r : ℕ}
    (hr : r ≠ instr.dst) : regStep assignment regs instr r = regs r := by
  cases instr <;> simp_all [regStep, RegInstr.dst, Function.update]

/-- A trace cannot change a register absent from its destination list. -/
theorem regRun_of_not_mem_dsts {Var : Type*} (assignment : Var → Bool)
    (code : List (RegInstr Var)) (regs : RegFile) {r : ℕ}
    (hr : r ∉ code.map RegInstr.dst) :
    regRun assignment code regs r = regs r := by
  induction code generalizing regs with
  | nil => rfl
  | cons instr code ih =>
      simp only [regRun, List.foldl_cons]
      change regRun assignment code (regStep assignment regs instr) r = regs r
      rw [ih]
      · apply regStep_of_ne_dst assignment regs instr
        intro heq
        apply hr
        simp [heq]
      · intro hmem
        apply hr
        simp [hmem]

/-- Compiled execution leaves all registers below the fresh base unchanged. -/
theorem compileRegsAt_preserves_below {Var : Type*}
    (formula : Formula Var) (base : ℕ) (assignment : Var → Bool)
    (regs : RegFile) {r : ℕ} (hr : r < base) :
    regRun assignment (compileRegsAt formula base) regs r = regs r := by
  apply regRun_of_not_mem_dsts
  rw [compileRegsAt_dsts]
  simp only [List.mem_map, List.mem_range, not_exists, not_and]
  intro i hi
  omega

/-- Compiled execution also leaves all registers above its interval unchanged. -/
theorem compileRegsAt_preserves_above {Var : Type*}
    (formula : Formula Var) (base : ℕ) (assignment : Var → Bool)
    (regs : RegFile) {r : ℕ} (hr : base + formula.nodes ≤ r) :
    regRun assignment (compileRegsAt formula base) regs r = regs r := by
  apply regRun_of_not_mem_dsts
  rw [compileRegsAt_dsts]
  simp only [List.mem_map, List.mem_range, not_exists, not_and]
  intro i hi
  omega

/-- Universal correctness of the fresh-register compiler. -/
theorem compileRegsAt_correct {Var : Type*} (formula : Formula Var)
    (base : ℕ) (assignment : Var → Bool) (regs : RegFile) :
    regRun assignment (compileRegsAt formula base) regs
      (rootReg formula base) = formula.eval assignment := by
  induction formula generalizing base regs with
  | var x => simp [compileRegsAt, regRun, regStep, rootReg, Formula.nodes,
      Formula.eval, Function.update]
  | nand left right ihLeft ihRight =>
      have hln : 0 < left.nodes := by cases left <;> simp [Formula.nodes]
      have hrn : 0 < right.nodes := by cases right <;> simp [Formula.nodes]
      rw [compileRegsAt, regRun_append, regRun_append]
      let afterLeft := regRun assignment (compileRegsAt left base) regs
      let rightBase := base + left.nodes
      let afterRight := regRun assignment (compileRegsAt right rightBase) afterLeft
      have hleft : afterRight (rootReg left base) = left.eval assignment := by
        have hp := compileRegsAt_preserves_below right rightBase assignment afterLeft
          (r := rootReg left base) (by simp [rightBase, rootReg]; omega)
        dsimp [afterRight]
        rw [hp]
        exact ihLeft base regs
      have hright : afterRight (rootReg right rightBase) = right.eval assignment := by
        exact ihRight rightBase afterLeft
      change regRun assignment
        [.nand (base + left.nodes + right.nodes)
          (base + left.nodes - 1)
          (base + left.nodes + right.nodes - 1)] afterRight
        (rootReg (.nand left right) base) = _
      simp only [regRun, List.foldl_cons, List.foldl_nil, regStep]
      simp only [rootReg, Formula.nodes, Formula.eval]
      have hroot : base + (left.nodes + right.nodes + 1) - 1 =
          base + left.nodes + right.nodes := by omega
      rw [hroot, Function.update_self]
      change nandBit
          (afterRight (rootReg left base))
          (afterRight (rootReg right rightBase)) =
        nandBit (left.eval assignment) (right.eval assignment)
      rw [hleft, hright]

/-- Every operand of generated NAND code is an older allocated register.
Loads have no register operands; canonical compilation itself emits no COPY. -/
theorem compileRegsAt_inputs_older {Var : Type*} (formula : Formula Var)
    (base : ℕ) (instr : RegInstr Var)
    (hi : instr ∈ compileRegsAt formula base) (r : ℕ)
    (hr : r ∈ instr.inputs) : base ≤ r ∧ r < instr.dst := by
  induction formula generalizing base instr r with
  | var x =>
      simp [compileRegsAt] at hi
      subst instr
      simp [RegInstr.inputs] at hr
  | nand left right ihLeft ihRight =>
      simp only [compileRegsAt, List.mem_append, List.mem_singleton] at hi
      rcases hi with (hi | hi) | hi
      · exact ihLeft base instr hi r hr
      · exact ihRight (base + left.nodes) instr hi r hr |>.imp (by omega) id
      · subst instr
        simp [RegInstr.inputs] at hr
        have hln : 0 < left.nodes := by cases left <;> simp [Formula.nodes]
        have hrn : 0 < right.nodes := by cases right <;> simp [Formula.nodes]
        rcases hr with rfl | rfl <;>
          simp only [RegInstr.dst] <;> omega

/-- LOAD reads the global assignment into its destination. -/
theorem load_correct {Var : Type*} (assignment : Var → Bool)
    (regs : RegFile) (dst : ℕ) (x : Var) :
    regRun assignment [.load dst x] regs dst = assignment x := by
  simp [regRun, regStep]

/-- Appending a COPY into the next fresh register preserves the source token
and places the same value at the new destination. -/
theorem fresh_copy_correct {Var : Type*} (assignment : Var → Bool)
    (regs : RegFile) (fresh src : ℕ) (h : src < fresh) :
    let regs' := regRun assignment [.copy fresh src] regs
    regs' fresh = regs src ∧ regs' src = regs src := by
  simp [regRun, regStep, Function.update, h.ne]

/-- Appending a NAND into a fresh register computes NAND and preserves both
older operands. -/
theorem fresh_nand_correct {Var : Type*} (assignment : Var → Bool)
    (regs : RegFile) (fresh left right : ℕ)
    (hl : left < fresh) (hr : right < fresh) :
    let regs' := regRun assignment [.nand fresh left right] regs
    regs' fresh = nandBit (regs left) (regs right) ∧
      regs' left = regs left ∧ regs' right = regs right := by
  simp [regRun, regStep, Function.update, hl.ne, hr.ne]

end VerifyNandRegisterCompiler
