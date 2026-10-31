import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import {
  evaluateHealthStatus,
  fetchHealth,
  generateInnerMonologue,
  openWordCabinet,
  rewriteLiteraryText,
  type HealthResponse,
} from "./client";

const rewriteResponse = {
  original_text: "The room was quiet.",
  rewritten_text: "The silent room waited.",
  word_count: 4,
  model: "dostoevsky-baseline:latest",
  validation_warnings: [],
};

const wordCabinetResponse = {
  context: "Conflicted feelings",
  words: [
    {
      word: "ambivalence",
      part_of_speech: "noun",
      definition: "The coexistence of opposing feelings.",
      connotation: "Often suggests unresolved tension.",
      intensity: 3,
      distinction: "Unlike uncertainty, it involves two simultaneous attitudes.",
      example: "Her ambivalence made the decision difficult.",
    },
  ],
  model: "dostoevsky-baseline:latest",
  validation_warnings: [],
};

const innerMonologueResponse = {
  scenario: "A student considers whether to apologize.",
  generated_text: ["I", ...Array.from({ length: 51 }, () => "reflect")]
    .join(" "),
  word_count: 52,
  requested_min_words: 50,
  requested_max_words: 60,
  within_requested_range: true,
  model: "dostoevsky-baseline:latest",
  validation_warnings: [],
};

function successfulResponse(payload: unknown): Response {
  return {
    ok: true,
    status: 200,
    json: async () => payload,
  } as Response;
}

function failedResponse(status: number, detail: string): Response {
  return {
    ok: false,
    status,
    json: async () => ({ detail }),
  } as Response;
}

function mockFetch(response: Response): void {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response));
}

afterEach(() => {
  vi.unstubAllGlobals();
});

beforeEach(() => {
  vi.stubGlobal("window", {
    setTimeout: globalThis.setTimeout,
    clearTimeout: globalThis.clearTimeout,
  });
});

describe("feature API response validation", () => {
  it("accepts a valid Literary Rewrite response", async () => {
    mockFetch(successfulResponse(rewriteResponse));

    await expect(rewriteLiteraryText("The room was quiet.")).resolves.toEqual(
      rewriteResponse,
    );
  });

  it("rejects an inconsistent Literary Rewrite word count", async () => {
    mockFetch(successfulResponse({ ...rewriteResponse, word_count: 3 }));

    await expect(rewriteLiteraryText("The room was quiet.")).rejects.toThrow(
      "invalid rewrite response",
    );
  });

  it("accepts a valid Word Cabinet response", async () => {
    mockFetch(successfulResponse(wordCabinetResponse));

    await expect(
      openWordCabinet("Conflicted feelings", 3),
    ).resolves.toEqual(wordCabinetResponse);
  });

  it("rejects an empty required Word Cabinet field", async () => {
    mockFetch(
      successfulResponse({
        ...wordCabinetResponse,
        words: [
          { ...wordCabinetResponse.words[0], definition: "  " },
        ],
      }),
    );

    await expect(openWordCabinet("Conflicted feelings", 3)).rejects.toThrow(
      "invalid vocabulary response",
    );
  });

  it("accepts a valid empty Word Cabinet response (words: [])", async () => {
    const emptyResponse = { ...wordCabinetResponse, words: [] };
    mockFetch(successfulResponse(emptyResponse));

    await expect(
      openWordCabinet("Conflicted feelings", 3),
    ).resolves.toEqual(emptyResponse);
  });

  it("rejects a Word Cabinet response when words property is missing", async () => {
    const { words: _words, ...missingWordsResponse } = wordCabinetResponse;
    mockFetch(successfulResponse(missingWordsResponse));

    await expect(openWordCabinet("Conflicted feelings", 3)).rejects.toThrow(
      "invalid vocabulary response",
    );
  });

  it("rejects a Word Cabinet response when words property is not an array", async () => {
    mockFetch(
      successfulResponse({
        ...wordCabinetResponse,
        words: "invalid-not-array",
      }),
    );

    await expect(openWordCabinet("Conflicted feelings", 3)).rejects.toThrow(
      "invalid vocabulary response",
    );
  });

  it("rejects a Word Cabinet response when an entry has intensity out of range", async () => {
    mockFetch(
      successfulResponse({
        ...wordCabinetResponse,
        words: [
          { ...wordCabinetResponse.words[0], intensity: 0 },
        ],
      }),
    );

    await expect(openWordCabinet("Conflicted feelings", 3)).rejects.toThrow(
      "invalid vocabulary response",
    );
  });

  it("rejects a Word Cabinet response when an entry has an invalid part of speech", async () => {
    mockFetch(
      successfulResponse({
        ...wordCabinetResponse,
        words: [
          { ...wordCabinetResponse.words[0], part_of_speech: "interjection" },
        ],
      }),
    );

    await expect(openWordCabinet("Conflicted feelings", 3)).rejects.toThrow(
      "invalid vocabulary response",
    );
  });

  it("accepts an internally consistent Inner Monologue response", async () => {
    mockFetch(successfulResponse(innerMonologueResponse));

    await expect(
      generateInnerMonologue(
        "A student considers whether to apologize.",
        "first_person",
        50,
        60,
      ),
    ).resolves.toEqual(innerMonologueResponse);
  });

  it("rejects an inconsistent Inner Monologue range flag", async () => {
    mockFetch(
      successfulResponse({
        ...innerMonologueResponse,
        within_requested_range: false,
      }),
    );

    await expect(
      generateInnerMonologue(
        "A student considers whether to apologize.",
        "first_person",
        50,
        60,
      ),
    ).rejects.toThrow("invalid monologue response");
  });

  it("surfaces a useful API error detail and status", async () => {
    mockFetch(failedResponse(504, "The monologue request timed out."));

    await expect(
      generateInnerMonologue(
        "A student considers whether to apologize.",
        "first_person",
        50,
        60,
      ),
    ).rejects.toMatchObject({
      name: "ApiError",
      message: "The monologue request timed out.",
      status: 504,
    });
  });
});


const healthyBackendResponse: HealthResponse = {
  status: "ok",
  ollama: {
    status: "connected",
    model: "dostoevsky-baseline:latest",
    model_available: true,
    error: null,
  },
};

const degradedOllamaResponse: HealthResponse = {
  status: "degraded",
  ollama: {
    status: "unavailable",
    model: "dostoevsky-baseline:latest",
    model_available: null,
    error: "Could not connect to the local Ollama service.",
  },
};

describe("health endpoint and connectivity evaluation", () => {
  it("accepts a healthy backend response and evaluates to connected", async () => {
    mockFetch(successfulResponse(healthyBackendResponse));

    const response = await fetchHealth();
    expect(response).toEqual(healthyBackendResponse);
    expect(evaluateHealthStatus(response)).toBe("connected");
  });

  it("handles HTTP 200 with degraded status and evaluates to degraded, never connected", async () => {
    mockFetch(successfulResponse(degradedOllamaResponse));

    const response = await fetchHealth();
    expect(response.status).toBe("degraded");
    expect(response.ollama.status).toBe("unavailable");
    expect(evaluateHealthStatus(response)).toBe("degraded");
    expect(evaluateHealthStatus(response)).not.toBe("connected");
  });

  it("rejects when backend request fails with non-200 HTTP status", async () => {
    mockFetch(failedResponse(500, "Internal Server Error"));

    await expect(fetchHealth()).rejects.toThrow(
      "Backend health check failed (500).",
    );
  });

  it("rejects when health response is malformed or missing fields", async () => {
    mockFetch(successfulResponse({ status: "unexpected_status", ollama: {} }));

    await expect(fetchHealth()).rejects.toThrow(
      "The backend returned an invalid health response.",
    );
  });

  it("verifies degraded status cannot become fully healthy under various degraded conditions", () => {
    // Model unavailable
    expect(
      evaluateHealthStatus({
        status: "ok",
        ollama: {
          status: "connected",
          model: "dostoevsky-baseline:latest",
          model_available: false,
          error: "Model not found",
        },
      }),
    ).toBe("degraded");

    // Model available null
    expect(
      evaluateHealthStatus({
        status: "ok",
        ollama: {
          status: "connected",
          model: "dostoevsky-baseline:latest",
          model_available: null,
          error: null,
        },
      }),
    ).toBe("degraded");

    // Ollama status unavailable despite status ok
    expect(
      evaluateHealthStatus({
        status: "ok",
        ollama: {
          status: "unavailable",
          model: "dostoevsky-baseline:latest",
          model_available: true,
          error: "Connection timeout",
        },
      }),
    ).toBe("degraded");

    // Status degraded despite connected ollama
    expect(
      evaluateHealthStatus({
        status: "degraded",
        ollama: {
          status: "connected",
          model: "dostoevsky-baseline:latest",
          model_available: true,
          error: null,
        },
      }),
    ).toBe("degraded");
  });
});
