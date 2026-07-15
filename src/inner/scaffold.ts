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
  domain_knowledge: string[];
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

/** Compose the full solver system prompt from the scaffold. */
export function composeSystemPrompt(s: Scaffold): string {
  const dk = s.domain_knowledge.length
    ? `\n\n## Domain knowledge\n${s.domain_knowledge.map((d) => `- ${d}`).join("\n")}`
    : "";
  return s.system_prompt + dk;
}
