/**
 * Research-proof solver, round 2 — GOAL-DIRECTED, CODE-FIRST variant.
 * Same pi scaffold / memory / nudge loop as dist/proofs/run.js, but the agent
 * is instructed to drive progress through executable code (searches, SAT/ILP,
 * verified experiments) and to keep attacking the stated goal instead of
 * banking partial results. No proof-assistant formalization (no Lean).
 * Seeds from the previous run's artifacts in <dir>/prior/.
 *
 *   OPENRSI_PROOFS_BUDGET_USD=100 OPENRSI_MLXFAST_THINKING=medium \
 *   node --env-file=.env dist/proofs/run2.js
 */
import { spawn } from "node:child_process";
import { createWriteStream, existsSync, mkdirSync, openSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { createAgentSession, SessionManager } from "@earendil-works/pi-coding-agent";
import { assertKey, modelSlug, tierModel } from "../provider.js";
import { recall, reflectAndStore } from "../memory/memory.js";

const SYS = `You are a research mathematician-programmer working autonomously on two research-level problems. Your objective is to ACHIEVE the stated goals — complete, correct proofs of the target statements — with COMPLETE INTELLECTUAL HONESTY: a claimed proof must actually be a proof; anything less is PARTIAL with the gap stated precisely. Partial results are stepping stones, not deliverables: after banking one, immediately return to attacking the main statement through its remaining gap.

Ground rules:
- These problems were recently solved in a document by another lab ("Ten Advances in Mathematics and Theoretical Computer Science", cdn.openai.com/pdf/ten-proofs-oai.pdf). That document and any copy, mirror, summary, or discussion of its proofs are STRICTLY OFF-LIMITS: do not fetch, search for, or read it or secondary sources describing its arguments. The experiment measures YOUR independent reasoning. Classical literature that predates it (textbooks, arXiv papers on prior bounds, standard techniques) is fair game — cite what you use.
- METHOD — CODE FIRST. Your primary instrument is executable code, not prose. Before proving a conjecture, write a program that tests it on small cases; before claiming a construction exists, write a search that finds it; before claiming one cannot exist, write an exhaustive check for the smallest open case. Install and use real tools: python-sat / pysat for SAT encodings, OR-tools or pulp for ILP, numpy for local search and spectral experiments, sympy for exact symbolic checks. Keep expensive searches running in background bash (nohup, &) while you reason about the next step, and harvest their results in later rounds. Put all experiment code in experiments/ with a one-line header saying what question it answers.
- NO PROOF ASSISTANTS: do not use or install Lean/Coq/Isabelle and do not spend budget on formalization. Rigor means: precise human-readable mathematics in the proof files, plus a machine-checkable script verify_<claim>.py (exit 0 = all checks pass) for every computational or finite claim the proof relies on.
- Work in visible files: NOTES_<problem>.md for the evolving attack log, proof_ehrhart.md and proof_ramsey.md for the current best write-up, STATUS.md with an honest one-page assessment (PROVED / PARTIAL / OPEN, what is rigorous, what is missing), experiments/ for all code.
- PRIOR WORK: the directory prior/ contains the full output of a previous $100 run on these same problems (STATUS.md, proof files, notes, verifiers). Both problems ended PARTIAL there, and its STATUS.md states the precise remaining gap for each. Read it first. Do NOT re-derive what it already proved — verify its verifiers still pass, import what you trust, and aim your entire budget at the stated gaps.
- Self-verify adversarially: after drafting any lemma or proof, attack it as a hostile referee — check every inequality's direction, every compactness/measurability assumption, every "clearly". A refereed gap demotes the claim to PARTIAL immediately.
- Budget discipline: fixed USD budget for the whole run. Spend it on goal-directed work — experiments that discriminate between attack routes, searches that could produce the missing construction — not on polishing write-ups of already-banked results. Update STATUS.md at every milestone so the run's value survives an abrupt stop.

The two problems:

PROBLEM 1 (Ehrhart volume conjecture, general case). Let K be a full-dimensional compact convex body in R^n with barycenter at the origin. Suppose the interior of K contains no lattice point of Z^n other than 0. Prove that vol(K) <= (n+1)^n / n!. (Sharp: the simplex (n+1)*conv{0,e_1,...,e_n} - (1,...,1) achieves it. Known classical results: Ehrhart proved n=2 and the simplex case in all n; Milman-Pajor gives vol(K) <= 4^n. Any improvement of 4^n toward (n+1)^n/n!, or a new proof of a nontrivial special case (e.g. all n=3 bodies), counts as valuable partial progress — but the goal is the full statement, with complete n=3 as the primary intermediate target.)

PROBLEM 2 (Superexponential multicolor Ramsey lower bound). Let R_k(3) be the least N such that every k-coloring of the edges of K_N contains a monochromatic triangle. Prove R_k(3) >= (c k^{1/3} / log k)^k for an absolute constant c > 0 and all k >= 2 — or any superexponential lower bound R_k(3) >= k^{ck}. (Classical: constructions give R_k(3) >= c^k (Schur-type, c about 3.199); upper bound R_k(3) <= 3 k!. Equivalent formulation: Shannon capacity of graphs with independence number 2 is unbounded. A construction with any exponent growing in k — even k^{c k / log k} — is major partial progress; the goal is a superexponential bound.)

Attack guidance, updated from the prior run's findings:
- Ramsey: the prior run PROVED that iid product codes, simple first-moment/expurgation, and basic LLL cannot beat base 2, and that the needed object is a coherent family of CORRELATED strong-power codes whose per-color base grows. That is a construction problem — attack it computationally: search correlated/algebraic code families (nonlinear codes, group-algebra constructions, Cayley colorings over growing groups, shifted product colorings) with SAT/ILP feasibility checks at small k, and let verified small-case wins guide the general amplification lemma. Also probe the open F_2^6 5-coloring case exhaustively-with-symmetry (SAT + symmetry breaking) — resolving it either way sharpens the local-coloring bounds.
- Ehrhart: primary intermediate target is ALL n=3 bodies. The prior run reduced the hard case to highly asymmetric bodies with no narrow near-symmetric zero section — explore exactly that class numerically (parametrized polytope optimization: maximize volume subject to interior-lattice-freeness and barycenter at 0, in n=3), find the true extremizers, and reverse-engineer the proof from what the optimizer shows. Ehrhart's own n=2 proof is fair game as a template.

Always look for the cheapest rigorous step that moves the MAIN statement forward, and let code tell you which step that is.`;

async function main() {
    assertKey();
    const dir = process.env.OPENRSI_PROOFS_DIR || "/home/alexw/OpenRsi/runs/proofs_code_r2";
    mkdirSync(dir, { recursive: true });
    const budget = Number(process.env.OPENRSI_PROOFS_BUDGET_USD || 100);
    const model = tierModel("outer");
    console.error(`[proofs2] model=openrouter:${modelSlug("outer")} dir=${dir} budget=$${budget}`);
    // Full event stream for the tracehouse bridge: tool args/results and complete
    // agent messages (text + thinking) go to events.jsonl next to the work files.
    // The header line is written SYNCHRONOUSLY before the bridge spawns so the
    // bridge always finds events.jsonl and never falls back to the bare log.
    const evPath = join(dir, "events.jsonl");
    const TRUNC = 4000;
    const trunc = (v, depth = 0) => {
        if (typeof v === "string")
            return v.length > TRUNC ? v.slice(0, TRUNC) + `…[+${v.length - TRUNC} chars]` : v;
        if (Array.isArray(v))
            return depth > 6 ? "[deep]" : v.map((x) => trunc(x, depth + 1));
        if (v && typeof v === "object") {
            if (depth > 6)
                return "[deep]";
            const o = {};
            for (const [k, x] of Object.entries(v))
                o[k] = trunc(x, depth + 1);
            return o;
        }
        return v;
    };
    writeFileSync(evPath, JSON.stringify({
        ts: new Date().toISOString(), t: "header",
        model: `openrouter:${modelSlug("outer")}`, budget, dir,
    }) + "\n", { flag: "a" });
    const evStream = createWriteStream(evPath, { flags: "a" });
    const evWrite = (o) => {
        try {
            evStream.write(JSON.stringify({ ts: new Date().toISOString(), ...o }) + "\n");
        }
        catch { /* logging must never kill the run */ }
    };
    // Stream this run to tracehouse (project rsi-proffer) by default; the bridge
    // tails events.jsonl. Its own output goes to `${dir}.thbridge.log`.
    try {
        const root = new URL("../..", import.meta.url).pathname;
        const py = join(root, ".thvenv/bin/python");
        const bridge = join(root, "scripts/tracehouse_tail_proofs.py");
        if (existsSync(py) && existsSync(bridge)) {
            const bridgeLog = openSync(`${dir}.thbridge.log`, "a");
            const child = spawn(py, [bridge, dir], { detached: true, stdio: ["ignore", bridgeLog, bridgeLog] });
            child.unref();
            console.error(`[proofs2] tracehouse bridge pid=${child.pid} project=${process.env.TRACEHOUSE_PROJECT || "rsi-proffer"}`);
        }
        else {
            console.error(`[proofs2] tracehouse bridge NOT started (missing ${py} or ${bridge})`);
        }
    }
    catch (e) {
        console.error(`[proofs2] tracehouse bridge failed: ${e?.message ?? e}`);
    }
    const mem = recall("proofs", "ehrhart-ramsey", 8);
    // pi has no systemPrompt option; project instructions load from AGENTS.md in cwd.
    writeFileSync(join(dir, "AGENTS.md"), SYS + mem);
    const { session } = await createAgentSession({
        model,
        thinkingLevel: (process.env.OPENRSI_MLXFAST_THINKING || "medium"),
        cwd: dir,
        sessionManager: SessionManager.inMemory(dir),
    });
    session.subscribe((e) => {
        if (e.type === "tool_execution_start") {
            process.stderr.write(`[proofs2 ${new Date().toISOString().slice(11, 19)}] tool ${e.toolName ?? e.name ?? "?"}\n`);
            evWrite({ t: "tool_start", id: e.toolCallId, tool: e.toolName, args: trunc(e.args) });
        }
        else if (e.type === "tool_execution_end") {
            evWrite({ t: "tool_end", id: e.toolCallId, tool: e.toolName, isError: !!e.isError, result: trunc(e.result) });
        }
        else if (e.type === "message_end") {
            evWrite({ t: "message", message: trunc(e.message) });
        }
    });
    const cost = () => (session.getSessionStats()?.cost ?? 0);
    await session.prompt(SYS + mem + `

---

Begin. First read everything in prior/ and rerun its verifiers. Then set up your files (STATUS.md seeded from prior findings, NOTES_ehrhart.md, NOTES_ramsey.md, experiments/), and for each problem list the 3 most promising CODE-DRIVEN attack routes on the stated gaps, with the first concrete experiment for each. Then start experiments immediately — get at least one search running in background bash within your first few rounds. No Lean; no peeking at the ten-proofs document or coverage of it; adversarial self-refereeing; STATUS.md always current.`);
    await session.waitForIdle();
    let round = 0;
    while (cost() < budget) {
        round++;
        const spent = cost().toFixed(2);
        console.error(`[proofs2] nudge ${round}, spent $${spent} of $${budget}`);
        evWrite({ t: "nudge", n: round, spent: Number(spent), budget });
        await session.prompt(`Keep going ($${spent} of $${budget} spent — pace yourself). Harvest any background experiments first; let their results pick the next step. Re-referee new claims adversarially before building on them. If a route has stalled for two nudges, bank what is rigorous and switch to a different CODE-driven route on the main gap — do not drift into polishing write-ups. Keep STATUS.md honest and current; every finite claim needs a passing verify_*.py.`);
        await session.waitForIdle();
    }
    const stats = session.getSessionStats();
    console.error(`[proofs2] DONE after ${round} rounds, cost=$${(stats?.cost ?? 0).toFixed(2)}`);
    evWrite({ t: "done", rounds: round, cost: Number((stats?.cost ?? 0).toFixed(2)) });
    await reflectAndStore({ model, benchmark: "proofs", problemId: "ehrhart-ramsey", score: 0, transcript: `Goal-directed code-first research run ($${budget} budget) on the Ehrhart volume conjecture and superexponential R_k(3) lower bounds in ${dir}, seeded from a prior PARTIAL run. The score field is a placeholder, NOT an outcome; base lessons only on what STATUS.md actually records as proved/partial.` }).catch(() => { });
    process.exit(0);
}
main().catch((e) => { console.error("[proofs2] FATAL", e?.stack || e); process.exit(1); });
