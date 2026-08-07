import Mathlib

/-!
# Sparse event-delta replay certificates

This file isolates the universal bookkeeping theorem needed to replace full
before/after token-map snapshots by sparse per-event deltas.  A token map is a
total function to `Option Lane`; a change either writes a lane or erases a
token, and a delta is replayed from left to right.  A certified event carries
its advertised logical event together with such a delta.

`allTransitionsMatch` checks the important state-dependent condition: at the
map reached by replaying all preceding deltas, the next sparse delta has
exactly the same result as the advertised logical step.  The main theorem says
that this local condition composes, so delta replay and logical execution have
the same final map.  A final-map corollary permits a certificate checker to
compare only the initial map, sparse deltas, and one claimed final map.

The theorem is deliberately generic.  It does not prove that a particular
Python/JSON producer emits matching deltas, that its token names are complete,
that XOR lane schedules stay in a finite width, or any CVP energy or soundness
claim.  Those remain serializer-specific obligations.
-/

namespace VerifyEventDeltaReplay

/-- A verifier-owned token map. `none` means that the token is not live. -/
abbrev TokenMap (Token Lane : Type*) := Token → Option Lane

/-- One sparse assignment.  `none` erases the named token. -/
structure Change (Token Lane : Type*) where
  token : Token
  value : Option Lane

/-- A delta is ordered: later assignments to a repeated token win. -/
abbrev Delta (Token Lane : Type*) := List (Change Token Lane)

/-- Apply one sparse assignment to a token map. -/
def applyChange {Token Lane : Type*} [DecidableEq Token]
    (before : TokenMap Token Lane) (change : Change Token Lane) :
    TokenMap Token Lane :=
  Function.update before change.token change.value

/-- Replay the assignments of one event delta from left to right. -/
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

/-- Chunking a delta does not change its replay semantics. -/
theorem applyDelta_append {Token Lane : Type*} [DecidableEq Token]
    (first second : Delta Token Lane) (before : TokenMap Token Lane) :
    applyDelta (first ++ second) before =
      applyDelta second (applyDelta first before) := by
  simp [applyDelta, List.foldl_append]

/-- An event plus the sparse token-map delta printed for that event. -/
structure CertifiedEvent (Event Token Lane : Type*) where
  event : Event
  delta : Delta Token Lane

/-- Replay only the sparse deltas, in event order. -/
def replayDeltas {Event Token Lane : Type*} [DecidableEq Token] :
    List (CertifiedEvent Event Token Lane) → TokenMap Token Lane →
      TokenMap Token Lane
  | [], before => before
  | certified :: rest, before =>
      replayDeltas rest (applyDelta certified.delta before)

/-- Execute only the advertised logical events, in the same order. -/
def runLogical {Event Token Lane : Type*}
    (logicalStep : Event → TokenMap Token Lane → TokenMap Token Lane) :
    List (CertifiedEvent Event Token Lane) → TokenMap Token Lane →
      TokenMap Token Lane
  | [], before => before
  | certified :: rest, before =>
      runLogical logicalStep rest (logicalStep certified.event before)

/-- State-dependent local certificate validity.  In the cons case the tail is
checked at the verifier-owned state obtained by actually applying the head
delta, rather than at a producer-supplied snapshot. -/
def allTransitionsMatch {Event Token Lane : Type*} [DecidableEq Token]
    (logicalStep : Event → TokenMap Token Lane → TokenMap Token Lane) :
    List (CertifiedEvent Event Token Lane) → TokenMap Token Lane → Prop
  | [], _ => True
  | certified :: rest, before =>
      applyDelta certified.delta before = logicalStep certified.event before ∧
      allTransitionsMatch logicalStep rest
        (applyDelta certified.delta before)

/-- Local delta/logical-step agreement composes over an arbitrary finite
trace.  Thus full per-event before/after snapshots are not needed. -/
theorem replayDeltas_eq_runLogical {Event Token Lane : Type*}
    [DecidableEq Token]
    (logicalStep : Event → TokenMap Token Lane → TokenMap Token Lane)
    (trace : List (CertifiedEvent Event Token Lane))
    (initial : TokenMap Token Lane)
    (hmatch : allTransitionsMatch logicalStep trace initial) :
    replayDeltas trace initial = runLogical logicalStep trace initial := by
  induction trace generalizing initial with
  | nil => rfl
  | cons certified rest ih =>
      rcases hmatch with ⟨hhead, htail⟩
      simp only [replayDeltas, runLogical]
      rw [← hhead]
      exact ih (applyDelta certified.delta initial) htail

/-- A convenient stronger premise: if every event's delta implements its
logical step on every map, then every trace made from those events replays
correctly. -/
theorem replayDeltas_eq_runLogical_of_eventwise {Event Token Lane : Type*}
    [DecidableEq Token]
    (logicalStep : Event → TokenMap Token Lane → TokenMap Token Lane)
    (trace : List (CertifiedEvent Event Token Lane))
    (hlocal : ∀ certified ∈ trace, ∀ before,
      applyDelta certified.delta before =
        logicalStep certified.event before)
    (initial : TokenMap Token Lane) :
    replayDeltas trace initial = runLogical logicalStep trace initial := by
  apply replayDeltas_eq_runLogical logicalStep trace initial
  induction trace generalizing initial with
  | nil => trivial
  | cons certified rest ih =>
      constructor
      · exact hlocal certified (by simp) initial
      · apply ih
        intro later hlater before
        exact hlocal later (by simp [hlater]) before

/-- Minimal trace certificate: one initial map, sparse event deltas, and one
claimed final map.  No intermediate snapshots occur in this structure. -/
structure TraceCertificate (Event Token Lane : Type*) where
  initial : TokenMap Token Lane
  events : List (CertifiedEvent Event Token Lane)
  claimedFinal : TokenMap Token Lane

/-- What a generic checker must establish about a snapshot-free certificate. -/
def TraceCertificate.Valid {Event Token Lane : Type*} [DecidableEq Token]
    (logicalStep : Event → TokenMap Token Lane → TokenMap Token Lane)
    (certificate : TraceCertificate Event Token Lane) : Prop :=
  allTransitionsMatch logicalStep certificate.events certificate.initial ∧
  replayDeltas certificate.events certificate.initial =
    certificate.claimedFinal

/-- If the sparse replay reaches the claimed final map and every local delta
matches its logical event, logical execution reaches that same map. -/
theorem TraceCertificate.logicalFinal_eq {Event Token Lane : Type*}
    [DecidableEq Token]
    (logicalStep : Event → TokenMap Token Lane → TokenMap Token Lane)
    (certificate : TraceCertificate Event Token Lane)
    (hvalid : certificate.Valid logicalStep) :
    runLogical logicalStep certificate.events certificate.initial =
      certificate.claimedFinal := by
  rcases hvalid with ⟨htransitions, hfinal⟩
  rw [← hfinal]
  exact (replayDeltas_eq_runLogical logicalStep certificate.events
    certificate.initial htransitions).symm

/-- Extensional form of the final theorem, useful for a checker that compares
one token lookup at a time. -/
theorem TraceCertificate.logicalFinal_token {Event Token Lane : Type*}
    [DecidableEq Token]
    (logicalStep : Event → TokenMap Token Lane → TokenMap Token Lane)
    (certificate : TraceCertificate Event Token Lane)
    (hvalid : certificate.Valid logicalStep) (token : Token) :
    runLogical logicalStep certificate.events certificate.initial token =
      certificate.claimedFinal token := by
  rw [certificate.logicalFinal_eq logicalStep hvalid]

end VerifyEventDeltaReplay
