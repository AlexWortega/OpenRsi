/**
 * Ramsey head-to-head — round 3. ONE problem only (superexponential R_k(3)
 * lower bound), goal-directed and code-first, seeded with the merged output of
 * round 1 and BOTH round-2 campaigns (gpt-5.6-sol and claude-fable-5).
 * Same pi scaffold / events.jsonl / tracehouse bridge as run2.js.
 *
 *   OPENRSI_PROOFS_DIR=... OPENRSI_PROOFS_BUDGET_USD=25 \
 *   [OPENRSI_OUTER_MODEL=anthropic/claude-fable-5] \
 *   node --env-file=.env dist/proofs/run3.js
 */
import { spawn } from "node:child_process";
import { createWriteStream, existsSync, mkdirSync, openSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { createAgentSession, SessionManager } from "@earendil-works/pi-coding-agent";
import { assertKey, modelSlug, tierModel } from "../provider.js";
import { recall, reflectAndStore } from "../memory/memory.js";

const SYS = `You are a research mathematician-programmer working autonomously on ONE research-level problem. Your objective is to ACHIEVE the stated goal — with COMPLETE INTELLECTUAL HONESTY: a claimed proof must actually be a proof; anything less is PARTIAL with the gap stated precisely. Partial results are stepping stones, not deliverables.

THE PROBLEM (the only one this run). Let R_k(3) be the least N such that every k-coloring of the edges of K_N contains a monochromatic triangle. Prove R_k(3) >= (c k^{1/3} / log k)^k for an absolute constant c > 0 — or any superexponential lower bound R_k(3) >= k^{ck}. Equivalent formulation: the Shannon capacity of graphs with independence number 2 is unbounded. Classical state: constructions give R_k(3) >= c^k with c ≈ 3.199 (Schur-type); upper bound R_k(3) <= 3k!.

Goal ladder (value strictly increasing):
(a) an explicit verified coloring whose per-color base (N^(1/k)) exceeds the classical 3.199 — a concrete record;
(b) a coherent construction family whose per-color base PROVABLY grows with k (even k^{c/log k} growth of the base) — major progress;
(c) a full superexponential bound — the goal.
Constant-base families below 3.199 are NOT progress; do not spend budget collecting more of them.

Ground rules:
- These problems were recently solved in a document by another lab ("Ten Advances in Mathematics and Theoretical Computer Science", cdn.openai.com/pdf/ten-proofs-oai.pdf). That document and any copy, mirror, summary, or discussion of its proofs are STRICTLY OFF-LIMITS: do not fetch, search for, or read it or secondary sources describing its arguments. The experiment measures YOUR independent reasoning. Classical literature that predates it is fair game — cite what you use.
- METHOD — CODE FIRST. Before proving a conjecture, test it on small cases; before claiming a construction exists, write a search; before claiming one cannot exist, write an exhaustive check for the smallest open case. Use pysat, OR-tools/pulp, numpy, sympy. Keep expensive searches running in background bash and harvest later. IMPORTANT: background them properly (nohup ... > log 2>&1 &) and NEVER block the session on a long foreground computation — cap every foreground command's runtime.
- NO PROOF ASSISTANTS (no Lean/Coq/Isabelle). Rigor = precise mathematics in proof_ramsey.md + a machine-checkable verify_<claim>.py (exit 0) for every finite claim.
- Work in visible files: NOTES.md (attack log), proof_ramsey.md (current best write-up), STATUS.md (honest one-page assessment, updated at EVERY milestone), experiments/ (all code).
- PRIOR WORK: prior/ contains round 1 (prior/round1/) and two independent round-2 campaigns (prior/sol/, prior/fable/) on this problem. Read their STATUS/notes first; verify what you import.
  Established NEGATIVE results — do NOT re-derive or re-attempt:
  * iid product codes, direct first moment, elementary expurgation, and basic dependency-graph LLL provably cannot beat base 2.
  * Fixed seeds with lexicographic / blow-up / first-difference amplification stay fixed-base exponential.
  * A dozen seed families (cyclic up to Z_2039/9, shifted-cyclic Z_N×[r], dihedral up to order 1024, interval-difference, local-palette hierarchies, SAT-induced structured local colorings, Mycielski/Cayley cube codes) are all banked at per-color base <= 2.63 with doubling scale — asymptotically useless.
  * A ternary (exponent-3) difference construction is impossible: -x = 2x forces the monochromatic triple (x, x, 2x).
  Established POSITIVE tools you may build on (verified in prior/):
  * exact capacity identity: max over alpha(G)<=2 of alpha(G^boxtimes k) = R_k(3+... ) — see prior/round1/proof_ramsey.md for the precise statement;
  * effective-capacity criterion: polynomial witness power + growing per-color base => k^{ck};
  * Grötzsch-complement 12-word cube code (capacity >= 12^(1/3) > sqrt(5)) — the best verified single-graph capacity seed;
  * the open F_2^6 four-color partition question (neither found nor excluded; fixed-layer extension of the F_2^5 partition is impossible).
- Self-verify adversarially; a refereed gap demotes the claim immediately. Independent verifier scripts before any claim is promoted.
- Budget discipline: fixed USD budget. Spend it where the goal ladder points: correlated/algebraic constructions whose base can grow — e.g. correlated strong-power codes beating independent repetition, palettes over growing algebraic structures (fields, nilpotent/solvable groups beyond the failed dihedral/abelian ones), recursive constructions with super-multiplicative color reuse, capacity lower bounds for independence-2 graphs beyond single fixed seeds, or settling F_2^6/4-color with SAT + symmetry breaking if you can make it decisive for a scalable family. Let code discriminate between routes fast, then prove what survives.`;

async function main() {
    assertKey();
    const dir = process.env.OPENRSI_PROOFS_DIR || "/home/alexw/OpenRsi/runs/ramsey_sol";
    mkdirSync(dir, { recursive: true });
    const budget = Number(process.env.OPENRSI_PROOFS_BUDGET_USD || 25);
    const model = tierModel("outer");
    console.error(`[proofs3] model=openrouter:${modelSlug("outer")} dir=${dir} budget=$${budget}`);
    const mem = recall("proofs", "ramsey", 8);
    // pi has no systemPrompt option; project instructions load from AGENTS.md in cwd.
    writeFileSync(join(dir, "AGENTS.md"), SYS + mem);
    // Full event stream for the tracehouse bridge; header written synchronously
    // BEFORE the bridge spawns so it never falls back to bare-log parsing.
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
        ts: new Date().toISOString(), t: "header", variant: "proofs3",
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
            console.error(`[proofs3] tracehouse bridge pid=${child.pid} project=${process.env.TRACEHOUSE_PROJECT || "rsi-proffer"}`);
        }
        else {
            console.error(`[proofs3] tracehouse bridge NOT started (missing ${py} or ${bridge})`);
        }
    }
    catch (e) {
        console.error(`[proofs3] tracehouse bridge failed: ${e?.message ?? e}`);
    }
    const { session } = await createAgentSession({
        model,
        thinkingLevel: (process.env.OPENRSI_MLXFAST_THINKING || "medium"),
        cwd: dir,
        sessionManager: SessionManager.inMemory(dir),
    });
    session.subscribe((e) => {
        if (e.type === "tool_execution_start") {
            process.stderr.write(`[proofs3 ${new Date().toISOString().slice(11, 19)}] tool ${e.toolName ?? e.name ?? "?"}\n`);
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

Begin. First read prior/round1/, prior/sol/, prior/fable/ (STATUS files first) and rerun the verifiers you intend to rely on. Then set up STATUS.md / NOTES.md / experiments/, pick the 2-3 routes with the best chance of a GROWING base per the goal ladder, and state for each the first discriminating experiment. Start experiments immediately — at least one background search running within your first few rounds, always with bounded foreground commands. No Lean; no peeking at the ten-proofs document or coverage of it; adversarial self-refereeing; STATUS.md always current.`);
    await session.waitForIdle();
    let round = 0;
    while (cost() < budget) {
        round++;
        const spent = cost().toFixed(2);
        console.error(`[proofs3] nudge ${round}, spent $${spent} of $${budget}`);
        evWrite({ t: "nudge", n: round, spent: Number(spent), budget });
        await session.prompt(`Keep going ($${spent} of $${budget} spent — pace yourself). Harvest background experiments first; let results pick the next step. Re-referee new claims adversarially. Remember the goal ladder: growing base or bust — bank-and-switch away from any route that converges to a constant base. Keep STATUS.md honest and current; every finite claim needs a passing verify_*.py.`);
        await session.waitForIdle();
    }
    const stats = session.getSessionStats();
    console.error(`[proofs3] DONE after ${round} rounds, cost=$${(stats?.cost ?? 0).toFixed(2)}`);
    evWrite({ t: "done", rounds: round, cost: Number((stats?.cost ?? 0).toFixed(2)) });
    await reflectAndStore({ model, benchmark: "proofs", problemId: "ramsey", score: 0, transcript: `Ramsey-only head-to-head run ($${budget} budget) on superexponential R_k(3) lower bounds in ${dir}, seeded from round 1 + both round-2 campaigns. The score field is a placeholder, NOT an outcome; base lessons only on what STATUS.md actually records as proved/partial.` }).catch(() => { });
    process.exit(0);
}
main().catch((e) => { console.error("[proofs3] FATAL", e?.stack || e); process.exit(1); });
