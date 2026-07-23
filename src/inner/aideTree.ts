/**
 * Explicit AIDE draft/improve/debug tree search (opt-in via OPENRSI_SOLVER=aide).
 *
 * The classic AIDE inner loop, made explicit: instead of one agent iterating with a
 * "nudge" loop, we grow a small search tree of solution nodes.
 *
 *   - draft   : generate a fresh candidate from scratch (root). We draft several in
 *               parallel (multi-candidate) and keep the best — best-of-N at the root.
 *   - improve : take the best VALID node and refine it (deeper search / better code).
 *   - debug   : take a buggy node (did not compile / invalid / scored 0) and fix it.
 *
 * Policy each step: if the best node is invalid -> debug it; else with prob epsilon
 * draft a new root (explore), otherwise improve the best (exploit). Budget = number
 * of evals (same budget the nudge path spends). Each node costs exactly one eval.
 *
 * This module is bench-agnostic: the caller supplies `generate` (produce code for a
 * node) and `evalFn` (score code). ALE and KernelBench both reuse it.
 */
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { Type } from "typebox";
import { createAgentSession, defineTool, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";

export const SCRATCH_ON = (process.env.OPENRSI_SCRATCH ?? "off") === "on";

export interface AideEval {
  valid: boolean;
  score: number; // higher = better AFTER the caller normalizes minimize problems
  feedback: string;
  error?: string;
}

export type NodeKind = "draft" | "improve" | "debug";

export interface AideNode {
  id: number;
  kind: NodeKind;
  parentId: number | null;
  code: string;
  valid: boolean; // AIDE: !is_buggy
  score: number;
  feedback: string; // AIDE: analysis / exec output
  plan: string; // short natural-language design (leading comment/docstring proxy)
  debugDepth: number; // AIDE: consecutive-debug counter; capped by max_debug_depth
}

export interface AideTreeResult {
  bestCode: string;
  bestValid: boolean;
  bestScore: number;
  nodes: AideNode[];
  evalsUsed: number;
  cost: number;
}

/**
 * Run ONE agent turn to produce a complete solution via a `write_solution` tool.
 * When scratch mode is on, the agent also gets pi's built-in bash/read/write/edit
 * scoped to a throwaway temp dir, so it can compile & test locally (for free) before
 * committing the solution. The eval/`submit` budget is spent only by the caller.
 */
export async function generateSolution(opts: {
  model: Model<any>;
  language: string;
  systemPrompt: string;
  userPrompt: string;
  scratch?: boolean;
  thinkingLevel?: "low" | "medium" | "high";
  timeoutMs?: number;
  log?: (m: string) => void;
}): Promise<{ code: string; cost: number }> {
  const scratch = opts.scratch ?? SCRATCH_ON;
  const captured: { code: string } = { code: "" };
  const write = defineTool({
    name: "write_solution",
    label: "write_solution",
    description:
      "Commit your COMPLETE solution source (single file). Call this exactly once when your solution is ready; it does NOT run or score the code.",
    parameters: Type.Object({
      code: Type.String({ description: "Complete source (a single file) in " + opts.language }),
    }),
    async execute(_id, { code }) {
      captured.code = code;
      return { content: [{ type: "text" as const, text: "solution recorded" }], details: undefined };
    },
  });

  let scratchDir: string | undefined;
  const sessionOpts: any = {
    model: opts.model,
    thinkingLevel: opts.thinkingLevel ?? "low",
    customTools: [write],
    systemPrompt: opts.systemPrompt,
  };
  if (scratch) {
    scratchDir = mkdtempSync(join(tmpdir(), "openrsi-scratch-"));
    sessionOpts.cwd = scratchDir; // built-in bash/read/write/edit operate here
    sessionOpts.sessionManager = SessionManager.inMemory(scratchDir);
    // NOTE: no `noTools` -> built-in tools (read, bash, edit, write) stay enabled.
  } else {
    sessionOpts.noTools = "builtin";
    sessionOpts.sessionManager = SessionManager.inMemory(process.cwd());
  }

  const timeoutMs = opts.timeoutMs ?? Number(process.env.OPENRSI_NODE_TIMEOUT_S || 180) * 1000;
  let cost = 0;
  try {
    const { session } = await createAgentSession(sessionOpts);
    const hint = scratch
      ? "\n\nYou have a scratch shell (bash/read/write/edit) in a private temp dir. Use it to compile and test locally BEFORE committing. Then call write_solution with the final source."
      : "\n\nWhen ready, call write_solution with the final source.";
    await Promise.race([
      (async () => { await session.prompt(opts.userPrompt + hint); await session.waitForIdle(); })(),
      new Promise<void>((r) => setTimeout(() => { session.abort().catch(() => {}); r(); }, timeoutMs)),
    ]);
    const stats = session.getSessionStats() as any;
    cost = stats?.cost ?? 0;
  } catch (e: any) {
    opts.log?.(`generateSolution error: ${e?.message || e}`);
  } finally {
    if (scratchDir) { try { rmSync(scratchDir, { recursive: true, force: true }); } catch { /* best effort */ } }
  }
  return { code: captured.code, cost };
}

/** A short plan proxy: leading comment/docstring, else the first code line. */
function planOf(code: string): string {
  const lines = code.split("\n").map((l) => l.trim()).filter(Boolean);
  const lead = lines.find((l) => l.startsWith("#") || l.startsWith("//") || l.startsWith('"""') || l.startsWith("/*"));
  return (lead ?? lines[0] ?? "").replace(/^[#/*"\s]+/, "").slice(0, 160);
}

/**
 * Journal summary (AIDE `generate_summary`): the memory of prior GOOD attempts fed to
 * every draft/improve/debug so the model builds on the whole tree, not just its parent.
 */
function generateSummary(nodes: AideNode[]): string {
  const good = nodes.filter((n) => n.valid).sort((a, b) => b.score - a.score).slice(0, 6);
  if (!good.length) return "";
  const lines = good.map((n) => `- (score ${n.score.toFixed(3)}) ${n.plan || "attempt #" + n.id}${n.feedback ? " — " + n.feedback.replace(/\s+/g, " ").slice(0, 120) : ""}`);
  return `\n\n## Prior working attempts (memory — build on the best, don't repeat these)\n${lines.join("\n")}`;
}

/**
 * Grow an AIDE search tree with the wecoai/aideml policy: draft until `num_drafts`,
 * then with prob `debug_prob` debug a still-fixable buggy leaf (depth < `max_debug_depth`),
 * else greedily improve the best good node. Journal memory of prior good nodes is fed
 * into every generation. Returns the best (valid, else last) solution found.
 */
export async function solveAideTree(opts: {
  budget: number;
  draftN: number;
  patience: number;
  numDrafts?: number; // AIDE search.num_drafts
  debugProb?: number; // AIDE search.debug_prob
  maxDebugDepth?: number; // AIDE search.max_debug_depth
  /** Produce code for a node given its kind, parent, and the journal memory string. */
  generate: (kind: NodeKind, parent: AideNode | null, memory: string) => Promise<{ code: string; cost: number }>;
  /** Score a node's code (compile/correctness/quality). */
  evalFn: (code: string) => Promise<AideEval>;
  log?: (m: string) => void;
}): Promise<AideTreeResult> {
  const { budget, patience } = opts;
  const numDrafts = opts.numDrafts ?? Number(process.env.OPENRSI_AIDE_NUM_DRAFTS || Math.max(1, opts.draftN));
  const debugProb = opts.debugProb ?? Number(process.env.OPENRSI_AIDE_DEBUG_PROB || 0.5);
  const maxDebugDepth = opts.maxDebugDepth ?? Number(process.env.OPENRSI_AIDE_MAX_DEBUG_DEPTH || 3);
  const nodes: AideNode[] = [];
  let evalsUsed = 0;
  let cost = 0;
  let nextId = 0;

  const bestGood = (): AideNode | null => {
    const good = nodes.filter((n) => n.valid);
    return good.length ? good.reduce((a, b) => (b.score > a.score ? b : a)) : null;
  };
  const bestNode = (): AideNode | null => bestGood() ?? (nodes.length ? nodes.reduce((a, b) => (b.score > a.score ? b : a)) : null);
  const isLeaf = (n: AideNode) => !nodes.some((c) => c.parentId === n.id);
  const draftCount = () => nodes.filter((n) => n.kind === "draft").length;

  const makeNode = async (kind: NodeKind, parent: AideNode | null): Promise<AideNode> => {
    const g = await opts.generate(kind, parent, generateSummary(nodes));
    cost += g.cost;
    let ev: AideEval;
    try {
      ev = g.code ? await opts.evalFn(g.code) : { valid: false, score: 0, feedback: "(no code produced)", error: "empty" };
    } catch (e: any) {
      ev = { valid: false, score: 0, feedback: `eval error: ${e?.message || e}`, error: String(e?.message || e) };
    }
    evalsUsed++;
    const debugDepth = kind === "debug" && parent ? parent.debugDepth + 1 : 0;
    const node: AideNode = { id: nextId++, kind, parentId: parent?.id ?? null, code: g.code, valid: ev.valid, score: ev.score, feedback: ev.feedback, plan: planOf(g.code), debugDepth };
    nodes.push(node);
    opts.log?.(`node#${node.id} ${kind}${parent ? "<-#" + parent.id : ""}${debugDepth ? " d" + debugDepth : ""}: valid=${node.valid} score=${node.score.toFixed(3)} (${evalsUsed}/${budget})`);
    return node;
  };

  // ---- draft phase: best-of-N parallel roots ----
  const initialDrafts = Math.min(Math.max(1, opts.draftN), budget);
  await Promise.all(Array.from({ length: initialDrafts }, () => makeNode("draft", null)));

  // ---- AIDE search policy ----
  let prevBest = bestNode()?.score ?? 0;
  let sinceImprove = 0;
  while (evalsUsed < budget && sinceImprove < patience) {
    let kind: NodeKind;
    let parent: AideNode | null;
    if (draftCount() < numDrafts) {
      kind = "draft"; parent = null;
    } else {
      const debuggable = nodes.filter((n) => !n.valid && isLeaf(n) && n.debugDepth < maxDebugDepth);
      if (debuggable.length && Math.random() < debugProb) {
        kind = "debug"; parent = debuggable[Math.floor(Math.random() * debuggable.length)];
      } else {
        const good = bestGood();
        if (good) { kind = "improve"; parent = good; } else { kind = "draft"; parent = null; }
      }
    }
    await makeNode(kind, parent);
    const curBest = bestNode()?.score ?? 0;
    if (curBest > prevBest) { prevBest = curBest; sinceImprove = 0; } else { sinceImprove++; }
  }

  const best = bestNode();
  return { bestCode: best?.code ?? "", bestValid: best?.valid ?? false, bestScore: best?.score ?? 0, nodes, evalsUsed, cost };
}
