/**
 * Agent memory — a claude-mem-style persistent, compressed memory for the OpenRSI
 * solver agents.
 *
 * After each solve the agent REFLECTS its session into 1-2 durable observations
 * ("what worked / what to avoid"), which are appended to a per-benchmark store. On
 * the next problem, relevant observations are RECALLED and injected into the prompt,
 * so knowledge compounds across problems, generations and runs — not just via scaffold
 * rewrites. Dependency-free: keyword/recency/score ranking, no embeddings.
 */
import { appendFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { Type } from "typebox";
import { createAgentSession, defineTool, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";

export interface MemoryItem {
  ts: number;
  benchmark: string;
  problemId: string;
  tags: string[];
  observation: string;
  score: number; // solver fitness at the time (perf / speedup) — weights recall
  genre?: string; // problem genre — same-genre observations are preferred on recall
}

const MEMORY_DIR =
  process.env.OPENRSI_MEMORY_DIR || fileURLToPath(new URL("../../agent/memory", import.meta.url));

function storePath(benchmark: string): string {
  return join(MEMORY_DIR, `${benchmark}.jsonl`);
}

export function loadMemory(benchmark: string): MemoryItem[] {
  const p = storePath(benchmark);
  if (!existsSync(p)) return [];
  return readFileSync(p, "utf8")
    .split("\n")
    .filter(Boolean)
    .map((l) => {
      try {
        return JSON.parse(l) as MemoryItem;
      } catch {
        return null;
      }
    })
    .filter((x): x is MemoryItem => !!x);
}

function appendMemory(m: MemoryItem): void {
  const p = storePath(m.benchmark);
  mkdirSync(dirname(p), { recursive: true });
  appendFileSync(p, JSON.stringify(m) + "\n");
}

/** Recall the most relevant observations for a problem; returns a promptable block. */
export function recall(benchmark: string, problemId: string, k = 6, genre?: string): string {
  const all = loadMemory(benchmark);
  if (!all.length) return "";
  const now = all.reduce((a, m) => Math.max(a, m.ts), 0) || 1;
  const scored = all.map((m) => {
    let s = 0;
    if (m.problemId === problemId) s += 5; // past attempts on THIS problem are gold
    if (genre && m.genre && m.genre === genre) s += 2; // same-genre insights transfer
    s += Math.min(3, m.score / 500); // higher-fitness sessions weigh more
    s += 2 * (m.ts / now); // recency
    return { m, s };
  });
  const top = scored.sort((a, b) => b.s - a.s).slice(0, k).map((x) => x.m);
  if (!top.length) return "";
  const lines = top.map((m) => `- (${m.problemId}) ${m.observation}`);
  return `\n\n## Recalled insights from past sessions (memory)\n${lines.join("\n")}`;
}

/** Reflect a finished session into 1-2 durable observations and store them. */
export async function reflectAndStore(opts: {
  model: Model<any>;
  benchmark: string;
  problemId: string;
  score: number;
  transcript: string; // compact summary: what was tried + the result
  genre?: string;
}): Promise<void> {
  const captured: { items: { observation: string; tags: string[] }[] } = { items: [] };
  const remember = defineTool({
    name: "remember",
    label: "remember",
    description: "Store 1-2 durable, reusable observations from this session (techniques that worked, pitfalls to avoid). Be concrete and transferable to similar problems.",
    parameters: Type.Object({
      observations: Type.Array(
        Type.Object({
          observation: Type.String({ description: "One concrete, reusable insight (<=200 chars)." }),
          tags: Type.Array(Type.String(), { description: "keywords, e.g. ['SA','grid','fusion']" }),
        }),
        { minItems: 1, maxItems: 2 },
      ),
    }),
    async execute(_id, args) {
      captured.items = args.observations;
      return { content: [{ type: "text" as const, text: "stored" }], details: undefined };
    },
  });

  const sys = `You compress a solver agent's session into durable memory for future problems. Extract 1-2 CONCRETE, transferable observations (a technique that helped, a bug that hurt, a parameter that mattered). Avoid vague platitudes. Call remember, then reply DONE.`;
  try {
    const { session } = await createAgentSession({
      model: opts.model,
      thinkingLevel: "low",
      customTools: [remember],
      noTools: "builtin",
      systemPrompt: sys,
      sessionManager: SessionManager.inMemory(process.cwd()),
    } as any);
    await Promise.race([
      (async () => {
        await session.prompt(`Problem ${opts.problemId} (${opts.benchmark}), final score ${opts.score}.\n\nSession summary:\n${opts.transcript}\n\nStore the durable observations now.`);
        await session.waitForIdle();
      })(),
      new Promise<void>((r) => setTimeout(() => { session.abort().catch(() => {}); r(); }, 90000)),
    ]);
  } catch {
    /* memory is best-effort */
  }
  const ts = Date.now();
  for (const it of captured.items) {
    appendMemory({ ts, benchmark: opts.benchmark, problemId: opts.problemId, tags: it.tags || [], observation: it.observation, score: opts.score, genre: opts.genre });
  }
}
