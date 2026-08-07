import Mathlib

/-!
A semantic bridge for the sparse butterfly program.

This file models only honest Boolean lane evaluation.  At a stage, port `A`
reads the lane with the same name and port `B` reads its butterfly neighbor.
The local mode table is exactly `COPY_A`, `COPY_B`, `NAND`, `ZERO`, `ONE`.
We prove that the mode patterns emitted for SWAP, DUPLICATE, NAND-with-cleanup,
WAIT/padding, and final cleanup have their advertised lane semantics.  We also
compose the local result over an arbitrary valid scheduled event trace, then
define a smart XOR-edge schedule whose generated traces are valid by
construction.

The results do not connect this Lean datatype to the Python serializer, prove
finite-width lane bounds, or assert anything about Euclidean energy, malformed
integer selectors, CVP soundness, an approximation factor, or polynomial-size
compilation.
-/

namespace VerifyButterflyLaneSemantics

abbrev Lane := ℕ
abbrev LaneState := Lane → Bool

/-- The five gate modes in the serializer, in its canonical order. -/
inductive GateMode where
  | COPY_A | COPY_B | NAND | ZERO | ONE
  deriving Repr, DecidableEq

/-- Truth semantics printed in the serialized manifest. -/
def GateMode.eval : GateMode → Bool → Bool → Bool
  | .COPY_A, a, _ => a
  | .COPY_B, _, b => b
  | .NAND, a, b => !(a && b)
  | .ZERO, _, _ => false
  | .ONE, _, _ => true

/-- The Boolean NAND operation used by the formula and register compilers. -/
def nandBit (a b : Bool) : Bool := !(a && b)

@[simp] theorem eval_copyA (a b : Bool) : GateMode.eval .COPY_A a b = a := rfl
@[simp] theorem eval_copyB (a b : Bool) : GateMode.eval .COPY_B a b = b := rfl
@[simp] theorem eval_nand (a b : Bool) : GateMode.eval .NAND a b = nandBit a b := rfl
@[simp] theorem eval_zero (a b : Bool) : GateMode.eval .ZERO a b = false := rfl
@[simp] theorem eval_one (a b : Bool) : GateMode.eval .ONE a b = true := rfl

/-- A butterfly stage evaluates every lane from its same-lane `A` parent and
its neighbor `B` parent. -/
def evalStage (neighbor : Lane → Lane) (modes : Lane → GateMode)
    (before : LaneState) : LaneState :=
  fun lane => (modes lane).eval (before lane) (before (neighbor lane))

/-- The actual (unbounded) XOR neighbor underlying a dimension-`d` butterfly
stage.  Restricting to a power-of-two lane interval is done by the serializer. -/
def butterflyNeighbor (offset lane : ℕ) : ℕ := lane ^^^ offset

/-- XOR by a fixed offset is an involution.  In particular, a B edge can be
traversed in either direction. -/
theorem butterflyNeighbor_involutive (offset : ℕ) :
    Function.Involutive (butterflyNeighbor offset) := by
  intro lane
  simp [butterflyNeighbor]

/-- At physical dimension `d`, the neighbor is XOR by `2^d`. -/
def dimensionNeighbor (d : ℕ) : Lane → Lane := butterflyNeighbor (2 ^ d)

theorem dimensionNeighbor_involutive (d : ℕ) :
    Function.Involutive (dimensionNeighbor d) :=
  butterflyNeighbor_involutive (2 ^ d)

/-- A stage whose cells are all `COPY_A` is an identity stage.  This is the
semantics of both WAIT events and pre-cleanup padding. -/
theorem copyA_stage_identity (neighbor : Lane → Lane) (before : LaneState) :
    evalStage neighbor (fun _ => .COPY_A) before = before := by
  funext lane
  rfl

/-- Local modes for each sparse compiler event.  The source of DUPLICATE is
left at the default `COPY_A`; NAND writes its first lane and zeroes the second.
Cleanup is structurally different: its default is `ZERO`. -/
inductive Event where
  | wait
  | swap (a b : Lane)
  | duplicate (source destination : Lane)
  | nandZero (output consumed : Lane)
  | cleanup (root : Lane)
  deriving Repr, DecidableEq

def Event.modes : Event → Lane → GateMode
  | .wait, _ => .COPY_A
  | .swap a b, lane => if lane = a ∨ lane = b then .COPY_B else .COPY_A
  | .duplicate _ destination, lane =>
      if lane = destination then .COPY_B else .COPY_A
  | .nandZero output consumed, lane =>
      if lane = output then .NAND
      else if lane = consumed then .ZERO
      else .COPY_A
  | .cleanup root, lane => if lane = root then .COPY_A else .ZERO

/-- Abstract lane effect advertised by an event.  Unlike `Event.modes`, this
function does not mention physical B ports. -/
def Event.logicalStep : Event → LaneState → LaneState
  | .wait, before => before
  | .swap a b, before => fun lane =>
      if lane = a then before b else if lane = b then before a else before lane
  | .duplicate source destination, before => fun lane =>
      if lane = destination then before source else before lane
  | .nandZero output consumed, before => fun lane =>
      if lane = output then nandBit (before output) (before consumed)
      else if lane = consumed then false else before lane
  | .cleanup root, before => fun lane =>
      if lane = root then before root else false

/-- The adjacency and distinctness obligations checked by the scheduler.
WAIT and cleanup do not use their B inputs. -/
def Event.Valid (neighbor : Lane → Lane) : Event → Prop
  | .wait => True
  | .swap a b => a ≠ b ∧ neighbor a = b
  | .duplicate source destination => source ≠ destination ∧ neighbor destination = source
  | .nandZero output consumed => output ≠ consumed ∧ neighbor output = consumed
  | .cleanup _ => True

/-- An involutive neighbor plus the one directed adjacency check gives the
reverse adjacency used by the second endpoint of a SWAP. -/
theorem reverse_neighbor {neighbor : Lane → Lane}
    (hinv : Function.Involutive neighbor) {a b : Lane}
    (hab : neighbor a = b) : neighbor b = a := by
  rw [← hab, hinv a]

/-- SWAP: putting `COPY_B` at both endpoints exchanges their bits and leaves
all other lanes unchanged. -/
theorem swap_stage (neighbor : Lane → Lane)
    (hinv : Function.Involutive neighbor) (before : LaneState)
    {a b : Lane} (hne : a ≠ b) (hab : neighbor a = b) :
    evalStage neighbor (Event.modes (.swap a b)) before =
      Event.logicalStep (.swap a b) before := by
  have hba : neighbor b = a := reverse_neighbor hinv hab
  funext lane
  by_cases ha : lane = a
  · subst lane
    simp [evalStage, Event.modes, Event.logicalStep, hne, hab]
  · by_cases hb : lane = b
    · subst lane
      have hne' : b ≠ a := Ne.symm hne
      simp [evalStage, Event.modes, Event.logicalStep, hne', hba]
    · simp [evalStage, Event.modes, Event.logicalStep, ha, hb]

/-- DUPLICATE: the destination reads its adjacent source through port B; every
other lane, including the source, retains its old value. -/
theorem duplicate_stage (neighbor : Lane → Lane) (before : LaneState)
    {source destination : Lane} (hadj : neighbor destination = source) :
    evalStage neighbor (Event.modes (.duplicate source destination)) before =
      Event.logicalStep (.duplicate source destination) before := by
  funext lane
  by_cases h : lane = destination
  · subst lane
    simp [evalStage, Event.modes, Event.logicalStep, hadj]
  · simp [evalStage, Event.modes, Event.logicalStep, h]

/-- NAND+ZERO: the output lane reads the consumed adjacent lane as its B input,
while the consumed lane is reset to zero.  Every other lane is copied. -/
theorem nandZero_stage (neighbor : Lane → Lane) (before : LaneState)
    {output consumed : Lane} (_hne : output ≠ consumed)
    (hadj : neighbor output = consumed) :
    evalStage neighbor (Event.modes (.nandZero output consumed)) before =
      Event.logicalStep (.nandZero output consumed) before := by
  funext lane
  by_cases ho : lane = output
  · subst lane
    simp [evalStage, Event.modes, Event.logicalStep, hadj]
  · by_cases hc : lane = consumed
    · subst lane
      simp [evalStage, Event.modes, Event.logicalStep, ho]
    · simp [evalStage, Event.modes, Event.logicalStep, ho, hc]

/-- WAIT and padding are genuine identity stages, independently of the current
butterfly dimension. -/
theorem wait_stage (neighbor : Lane → Lane) (before : LaneState) :
    evalStage neighbor (Event.modes .wait) before =
      Event.logicalStep .wait before := by
  exact copyA_stage_identity neighbor before

/-- Final cleanup retains precisely the root lane and sets every other lane to
zero.  It is independent of the neighbor schedule. -/
theorem cleanup_stage (neighbor : Lane → Lane) (before : LaneState)
    (root : Lane) :
    evalStage neighbor (Event.modes (.cleanup root)) before =
      Event.logicalStep (.cleanup root) before := by
  funext lane
  by_cases h : lane = root
  · subst lane
    simp [evalStage, Event.modes, Event.logicalStep]
  · simp [evalStage, Event.modes, Event.logicalStep, h]

@[simp] theorem cleanup_root (before : LaneState) (root : Lane) :
    Event.logicalStep (.cleanup root) before root = before root := by
  simp [Event.logicalStep]

@[simp] theorem cleanup_other (before : LaneState) {root lane : Lane}
    (h : lane ≠ root) :
    Event.logicalStep (.cleanup root) before lane = false := by
  simp [Event.logicalStep, h]

/-- ONE is not used by the listed routing events, but its local serializer
semantics is constant true. -/
theorem one_cell (neighbor : Lane → Lane) (before : LaneState) (lane : Lane) :
    evalStage neighbor (fun i => if i = lane then .ONE else .COPY_A) before lane = true := by
  simp [evalStage]

/-- A scheduled event remembers the physical neighbor map of its stage. -/
structure ScheduledEvent where
  neighbor : Lane → Lane
  event : Event

/-- Exact condition under which the physical mode stage realizes the abstract
lane event. -/
def ScheduledEvent.Valid (scheduled : ScheduledEvent) : Prop :=
  Function.Involutive scheduled.neighbor ∧ scheduled.event.Valid scheduled.neighbor

/-- Physical execution of one scheduled event. -/
def ScheduledEvent.physicalStep (scheduled : ScheduledEvent)
    (before : LaneState) : LaneState :=
  evalStage scheduled.neighbor scheduled.event.modes before

/-- Every locally valid scheduled event realizes its advertised lane effect. -/
theorem scheduledEvent_correct (scheduled : ScheduledEvent)
    (hvalid : scheduled.Valid) (before : LaneState) :
    scheduled.physicalStep before = scheduled.event.logicalStep before := by
  rcases scheduled with ⟨neighbor, event⟩
  rcases hvalid with ⟨hinv, hlocal⟩
  cases event with
  | wait => exact wait_stage neighbor before
  | swap a b =>
      exact swap_stage neighbor hinv before hlocal.1 hlocal.2
  | duplicate source destination =>
      exact duplicate_stage neighbor before hlocal.2
  | nandZero output consumed =>
      exact nandZero_stage neighbor before hlocal.1 hlocal.2
  | cleanup root => exact cleanup_stage neighbor before root

/-- Execute a physical stage trace in list order. -/
def runPhysical : List ScheduledEvent → LaneState → LaneState
  | [], before => before
  | scheduled :: rest, before =>
      runPhysical rest (scheduled.physicalStep before)

/-- Execute the corresponding abstract lane events in the same order. -/
def runLogical : List ScheduledEvent → LaneState → LaneState
  | [], before => before
  | scheduled :: rest, before =>
      runLogical rest (scheduled.event.logicalStep before)

/-- Induction bridge from all locally checked event stages to the complete
lane trace.  This is a token/lane semantic theorem, not a CVP soundness theorem. -/
theorem runPhysical_eq_runLogical (trace : List ScheduledEvent)
    (hvalid : ∀ scheduled ∈ trace, scheduled.Valid) (initial : LaneState) :
    runPhysical trace initial = runLogical trace initial := by
  induction trace generalizing initial with
  | nil => rfl
  | cons scheduled rest ih =>
      rw [runPhysical, runLogical,
        scheduledEvent_correct scheduled (hvalid scheduled (by simp)) initial]
      apply ih
      intro later hlater
      exact hvalid later (by simp [hlater])



/-! ## Valid-by-construction XOR schedules

The preceding trace theorem accepts arbitrary neighbor maps and therefore has
an explicit validity hypothesis.  The serializer, however, only schedules
edges of a physical butterfly dimension: an endpoint is paired with its XOR
neighbor.  `XorEvent` records just the free endpoint and dimension.  Its
`schedule` function fills in the other endpoint, so malformed non-adjacent
SWAP/DUPLICATE/NAND events are not representable by this interface.
-/

/-- XOR by a positive power of two never fixes a natural-number lane. -/
theorem dimensionNeighbor_ne (d lane : ℕ) :
    dimensionNeighbor d lane ≠ lane := by
  intro h
  have hx : lane ^^^ (2 ^ d) = lane ^^^ 0 := by
    simpa [dimensionNeighbor, butterflyNeighbor] using h
  have hz : 2 ^ d = 0 := Nat.xor_right_inj.mp hx
  exact (Nat.two_pow_pos d).ne' hz

/-- A smart event for the actual XOR edge at dimension `d`.  For DUPLICATE the
stored lane is the destination; for NAND it is the output.  The required
source/consumed endpoint is generated as its XOR neighbor. -/
inductive XorEvent where
  | wait (d : ℕ)
  | swap (d lane : ℕ)
  | duplicate (d destination : ℕ)
  | nandZero (d output : ℕ)
  | cleanup (d root : ℕ)
  deriving Repr, DecidableEq

/-- Elaborate a smart XOR event into the general scheduled-event interface. -/
def XorEvent.schedule : XorEvent → ScheduledEvent
  | .wait d => ⟨dimensionNeighbor d, .wait⟩
  | .swap d lane =>
      ⟨dimensionNeighbor d, .swap lane (dimensionNeighbor d lane)⟩
  | .duplicate d destination =>
      ⟨dimensionNeighbor d,
        .duplicate (dimensionNeighbor d destination) destination⟩
  | .nandZero d output =>
      ⟨dimensionNeighbor d, .nandZero output (dimensionNeighbor d output)⟩
  | .cleanup d root => ⟨dimensionNeighbor d, .cleanup root⟩

/-- Every event generated by `XorEvent.schedule` satisfies all adjacency,
distinctness, and involution obligations of `ScheduledEvent.Valid`. -/
theorem XorEvent.schedule_valid (event : XorEvent) :
    event.schedule.Valid := by
  cases event with
  | wait d =>
      exact ⟨dimensionNeighbor_involutive d, trivial⟩
  | swap d lane =>
      refine ⟨dimensionNeighbor_involutive d, ?_, rfl⟩
      exact (dimensionNeighbor_ne d lane).symm
  | duplicate d destination =>
      refine ⟨dimensionNeighbor_involutive d, ?_, rfl⟩
      exact dimensionNeighbor_ne d destination
  | nandZero d output =>
      refine ⟨dimensionNeighbor_involutive d, ?_, rfl⟩
      exact (dimensionNeighbor_ne d output).symm
  | cleanup d root =>
      exact ⟨dimensionNeighbor_involutive d, trivial⟩

/-- Elaborate an entire smart trace. -/
def scheduleXorTrace (trace : List XorEvent) : List ScheduledEvent :=
  trace.map XorEvent.schedule

/-- Trace elaboration cannot introduce an invalid scheduled event. -/
theorem scheduleXorTrace_all_valid (trace : List XorEvent) :
    ∀ scheduled ∈ scheduleXorTrace trace, scheduled.Valid := by
  intro scheduled hmem
  simp only [scheduleXorTrace, List.mem_map] at hmem
  rcases hmem with ⟨event, _hevent, rfl⟩
  exact event.schedule_valid

/-- Consequently physical and abstract execution agree for every smart XOR
trace, with no conditional trace-validity premise left to discharge. -/
theorem run_scheduledXorTrace_correct (trace : List XorEvent)
    (initial : LaneState) :
    runPhysical (scheduleXorTrace trace) initial =
      runLogical (scheduleXorTrace trace) initial := by
  exact runPhysical_eq_runLogical (scheduleXorTrace trace)
    (scheduleXorTrace_all_valid trace) initial

end VerifyButterflyLaneSemantics
