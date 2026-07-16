/**
 * The inner solver's SCAFFOLD — the mutable artifact the outer RSI loop rewrites.
 *
 * It is stored as JSON (agent/inner/scaffold.json) because the outer agent edits it
 * with the `edit`/`write` tools; keeping it as data (prompt + strategy params +
 * domain knowledge) rather than executable code makes rewrites safe (no compile /
 * injection surface) while still capturing the substance AIDE² actually evolved:
 * the system prompt, the search policy, and injected domain knowledge.
 */
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

export interface Scaffold {
  version: number;
  language: string;
  max_public_evals: number;
  system_prompt: string;
  /** Always-on general tips, injected for every problem. */
  domain_knowledge: string[];
  /**
   * Optional per-genre tips: only the tips whose genre matches the current problem
   * are injected (in addition to the general `domain_knowledge`). Backward
   * compatible — an absent map behaves exactly like the old flat scaffold.
   */
  domain_knowledge_by_genre?: Record<string, string[]>;
}

export const SCAFFOLD_PATH =
  process.env.OPENRSI_SCAFFOLD ||
  fileURLToPath(new URL("../../agent/inner/scaffold.json", import.meta.url));

export function loadScaffold(path: string = SCAFFOLD_PATH): Scaffold {
  const raw = JSON.parse(readFileSync(path, "utf8"));
  return raw as Scaffold;
}

export function saveScaffold(s: Scaffold, path: string = SCAFFOLD_PATH): void {
  writeFileSync(path, JSON.stringify(s, null, 2) + "\n");
}

/**
 * Compose the full solver system prompt from the scaffold. When `genre` is given
 * and the scaffold has a matching bucket in `domain_knowledge_by_genre`, those tips
 * are appended after the general ones (per-genre routing).
 */
export function composeSystemPrompt(s: Scaffold, genre?: string): string {
  const general = s.domain_knowledge ?? [];
  const genreTips = genre ? s.domain_knowledge_by_genre?.[genre] ?? [] : [];
  const dk = general.length
    ? `\n\n## Domain knowledge\n${general.map((d) => `- ${d}`).join("\n")}`
    : "";
  const gk = genreTips.length
    ? `\n\n## Domain knowledge for ${genre} problems\n${genreTips.map((d) => `- ${d}`).join("\n")}`
    : "";
  return s.system_prompt + dk + gk;
}
