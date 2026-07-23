/**
 * Model / provider wiring for OpenRSI.
 *
 * pi-ai's built-in OpenRouter provider resolves its key from the OPENROUTER_API_KEY
 * env var (via `envApiKeyAuth`), so we only need the env var set (run node with
 * `--env-file=.env`) and a valid OpenRouter model slug. `getBuiltinModel` returns a
 * fully-formed `Model` that `createAgentSession({ model })` can consume directly.
 */
import { getBuiltinModel } from "@earendil-works/pi-ai/providers/all";
import type { Model } from "@earendil-works/pi-ai";

export type Tier = "inner" | "outer";

const DEFAULTS: Record<Tier, string> = {
  inner: "anthropic/claude-sonnet-5",
  outer: "anthropic/claude-opus-4.8",
};

/** OpenRouter slug for a tier, from env with a sane strong default. */
export function modelSlug(tier: Tier): string {
  const envKey = tier === "inner" ? "OPENRSI_INNER_MODEL" : "OPENRSI_OUTER_MODEL";
  return process.env[envKey]?.trim() || DEFAULTS[tier];
}

/** Build a pi `Model` for the given OpenRouter slug (defaults per tier). */
export function buildModel(slug: string): Model<any> {
  const factory = getBuiltinModel as unknown as (p: string, id: string) => Model<any> | null;
  let model: Model<any> | null = null;
  try {
    model = factory("openrouter", slug);
  } catch {
    model = null;
  }
  if (!model) {
    // Slug not in pi-ai's static catalog (e.g. a newly-listed OpenRouter model like
    // poolside/laguna-s-2.1). Build it by cloning a known OpenRouter model and
    // overriding `id` — the id is the slug sent to OpenRouter, so any live model works.
    const base = factory("openrouter", "anthropic/claude-sonnet-5");
    if (!base) throw new Error(`cannot build OpenRouter model "${slug}" (no base model available)`);
    const reasoning = (process.env.OPENRSI_MODEL_REASONING ?? "off") === "on";
    model = { ...(base as any), id: slug, name: slug, reasoning } as Model<any>;
    process.stderr.write(`[provider] built non-catalog OpenRouter model "${slug}" (reasoning=${reasoning})\n`);
  }
  // Bound per-turn output (any model) so a slow/verbose model can't burn a whole turn on
  // one giant dump — capping maxTokens forces it to commit + run tools incrementally.
  const maxTok = Number(process.env.OPENRSI_MODEL_MAX_TOKENS || 0);
  if (maxTok > 0) (model as any).maxTokens = maxTok;
  return model;
}

export function tierModel(tier: Tier): Model<any> {
  return buildModel(modelSlug(tier));
}

export function assertKey(): void {
  if (!process.env.OPENROUTER_API_KEY) {
    throw new Error(
      "OPENROUTER_API_KEY is not set. Run node with `--env-file=.env` (Node >= 20).",
    );
  }
}
