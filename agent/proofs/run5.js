/**
 * CVP hardness — worker + oracle. Worker gpt-5.6-sol (thinking high) codes and
 * verifies; oracle gpt-5.6-sol-pro via scripts/ask_pro.py for conceptual steps
 * (costs logged to pro_costs.jsonl, counted in the run budget). New here: an
 * in-process budget guard aborts mid-round at 1.2x budget (the ramsey_fable
 * lesson — the nudge loop alone cannot stop a long round).
 *
 *   OPENRSI_PROOFS_DIR=... OPENRSI_PROOFS_BUDGET_USD=50 \
 *   OPENRSI_MLXFAST_THINKING=high node --env-file=.env dist/proofs/run5.js
 */
import { spawn } from "node:child_process";
import { createWriteStream, existsSync, mkdirSync, openSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { createAgentSession, SessionManager } from "@earendil-works/pi-coding-agent";
import { assertKey, modelSlug, tierModel } from "../provider.js";
import { recall, reflectAndStore } from "../memory/memory.js";

const SYS = `You are a research mathematician / theoretical computer scientist working autonomously on ONE research-level problem. Your objective is to ACHIEVE the stated goal — with COMPLETE INTELLECTUAL HONESTY: a claimed proof must actually be a proof; anything less is PARTIAL with the gap stated precisely.

THE PROBLEM (the only one this run). Prove that the Euclidean closest vector problem (CVP) is NP-hard to approximate within a FIXED POLYNOMIAL factor of the lattice rank: exhibit a deterministic polynomial-time many-one reduction from 3SAT to GapCVP_{n^c} in the l2 norm, for an explicit absolute constant c > 0 (reference target: c = 1/400), where the lattice is given by an explicit integer basis. The reduction must NOT invoke the PCP theorem and must not assume unproven conjectures (e.g. the Projection Games Conjecture).

Classical state (fair game to use and cite): exact CVP is NP-hard (van Emde Boas 1981); constant-factor and almost-polynomial-factor hardness n^{c/log log n} are known via PCP machinery (Arora–Babai–Stern–Sweedyk 1997; Dinur–Kindler–Raz–Safra 2003); NP-hardness of polynomial factors was open — known conditionally under the Projection Games Conjecture. The nearest codeword problem (NCP) and syndrome decoding for binary linear codes are the natural stepping stones: a PCP-free polynomial-factor NP-hardness for NCP transfers toward CVP by standard code-to-lattice liftings (mod-2 constructions à la Micciancio).

Goal ladder (value strictly increasing):
(a) a rigorous deterministic reduction from 3SAT giving n^c-factor NP-hardness for binary nearest codeword / syndrome decoding, any explicit c > 0;
(b) transfer to GapCVP in l2 (and other lp) with an explicit polynomial factor;
(c) the full target with clean constants and a complete soundness proof.
Constant-factor results and PCP-based rederivations are NOT progress. An honest, fully-verified (a) alone would already be a major result.

THE ORACLE. You may consult a much deeper reasoning model:

    timeout 1800 python3 /home/alexw/OpenRsi/scripts/ask_pro.py "<self-contained question>" [context-file ...]

Its answer prints to stdout; its USD cost (typically $0.5–$3 per call) is logged to pro_costs.jsonl and COUNTS AGAINST YOUR RUN BUDGET. Use it ONLY for the highest-leverage conceptual steps: (i) designing the encoding of assignments and clause constraints AFTER you have written a compressed brief of the obstacle landscape; (ii) breaking a precisely-stated stuck lemma (exact statement, what you tried, why it failed); (iii) a final adversarial referee pass. Never for routine coding or literature summaries. Plan roughly 4–8 oracle calls across the run; ACT on each answer with code immediately and report exact outcomes back in the next call.

Ground rules:
- This problem was recently solved in a document by another lab ("Ten Advances in Mathematics and Theoretical Computer Science", cdn.openai.com/pdf/ten-proofs-oai.pdf). That document and any copy, mirror, summary, or discussion of its solution are STRICTLY OFF-LIMITS for both you AND the oracle: do not fetch, search for, or read it or secondary sources describing its argument, and do not ask the oracle to recall it. The experiment measures YOUR independent reasoning. Classical literature that predates it is fair game — cite what you use.
- METHOD — CODE FIRST. Reductions are programs: implement every candidate reduction on SMALL 3SAT instances end-to-end and test completeness AND soundness numerically before proving anything (brute-force the small lattices/codes; random and adversarial low-weight solutions). Use numpy, sympy (GF(2^m) arithmetic), python-sat for instance generation, exact rational arithmetic where needed. Background long searches (nohup ... > log 2>&1 &); cap EVERY foreground command with timeout.
- NO PROOF ASSISTANTS. Rigor = precise mathematics in proof_cvp.md + a machine-checkable verify_<claim>.py (exit 0) for every finite/computational claim (e.g. end-to-end checks of the reduction on batches of small instances, completeness/soundness gap measurements).
- Work in visible files: ORACLE_BRIEF.md, NOTES.md (attack log), proof_cvp.md (current best write-up), STATUS.md (honest one-page assessment, updated at EVERY milestone), experiments/ (all code).
- Self-verify adversarially: soundness is where reductions die — attack your own gap analysis as a hostile referee; hunt for cheating low-weight solutions with search. A refereed gap demotes the claim immediately.
- Budget discipline: fixed USD budget shared between your inference and oracle calls. Do not drift into survey mode — pick an encoding strategy, implement, measure, iterate.`;

async function main() {
    assertKey();
    const dir = process.env.OPENRSI_PROOFS_DIR || "/home/alexw/OpenRsi/runs/cvp_oracle";
    mkdirSync(dir, { recursive: true });
    const budget = Number(process.env.OPENRSI_PROOFS_BUDGET_USD || 50);
    const model = tierModel("outer");
    console.error(`[proofs5] model=openrouter:${modelSlug("outer")} oracle=${process.env.OPENRSI_PRO_MODEL || "openai/gpt-5.6-sol-pro"} dir=${dir} budget=$${budget} thinking=${process.env.OPENRSI_MLXFAST_THINKING || "medium"}`);
    const mem = recall("proofs", "cvp", 8);
    writeFileSync(join(dir, "AGENTS.md"), SYS + mem);
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
        ts: new Date().toISOString(), t: "header", variant: "proofs5",
        model: `openrouter:${modelSlug("outer")}`, budget, dir,
    }) + "\n", { flag: "a" });
    const evStream = createWriteStream(evPath, { flags: "a" });
    const evWrite = (o) => {
        try {
            evStream.write(JSON.stringify({ ts: new Date().toISOString(), ...o }) + "\n");
        }
        catch { /* logging must never kill the run */ }
    };
    try {
        const root = new URL("../..", import.meta.url).pathname;
        const py = join(root, ".thvenv/bin/python");
        const bridge = join(root, "scripts/tracehouse_tail_proofs.py");
        if (existsSync(py) && existsSync(bridge)) {
            const bridgeLog = openSync(`${dir}.thbridge.log`, "a");
            const child = spawn(py, [bridge, dir], { detached: true, stdio: ["ignore", bridgeLog, bridgeLog] });
            child.unref();
            console.error(`[proofs5] tracehouse bridge pid=${child.pid} project=${process.env.TRACEHOUSE_PROJECT || "rsi-proffer"}`);
        }
    }
    catch (e) {
        console.error(`[proofs5] tracehouse bridge failed: ${e?.message ?? e}`);
    }
    const { session } = await createAgentSession({
        model,
        thinkingLevel: (process.env.OPENRSI_MLXFAST_THINKING || "high"),
        cwd: dir,
        sessionManager: SessionManager.inMemory(dir),
    });
    session.subscribe((e) => {
        if (e.type === "tool_execution_start") {
            process.stderr.write(`[proofs5 ${new Date().toISOString().slice(11, 19)}] tool ${e.toolName ?? e.name ?? "?"}\n`);
            evWrite({ t: "tool_start", id: e.toolCallId, tool: e.toolName, args: trunc(e.args) });
        }
        else if (e.type === "tool_execution_end") {
            evWrite({ t: "tool_end", id: e.toolCallId, tool: e.toolName, isError: !!e.isError, result: trunc(e.result) });
        }
        else if (e.type === "message_end") {
            evWrite({ t: "message", message: trunc(e.message) });
        }
    });
    const proCost = () => {
        try {
            return readFileSync(join(dir, "pro_costs.jsonl"), "utf8").split("\n").filter(Boolean)
                .reduce((s, l) => { try { return s + (JSON.parse(l).cost || 0); } catch { return s; } }, 0);
        }
        catch {
            return 0;
        }
    };
    const cost = () => (session.getSessionStats()?.cost ?? 0) + proCost();
    // Budget guard: the nudge loop only checks cost BETWEEN rounds; a single long
    // round burned 4x budget once (ramsey_fable). Abort mid-round at 1.2x.
    let round = 0;
    const guard = setInterval(() => {
        if (cost() >= budget * 1.2) {
            const c = cost().toFixed(2);
            console.error(`[proofs5] BUDGET GUARD tripped at $${c} (1.2x $${budget}) mid-round — aborting`);
            evWrite({ t: "done", rounds: round, cost: Number(c), aborted: "budget_guard" });
            console.error(`[proofs5] DONE after ${round} rounds, cost=$${c} (budget-guard abort)`);
            process.exit(0);
        }
    }, 60_000);
    guard.unref();
    await session.prompt(SYS + mem + `

---

Begin. Phase 1: write NOTES.md restating the problem in your own words, the classical hardness landscape, and the 2-3 most promising ENCODING strategies for a PCP-free reduction (how to encode assignments, how clause constraints become linear/lattice constraints, where the polynomial gap can come from) — then distill ORACLE_BRIEF.md. Phase 2: FIRST oracle call with ORACLE_BRIEF.md attached: ask it to pick the strategy and design the encoding precisely enough to implement. Phase 3: implement the candidate reduction end-to-end on small 3SAT instances, measure completeness/soundness gaps by brute force, and iterate — further oracle calls only at genuine conceptual walls. Bounded foreground commands; background long searches; STATUS.md always current.`);
    await session.waitForIdle();
    while (cost() < budget) {
        round++;
        const spent = cost().toFixed(2);
        const pro = proCost().toFixed(2);
        console.error(`[proofs5] nudge ${round}, spent $${spent} of $${budget} (oracle $${pro})`);
        evWrite({ t: "nudge", n: round, spent: Number(spent), budget, oracle: Number(pro) });
        await session.prompt(`Keep going ($${spent} of $${budget} spent, of which oracle $${pro} — pace yourself). Harvest background experiments first. Soundness is the graveyard: keep attacking your own reduction with low-weight cheating solutions before believing any gap. Act on oracle advice with code; record exact failure modes in ORACLE_BRIEF.md before the next call. STATUS.md honest and current; every finite claim needs a passing verify_*.py.`);
        await session.waitForIdle();
    }
    clearInterval(guard);
    const stats = session.getSessionStats();
    console.error(`[proofs5] DONE after ${round} rounds, cost=$${cost().toFixed(2)} (oracle $${proCost().toFixed(2)})`);
    evWrite({ t: "done", rounds: round, cost: Number(cost().toFixed(2)) });
    await reflectAndStore({ model, benchmark: "proofs", problemId: "cvp", score: 0, transcript: `Worker+oracle CVP-hardness run ($${budget} budget, thinking high, oracle=gpt-5.6-sol-pro) in ${dir}: PCP-free polynomial-factor NP-hardness for CVP/NCP from 3SAT. The score field is a placeholder, NOT an outcome; base lessons only on what STATUS.md actually records.` }).catch(() => { });
    process.exit(0);
}
main().catch((e) => { console.error("[proofs5] FATAL", e?.stack || e); process.exit(1); });
