import Mathlib

/-!
A universal semantic kernel for a postorder NAND-formula compiler.

This file deliberately proves only formula evaluation and straight-line
postorder execution.  It does not formalize butterfly routing, register
placement, CVP rows, energy, or signed soundness.
-/

namespace VerifyNandFormulaCompiler

/-- Binary NAND formulas.  A variable name may occur at any number of leaves. -/
inductive Formula (Var : Type*) where
  | var : Var → Formula Var
  | nand : Formula Var → Formula Var → Formula Var
  deriving Repr, DecidableEq

/-- Boolean NAND. -/
def nandBit (a b : Bool) : Bool := !(a && b)

/-- Recursive formula semantics under one global variable assignment. -/
def Formula.eval {Var : Type*} (assignment : Var → Bool) : Formula Var → Bool
  | .var x => assignment x
  | .nand left right => nandBit (left.eval assignment) (right.eval assignment)

/-- Postorder stack-machine instructions.  `read x` reads the unique global
assignment at every occurrence of `x`; `nand` consumes the top two values. -/
inductive Instr (Var : Type*) where
  | read : Var → Instr Var
  | nand : Instr Var
  deriving Repr, DecidableEq

/-- One total machine step.  The underflow branch is irrelevant to compiled
programs, but makes execution a total function. -/
def step {Var : Type*} (assignment : Var → Bool) :
    List Bool → Instr Var → List Bool
  | stack, .read x => assignment x :: stack
  | b :: a :: stack, .nand => nandBit a b :: stack
  | stack, .nand => stack

/-- Execute a straight-line instruction list from the supplied stack. -/
def run {Var : Type*} (assignment : Var → Bool)
    (code : List (Instr Var)) (stack : List Bool) : List Bool :=
  code.foldl (step assignment) stack

/-- Canonical postorder compilation. -/
def compile {Var : Type*} : Formula Var → List (Instr Var)
  | .var x => [.read x]
  | .nand left right => compile left ++ compile right ++ [.nand]

lemma run_append {Var : Type*} (assignment : Var → Bool)
    (first second : List (Instr Var)) (stack : List Bool) :
    run assignment (first ++ second) stack =
      run assignment second (run assignment first stack) := by
  simp [run, List.foldl_append]

/-- Universal compiler correctness, strengthened to an arbitrary preexisting
stack.  Thus every formula contributes exactly its recursive value on top. -/
theorem compile_correct {Var : Type*} (formula : Formula Var)
    (assignment : Var → Bool) (stack : List Bool) :
    run assignment (compile formula) stack = formula.eval assignment :: stack := by
  induction formula generalizing stack with
  | var x => simp [compile, run, step, Formula.eval]
  | nand left right ihLeft ihRight =>
      rw [compile, run_append, run_append, ihLeft, ihRight]
      rfl

/-- In particular, execution from an empty stack returns exactly one bit. -/
theorem compile_correct_empty {Var : Type*} (formula : Formula Var)
    (assignment : Var → Bool) :
    run assignment (compile formula) [] = [formula.eval assignment] := by
  simpa using compile_correct formula assignment []

/-- An explicit fanout/repeated-variable instance.  Both generated reads use
exactly the same value `assignment x`, rather than independent leaf values. -/
theorem repeated_variable_shares_assignment {Var : Type*} (x : Var)
    (assignment : Var → Bool) (stack : List Bool) :
    run assignment (compile (.nand (.var x) (.var x))) stack =
      nandBit (assignment x) (assignment x) :: stack := by
  simpa [Formula.eval] using
    (compile_correct (.nand (.var x) (.var x)) assignment stack)

/-- A compiled assertion consists only of formula-dependent code and one
requested root bit.  In particular, no assignment is stored in the target. -/
structure AssertionProgram (Var : Type*) where
  code : List (Instr Var)
  rootTarget : Bool
  deriving Repr, DecidableEq

/-- Compile a formula against a fixed desired root bit. -/
def compileAssertion {Var : Type*} (formula : Formula Var)
    (desired : Bool) : AssertionProgram Var :=
  ⟨compile formula, desired⟩

/-- The root assertion target is literally the requested bit and therefore is
independent of the assignment used later to execute the program. -/
theorem compileAssertion_fixed_target {Var : Type*} (formula : Formula Var)
    (desired : Bool) :
    (compileAssertion formula desired).rootTarget = desired := rfl

/-- Correctness of the fixed root assertion: the compiled execution hits its
assignment-independent target exactly when recursive evaluation does. -/
theorem compileAssertion_hits_target_iff {Var : Type*} (formula : Formula Var)
    (assignment : Var → Bool) (desired : Bool) :
    run assignment (compileAssertion formula desired).code [] =
        [(compileAssertion formula desired).rootTarget] ↔
      formula.eval assignment = desired := by
  change run assignment (compile formula) [] = [desired] ↔
    formula.eval assignment = desired
  rw [compile_correct_empty]
  simp

/-- Number of syntax nodes (variable occurrences plus NAND gates). -/
def Formula.nodes {Var : Type*} : Formula Var → ℕ
  | .var _ => 1
  | .nand left right => left.nodes + right.nodes + 1

/-- Canonical postorder compilation emits exactly one instruction per syntax
node, hence is linear in the encoded formula tree. -/
theorem compile_length {Var : Type*} (formula : Formula Var) :
    (compile formula).length = formula.nodes := by
  induction formula with
  | var x => rfl
  | nand left right ihLeft ihRight =>
      simp [compile, Formula.nodes, ihLeft, ihRight, Nat.add_assoc]

end VerifyNandFormulaCompiler
