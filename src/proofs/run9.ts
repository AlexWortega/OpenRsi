/**
 * run9: run8's goal-directed roadmap loop plus two new channels:
 *  - Lean 4 verification: universal ("for all sizes") claims require a sorry-free
 *    lean/Verify_*.lean compiling against Mathlib, machine-checked next to the
 *    python verifiers; finite claims keep verify_*.py.
 *  - Literature scout: a web-search oracle call feeds SCOUT.md into roadmap
 *    synthesis, and every roadmap replan gets a fresh targeted scout pass.
 */
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import {
  appendFileSync,
  copyFileSync,
  cpSync,
  existsSync,
  mkdirSync,
  readFileSync,
  renameSync,
  writeFileSync,
} from "node:fs";
import { basename, join, resolve } from "node:path";
import { createAgentSession, SessionManager } from "@earendil-works/pi-coding-agent";
import { assertKey, buildModel } from "../provider.js";

const FABLE = process.env.OPENRSI_FABLE_MODEL || "anthropic/claude-fable-5";
const PRO = process.env.OPENRSI_PRO_MODEL || "openai/gpt-5.6-sol-pro";
const SOL = process.env.OPENRSI_SOL_MODEL || "openai/gpt-5.6-sol";
const MAX_GENERATIONS = positiveIntegerEnv("OPENRSI_MAX_GENERATIONS", 40);
const ORACLE_TIMEOUT_MS = positiveIntegerEnv("OPENRSI_ORACLE_TIMEOUT_MS", 30 * 60_000);
const VERIFIER_TIMEOUT_MS = positiveIntegerEnv("OPENRSI_VERIFIER_TIMEOUT_MS", 10 * 60_000);
const UNKNOWN_CALL_COST_USD = numberEnv("OPENRSI_UNKNOWN_CALL_COST_USD", 2);
const SOL_TURN_RESERVE_USD = numberEnv("OPENRSI_SOL_TURN_RESERVE_USD", 5);
const SOL_MAX_TOKENS = positiveIntegerEnv("OPENRSI_SOL_MAX_TOKENS", 32_000);
const REPLAN_KILLS = positiveIntegerEnv("OPENRSI_ROADMAP_REPLAN_KILLS", 2);
const RESUME = process.argv.includes("--resume");
const SCOUT = process.env.OPENRSI_SCOUT_MODEL || "openai/gpt-5.6-sol:online";
const LEAN_PROJECT = process.env.OPENRSI_LEAN_PROJECT || join(process.env.HOME || "/root", "leanverify");
const LAKE = process.env.OPENRSI_LAKE || join(process.env.HOME || "/root", ".elan/bin/lake");
const LEAN_TIMEOUT_MS = positiveIntegerEnv("OPENRSI_LEAN_TIMEOUT_MS", 15 * 60_000);

const SOL_SYSTEM = `You are the implementation worker in a goal-directed CVP proof-research loop.
The target is a deterministic PCP-free polynomial-factor hardness reduction from 3SAT to Euclidean
GapCVP. Never describe finite evidence as an asymptotic theorem.

ROADMAP.md fixes the campaign's proof strategy and its FRONTIER lemma; your generation exists to
move that frontier. Read both proposer documents and both cross-reviews, select only a proposal
that survives its opponent review, state its causal mechanism, expected move against the frontier,
and falsification condition, then implement the smallest discriminating experiment. Attack
soundness with exact low-weight search. Update IDEAS.md, NOTES.md, STATUS.md, proof_cvp.md, and
the frontier-status section of ROADMAP.md honestly, and keep them as brief as accuracy allows.

Two verification channels exist, and every claim must use the matching one. Finite claims need a
deterministic experiments/verify_*.py that exits zero. Universal claims — any statement quantified
over all sizes or all instances — need a Lean 4 file lean/Verify_<name>.lean in the run directory
that compiles against Mathlib (import Mathlib is available; native_decide is acceptable for finite
kernels; files containing sorry, admit, or new axioms are rejected mechanically). A compiled Lean
theorem is the only way to claim progress beyond FINITE. List Lean files in the verifiers array
exactly like python ones.

Proposal grading and the continue/kill gate belong to other components — end your generation by
writing the requested SOL_RESULT.json: valid JSON with keys summary (string), hypothesis (string),
changed_files (array), verifiers (array of relative paths to newly written
experiments/verify_*.py or lean/Verify_*.lean files), tests (array of objects with command,
exit_code, and finding), claimed_progress (one of NONE, FINITE, LEMMA, GOAL), and next_experiment.
The recent Ten Advances document and any coverage of its solutions are off-limits: do not read,
search for, or use them.`;

type Verdict = "CONTINUE" | "KILL";
type GateDecision = "CONTINUE_IDEA" | "KILL_IDEA";
type Review = {
  verdict: Verdict;
  fatal_blockers: string[];
  evidence: string[];
  next_experiment: string;
  confidence: number;
};

type State = {
  run_id: string;
  phase: string;
  generation: number;
  outcome: "running" | "completed" | "budget_exhausted" | "fatal";
  decision?: GateDecision;
  reason?: string;
  models: { fable: string; pro: string; sol: string };
  budget_usd: number;
  spent_usd: number;
  kills_since_progress?: number;
};

function numberEnv(name: string, fallback: number): number {
  const raw = process.env[name];
  const value = raw === undefined ? fallback : Number(raw);
  if (!Number.isFinite(value) || value <= 0) throw new Error(`${name} must be a positive finite number`);
  return value;
}

function positiveIntegerEnv(name: string, fallback: number): number {
  const value = numberEnv(name, fallback);
  if (!Number.isSafeInteger(value)) throw new Error(`${name} must be a positive integer`);
  return value;
}

function atomicJson(path: string, value: unknown): void {
  const tmp = `${path}.tmp`;
  writeFileSync(tmp, `${JSON.stringify(value, null, 2)}\n`);
  renameSync(tmp, path);
}

function parseJsonObject(text: string): unknown {
  const trimmed = text.trim().replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/, "");
  try {
    return JSON.parse(trimmed);
  } catch {
    const start = trimmed.indexOf("{");
    const end = trimmed.lastIndexOf("}");
    if (start >= 0 && end > start) return JSON.parse(trimmed.slice(start, end + 1));
    throw new Error("response did not contain a JSON object");
  }
}

function parseReview(text: string): Review {
  const raw = parseJsonObject(text) as Partial<Review>;
  if (raw.verdict !== "CONTINUE" && raw.verdict !== "KILL") {
    throw new Error("review verdict must be CONTINUE or KILL");
  }
  if (!Array.isArray(raw.fatal_blockers) || !Array.isArray(raw.evidence)) {
    throw new Error("review blockers/evidence must be arrays");
  }
  const confidence = Number(raw.confidence);
  const nextExperiment = String(raw.next_experiment || "");
  if (!Number.isFinite(confidence) || confidence < 0 || confidence > 1) {
    throw new Error("review confidence must be in [0,1]");
  }
  if (raw.verdict === "CONTINUE" && !nextExperiment.trim()) {
    throw new Error("CONTINUE review must name a next experiment");
  }
  return {
    verdict: raw.verdict,
    fatal_blockers: raw.fatal_blockers.map(String),
    evidence: raw.evidence.map(String),
    next_experiment: nextExperiment,
    confidence,
  };
}

function gateDecision(verifiersPassed: boolean, fable: Verdict, pro: Verdict): GateDecision {
  return verifiersPassed && fable === "CONTINUE" && pro === "CONTINUE" ? "CONTINUE_IDEA" : "KILL_IDEA";
}

async function rerunVerifiers(python: string, runDir: string, packetPath: string, outputPath: string): Promise<boolean> {
  let verifiers: unknown;
  try {
    verifiers = (JSON.parse(readFileSync(packetPath, "utf8")) as { verifiers?: unknown }).verifiers;
  } catch {
    verifiers = undefined;
  }
  const results: Array<{ path: string; exit_code: number | null; signal: string | null; stdout: string; stderr: string; source_sha256?: string; source?: string }> = [];
  if (!Array.isArray(verifiers) || verifiers.length === 0 || verifiers.length > 5) {
    atomicJson(outputPath, { passed: false, reason: "packet must name 1-5 verifier paths", results });
    return false;
  }
  for (const item of verifiers) {
    const relative = String(item);
    const absolute = resolve(runDir, relative);
    const runRoot = `${resolve(runDir)}/`;
    const isLean = /^lean\/[Vv]erify_[^/]+\.lean$/.test(relative);
    const allowedRelative = isLean || /^(?:experiments|gen-\d+\/experiments)\/verify_[^/]+\.py$/.test(relative);
    if (!absolute.startsWith(runRoot) || !allowedRelative || !existsSync(absolute)) {
      results.push({ path: relative, exit_code: null, signal: null, stdout: "", stderr: "invalid or missing verifier path" });
      continue;
    }
    const source = readFileSync(absolute, "utf8");
    if (isLean && (/\b(sorry|admit)\b/.test(source) || /^\s*axiom\b/m.test(source))) {
      results.push({ path: relative, exit_code: null, signal: null, stdout: "", stderr: "lean file contains sorry/admit/axiom and is rejected" });
      continue;
    }
    const command = isLean
      ? { bin: LAKE, args: ["env", "lean", absolute], cwd: LEAN_PROJECT, timeout: LEAN_TIMEOUT_MS }
      : { bin: python, args: [absolute], cwd: runDir, timeout: VERIFIER_TIMEOUT_MS };
    const result = await new Promise<{ exit_code: number | null; signal: string | null; stdout: string; stderr: string }>((resolvePromise) => {
      const child = spawn(command.bin, command.args, { cwd: command.cwd, env: process.env, stdio: ["ignore", "pipe", "pipe"] });
      let stdout = "";
      let stderr = "";
      child.stdout.on("data", (chunk: Buffer) => { if (stdout.length < 200_000) stdout += chunk.toString(); });
      child.stderr.on("data", (chunk: Buffer) => { if (stderr.length < 200_000) stderr += chunk.toString(); });
      const timer = setTimeout(() => {
        child.kill("SIGTERM");
        setTimeout(() => { if (child.exitCode === null) child.kill("SIGKILL"); }, 10_000).unref();
      }, command.timeout);
      child.once("error", (error) => {
        clearTimeout(timer);
        resolvePromise({ exit_code: null, signal: null, stdout, stderr: String(error) });
      });
      child.once("close", (code, signal) => {
        clearTimeout(timer);
        resolvePromise({ exit_code: code, signal, stdout: stdout.slice(-100_000), stderr: stderr.slice(-20_000) });
      });
    });
    results.push({
      path: relative,
      ...result,
      source_sha256: createHash("sha256").update(source).digest("hex"),
      source: source.slice(0, 60_000),
    });
  }
  const passed = results.length === verifiers.length && results.every((result) => result.exit_code === 0);
  atomicJson(outputPath, { passed, results });
  return passed;
}

async function settleParallel(tasks: Array<Promise<void>>): Promise<void> {
  const results = await Promise.allSettled(tasks);
  const failures = results.filter((result): result is PromiseRejectedResult => result.status === "rejected");
  if (failures.length > 0) {
    throw new Error(`parallel stage failed: ${failures.map((failure) => String(failure.reason)).join(" | ")}`);
  }
}

async function ensureReview(
  python: string,
  cwd: string,
  outputPath: string,
  args: string[],
): Promise<void> {
  for (let attempt = 1; attempt <= 2; attempt++) {
    if (existsSync(outputPath)) {
      try {
        parseReview(readFileSync(outputPath, "utf8"));
        return;
      } catch (error) {
        renameSync(outputPath, `${outputPath}.invalid-${Date.now()}-attempt-${attempt}`);
      }
    }
    await runOracle(python, cwd, outputPath, args);
  }
  parseReview(readFileSync(outputPath, "utf8"));
}

function oracleCost(path: string): number {
  if (!existsSync(path)) return 0;
  let sum = 0;
  for (const line of readFileSync(path, "utf8").split("\n")) {
    if (!line.trim()) continue;
    try {
      const record = JSON.parse(line) as { cost?: unknown; reserved_cost?: unknown };
      const cost = typeof record.cost === "number" ? record.cost : Number(record.reserved_cost ?? UNKNOWN_CALL_COST_USD);
      if (Number.isFinite(cost) && cost >= 0) sum += cost;
    } catch {
      // A final truncated ledger line after a crash is ignored; all completed lines still count.
    }
  }
  return sum;
}

function runOracle(
  python: string,
  cwd: string,
  outputPath: string,
  args: string[],
  attempt = 1,
): Promise<void> {
  return new Promise((resolvePromise, reject) => {
    const child = spawn(python, args, { cwd, env: process.env, stdio: ["ignore", "pipe", "pipe"] });
    let stdout = "";
    let stderr = "";
    const limit = 4_000_000;
    child.stdout.on("data", (chunk: Buffer) => { if (stdout.length < limit) stdout += chunk.toString(); });
    child.stderr.on("data", (chunk: Buffer) => { if (stderr.length < limit) stderr += chunk.toString(); });
    const timer = setTimeout(() => {
      child.kill("SIGTERM");
      setTimeout(() => { if (child.exitCode === null) child.kill("SIGKILL"); }, 10_000).unref();
    }, ORACLE_TIMEOUT_MS);
    child.once("error", (error) => {
      clearTimeout(timer);
      reject(error);
    });
    child.once("close", (code, signal) => {
      clearTimeout(timer);
      if (code !== 0) {
        appendFileSync(join(cwd, "pro_costs.jsonl"), `${JSON.stringify({
          ts: new Date().toISOString(), status: "failed", output: basename(outputPath),
          cost: null, reserved_cost: UNKNOWN_CALL_COST_USD, code, signal,
        })}\n`);
        reject(new Error(`oracle ${basename(outputPath)} failed code=${code} signal=${signal}: ${stderr.slice(-2000)}`));
        return;
      }
      if (stdout.trim().length < 200) {
        writeFileSync(`${outputPath}.short-attempt-${attempt}`, stdout);
        if (attempt < 2) {
          runOracle(python, cwd, outputPath, args, attempt + 1).then(resolvePromise, reject);
          return;
        }
        if (args.includes("--ideate") || args.includes("--roadmap")) {
          writeFileSync(outputPath, stdout);
          writeFileSync(`${outputPath}.stderr`, `${stderr}\n[proofs9] proposer response remained truncated after retry; peer review will reject it.\n`);
          resolvePromise();
          return;
        }
        reject(new Error(`oracle ${basename(outputPath)} returned a truncated response twice`));
        return;
      }
      writeFileSync(outputPath, stdout);
      if (stderr) writeFileSync(`${outputPath}.stderr`, stderr);
      resolvePromise();
    });
  });
}

/** Seed the run's live documents from a prior campaign's run directory. */
function seedPrior(seedDir: string, runDir: string): void {
  const prior = join(runDir, "prior");
  mkdirSync(prior);
  const files = ["AGENTS.md", "STATUS.md", "IDEAS.md", "NOTES.md", "proof_cvp.md", "ORACLE_BRIEF.md", "LITERATURE.md"];
  for (const file of files) {
    const source = join(seedDir, file);
    if (existsSync(source)) copyFileSync(source, join(prior, file));
  }
  if (existsSync(join(seedDir, "experiments"))) {
    cpSync(join(seedDir, "experiments"), join(prior, "experiments"), { recursive: true });
  }
  for (const file of ["STATUS.md", "IDEAS.md", "NOTES.md", "proof_cvp.md", "ORACLE_BRIEF.md", "LITERATURE.md"]) {
    const source = join(seedDir, file);
    if (existsSync(source)) copyFileSync(source, join(runDir, file));
  }
  mkdirSync(join(runDir, "experiments"), { recursive: true });
  mkdirSync(join(runDir, "lean"), { recursive: true });
}

async function main(): Promise<void> {
  const repoRoot = resolve(new URL("../..", import.meta.url).pathname);

  assertKey();
  const budget = numberEnv("OPENRSI_PROOFS_BUDGET_USD", Number.NaN);
  const runId = process.env.OPENRSI_RUN_ID || `cvp_goal_directed_${new Date().toISOString().replace(/[:.]/g, "-")}`;
  if (!/^[A-Za-z0-9._-]+$/.test(runId)) throw new Error("OPENRSI_RUN_ID must be basename-safe");
  const runDir = resolve(process.env.OPENRSI_PROOFS_DIR || join(repoRoot, "runs", runId));
  const runExists = existsSync(runDir);
  if (runExists && !RESUME) throw new Error(`run directory already exists; choose a fresh OPENRSI_PROOFS_DIR or pass --resume: ${runDir}`);
  if (!runExists && RESUME) throw new Error(`cannot resume missing run directory: ${runDir}`);
  if (!runExists) {
    const seedDir = process.env.OPENRSI_SEED_DIR;
    if (!seedDir || !existsSync(seedDir)) {
      throw new Error("OPENRSI_SEED_DIR must point at a prior run directory (goal-directed runs start from an obstruction map)");
    }
    mkdirSync(runDir, { recursive: true });
    seedPrior(resolve(seedDir), runDir);
    writeFileSync(join(runDir, "AGENTS.md"), `${SOL_SYSTEM}\n`);
  }

  const events = join(runDir, "events.jsonl");
  const costLedger = join(runDir, "pro_costs.jsonl");
  const event = (value: unknown) => appendFileSync(events, `${JSON.stringify({ ts: new Date().toISOString(), ...value as object })}\n`);
  const python = process.env.OPENRSI_PYTHON || "python3";
  const askPro = join(repoRoot, "scripts", "ask_pro.py");
  const solModel = buildModel(SOL);
  (solModel as unknown as { maxTokens: number }).maxTokens = SOL_MAX_TOKENS;
  const { session } = await createAgentSession({
    model: solModel,
    thinkingLevel: (process.env.OPENRSI_MLXFAST_THINKING || "high") as "off" | "minimal" | "low" | "medium" | "high" | "xhigh",
    cwd: runDir,
    sessionManager: SessionManager.inMemory(runDir),
  });
  const priorState = RESUME
    ? JSON.parse(readFileSync(join(runDir, "state.json"), "utf8")) as State
    : undefined;
  const persistedNonOracleCost = priorState
    ? Math.max(0, Number(priorState.spent_usd || 0) - oracleCost(costLedger))
    : 0;
  const spent = () => persistedNonOracleCost + (session.getSessionStats()?.cost || 0) + oracleCost(costLedger);
  let state: State = priorState ? {
    ...priorState,
    phase: "resuming",
    outcome: "running",
    reason: undefined,
    budget_usd: budget,
  } : {
    run_id: runId,
    phase: "initialized",
    generation: 0,
    outcome: "running",
    models: { fable: FABLE, pro: PRO, sol: SOL },
    budget_usd: budget,
    spent_usd: 0,
    kills_since_progress: 0,
  };
  const checkpoint = () => {
    state.spent_usd = spent();
    atomicJson(join(runDir, "state.json"), state);
  };
  const canReserve = (usd: number) => budget - spent() >= usd;
  checkpoint();

  let solPrimed = false;
  try {
  // ---- Literature scout: once per campaign, idempotent on SCOUT.md ---- //
  const scoutPath = join(runDir, "SCOUT.md");
  if (!existsSync(scoutPath)) {
    state = { ...state, phase: "scout" };
    checkpoint();
    event({ phase: "scout", status: "started" });
    await runOracle(python, runDir, scoutPath, [askPro, "--scout", "--model", SCOUT,
      "Find published machinery relevant to proving polynomial-factor NP-hardness of Euclidean GapCVP without PCP: lattice gadget constructions, branching-program arithmetization, quaternion orders and trace bounds, tensor-coherence and integral flow rigidity, kernel-free lifts. The attached files carry this campaign's obstruction map — look specifically for tools that address its recurring parity-kernel and composition failures.",
      "STATUS.md", "IDEAS.md", "NOTES.md"]);
    event({ phase: "scout", status: "completed", spent_usd: spent() });
  }

  // ---- Roadmap synthesis: once per campaign, idempotent on ROADMAP.md ---- //
  const roadmapPath = join(runDir, "ROADMAP.md");
  if (!existsSync(roadmapPath)) {
    state = { ...state, phase: "roadmap" };
    checkpoint();
    event({ phase: "roadmap", status: "started" });
    if (!canReserve(4 * UNKNOWN_CALL_COST_USD)) {
      throw new Error("insufficient budget for roadmap synthesis");
    }
    const seedContext = ["SCOUT.md", "ORACLE_BRIEF.md", "IDEAS.md", "STATUS.md", "LITERATURE.md", "NOTES.md"];
    const roadmapQuestion = "Design the route to the target theorem: a deterministic polynomial-time many-one reduction from 3SAT to Euclidean GapCVP with approximation factor n^c for explicit c>0, without PCP and without unproved conjectures. The attached files carry a large map of proved obstructions from prior campaigns — the strategies must route around all of them by name.";
    const fableRoadmap = join(runDir, "roadmap_fable.md");
    const proRoadmap = join(runDir, "roadmap_pro.md");
    await settleParallel([
      ...(!existsSync(fableRoadmap) ? [runOracle(python, runDir, fableRoadmap, [askPro, "--roadmap", "--model", FABLE, roadmapQuestion, ...seedContext])] : []),
      ...(!existsSync(proRoadmap) ? [runOracle(python, runDir, proRoadmap, [askPro, "--roadmap", "--model", PRO, roadmapQuestion, ...seedContext])] : []),
    ]);
    const reviewOfFable = join(runDir, "roadmap_review_of_fable.json");
    const reviewOfPro = join(runDir, "roadmap_review_of_pro.json");
    const roadmapReviewQuestion = "Review this proof roadmap's lemma chains against every obstruction in the attached map. CONTINUE only if its recommended frontier lemma admits a genuinely discriminating first experiment.";
    await settleParallel([
      ensureReview(python, runDir, reviewOfFable, [askPro, "--review", "--model", PRO, roadmapReviewQuestion, fableRoadmap, ...seedContext]),
      ensureReview(python, runDir, reviewOfPro, [askPro, "--review", "--model", FABLE, roadmapReviewQuestion, proRoadmap, ...seedContext]),
    ]);
    const fableScore = parseReview(readFileSync(reviewOfFable, "utf8"));
    const proScore = parseReview(readFileSync(reviewOfPro, "utf8"));
    const score = (review: Review) => (review.verdict === "CONTINUE" ? 10 : 0) + review.confidence;
    const picked = score(fableScore) >= score(proScore) ? fableRoadmap : proRoadmap;
    copyFileSync(picked, roadmapPath);
    event({
      phase: "roadmap", status: "completed", picked: basename(picked),
      review_of_fable: fableScore.verdict, review_of_pro: proScore.verdict, spent_usd: spent(),
    });
  }

  const firstGeneration = RESUME ? Math.max(1, state.generation) : 1;
  researchLoop: for (let generation = firstGeneration; generation <= MAX_GENERATIONS; generation++) {
    if (spent() >= budget) {
      state = { ...state, phase: "done", generation: generation - 1, outcome: "budget_exhausted", reason: "USD cap reached before next generation" };
      checkpoint();
      break;
    }
    if (!canReserve(2 * UNKNOWN_CALL_COST_USD)) {
      state = { ...state, phase: "done", generation: generation - 1, outcome: "budget_exhausted", reason: "insufficient reserve for parallel ideation" };
      checkpoint();
      break;
    }
    const genDir = join(runDir, `gen-${generation}`);
    mkdirSync(genDir, { recursive: true });

    // ---- Roadmap replan after consecutive frontier kills ---- //
    if ((state.kills_since_progress ?? 0) >= REPLAN_KILLS) {
      state = { ...state, phase: "roadmap_replan", generation };
      checkpoint();
      const scoutRevision = join(genDir, "scout_revision.md");
      if (!existsSync(scoutRevision)) {
        await runOracle(python, runDir, scoutRevision, [askPro, "--scout", "--model", SCOUT,
          `The campaign's roadmap frontier has been killed ${state.kills_since_progress} consecutive generations. Search the literature for machinery that addresses exactly the failure recorded in the attached STATUS.md — prior work on the same wall, alternative formalisms, or fields where an analogous obstruction was overcome.`,
          "ROADMAP.md", "STATUS.md", "IDEAS.md"]);
      }
      const revision = join(genDir, "roadmap_revision.md");
      if (!existsSync(revision)) {
        await runOracle(python, runDir, revision, [askPro, "--roadmap", "--model", PRO,
          `The current roadmap's frontier lemma has now been killed ${state.kills_since_progress} consecutive generations. Rewrite the roadmap: keep the target theorem fixed, absorb every obstruction recorded since the last revision plus the fresh literature scout attached, and either reroute around the dead frontier or replace the strategy entirely. Output the complete replacement ROADMAP.md.`,
          "ROADMAP.md", "STATUS.md", "IDEAS.md", "NOTES.md", scoutRevision]);
      }
      copyFileSync(roadmapPath, join(runDir, `ROADMAP.gen${generation}.bak.md`));
      copyFileSync(revision, roadmapPath);
      state.kills_since_progress = 0;
      checkpoint();
      event({ phase: "roadmap_replan", generation, status: "completed", spent_usd: spent() });
    }

    state = { ...state, phase: "ideation", generation };
    checkpoint();
    event({ phase: state.phase, generation, status: "started" });

    const fableIdeas = join(genDir, "fable_ideas.md");
    const proIdeas = join(genDir, "pro_ideas.md");
    const ideaQuestion = `Generation ${generation}: ROADMAP.md fixes the campaign's proof strategy and its FRONTIER lemma. Independently propose 5-8 distinct mechanisms aimed squarely at that frontier — prove it, refute it, or (only with explicit justification against the obstruction map) amend the roadmap edge it sits on. A Lean 4 + Mathlib channel is available: a proposal may be "state lemma X precisely and prove it in Lean", and that is the only route to progress beyond FINITE. Start from the CURRENT IDEAS.md and STATUS.md, do not repeat killed routes unchanged, and give mechanism, expected move against the frontier, falsification test, and smallest executable experiment for each.`;
    const liveContext = ["ROADMAP.md", "ORACLE_BRIEF.md", "IDEAS.md", "STATUS.md", "LITERATURE.md", "NOTES.md"];
    if (generation > 1) {
      // A generation killed before Sol has GATE.json but no SOL_RESULT.json.
      for (const rel of [`gen-${generation - 1}/SOL_RESULT.json`, `gen-${generation - 1}/GATE.json`]) {
        if (existsSync(join(runDir, rel))) liveContext.push(rel);
      }
    }
    await settleParallel([
      ...(!existsSync(fableIdeas) ? [runOracle(python, runDir, fableIdeas, [askPro, "--ideate", "--model", FABLE, ideaQuestion, ...liveContext])] : []),
      ...(!existsSync(proIdeas) ? [runOracle(python, runDir, proIdeas, [askPro, "--ideate", "--model", PRO, ideaQuestion, ...liveContext])] : []),
    ]);
    if (spent() >= budget) {
      state = { ...state, phase: "done", outcome: "budget_exhausted", reason: "USD cap reached after ideation; cross-review not launched" };
      checkpoint();
      break researchLoop;
    }

    state.phase = "cross_review";
    checkpoint();
    if (!canReserve(2 * UNKNOWN_CALL_COST_USD)) {
      state = { ...state, phase: "done", outcome: "budget_exhausted", reason: "insufficient reserve for parallel cross-review" };
      checkpoint();
      break researchLoop;
    }
    const proReviewsFable = join(genDir, "pro_reviews_fable.json");
    const fableReviewsPro = join(genDir, "fable_reviews_pro.json");
    await settleParallel([
      ensureReview(python, runDir, proReviewsFable, [askPro, "--review", "--model", PRO, "Review Fable's proposals before any implementation. Select or kill them against every CURRENT obstruction and against ROADMAP.md's frontier; CONTINUE only if at least one bounded experiment genuinely discriminates at the frontier.", fableIdeas, ...liveContext]),
      ensureReview(python, runDir, fableReviewsPro, [askPro, "--review", "--model", FABLE, "Review Pro's proposals before any implementation. Select or kill them against every CURRENT obstruction and against ROADMAP.md's frontier; CONTINUE only if at least one bounded experiment genuinely discriminates at the frontier.", proIdeas, ...liveContext]),
    ]);
    const fableProposalReview = parseReview(readFileSync(proReviewsFable, "utf8"));
    const proProposalReview = parseReview(readFileSync(fableReviewsPro, "utf8"));
    if (fableProposalReview.verdict === "KILL" && proProposalReview.verdict === "KILL") {
      atomicJson(join(genDir, "GATE.json"), {
        decision: "KILL_IDEA", stage: "pre_implementation", pro_reviews_fable: fableProposalReview,
        fable_reviews_pro: proProposalReview, reason: "both proposal populations rejected",
      });
      state = { ...state, phase: "gate", outcome: "running", decision: "KILL_IDEA", reason: "both proposal populations rejected before Sol; advance to a fresh generation" };
      state.kills_since_progress = (state.kills_since_progress ?? 0) + 1;
      checkpoint();
      event({ phase: state.phase, generation, status: "completed", decision: "KILL_IDEA", spent_usd: spent() });
      continue researchLoop;
    }

    if (spent() >= budget) {
      state = { ...state, phase: "done", outcome: "budget_exhausted", reason: "USD cap reached after cross-review" };
      checkpoint();
      break;
    }
    state.phase = "sol_implementation";
    checkpoint();
    if (!canReserve(SOL_TURN_RESERVE_USD)) {
      state = { ...state, phase: "done", outcome: "budget_exhausted", reason: "insufficient reserve for Sol implementation turn" };
      checkpoint();
      break researchLoop;
    }
    const resultPacket = join(genDir, "SOL_RESULT.json");
    const eligible = [
      fableProposalReview.verdict === "CONTINUE" ? "Fable proposals" : "",
      proProposalReview.verdict === "CONTINUE" ? "Pro proposals" : "",
    ].filter(Boolean).join(" and ");
    if (!existsSync(resultPacket)) {
      const preamble = solPrimed ? "" : `${SOL_SYSTEM}\n\n`;
      await session.prompt(`${preamble}Generation ${generation}. Read ROADMAP.md, ${fableIdeas}, ${proIdeas}, ${proReviewsFable}, and ${fableReviewsPro}. Only ${eligible} survived cross-review. Implement and adversarially verify the single best surviving bounded experiment against the roadmap frontier; do not revive the rejected population. Write the required result packet to ${resultPacket}.`);
      solPrimed = true;
      await session.waitForIdle();
    }
    if (!existsSync(resultPacket)) {
      atomicJson(resultPacket, { summary: "Sol did not produce a result packet", hypothesis: "", changed_files: [], verifiers: [], tests: [], claimed_progress: "NONE", next_experiment: "" });
    }
    state.phase = "machine_verification";
    checkpoint();
    const machineVerification = join(genDir, "MACHINE_VERIFICATION.json");
    const verifierPassed = await rerunVerifiers(python, runDir, resultPacket, machineVerification);
    if (spent() >= budget) {
      state = { ...state, phase: "done", outcome: "budget_exhausted", reason: "USD cap reached after Sol; result review not launched" };
      checkpoint();
      break researchLoop;
    }

    state.phase = "result_review";
    checkpoint();
    if (!canReserve(2 * UNKNOWN_CALL_COST_USD)) {
      state = { ...state, phase: "done", outcome: "budget_exhausted", reason: "insufficient reserve for parallel result review" };
      checkpoint();
      break researchLoop;
    }
    const fableResult = join(genDir, "fable_result_review.json");
    const proResult = join(genDir, "pro_result_review.json");
    const reviewQuestion = `Review generation ${generation}'s Sol result. Check the packet against ROADMAP.md's frontier and STATUS/IDEAS/NOTES, and refuse any promotion from finite evidence to asymptotic hardness. CONTINUE only for one precise next bounded experiment that moves the frontier; otherwise KILL.`;
    await settleParallel([
      ensureReview(python, runDir, fableResult, [askPro, "--review", "--model", FABLE, reviewQuestion, resultPacket, machineVerification, "ROADMAP.md", "STATUS.md", "IDEAS.md", "NOTES.md", "proof_cvp.md"]),
      ensureReview(python, runDir, proResult, [askPro, "--review", "--model", PRO, reviewQuestion, resultPacket, machineVerification, "ROADMAP.md", "STATUS.md", "IDEAS.md", "NOTES.md", "proof_cvp.md"]),
    ]);
    let fableReview = parseReview(readFileSync(fableResult, "utf8"));
    let proReview = parseReview(readFileSync(proResult, "utf8"));

    if (fableReview.verdict !== proReview.verdict && !canReserve(2 * UNKNOWN_CALL_COST_USD)) {
      atomicJson(join(genDir, "GATE.json"), {
        decision: "UNDECIDED", stage: "result_review", fable: fableReview, pro: proReview,
        reason: "split verdict; insufficient reserve for the required rebuttal",
      });
      state = { ...state, phase: "done", outcome: "budget_exhausted", reason: "split verdict requires a rebuttal" };
      checkpoint();
      break researchLoop;
    }
    if (fableReview.verdict !== proReview.verdict) {
      state.phase = "rebuttal";
      checkpoint();
      const fableRebuttal = join(genDir, "fable_rebuttal.json");
      const proRebuttal = join(genDir, "pro_rebuttal.json");
      await settleParallel([
        ensureReview(python, runDir, fableRebuttal, [askPro, "--review", "--model", FABLE, "One final rebuttal: read Pro's result review and reconsider your verdict. Return strict review JSON. No further debate follows.", proResult, fableResult, resultPacket]),
        ensureReview(python, runDir, proRebuttal, [askPro, "--review", "--model", PRO, "One final rebuttal: read Fable's result review and reconsider your verdict. Return strict review JSON. No further debate follows.", fableResult, proResult, resultPacket]),
      ]);
      fableReview = parseReview(readFileSync(fableRebuttal, "utf8"));
      proReview = parseReview(readFileSync(proRebuttal, "utf8"));
    }

    const decision = gateDecision(verifierPassed, fableReview.verdict, proReview.verdict);
    atomicJson(join(genDir, "GATE.json"), {
      decision,
      verifier_passed: verifierPassed,
      machine_verification: machineVerification,
      fable: fableReview,
      pro: proReview,
      rule: "CONTINUE_IDEA requires a passing verifier and two CONTINUE verdicts; all other states KILL_IDEA, then the campaign advances to a fresh generation",
    });
    state = { ...state, phase: "gate", decision, reason: decision === "CONTINUE_IDEA" ? "two approvals plus verifier; mutate or extend in the next generation" : "candidate killed; advance to a fresh generation" };
    state.kills_since_progress = decision === "CONTINUE_IDEA" ? 0 : (state.kills_since_progress ?? 0) + 1;
    checkpoint();
    event({ phase: state.phase, generation, status: "completed", decision, spent_usd: spent() });
    if (generation === MAX_GENERATIONS) {
      state = { ...state, phase: "done", outcome: "completed", reason: "max generations reached" };
      checkpoint();
    }
  }
  if (state.phase !== "done") {
    state = { ...state, phase: "done", outcome: state.outcome === "running" ? "completed" : state.outcome, reason: state.reason || "generation loop finished" };
    checkpoint();
  }
  } catch (error) {
    state = { ...state, phase: "done", outcome: "fatal", reason: error instanceof Error ? error.message : String(error) };
    checkpoint();
    event({ phase: "done", status: "fatal", generation: state.generation, spent_usd: spent(), reason: state.reason });
    throw error;
  }
  event({ phase: "done", status: state.outcome, generation: state.generation, spent_usd: spent(), decision: state.decision });
  process.stdout.write(`${JSON.stringify(state, null, 2)}\n`);
}

main().catch((error) => {
  process.stderr.write(`[proofs9] FATAL ${error instanceof Error ? error.stack : String(error)}\n`);
  process.exitCode = 1;
});
