import { describe, expect, it } from "vitest";
import { FEATURE_TO_HASH, getFeatureFromHash } from "./navigation";

describe("navigation utility", () => {
  it("maps feature IDs to their canonical URL hashes", () => {
    expect(FEATURE_TO_HASH.rewrite).toBe("#rewrite");
    expect(FEATURE_TO_HASH.cabinet).toBe("#word-cabinet");
    expect(FEATURE_TO_HASH.monologue).toBe("#inner-monologue");
  });

  it("resolves valid canonical hashes to corresponding feature IDs", () => {
    expect(getFeatureFromHash("#rewrite")).toBe("rewrite");
    expect(getFeatureFromHash("#word-cabinet")).toBe("cabinet");
    expect(getFeatureFromHash("#inner-monologue")).toBe("monologue");
  });

  it("resolves alternative alias hashes gracefully", () => {
    expect(getFeatureFromHash("#cabinet")).toBe("cabinet");
    expect(getFeatureFromHash("#monologue")).toBe("monologue");
  });

  it("handles case-insensitivity in URL hashes", () => {
    expect(getFeatureFromHash("#REWRITE")).toBe("rewrite");
    expect(getFeatureFromHash("#Word-Cabinet")).toBe("cabinet");
    expect(getFeatureFromHash("#INNER-MONOLOGUE")).toBe("monologue");
  });

  it("falls back safely to default studio ('rewrite') on missing or invalid hash", () => {
    expect(getFeatureFromHash("")).toBe("rewrite");
    expect(getFeatureFromHash("#")).toBe("rewrite");
    expect(getFeatureFromHash("#unknown")).toBe("rewrite");
    expect(getFeatureFromHash("#invalid-route")).toBe("rewrite");
  });
});

