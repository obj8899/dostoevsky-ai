import type { FeatureId } from "../components/FeatureNav";

export const FEATURE_TO_HASH: Record<FeatureId, string> = {
  rewrite: "#rewrite",
  cabinet: "#word-cabinet",
  monologue: "#inner-monologue",
};

export const HASH_MAP: Record<string, FeatureId> = {
  "#rewrite": "rewrite",
  "#word-cabinet": "cabinet",
  "#cabinet": "cabinet",
  "#inner-monologue": "monologue",
  "#monologue": "monologue",
};

export function getFeatureFromHash(hash: string): FeatureId {
  const normalized = hash.toLowerCase();
  return HASH_MAP[normalized] ?? "rewrite";
}

