import Mathlib

/-!
# Concrete token-map deltas for sparse butterfly events

This file formalizes only the snapshot-free token bookkeeping performed by a
v2-style event checker.  SWAP records the verifier-derived occupants of its
two endpoints (either may be empty), DUPLICATE records an existing source and
a fresh token, and NAND consumes two existing tokens and creates a fresh
output.  Explicit short `Change` lists are proved equal to the corresponding
logical token-map steps under exact occupancy, freeness, and distinctness
preconditions.  The local results are then composed into a snapshot-free
final-map theorem.

It does not formalize JSON parsing, checkpoint hashes, finite-width lane
bounds, generation of the event stream, Boolean lane values, or CVP claims.
-/

namespace VerifyConcreteEventDeltas

abbrev TokenMap (Token Lane : Type*) := Token → Option Lane

structure Change (Token Lane : Type*) where
  token : Token
  value : Option Lane

abbrev Delta (Token Lane : Type*) := List (Change Token Lane)

def applyChange {Token Lane : Type*} [DecidableEq Token]
    (before : TokenMap Token Lane) (change : Change Token Lane) :
    TokenMap Token Lane :=
  Function.update before change.token change.value

def applyDelta {Token Lane : Type*} [DecidableEq Token]
    (delta : Delta Token Lane) (before : TokenMap Token Lane) :
    TokenMap Token Lane :=
  delta.foldl applyChange before

@[simp] theorem applyDelta_nil {Token Lane : Type*} [DecidableEq Token]
    (before : TokenMap Token Lane) :
    applyDelta ([] : Delta Token Lane) before = before := rfl

@[simp] theorem applyDelta_cons {Token Lane : Type*} [DecidableEq Token]
    (change : Change Token Lane) (rest : Delta Token Lane)
    (before : TokenMap Token Lane) :
    applyDelta (change :: rest) before =
      applyDelta rest (applyChange before change) := rfl

/-- `advertised = some token` precisely when `token` occupies this lane. -/
def ExactOccupant (before : TokenMap Token Lane) (lane : Lane)
    (advertised : Option Token) : Prop :=
  ∀ token, before token = some lane ↔ advertised = some token

/-- No live token occupies `lane`. -/
def LaneFree (before : TokenMap Token Lane) (lane : Lane) : Prop :=
  ∀ token, before token ≠ some lane

inductive Event (Token Lane : Type*) where
  | wait
  | swap (a b : Lane) (atA atB : Option Token)
  | duplicate (source fresh : Token) (sourceLane destinationLane : Lane)
  | nand (left right output : Token) (leftLane rightLane : Lane)
  deriving Repr

/-- Logical token ownership effect, independent of the sparse encoding. -/
def Event.logicalStep [DecidableEq Token] [DecidableEq Lane] :
    Event Token Lane → TokenMap Token Lane → TokenMap Token Lane
  | .wait, before => before
  | .swap a b _ _, before => fun token =>
      match before token with
      | none => none
      | some lane =>
          if lane = a then some b else if lane = b then some a else some lane
  | .duplicate source fresh sourceLane destinationLane, before => fun token =>
      if token = source then some sourceLane
      else if token = fresh then some destinationLane else before token
  | .nand left right output leftLane _, before => fun token =>
      if token = output then some leftLane
      else if token = left then none
      else if token = right then none else before token

/-- The exact ordered sparse assignment list printed/derived for an event. -/
def Event.delta : Event Token Lane → Delta Token Lane
  | .wait => []
  | .swap _ _ none none => []
  | .swap _ b (some atA) none => [⟨atA, some b⟩]
  | .swap a _ none (some atB) => [⟨atB, some a⟩]
  | .swap a b (some atA) (some atB) =>
      [⟨atA, some b⟩, ⟨atB, some a⟩]
  | .duplicate _ fresh _ destinationLane => [⟨fresh, some destinationLane⟩]
  | .nand left right output leftLane _ =>
      [⟨left, none⟩, ⟨right, none⟩, ⟨output, some leftLane⟩]

/-- Preconditions independently checked from the verifier-owned current map. -/
def Event.Valid [DecidableEq Token] (before : TokenMap Token Lane) :
    Event Token Lane → Prop
  | .wait => True
  | .swap a b atA atB =>
      a ≠ b ∧ ExactOccupant before a atA ∧ ExactOccupant before b atB
  | .duplicate source fresh sourceLane destinationLane =>
      source ≠ fresh ∧ sourceLane ≠ destinationLane ∧
      ExactOccupant before sourceLane (some source) ∧
      before fresh = none ∧ LaneFree before destinationLane
  | .nand left right output leftLane rightLane =>
      left ≠ right ∧ left ≠ output ∧ right ≠ output ∧
      leftLane ≠ rightLane ∧
      ExactOccupant before leftLane (some left) ∧
      ExactOccupant before rightLane (some right) ∧ before output = none

@[simp] theorem wait_delta (before : TokenMap Token Lane) [DecidableEq Token]
    [DecidableEq Lane] :
    applyDelta (Event.delta (Event.wait : Event Token Lane)) before =
      Event.logicalStep .wait before := rfl

theorem swap_none_none [DecidableEq Token] [DecidableEq Lane]
    (before : TokenMap Token Lane) {a b : Lane}
    (ha : ExactOccupant before a none) (hb : ExactOccupant before b none) :
    applyDelta (Event.delta (Event.swap a b none none : Event Token Lane)) before =
      Event.logicalStep (.swap a b none none) before := by
  funext token
  have hna : before token ≠ some a := by
    intro h
    have := (ha token).mp h
    simp at this
  have hnb : before token ≠ some b := by
    intro h
    have := (hb token).mp h
    simp at this
  simp only [Event.delta, applyDelta_nil, Event.logicalStep]
  cases h : before token with
  | none => rfl
  | some lane =>
      have hla : lane ≠ a := by intro e; subst lane; exact hna h
      have hlb : lane ≠ b := by intro e; subst lane; exact hnb h
      simp [hla, hlb]

theorem swap_some_none [DecidableEq Token] [DecidableEq Lane]
    (before : TokenMap Token Lane) {a b : Lane} {atA : Token}
    (ha : ExactOccupant before a (some atA))
    (hb : ExactOccupant before b none) :
    applyDelta (Event.delta (Event.swap a b (some atA) none : Event Token Lane)) before =
      Event.logicalStep (.swap a b (some atA) none) before := by
  funext token
  by_cases ht : token = atA
  · subst token
    have hat : before atA = some a := (ha atA).mpr rfl
    simp [Event.delta, applyDelta, applyChange, Event.logicalStep, hat]
  · have hna : before token ≠ some a := by
      intro h
      have hs : (some atA : Option Token) = some token := (ha token).mp h
      simp at hs
      exact ht hs.symm
    have hnb : before token ≠ some b := by
      intro h
      have := (hb token).mp h
      simp at this
    simp only [Event.delta, applyDelta, List.foldl_cons, List.foldl_nil,
      applyChange, Event.logicalStep]
    rw [Function.update_of_ne ht]
    cases h : before token with
    | none => rfl
    | some lane =>
        have hla : lane ≠ a := by intro e; subst lane; exact hna h
        have hlb : lane ≠ b := by intro e; subst lane; exact hnb h
        simp [hla, hlb]

theorem swap_none_some [DecidableEq Token] [DecidableEq Lane]
    (before : TokenMap Token Lane) {a b : Lane} {atB : Token}
    (hab : a ≠ b) (ha : ExactOccupant before a none)
    (hb : ExactOccupant before b (some atB)) :
    applyDelta (Event.delta (Event.swap a b none (some atB) : Event Token Lane)) before =
      Event.logicalStep (.swap a b none (some atB)) before := by
  funext token
  by_cases ht : token = atB
  · subst token
    have hat : before atB = some b := (hb atB).mpr rfl
    simp [Event.delta, applyDelta, applyChange, Event.logicalStep, hat, Ne.symm hab]
  · have hna : before token ≠ some a := by
      intro h
      have := (ha token).mp h
      simp at this
    have hnb : before token ≠ some b := by
      intro h
      have hs : (some atB : Option Token) = some token := (hb token).mp h
      simp at hs
      exact ht hs.symm
    simp only [Event.delta, applyDelta, List.foldl_cons, List.foldl_nil,
      applyChange, Event.logicalStep]
    rw [Function.update_of_ne ht]
    cases h : before token with
    | none => rfl
    | some lane =>
        have hla : lane ≠ a := by intro e; subst lane; exact hna h
        have hlb : lane ≠ b := by intro e; subst lane; exact hnb h
        simp [hla, hlb]

theorem swap_some_some [DecidableEq Token] [DecidableEq Lane]
    (before : TokenMap Token Lane) {a b : Lane} {atA atB : Token}
    (hab : a ≠ b) (ha : ExactOccupant before a (some atA))
    (hb : ExactOccupant before b (some atB)) :
    applyDelta (Event.delta (Event.swap a b (some atA) (some atB) : Event Token Lane)) before =
      Event.logicalStep (.swap a b (some atA) (some atB)) before := by
  have htokens : atA ≠ atB := by
    intro h
    subst atB
    have h1 : before atA = some a := (ha atA).mpr rfl
    have h2 : before atA = some b := (hb atA).mpr rfl
    rw [h1] at h2
    exact hab (Option.some.inj h2)
  funext token
  by_cases hA : token = atA
  · subst token
    have hat : before atA = some a := (ha atA).mpr rfl
    simp [Event.delta, applyDelta, applyChange, Event.logicalStep, hat,
      htokens]
  · by_cases hB : token = atB
    · subst token
      have hat : before atB = some b := (hb atB).mpr rfl
      simp [Event.delta, applyDelta, applyChange, Event.logicalStep, hat,
        Ne.symm hab]
    · have hna : before token ≠ some a := by
        intro h
        have hs : (some atA : Option Token) = some token := (ha token).mp h
        simp at hs
        exact hA hs.symm
      have hnb : before token ≠ some b := by
        intro h
        have hs : (some atB : Option Token) = some token := (hb token).mp h
        simp at hs
        exact hB hs.symm
      simp only [Event.delta, applyDelta, List.foldl_cons, List.foldl_nil,
        applyChange, Event.logicalStep]
      rw [Function.update_of_ne hB, Function.update_of_ne hA]
      cases h : before token with
      | none => rfl
      | some lane =>
          have hla : lane ≠ a := by intro e; subst lane; exact hna h
          have hlb : lane ≠ b := by intro e; subst lane; exact hnb h
          simp [hla, hlb]

/-- Every concrete explicit delta realizes its advertised token transition. -/
theorem Event.delta_correct [DecidableEq Token] [DecidableEq Lane]
    (event : Event Token Lane) (before : TokenMap Token Lane)
    (hvalid : event.Valid before) :
    applyDelta event.delta before = event.logicalStep before := by
  cases event with
  | wait => rfl
  | swap a b atA atB =>
      rcases hvalid with ⟨hab, ha, hb⟩
      cases atA with
      | none =>
          cases atB with
          | none => exact swap_none_none before ha hb
          | some atB => exact swap_none_some before hab ha hb
      | some atA =>
          cases atB with
          | none => exact swap_some_none before ha hb
          | some atB => exact swap_some_some before hab ha hb
  | duplicate source fresh sourceLane destinationLane =>
      rcases hvalid with ⟨hsf, _hlanes, hsource, _hfresh, _hfree⟩
      have hs : before source = some sourceLane := (hsource source).mpr rfl
      funext token
      by_cases hsourceToken : token = source
      · subst token
        simp [Event.delta, applyDelta, applyChange, Event.logicalStep, hs,
          hsf]
      · by_cases hfreshToken : token = fresh
        · subst token
          simp [Event.delta, applyDelta, applyChange, Event.logicalStep,
            hsourceToken]
        · simp [Event.delta, applyDelta, applyChange, Event.logicalStep,
            hsourceToken, hfreshToken]
  | nand left right output leftLane rightLane =>
      rcases hvalid with
        ⟨hlr, hlo, hro, _hlanes, _hleft, _hright, _houtput⟩
      funext token
      by_cases hout : token = output
      · subst token
        simp [Event.delta, applyDelta, applyChange, Event.logicalStep]
      · by_cases hleft : token = left
        · subst token
          simp [Event.delta, applyDelta, applyChange, Event.logicalStep,
            hlo, hlr]
        · by_cases hright : token = right
          · subst token
            simp [Event.delta, applyDelta, applyChange, Event.logicalStep,
              hro]
          · simp [Event.delta, applyDelta, applyChange, Event.logicalStep,
              hout, hleft, hright]

/-- The one-write DUPLICATE list, displayed without the `Event.delta`
abbreviation, implements the logical transition. -/
theorem duplicate_changes_correct [DecidableEq Token] [DecidableEq Lane]
    (before : TokenMap Token Lane) (source fresh : Token)
    (sourceLane destinationLane : Lane)
    (hvalid : (Event.duplicate source fresh sourceLane destinationLane).Valid before) :
    applyDelta [⟨fresh, some destinationLane⟩] before =
      Event.logicalStep (.duplicate source fresh sourceLane destinationLane) before := by
  exact Event.delta_correct (.duplicate source fresh sourceLane destinationLane)
    before hvalid

/-- The ordered erase-left, erase-right, write-output NAND list implements the
logical consume/create transition. -/
theorem nand_changes_correct [DecidableEq Token] [DecidableEq Lane]
    (before : TokenMap Token Lane) (left right output : Token)
    (leftLane rightLane : Lane)
    (hvalid : (Event.nand left right output leftLane rightLane).Valid before) :
    applyDelta [⟨left, none⟩, ⟨right, none⟩, ⟨output, some leftLane⟩] before =
      Event.logicalStep (.nand left right output leftLane rightLane) before := by
  exact Event.delta_correct (.nand left right output leftLane rightLane)
    before hvalid

structure CertifiedEvent (Token Lane : Type*) where
  event : Event Token Lane
  delta : Delta Token Lane

/-- A concrete certificate binds the supplied delta to the canonical short
list, and checks event validity at the verifier-owned replay state. -/
def allConcreteTransitionsMatch [DecidableEq Token] :
    List (CertifiedEvent Token Lane) → TokenMap Token Lane → Prop
  | [], _ => True
  | certified :: rest, before =>
      certified.delta = certified.event.delta ∧
      certified.event.Valid before ∧
      allConcreteTransitionsMatch rest (applyDelta certified.delta before)

def replayDeltas [DecidableEq Token] :
    List (CertifiedEvent Token Lane) → TokenMap Token Lane → TokenMap Token Lane
  | [], before => before
  | certified :: rest, before =>
      replayDeltas rest (applyDelta certified.delta before)

def runLogical [DecidableEq Token] [DecidableEq Lane] :
    List (CertifiedEvent Token Lane) → TokenMap Token Lane → TokenMap Token Lane
  | [], before => before
  | certified :: rest, before =>
      runLogical rest (certified.event.logicalStep before)

/-- Concrete analogue of `Verify_event_delta_replay.replayDeltas_eq_runLogical`:
canonical local WAIT/SWAP/DUPLICATE/NAND deltas compose without snapshots. -/
theorem replayDeltas_eq_runLogical [DecidableEq Token] [DecidableEq Lane]
    (trace : List (CertifiedEvent Token Lane))
    (initial : TokenMap Token Lane)
    (hmatch : allConcreteTransitionsMatch trace initial) :
    replayDeltas trace initial = runLogical trace initial := by
  induction trace generalizing initial with
  | nil => rfl
  | cons certified rest ih =>
      rcases hmatch with ⟨hdelta, hvalid, htail⟩
      simp only [replayDeltas, runLogical]
      have hlocal : applyDelta certified.delta initial =
          certified.event.logicalStep initial := by
        rw [hdelta]
        exact certified.event.delta_correct initial hvalid
      rw [← hlocal]
      exact ih (applyDelta certified.delta initial) htail

structure TraceCertificate (Token Lane : Type*) where
  initial : TokenMap Token Lane
  events : List (CertifiedEvent Token Lane)
  claimedFinal : TokenMap Token Lane

def TraceCertificate.Valid [DecidableEq Token]
    (certificate : TraceCertificate Token Lane) : Prop :=
  allConcreteTransitionsMatch certificate.events certificate.initial ∧
  replayDeltas certificate.events certificate.initial = certificate.claimedFinal

/-- Final snapshot-free theorem: logical execution reaches the single claimed
final token map, and hence agrees with it at every token lookup. -/
theorem TraceCertificate.logicalFinal_eq [DecidableEq Token] [DecidableEq Lane]
    (certificate : TraceCertificate Token Lane)
    (hvalid : certificate.Valid) :
    runLogical certificate.events certificate.initial = certificate.claimedFinal := by
  rcases hvalid with ⟨htransitions, hfinal⟩
  rw [← hfinal]
  exact (replayDeltas_eq_runLogical certificate.events certificate.initial
    htransitions).symm

theorem TraceCertificate.logicalFinal_token [DecidableEq Token] [DecidableEq Lane]
    (certificate : TraceCertificate Token Lane)
    (hvalid : certificate.Valid) (token : Token) :
    runLogical certificate.events certificate.initial token =
      certificate.claimedFinal token := by
  rw [certificate.logicalFinal_eq hvalid]




/-! ## Global lane-occupancy and active-token invariants -/

/-- No two live tokens own the same lane.  This is the scheduler's global
occupancy invariant, stated without a finiteness assumption. -/
def OccupancyInjective (state : TokenMap Token Lane) : Prop :=
  ∀ ⦃first second : Token⦄ ⦃lane : Lane⦄,
    state first = some lane → state second = some lane → first = second

/-- A token is active exactly when its map entry is nonempty. -/
def Active (state : TokenMap Token Lane) (token : Token) : Prop :=
  state token ≠ none

/-- Erasing a token cannot create a lane collision. -/
theorem occupancyInjective_update_none [DecidableEq Token]
    {state : TokenMap Token Lane} (hinj : OccupancyInjective state) (erased : Token) :
    OccupancyInjective (Function.update state erased none) := by
  intro first second lane hfirst hsecond
  by_cases hf : first = erased
  · subst first; simp at hfirst
  · by_cases hs : second = erased
    · subst second; simp at hsecond
    · rw [Function.update_of_ne hf] at hfirst
      rw [Function.update_of_ne hs] at hsecond
      exact hinj hfirst hsecond

/-- Writing one token into a verifier-checked free lane preserves exclusive
ownership.  The token may be either fresh or moved from another lane. -/
theorem occupancyInjective_update_some [DecidableEq Token]
    {state : TokenMap Token Lane} (hinj : OccupancyInjective state)
    (token : Token) (lane : Lane) (hfree : LaneFree state lane) :
    OccupancyInjective (Function.update state token (some lane)) := by
  intro first second occupied hfirst hsecond
  by_cases hf : first = token
  · subst first
    simp at hfirst
    subst occupied
    by_cases hs : second = token
    · exact hs.symm
    · rw [Function.update_of_ne hs] at hsecond
      exact (hfree second hsecond).elim
  · rw [Function.update_of_ne hf] at hfirst
    by_cases hs : second = token
    · subst second
      simp at hsecond
      subst occupied
      exact (hfree first hfirst).elim
    · rw [Function.update_of_ne hs] at hsecond
      exact hinj hfirst hsecond

/-- Deleting the exact occupant makes its lane free. -/
theorem laneFree_update_exact_none [DecidableEq Token]
    {state : TokenMap Token Lane} {token : Token} {lane : Lane}
    (hexact : ExactOccupant state lane (some token)) :
    LaneFree (Function.update state token none) lane := by
  intro other hother
  by_cases h : other = token
  · subst other; simp at hother
  · rw [Function.update_of_ne h] at hother
    have hs : (some token : Option Token) = some other := (hexact other).mp hother
    exact h (Option.some.inj hs).symm

/-- The lane permutation used by SWAP. -/
def swapLane [DecidableEq Lane] (a b : Lane) (lane : Lane) : Lane :=
  if lane = a then b else if lane = b then a else lane

/-- Swapping distinct lanes is its own inverse. -/
theorem swapLane_involutive [DecidableEq Lane] {a b : Lane} (hab : a ≠ b)
    (lane : Lane) : swapLane a b (swapLane a b lane) = lane := by
  by_cases ha : lane = a
  · subst lane; simp [swapLane, hab, Ne.symm hab]
  · by_cases hb : lane = b
    · subst lane; simp [swapLane, hab, Ne.symm hab]
    · simp [swapLane, ha, hb]

 theorem swapLane_injective [DecidableEq Lane] {a b : Lane} (hab : a ≠ b) :
    Function.Injective (swapLane a b) := by
  intro x y h
  have := congrArg (swapLane a b) h
  simpa [swapLane_involutive hab] using this

/-- A valid WAIT/SWAP/DUPLICATE/NAND event preserves exclusive ownership of
physical lanes. -/
theorem Event.logicalStep_occupancyInjective [DecidableEq Token]
    [DecidableEq Lane] (event : Event Token Lane) (before : TokenMap Token Lane)
    (hinj : OccupancyInjective before) (hvalid : event.Valid before) :
    OccupancyInjective (event.logicalStep before) := by
  cases event with
  | wait => exact hinj
  | swap a b atA atB =>
      rcases hvalid with ⟨hab, _ha, _hb⟩
      intro first second lane hfirst hsecond
      simp only [Event.logicalStep] at hfirst hsecond
      cases hf : before first with
      | none => simp [hf] at hfirst
      | some firstLane =>
          simp only [hf] at hfirst
          cases hs : before second with
          | none => simp [hs] at hsecond
          | some secondLane =>
              simp only [hs] at hsecond
              have hfl : swapLane a b firstLane = lane := by
                by_cases hfa : firstLane = a
                · simpa [swapLane, hfa] using hfirst
                · by_cases hfb : firstLane = b
                  · simpa [swapLane, hfa, hfb, Ne.symm hab] using hfirst
                  · simpa [swapLane, hfa, hfb, Ne.symm hab] using hfirst
              have hsl : swapLane a b secondLane = lane := by
                by_cases hsa : secondLane = a
                · simpa [swapLane, hsa] using hsecond
                · by_cases hsb : secondLane = b
                  · simpa [swapLane, hsa, hsb, Ne.symm hab] using hsecond
                  · simpa [swapLane, hsa, hsb, Ne.symm hab] using hsecond
              have hlane : firstLane = secondLane :=
                swapLane_injective hab (hfl.trans hsl.symm)
              subst secondLane
              exact hinj hf hs
  | duplicate source fresh sourceLane destinationLane =>
      have hdelta := Event.delta_correct
        (.duplicate source fresh sourceLane destinationLane) before hvalid
      rw [← hdelta]
      exact occupancyInjective_update_some hinj fresh destinationLane hvalid.2.2.2.2
  | nand left right output leftLane rightLane =>
      have hdelta := Event.delta_correct
        (.nand left right output leftLane rightLane) before hvalid
      rw [← hdelta]
      simp only [Event.delta, applyDelta, List.foldl_cons, List.foldl_nil,
        applyChange]
      have hinjLeft := occupancyInjective_update_none hinj left
      have hfreeLeft := laneFree_update_exact_none hvalid.2.2.2.2.1
      have hinjRight := occupancyInjective_update_none hinjLeft right
      have hfreeBoth : LaneFree
          (Function.update (Function.update before left none) right none) leftLane := by
        intro token htoken
        by_cases h : token = right
        · subst token; simp at htoken
        · rw [Function.update_of_ne h] at htoken
          exact hfreeLeft token htoken
      exact occupancyInjective_update_some hinjRight output leftLane hfreeBoth

/-- Replaying any sequence whose events are valid at the reached state
preserves injective lane occupancy. -/
theorem replayDeltas_occupancyInjective [DecidableEq Token] [DecidableEq Lane]
    (trace : List (CertifiedEvent Token Lane))
    (initial : TokenMap Token Lane)
    (hmatch : allConcreteTransitionsMatch trace initial)
    (hinj : OccupancyInjective initial) :
    OccupancyInjective (replayDeltas trace initial) := by
  induction trace generalizing initial with
  | nil => exact hinj
  | cons certified rest ih =>
      rcases hmatch with ⟨hdelta, hvalid, htail⟩
      simp only [replayDeltas]
      apply ih (applyDelta certified.delta initial) htail
      have hstep := certified.event.logicalStep_occupancyInjective initial hinj hvalid
      rwa [← certified.event.delta_correct initial hvalid, ← hdelta] at hstep

/-- WAIT and SWAP preserve the active/inactive status of every token. -/
theorem wait_active_iff [DecidableEq Token] [DecidableEq Lane]
    (before : TokenMap Token Lane) (token : Token) :
    Active (Event.logicalStep (.wait : Event Token Lane) before) token ↔
      Active before token := Iff.rfl

theorem swap_active_iff [DecidableEq Token] [DecidableEq Lane]
    (before : TokenMap Token Lane) (a b : Lane) (atA atB : Option Token)
    (token : Token) :
    Active (Event.logicalStep (.swap a b atA atB) before) token ↔
      Active before token := by
  simp only [Active, Event.logicalStep]
  cases h : before token with
  | none => simp
  | some lane =>
      constructor
      · intro _; simp
      · intro _
        simp only [h]
        split <;> simp
        split <;> simp

/-- DUPLICATE activates precisely its fresh token and preserves every other
active-token status. -/
theorem duplicate_active_iff [DecidableEq Token] [DecidableEq Lane]
    (before : TokenMap Token Lane) (source fresh : Token)
    (sourceLane destinationLane : Lane)
    (hvalid : (Event.duplicate source fresh sourceLane destinationLane).Valid before)
    (token : Token) :
    Active ((Event.duplicate source fresh sourceLane destinationLane).logicalStep before) token ↔
      token = fresh ∨ Active before token := by
  rcases hvalid with ⟨hsf, _hlanes, hsource, hfresh, _hfree⟩
  simp only [Active, Event.logicalStep]
  by_cases hs : token = source
  · subst token
    have hactive : before source ≠ none := by
      rw [(hsource source).mpr rfl]
      simp
    simp [hsf, hactive]
  · by_cases hf : token = fresh
    · subst token; simp [hs, hfresh]
    · simp [hs, hf]

/-- NAND deactivates its two input tokens, activates its fresh output, and
preserves every other active-token status. -/
theorem nand_active_iff [DecidableEq Token] [DecidableEq Lane]
    (before : TokenMap Token Lane) (left right output : Token)
    (leftLane rightLane : Lane)
    (hvalid : (Event.nand left right output leftLane rightLane).Valid before)
    (token : Token) :
    Active ((Event.nand left right output leftLane rightLane).logicalStep before) token ↔
      token = output ∨ (token ≠ left ∧ token ≠ right ∧ Active before token) := by
  rcases hvalid with
    ⟨hlr, hlo, hro, _hlanes, _hleft, _hright, houtput⟩
  simp only [Active, Event.logicalStep]
  by_cases ho : token = output
  · subst token; simp [hlo, hro]
  · by_cases hl : token = left
    · subst token; simp [hlo]
    · by_cases hr : token = right
      · subst token; simp [hro]
      · simp [ho, hl, hr]

/-- The finite active-token set, used to state exact count changes. -/
def activeFinset [Fintype Token] [DecidableEq Token] [DecidableEq Lane]
    (state : TokenMap Token Lane) : Finset Token :=
  Finset.univ.filter (fun token => state token ≠ none)

@[simp] theorem mem_activeFinset [Fintype Token] [DecidableEq Token] [DecidableEq Lane]
    (state : TokenMap Token Lane) (token : Token) :
    token ∈ activeFinset state ↔ Active state token := by
  simp only [activeFinset, Finset.mem_filter, Finset.mem_univ, true_and]
  rfl

/-- WAIT and SWAP leave the finite active-token count unchanged. -/
theorem wait_active_count [Fintype Token] [DecidableEq Token] [DecidableEq Lane]
    (before : TokenMap Token Lane) :
    (activeFinset (Event.logicalStep (.wait : Event Token Lane) before)).card =
      (activeFinset before).card := by
  congr 1

theorem swap_active_count [Fintype Token] [DecidableEq Token] [DecidableEq Lane]
    (before : TokenMap Token Lane) (a b : Lane) (atA atB : Option Token) :
    (activeFinset (Event.logicalStep (.swap a b atA atB) before)).card =
      (activeFinset before).card := by
  congr 1
  ext token
  simp [swap_active_iff before a b atA atB token]

/-- A valid DUPLICATE increases the number of active tokens by exactly one. -/
theorem duplicate_active_count [Fintype Token] [DecidableEq Token]
    [DecidableEq Lane] (before : TokenMap Token Lane) (source fresh : Token)
    (sourceLane destinationLane : Lane)
    (hvalid : (Event.duplicate source fresh sourceLane destinationLane).Valid before) :
    (activeFinset ((Event.duplicate source fresh sourceLane destinationLane).logicalStep before)).card =
      (activeFinset before).card + 1 := by
  have hfresh : fresh ∉ activeFinset before := by
    simp only [mem_activeFinset, Active]
    exact fun h => h (hvalid.2.2.2.1)
  have hset : activeFinset
        ((Event.duplicate source fresh sourceLane destinationLane).logicalStep before) =
      insert fresh (activeFinset before) := by
    ext token
    simp [duplicate_active_iff before source fresh sourceLane destinationLane hvalid]
  rw [hset, ← Finset.cons_eq_insert fresh (activeFinset before) hfresh]
  exact Finset.card_cons hfresh

/-- A valid NAND replaces two distinct active inputs by one fresh output, so
its post-event active count plus one equals its pre-event active count. -/
theorem nand_active_count [Fintype Token] [DecidableEq Token]
    [DecidableEq Lane] (before : TokenMap Token Lane)
    (left right output : Token) (leftLane rightLane : Lane)
    (hvalid : (Event.nand left right output leftLane rightLane).Valid before) :
    (activeFinset ((Event.nand left right output leftLane rightLane).logicalStep before)).card + 1 =
      (activeFinset before).card := by
  let live := activeFinset before
  have hleft : left ∈ live := by
    simp only [live, mem_activeFinset, Active]
    rw [(hvalid.2.2.2.2.1 left).mpr rfl]
    simp
  have hright : right ∈ live := by
    simp only [live, mem_activeFinset, Active]
    rw [(hvalid.2.2.2.2.2.1 right).mpr rfl]
    simp
  have houtput : output ∉ live := by
    simp only [live, mem_activeFinset, Active]
    exact fun h => h (hvalid.2.2.2.2.2.2)
  have hset : activeFinset
        ((Event.nand left right output leftLane rightLane).logicalStep before) =
      insert output ((live.erase left).erase right) := by
    ext token
    simp [live, nand_active_iff before left right output leftLane rightLane hvalid,
      and_left_comm]
  have houtErase : output ∉ (live.erase left).erase right := by
    simp [houtput]
  have hrightErase : right ∈ live.erase left := by
    simp [Ne.symm hvalid.1, hright]
  have hcInsert : (insert output ((live.erase left).erase right)).card =
      ((live.erase left).erase right).card + 1 := by
    rw [← Finset.cons_eq_insert output ((live.erase left).erase right) houtErase]
    exact Finset.card_cons houtErase
  have hcRight := Finset.card_erase_add_one hrightErase
  have hcLeft := Finset.card_erase_add_one hleft
  rw [hset, hcInsert]
  dsimp [live] at hcRight hcLeft ⊢
  omega

end VerifyConcreteEventDeltas
