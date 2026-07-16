/**
 * Per-genre routing: classify a benchmark problem into a coarse "genre" so the
 * scaffold can inject genre-specific domain knowledge (and memory can prefer
 * same-genre observations). One cheap LLM classification per problem, cached to
 * disk so it costs nothing on repeat.
 */
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { Type } from "typebox";
import { createAgentSession, defineTool, SessionManager } from "@earendil-works/pi-coding-agent";
import type { Model } from "@earendil-works/pi-ai";

export const GENRES: Record<string, string[]> = {
  ale: ["grid", "graph", "scheduling", "geometry", "permutation", "construction", "other"],
  kernel: ["elementwise", "reduction", "matmul", "conv", "fusion", "other"],
  mega: ["fusion", "other"],
};

const CACHE_DIR =
  process.env.OPENRSI_MEMORY_DIR || fileURLToPath(new URL("../agent/memory", import.meta.url));

function cachePath(benchmark: string): string {
  return join(CACHE_DIR, `genre_${benchmark}.json`);
}

function loadCache(benchmark: string): Record<string, string> {
  const p = cachePath(benchmark);
  if (!existsSync(p)) return {};
  try {
    return JSON.parse(readFileSync(p, "utf8")) as Record<string, string>;
  } catch {
    return {};
  }
}

function saveCache(benchmark: string, cache: Record<string, string>): void {
  const p = cachePath(benchmark);
  mkdirSync(dirname(p), { recursive: true });
  writeFileSync(p, JSON.stringify(cache, null, 2) + "\n");
}

/** The list of genres valid for a benchmark (default: ["other"]). */
export function genresFor(benchmark: string): string[] {
  return GENRES[benchmark] ?? ["other"];
}

/**
 * Classify a problem into one genre from `genresFor(benchmark)`. Result is cached
 * per (benchmark, problemId). Returns "other" if disabled or on any failure.
 */
export async function classifyGenre(opts: {
  model: Model<any>;
  benchmark: string;
  problemId: string;
  text: string; // problem statement / reference source (excerpt is fine)
}): Promise<string> {
  if ((process.env.OPENRSI_GENRE ?? "on") === "off") return "other";
  const genres = genresFor(opts.benchmark);
  const cache = loadCache(opts.benchmark);
  if (cache[opts.problemId] && genres.includes(cache[opts.problemId])) return cache[opts.problemId];

  let picked = "other";
  try {
    const captured: { genre: string } = { genre: "other" };
    const setGenre = defineTool({
      name: "set_genre",
      label: "set_genre",
      description: "Record the single best-fitting genre for this problem.",
      parameters: Type.Object({
        genre: Type.String({ description: `Exactly one of: ${genres.join(", ")}` }),
      }),
      async execute(_id, args) {
        captured.genre = args.genre;
        return { content: [{ type: "text" as const, text: "recorded" }], details: undefined };
      },
    });
    const sys = `You are a triage classifier. Read a ${opts.benchmark} problem and pick the ONE genre that best matches its dominant structure. Valid genres: ${genres.join(", ")}. Call set_genre once, then reply DONE.`;
    const { session } = await createAgentSession({
      model: opts.model,
      thinkingLevel: "low",
      customTools: [setGenre],
      noTools: "builtin",
      systemPrompt: sys,
      sessionManager: SessionManager.inMemory(process.cwd()),
    } as any);
    await Promise.race([
      (async () => {
        await session.prompt(`Problem ${opts.problemId}:\n\n${opts.text.slice(0, 4000)}\n\nPick the genre.`);
        await session.waitForIdle();
      })(),
      new Promise<void>((r) => setTimeout(() => { session.abort().catch(() => {}); r(); }, 60000)),
    ]);
    picked = genres.includes(captured.genre) ? captured.genre : "other";
  } catch {
    picked = "other";
  }
  cache[opts.problemId] = picked;
  saveCache(opts.benchmark, cache);
  return picked;
}
