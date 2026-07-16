/**
 * Shared board: durable per-generation records + human-readable leaderboard/findings.
 * The RSI loop checkpoints here every generation so progress survives interruption.
 */
import { appendFileSync, mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

export interface GenRecord {
  gen: number;
  scaffoldVersion: number;
  fitness: number; // primary fitness (ALE: mean perf; kernel: fast_p)
  accepted: boolean;
  champion: boolean;
  rationale: string;
  perProblem: { problemId: string; performance: number | null; rank: number | null; valid: boolean; evalsUsed: number }[];
  cost: number;
  seconds: number;
  /** Optional KernelBench fast_p sweep for this gen's champion results. */
  fastP?: { p: number; value: number }[];
  /** Optional grok-build goal-plan verdict for this generation. */
  goal?: { achieved: boolean; onTrack: boolean; holding: number[]; failing: number[]; steer?: string };
  /** Metric label for the leaderboard header (default "fitness"). */
  metricLabel?: string;
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
    const hasFastP = this.records.some((r) => r.fastP?.length);
    const label = this.records.find((r) => r.metricLabel)?.metricLabel ?? "fitness";
    const lines = [
      `# OpenRSI leaderboard (${label})`,
      "",
      `| rank | gen | scaffold.v | ${label} |${hasFastP ? " fast_p |" : ""} accepted | champion | cost | secs |`,
      `|------|-----|-----------|---------|${hasFastP ? "--------|" : ""}----------|----------|------|------|`,
      ...rows.map((r, i) => {
        const fp = hasFastP ? ` ${(r.fastP ?? []).map((s) => `${s.p}:${s.value.toFixed(2)}`).join(" ") || "-"} |` : "";
        return `| ${i + 1} | ${r.gen} | ${r.scaffoldVersion} | ${r.fitness.toFixed(3)} |${fp} ${r.accepted ? "yes" : "no"} | ${r.champion ? "★" : ""} | $${r.cost.toFixed(2)} | ${r.seconds} |`;
      }),
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
      champ && champ.goal ? `Goal: achieved=${champ.goal.achieved} onTrack=${champ.goal.onTrack} holding=[${champ.goal.holding.join(",")}] failing=[${champ.goal.failing.join(",")}]` : "",
      champ?.goal?.steer ? `Steer: ${champ.goal.steer.slice(0, 200)}` : "",
      "",
      "## Generation log",
      ...this.records.map(
        (r) =>
          `- gen${r.gen} v${r.scaffoldVersion}: fitness=${r.fitness.toFixed(3)} ${r.accepted ? "ACCEPTED" : "rejected"}${r.champion ? " ★champion" : ""}${r.goal ? ` [goal ${r.goal.achieved ? "ACHIEVED" : r.goal.onTrack ? "on-track" : "off-track"}]` : ""} — ${r.rationale.slice(0, 140)}`,
      ),
      "",
      "## Levers (shipped)",
      "- Explicit AIDE draft/improve/debug tree search (OPENRSI_SOLVER=aide).",
      "- Per-genre domain-knowledge routing (scaffold.domain_knowledge_by_genre).",
      "- Scratch bash shell for the inner agent (OPENRSI_SCRATCH=on).",
      "- Multi-candidate generations (OPENRSI_INNER_CANDIDATES best-of-N at the draft root).",
      "- grok-build goal plan + direction checker (goal_plan.json + per-gen verdict above).",
      "- KernelBench fast_p fitness on the RTX PRO 6000 (OPENRSI_KB_FITNESS=fast_p).",
    ];
    writeFileSync(join(this.dir, "FINDINGS.md"), lines.filter((l) => l !== "").join("\n") + "\n");
  }
}
