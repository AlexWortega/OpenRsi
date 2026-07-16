/**
 * KernelBench `fast_p`: the fraction of problems that are BOTH correct AND achieve a
 * speedup >= p over the torch reference. This is the canonical KernelBench metric and
 * the fitness the kernel RSI loop selects on (OPENRSI_KB_FITNESS=fast_p, default),
 * so the loop is rewarded for making MORE kernels fast — not one kernel very fast.
 *
 *   fast_0   = fraction correct (speedup >= 0, i.e. just correct)
 *   fast_1.0 = fraction correct AND at least as fast as torch  (headline)
 *   fast_2.0 = fraction correct AND >= 2x torch
 */
import type { SolveResult } from "../inner/solve.js";

/** fast_p over a result set: fraction correct with speedup >= p. */
export function fastP(results: SolveResult[], p = 1.0): number {
  if (!results.length) return 0;
  const hits = results.filter((r) => r.bestValid && (r.performance ?? 0) >= p).length;
  return hits / results.length;
}

export const P_SWEEP = [0, 0.5, 1.0, 2.0];

/** fast_p for each p in the sweep, as a "0:0.75 0.5:0.50 1.0:0.25 2.0:0.00" string. */
export function fastPSweep(results: SolveResult[], sweep: number[] = P_SWEEP): { p: number; value: number }[] {
  return sweep.map((p) => ({ p, value: fastP(results, p) }));
}

export function formatSweep(results: SolveResult[], sweep: number[] = P_SWEEP): string {
  return fastPSweep(results, sweep).map((s) => `fast_${s.p}=${s.value.toFixed(3)}`).join("  ");
}

/** The default kernel-loop fitness: fast_p at the configured threshold (default 1.0). */
export function kernelFitness(results: SolveResult[]): number {
  const mode = (process.env.OPENRSI_KB_FITNESS ?? "fast_p").toLowerCase();
  if (mode === "mean" || mode === "speedup") {
    return results.length ? results.reduce((a, r) => a + (r.performance ?? 0), 0) / results.length : 0;
  }
  const p = Number(process.env.OPENRSI_KB_FASTP_P || 1.0);
  return fastP(results, p);
}
