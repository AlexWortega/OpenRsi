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
  valid: boolean;
  score: number;
  feedback: string;
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

/** Grow an AIDE search tree. Returns the best (valid, else last) solution found. */
export async function solveAideTree(opts: {
  budget: number;
  draftN: number;
  patience: number;
  epsilon?: number; // explore probability when the best node is already valid
  /** Produce code for a node given its kind and (for improve/debug) the parent node. */
  generate: (kind: NodeKind, parent: AideNode | null) => Promise<{ code: string; cost: number }>;
  /** Score a node's code (compile/correctness/quality). */
  evalFn: (code: string) => Promise<AideEval>;
  log?: (m: string) => void;
}): Promise<AideTreeResult> {
  const { budget, patience } = opts;
  const epsilon = opts.epsilon ?? Number(process.env.OPENRSI_AIDE_EPSILON || 0.3);
  const nodes: AideNode[] = [];
  let evalsUsed = 0;
  let cost = 0;
  let nextId = 0;

  const bestNode = (): AideNode | null => {
    const valid = nodes.filter((n) => n.valid);
    if (valid.length) return valid.reduce((a, b) => (b.score > a.score ? b : a));
    return nodes.length ? nodes.reduce((a, b) => (b.score > a.score ? b : a)) : null;
  };

  const makeNode = async (kind: NodeKind, parent: AideNode | null): Promise<AideNode> => {
    const g = await opts.generate(kind, parent);
    cost += g.cost;
    let ev: AideEval;
    try {
      ev = g.code ? await opts.evalFn(g.code) : { valid: false, score: 0, feedback: "(no code produced)", error: "empty" };
    } catch (e: any) {
      ev = { valid: false, score: 0, feedback: `eval error: ${e?.message || e}`, error: String(e?.message || e) };
    }
    evalsUsed++;
    const node: AideNode = { id: nextId++, kind, parentId: parent?.id ?? null, code: g.code, valid: ev.valid, score: ev.score, feedback: ev.feedback };
    nodes.push(node);
    opts.log?.(`node#${node.id} ${kind}${parent ? "<-#" + parent.id : ""}: valid=${node.valid} score=${node.score.toFixed(3)} (${evalsUsed}/${budget})`);
    return node;
  };

  // ---- draft phase: best-of-N parallel roots ----
  const draftCount = Math.min(Math.max(1, opts.draftN), budget);
  await Promise.all(Array.from({ length: draftCount }, () => makeNode("draft", null)));

  // ---- search phase ----
  let prevBest = bestNode()?.score ?? 0;
  let sinceImprove = 0;
  while (evalsUsed < budget && sinceImprove < patience) {
    const best = bestNode();
    let kind: NodeKind;
    let parent: AideNode | null;
    if (!best || !best.valid) {
      kind = "debug";
      parent = best;
    } else if (Math.random() < epsilon) {
      kind = "draft";
      parent = null;
    } else {
      kind = "improve";
      parent = best;
    }
    await makeNode(kind, parent);
    const curBest = bestNode()?.score ?? 0;
    if (curBest > prevBest) { prevBest = curBest; sinceImprove = 0; } else { sinceImprove++; }
  }

  const best = bestNode();
  return {
    bestCode: best?.code ?? "",
    bestValid: best?.valid ?? false,
    bestScore: best?.score ?? 0,
    nodes,
    evalsUsed,
    cost,
  };
}
