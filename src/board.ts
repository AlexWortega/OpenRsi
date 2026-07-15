/**
 * Shared board: durable per-generation records + human-readable leaderboard/findings.
 * The RSI loop checkpoints here every generation so progress survives interruption.
 */
import { appendFileSync, mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

export interface GenRecord {
  gen: number;
  scaffoldVersion: number;
  fitness: number; // mean private performance over the problem set
  accepted: boolean;
  champion: boolean;
  rationale: string;
  perProblem: { problemId: string; performance: number | null; rank: number | null; valid: boolean; evalsUsed: number }[];
  cost: number;
  seconds: number;
}

export class Board {
  readonly dir: string;
  private records: GenRecord[] = [];
  constructor(runDir: string) {
    this.dir = runDir;
    mkdirSync(runDir, { recursive: true });
  }

  append(rec: GenRecord): void {
    this.records.push(rec);
    appendFileSync(join(this.dir, "board.jsonl"), JSON.stringify(rec) + "\n");
    this.writeLeaderboard();
    this.writeFindings();
  }

  private writeLeaderboard(): void {
    const rows = [...this.records].sort((a, b) => b.fitness - a.fitness);
    const lines = [
      "# OpenRSI leaderboard (ALE-Bench Lite, mean private performance)",
      "",
      "| rank | gen | scaffold.v | fitness | accepted | champion | cost | secs |",
      "|------|-----|-----------|---------|----------|----------|------|------|",
      ...rows.map(
        (r, i) =>
          `| ${i + 1} | ${r.gen} | ${r.scaffoldVersion} | ${r.fitness.toFixed(1)} | ${r.accepted ? "yes" : "no"} | ${r.champion ? "★" : ""} | $${r.cost.toFixed(2)} | ${r.seconds} |`,
      ),
    ];
    writeFileSync(join(this.dir, "leaderboard.md"), lines.join("\n") + "\n");
  }

  private writeFindings(): void {
    const champ = [...this.records].filter((r) => r.champion).sort((a, b) => b.gen - a.gen)[0];
    const gen0 = this.records.find((r) => r.gen === 0);
    const lines: string[] = [
      "# OpenRSI findings (shared board)",
      "",
      `Generations run: ${this.records.length ? Math.max(...this.records.map((r) => r.gen)) : 0}`,
      gen0 ? `Baseline (gen-0) fitness: ${gen0.fitness.toFixed(1)}` : "",
      champ ? `Current champion: gen${champ.gen} scaffold.v${champ.scaffoldVersion} fitness=${champ.fitness.toFixed(1)}` : "",
      gen0 && champ ? `RSI delta: ${(champ.fitness - gen0.fitness >= 0 ? "+" : "")}${(champ.fitness - gen0.fitness).toFixed(1)} over baseline` : "",
      "",
      "## Generation log",
      ...this.records.map(
        (r) =>
          `- gen${r.gen} v${r.scaffoldVersion}: fitness=${r.fitness.toFixed(1)} ${r.accepted ? "ACCEPTED" : "rejected"}${r.champion ? " ★champion" : ""} — ${r.rationale.slice(0, 140)}`,
      ),
      "",
      "## Next levers (climb on stagnation)",
      "- Explicit AIDE tree search (draft/improve/debug nodes) instead of single-agent refinement.",
      "- Per-problem specialization: route domain knowledge by problem genre.",
      "- Give the inner agent a scratch bash tool to test locally before submit.",
      "- Multi-candidate per generation + pick best (widen the outer search).",
    ];
    writeFileSync(join(this.dir, "FINDINGS.md"), lines.filter((l) => l !== "").join("\n") + "\n");
  }
}
