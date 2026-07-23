/**
 * De-noise the RSI result: run the baseline (v0) and champion (evolved) scaffolds
 * through N independent agent solves each (same fixed compute budget), across a pool
 * of GPUs, and report mean±std skill so the baseline→champion delta can be read
 * against its noise band.
 *
 *   OPENRSI_SEEDS=5 OPENRSI_WB_TRAIN_S=120 OPENRSI_WB_GPUS=3,2 \
 *   WB_BASE=agent/weather/scaffold.json WB_CHAMP=/mnt/storage/wb2/run_10gen/champion_scaffold.json \
 *     node --env-file=.env dist/weather/seedSweep.js
 */
import { writeFileSync } from "node:fs";
import { loadScaffold } from "../inner/scaffold.js";
import { assertKey, modelSlug, tierModel } from "../provider.js";
import { WeatherEvalServer } from "./evalClient.js";
import { solveWeather } from "./solve.js";

function stats(xs: number[]) {
  const n = xs.length;
  const mean = xs.reduce((a, b) => a + b, 0) / n;
  const sd = Math.sqrt(xs.reduce((a, b) => a + (b - mean) ** 2, 0) / Math.max(1, n - 1));
  return { mean, sd, min: Math.min(...xs), max: Math.max(...xs), n };
}

async function main() {
  assertKey();
  const N = Number(process.env.OPENRSI_SEEDS || 5);
  const trainS = Number(process.env.OPENRSI_WB_TRAIN_S || 120);
  const gpus = (process.env.OPENRSI_WB_GPUS || "3").split(",").map((s) => s.trim()).filter(Boolean);
  const model = tierModel("inner");
  const base = process.env.WB_BASE || new URL("../../agent/weather/scaffold.json", import.meta.url).pathname;
  // OPENRSI_AB_RECON=1 → A/B "submit-only vs full pi coding agent" on the SAME scaffold
  // (isolates the effect of giving the inner agent real bash/read/edit/write tools).
  const scaffolds =
    process.env.OPENRSI_AB_RECON === "1"
      ? [
          { name: "submit_only", path: base, recon: false },
          { name: "full_coding_agent", path: base, recon: true },
        ]
      : [
          { name: "baseline_v0", path: base, recon: undefined as boolean | undefined },
          { name: "champion", path: process.env.WB_CHAMP || "/mnt/storage/wb2/run_10gen/champion_scaffold.json", recon: undefined as boolean | undefined },
        ];
  console.error(`[sweep] inner=${modelSlug("inner")} seeds=${N} trainS=${trainS} gpus=${gpus.join(",")} mode=${process.env.OPENRSI_AB_RECON === "1" ? "recon-AB" : "scaffold-AB"}`);

  type Task = { scaf: string; path: string; seed: number; recon?: boolean };
  const tasks: Task[] = scaffolds.flatMap((s) => Array.from({ length: N }, (_, i) => ({ scaf: s.name, path: s.path, seed: i, recon: s.recon })));
  const results: Record<string, { skill: number; z500: number; t850: number; err?: string }[]> = {};
  for (const s of scaffolds) results[s.name] = [];

  // GPU-pinned worker pool: one worker per gpu, pulls tasks off the queue.
  let idx = 0;
  const runWorker = async (gpu: string) => {
    while (true) {
      const my = idx++;
      if (my >= tasks.length) break;
      const t = tasks[my];
      const server = new WeatherEvalServer(trainS, gpu);
      try {
        const r = await solveWeather({ server, scaffold: loadScaffold(t.path), model, recon: t.recon });
        const z = r.privateJudge?.match(/z500=([\d.]+)/)?.[1];
        const tt = r.privateJudge?.match(/t850=([\d.]+)/)?.[1];
        results[t.scaf].push({ skill: r.performance ?? 0, z500: z ? +z : NaN, t850: tt ? +tt : NaN, err: r.error });
        console.error(`[sweep gpu${gpu}] ${t.scaf} seed${t.seed}: skill=${(r.performance ?? 0).toFixed(4)} (${r.privateJudge ?? ""})${r.error ? " ERR=" + r.error : ""}`);
      } catch (e: any) {
        results[t.scaf].push({ skill: 0, z500: NaN, t850: NaN, err: e?.message || String(e) });
        console.error(`[sweep gpu${gpu}] ${t.scaf} seed${t.seed}: FAILED ${e?.message || e}`);
      }
    }
  };
  await Promise.all(gpus.map((g) => runWorker(g)));

  const lines = ["# WeatherBench-2 seed sweep — de-noised baseline vs champion", "", `${N} seeds/scaffold, fixed ${trainS}s compute, inner=${modelSlug("inner")}`, ""];
  const summary: Record<string, any> = {};
  for (const s of scaffolds) {
    const rs = results[s.name];
    const sk = stats(rs.map((r) => r.skill));
    const z = stats(rs.map((r) => r.z500).filter((x) => !isNaN(x)));
    const t = stats(rs.map((r) => r.t850).filter((x) => !isNaN(x)));
    summary[s.name] = { skill: sk, z500: z, t850: t, raw: rs.map((r) => r.skill) };
    lines.push(`## ${s.name}`);
    lines.push(`- skill: **${sk.mean.toFixed(4)} ± ${sk.sd.toFixed(4)}**  (min ${sk.min.toFixed(4)}, max ${sk.max.toFixed(4)}, n=${sk.n})`);
    lines.push(`- z500 RMSE: ${z.mean.toFixed(1)} ± ${z.sd.toFixed(1)}   t850 RMSE: ${t.mean.toFixed(3)} ± ${t.sd.toFixed(3)}`);
    lines.push(`- raw skills: ${rs.map((r) => r.skill.toFixed(3)).join(", ")}`);
    lines.push("");
  }
  const b = summary[scaffolds[0].name].skill, c = summary[scaffolds[1].name].skill;
  const pooledSd = Math.sqrt((b.sd ** 2 + c.sd ** 2) / 2);
  const delta = c.mean - b.mean;
  lines.push(`## Verdict`);
  lines.push(`Δ(champion − baseline) skill = **${delta >= 0 ? "+" : ""}${delta.toFixed(4)}**  (pooled sd ≈ ${pooledSd.toFixed(4)}, ~${(delta / (pooledSd || 1e-9)).toFixed(2)}σ)`);
  lines.push(delta > pooledSd ? "→ champion beats baseline by more than ~1 pooled sd — the gain looks real." : "→ delta is within ~1 pooled sd — not clearly above the noise; needs more seeds/compute.");
  const out = lines.join("\n") + "\n";
  writeFileSync(process.env.OPENRSI_SWEEP_OUT || "/mnt/storage/wb2/sweep_RESULTS.md", out);
  writeFileSync(process.env.OPENRSI_SWEEP_JSON || "/mnt/storage/wb2/sweep.json", JSON.stringify(summary, null, 2) + "\n");
  console.error("\n" + out);
  console.error("[sweep] DONE");
  process.exit(0);
}
main().catch((e) => { console.error("[sweep] FATAL:", e?.stack || e); process.exit(1); });
