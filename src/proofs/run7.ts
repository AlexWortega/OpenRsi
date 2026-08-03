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
import { fileURLToPath } from "node:url";
import { createAgentSession, SessionManager } from "@earendil-works/pi-coding-agent";
import { assertKey, buildModel } from "../provider.js";

const FABLE = process.env.OPENRSI_FABLE_MODEL || "anthropic/claude-fable-5";
const PRO = process.env.OPENRSI_PRO_MODEL || "openai/gpt-5.6-sol-pro";
const SOL = process.env.OPENRSI_SOL_MODEL || "openai/gpt-5.6-sol";
const MAX_GENERATIONS = positiveIntegerEnv("OPENRSI_MAX_GENERATIONS", 3);
const ORACLE_TIMEOUT_MS = positiveIntegerEnv("OPENRSI_ORACLE_TIMEOUT_MS", 30 * 60_000);
const VERIFIER_TIMEOUT_MS = positiveIntegerEnv("OPENRSI_VERIFIER_TIMEOUT_MS", 10 * 60_000);
const UNKNOWN_CALL_COST_USD = numberEnv("OPENRSI_UNKNOWN_CALL_COST_USD", 2);
const SOL_TURN_RESERVE_USD = numberEnv("OPENRSI_SOL_TURN_RESERVE_USD", 5);
const SOL_MAX_TOKENS = positiveIntegerEnv("OPENRSI_SOL_MAX_TOKENS", 12_000);

const SOL_SYSTEM = `You are the implementation worker in a model-separated CVP proof-research loop.
The target is a deterministic PCP-free polynomial-factor hardness reduction from 3SAT to Euclidean
GapCVP. The inherited campaign is PARTIAL: never describe finite evidence as an asymptotic theorem.

Your role is implementation and adversarial verification, not proposal grading and not the final
continue/kill decision. Read both proposer documents and both cross-reviews for the current
generation. Select only a proposal that survives its opponent review, state its causal mechanism,
expected move, and falsification condition, then implement the smallest discriminating experiment.
Every finite claim needs a deterministic verify_*.py that exits zero. Attack soundness with exact
low-weight search. Update IDEAS.md, NOTES.md, STATUS.md, and proof_cvp.md honestly.

At the end of the generation write the requested SOL_RESULT.json. It must be valid JSON with keys:
summary (string), hypothesis (string), changed_files (array), verifiers (an array of relative paths
to newly written experiments/verify_*.py files), tests (array of objects with command, exit_code,
and finding), claimed_progress (one of NONE, FINITE, LEMMA, GOAL), and next_experiment.
Do not set the campaign gate. Do not read, search for, or use the prohibited recent Ten Advances
document or any coverage of its solutions.`;

type Verdict = "CONTINUE" | "KILL";
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
  decision?: Verdict;
  reason?: string;
  models: { fable: string; pro: string; sol: string };
  budget_usd: number;
  spent_usd: number;
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
  if (raw.verdict === "CONTINUE" && (raw.fatal_blockers.length > 0 || !nextExperiment.trim())) {
    throw new Error("CONTINUE review must have no fatal blockers and must name a next experiment");
  }
  return {
    verdict: raw.verdict,
    fatal_blockers: raw.fatal_blockers.map(String),
    evidence: raw.evidence.map(String),
    next_experiment: nextExperiment,
    confidence,
  };
}

function gateDecision(verifiersPassed: boolean, fable: Verdict, pro: Verdict): Verdict {
  return verifiersPassed && fable === "CONTINUE" && pro === "CONTINUE" ? "CONTINUE" : "KILL";
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
    const allowedRoot = `${resolve(runDir, "experiments")}/`;
    if (!absolute.startsWith(allowedRoot) || !basename(absolute).startsWith("verify_") || !absolute.endsWith(".py") || !existsSync(absolute)) {
      results.push({ path: relative, exit_code: null, signal: null, stdout: "", stderr: "invalid or missing verifier path" });
      continue;
    }
    const source = readFileSync(absolute, "utf8");
    const result = await new Promise<{ exit_code: number | null; signal: string | null; stdout: string; stderr: string }>((resolvePromise) => {
      const child = spawn(python, [absolute], { cwd: runDir, env: process.env, stdio: ["ignore", "pipe", "pipe"] });
      let stdout = "";
      let stderr = "";
      child.stdout.on("data", (chunk: Buffer) => { if (stdout.length < 200_000) stdout += chunk.toString(); });
      child.stderr.on("data", (chunk: Buffer) => { if (stderr.length < 200_000) stderr += chunk.toString(); });
      const timer = setTimeout(() => {
        child.kill("SIGTERM");
        setTimeout(() => { if (child.exitCode === null) child.kill("SIGKILL"); }, 10_000).unref();
      }, VERIFIER_TIMEOUT_MS);
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
      writeFileSync(outputPath, stdout);
      if (stderr) writeFileSync(`${outputPath}.stderr`, stderr);
      resolvePromise();
    });
  });
}

function seedPrior(repoRoot: string, runDir: string): void {
  const source = join(repoRoot, "traces/proofs_2026-08/cvp_ideate");
  const prior = join(runDir, "prior");
  mkdirSync(prior);
  const files = [
    "AGENTS.md", "STATUS.md", "IDEAS.md", "NOTES.md", "proof_cvp.md", "ORACLE_BRIEF.md",
    "LITERATURE.md", "ideate_2.txt", "converge_fold_1.txt", "referee_final.txt",
  ];
  for (const file of files) copyFileSync(join(source, file), join(prior, file));
  cpSync(join(source, "experiments"), join(prior, "experiments"), { recursive: true });
  for (const file of ["STATUS.md", "IDEAS.md", "NOTES.md", "proof_cvp.md", "ORACLE_BRIEF.md", "LITERATURE.md"]) {
    copyFileSync(join(source, file), join(runDir, file));
  }
}

function dryRunPlan(repoRoot: string): void {
  const sampleContinue = parseReview('{"verdict":"CONTINUE","fatal_blockers":[],"evidence":["verifier exit 0"],"next_experiment":"bounded mutation","confidence":0.8}');
  const sampleKill = parseReview('{"verdict":"KILL","fatal_blockers":["counterexample"],"evidence":[],"next_experiment":"","confidence":0.9}');
  process.stdout.write(`${JSON.stringify({
    dry_run: true,
    repo_root: repoRoot,
    models: { fable: FABLE, pro: PRO, sol: SOL },
    stages: ["parallel ideation", "parallel cross-review", "Sol implementation+verification", "parallel result review", "optional one-round rebuttal", "code-owned gate"],
    max_generations: MAX_GENERATIONS,
    oracle_timeout_ms: ORACLE_TIMEOUT_MS,
    simulated_gate: { unanimous_continue: sampleContinue.verdict, unanimous_kill: sampleKill.verdict, split: "one rebuttal then KILL unless unanimous CONTINUE" },
    simulated_matrix: {
      approvals_and_verifier: gateDecision(true, "CONTINUE", "CONTINUE"),
      approvals_without_verifier: gateDecision(false, "CONTINUE", "CONTINUE"),
      split_after_rebuttal: gateDecision(true, "CONTINUE", "KILL"),
    },
    network_calls: 0,
    filesystem_writes: 0,
  }, null, 2)}\n`);
}

async function main(): Promise<void> {
  const repoRoot = resolve(fileURLToPath(new URL("../..", import.meta.url)));
  if (process.argv.includes("--dry-run")) {
    dryRunPlan(repoRoot);
    return;
  }

  assertKey();
  const budget = numberEnv("OPENRSI_PROOFS_BUDGET_USD", Number.NaN);
  const runId = process.env.OPENRSI_RUN_ID || `cvp_fable_pro_sol_${new Date().toISOString().replace(/[:.]/g, "-")}`;
  if (!/^[A-Za-z0-9._-]+$/.test(runId)) throw new Error("OPENRSI_RUN_ID must be basename-safe");
  const runDir = resolve(process.env.OPENRSI_PROOFS_DIR || join(repoRoot, "runs", runId));
  if (existsSync(runDir)) throw new Error(`run directory already exists; choose a fresh OPENRSI_PROOFS_DIR: ${runDir}`);
  mkdirSync(runDir, { recursive: true });
  seedPrior(repoRoot, runDir);
  writeFileSync(join(runDir, "AGENTS.md"), `${SOL_SYSTEM}\n`);

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
  const spent = () => (session.getSessionStats()?.cost || 0) + oracleCost(costLedger);
  let state: State = {
    run_id: runId,
    phase: "initialized",
    generation: 0,
    outcome: "running",
    models: { fable: FABLE, pro: PRO, sol: SOL },
    budget_usd: budget,
    spent_usd: 0,
  };
  const checkpoint = () => {
    state.spent_usd = spent();
    atomicJson(join(runDir, "state.json"), state);
  };
  const canReserve = (usd: number) => budget - spent() >= usd;
  checkpoint();

  try {
  researchLoop: for (let generation = 1; generation <= MAX_GENERATIONS; generation++) {
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
    mkdirSync(genDir);
    state = { ...state, phase: "ideation", generation };
    checkpoint();
    event({ phase: state.phase, generation, status: "started" });

    const fableIdeas = join(genDir, "fable_ideas.md");
    const proIdeas = join(genDir, "pro_ideas.md");
    const ideaQuestion = `Generation ${generation}: independently propose 5-8 distinct mechanisms that could advance the PCP-free polynomial-gap CVP campaign. Start from the CURRENT IDEAS.md and STATUS.md, do not repeat killed routes unchanged, and give mechanism, expected move, falsification test, and smallest executable experiment for each.`;
    const liveContext = ["ORACLE_BRIEF.md", "IDEAS.md", "STATUS.md", "LITERATURE.md", "NOTES.md"];
    if (generation > 1) liveContext.push(`gen-${generation - 1}/SOL_RESULT.json`, `gen-${generation - 1}/GATE.json`);
    await settleParallel([
      runOracle(python, runDir, fableIdeas, [askPro, "--ideate", "--model", FABLE, ideaQuestion, ...liveContext]),
      runOracle(python, runDir, proIdeas, [askPro, "--ideate", "--model", PRO, ideaQuestion, ...liveContext]),
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
      runOracle(python, runDir, proReviewsFable, [askPro, "--review", "--model", PRO, "Review Fable's proposals before any implementation. Select or kill them against every CURRENT obstruction; CONTINUE only if at least one bounded experiment is genuinely discriminating.", fableIdeas, ...liveContext]),
      runOracle(python, runDir, fableReviewsPro, [askPro, "--review", "--model", FABLE, "Review Pro's proposals before any implementation. Select or kill them against every CURRENT obstruction; CONTINUE only if at least one bounded experiment is genuinely discriminating.", proIdeas, ...liveContext]),
    ]);
    const fableProposalReview = parseReview(readFileSync(proReviewsFable, "utf8"));
    const proProposalReview = parseReview(readFileSync(fableReviewsPro, "utf8"));
    if (fableProposalReview.verdict === "KILL" && proProposalReview.verdict === "KILL") {
      atomicJson(join(genDir, "GATE.json"), {
        decision: "KILL", stage: "pre_implementation", pro_reviews_fable: fableProposalReview,
        fable_reviews_pro: proProposalReview, reason: "both proposal populations rejected",
      });
      state = { ...state, phase: "done", outcome: "completed", decision: "KILL", reason: "both proposal populations rejected before Sol" };
      checkpoint();
      break researchLoop;
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
    await session.prompt(`${SOL_SYSTEM}\n\nGeneration ${generation}. Read ${fableIdeas}, ${proIdeas}, ${proReviewsFable}, and ${fableReviewsPro}. Only ${eligible} survived cross-review. Implement and adversarially verify the single best surviving bounded experiment; do not revive the rejected population. Write the required result packet to ${resultPacket}.`);
    await session.waitForIdle();
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
    const reviewQuestion = `Review generation ${generation}'s Sol result. Check the packet against STATUS/IDEAS/NOTES and refuse any promotion from finite evidence to asymptotic hardness. CONTINUE only for one precise next bounded experiment; otherwise KILL.`;
    await settleParallel([
      runOracle(python, runDir, fableResult, [askPro, "--review", "--model", FABLE, reviewQuestion, resultPacket, machineVerification, "STATUS.md", "IDEAS.md", "NOTES.md", "proof_cvp.md"]),
      runOracle(python, runDir, proResult, [askPro, "--review", "--model", PRO, reviewQuestion, resultPacket, machineVerification, "STATUS.md", "IDEAS.md", "NOTES.md", "proof_cvp.md"]),
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
        runOracle(python, runDir, fableRebuttal, [askPro, "--review", "--model", FABLE, "One final rebuttal: read Pro's result review and reconsider your verdict. Return strict review JSON. No further debate follows.", proResult, fableResult, resultPacket]),
        runOracle(python, runDir, proRebuttal, [askPro, "--review", "--model", PRO, "One final rebuttal: read Fable's result review and reconsider your verdict. Return strict review JSON. No further debate follows.", fableResult, proResult, resultPacket]),
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
      rule: "CONTINUE requires a passing verifier and two CONTINUE verdicts; all other states KILL",
    });
    state = { ...state, phase: "gate", decision, reason: decision === "CONTINUE" ? "two approvals plus verifier" : "verification/review gate failed" };
    checkpoint();
    event({ phase: state.phase, generation, status: "completed", decision, spent_usd: spent() });
    if (decision === "KILL") {
      state = { ...state, phase: "done", outcome: "completed" };
      checkpoint();
      break;
    }
    if (generation === MAX_GENERATIONS) {
      state = { ...state, phase: "done", outcome: "completed", reason: "max generations reached" };
      checkpoint();
    }
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
  process.stderr.write(`[proofs7] FATAL ${error instanceof Error ? error.stack : String(error)}\n`);
  process.exitCode = 1;
});
