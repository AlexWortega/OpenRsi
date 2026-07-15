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
  // getBuiltinModel is statically typed to known ids; our slug is dynamic -> cast.
  const model = (getBuiltinModel as unknown as (p: string, id: string) => Model<any>)(
    "openrouter",
    slug,
  );
  if (!model) {
    throw new Error(
      `OpenRouter model "${slug}" not found in pi-ai catalog. Check the slug against the catalog.`,
    );
  }
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
