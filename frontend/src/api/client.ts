export type OllamaHealth = {
  status: "connected" | "unavailable";
  model: string;
  model_available: boolean | null;
  error: string | null;
};

export type HealthResponse = {
  status: "ok" | "degraded";
  ollama: OllamaHealth;
};

export type ConnectionState =
  | "checking"
  | "connected"
  | "degraded"
  | "unavailable"
  | "malformed";

export function evaluateHealthStatus(
  health: HealthResponse,
): "connected" | "degraded" {
  if (
    health.status === "ok" &&
    health.ollama.status === "connected" &&
    health.ollama.model_available === true
  ) {
    return "connected";
  }
  return "degraded";
}


export type LiteraryRewriteResponse = {
  original_text: string;
  rewritten_text: string;
  word_count: number;
  model: string;
  validation_warnings: string[];
};

export type WordCabinetEntry = {
  word: string;
  part_of_speech: "noun" | "verb" | "adjective" | "adverb" | "phrase";
  definition: string;
  connotation: string;
  intensity: number;
  distinction: string;
  example: string;
};

export type WordCabinetResponse = {
  context: string;
  words: WordCabinetEntry[];
  model: string;
  validation_warnings: string[];
};

export type InnerMonologueResponse = {
  scenario: string;
  generated_text: string;
  word_count: number;
  requested_min_words: number;
  requested_max_words: number;
  within_requested_range: boolean;
  model: string;
  validation_warnings: string[];
};

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status?: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function isHealthResponse(value: unknown): value is HealthResponse {
  if (!isRecord(value)) {
    return false;
  }

  if (
    (value.status !== "ok" && value.status !== "degraded") ||
    !isRecord(value.ollama)
  ) {
    return false;
  }

  const ollama = value.ollama;
  return (
    (ollama.status === "connected" || ollama.status === "unavailable") &&
    typeof ollama.model === "string" &&
    (typeof ollama.model_available === "boolean" ||
      ollama.model_available === null) &&
    (typeof ollama.error === "string" || ollama.error === null)
  );
}

function isLiteraryRewriteResponse(
  value: unknown,
): value is LiteraryRewriteResponse {
  return (
    isRecord(value) &&
    isNonEmptyString(value.original_text) &&
    isNonEmptyString(value.rewritten_text) &&
    typeof value.word_count === "number" &&
    Number.isInteger(value.word_count) &&
    value.word_count >= 0 &&
    value.word_count === countWhitespaceDelimitedWords(value.rewritten_text) &&
    isNonEmptyString(value.model) &&
    Array.isArray(value.validation_warnings) &&
    value.validation_warnings.every(
      (warning: unknown) => typeof warning === "string",
    )
  );
}

function isWordCabinetEntry(value: unknown): value is WordCabinetEntry {
  if (!isRecord(value)) {
    return false;
  }
  return (
    isNonEmptyString(value.word) &&
    ["noun", "verb", "adjective", "adverb", "phrase"].includes(
      String(value.part_of_speech),
    ) &&
    isNonEmptyString(value.definition) &&
    isNonEmptyString(value.connotation) &&
    typeof value.intensity === "number" &&
    Number.isInteger(value.intensity) &&
    value.intensity >= 1 &&
    value.intensity <= 5 &&
    isNonEmptyString(value.distinction) &&
    isNonEmptyString(value.example)
  );
}

function isWordCabinetResponse(value: unknown): value is WordCabinetResponse {
  return (
    isRecord(value) &&
    isNonEmptyString(value.context) &&
    Array.isArray(value.words) &&
    value.words.every(isWordCabinetEntry) &&
    isNonEmptyString(value.model) &&
    Array.isArray(value.validation_warnings) &&
    value.validation_warnings.every(
      (warning: unknown) => typeof warning === "string",
    )
  );
}

function isInnerMonologueResponse(
  value: unknown,
): value is InnerMonologueResponse {
  return (
    isRecord(value) &&
    isNonEmptyString(value.scenario) &&
    isNonEmptyString(value.generated_text) &&
    typeof value.word_count === "number" &&
    Number.isInteger(value.word_count) &&
    value.word_count >= 0 &&
    value.word_count === countWhitespaceDelimitedWords(value.generated_text) &&
    typeof value.requested_min_words === "number" &&
    Number.isInteger(value.requested_min_words) &&
    value.requested_min_words >= 50 &&
    typeof value.requested_max_words === "number" &&
    Number.isInteger(value.requested_max_words) &&
    value.requested_max_words <= 500 &&
    value.requested_max_words >= value.requested_min_words &&
    typeof value.within_requested_range === "boolean" &&
    value.within_requested_range ===
      (value.word_count >= value.requested_min_words &&
        value.word_count <= value.requested_max_words) &&
    isNonEmptyString(value.model) &&
    Array.isArray(value.validation_warnings) &&
    value.validation_warnings.every(
      (warning: unknown) => typeof warning === "string",
    )
  );
}

function isNonEmptyString(value: unknown): value is string {
  return typeof value === "string" && value.trim().length > 0;
}

function countWhitespaceDelimitedWords(text: string): number {
  return text.trim().split(/\s+/).length;
}

const apiBaseUrl = (
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"
).replace(/\/+$/, "");

export async function fetchHealth(): Promise<HealthResponse> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), 5000);

  try {
    const response = await fetch(`${apiBaseUrl}/api/health`, {
      headers: { Accept: "application/json" },
      signal: controller.signal,
    });

    if (!response.ok) {
      throw new ApiError(`Backend health check failed (${response.status}).`);
    }

    const payload: unknown = await response.json();
    if (!isHealthResponse(payload)) {
      throw new ApiError("The backend returned an invalid health response.");
    }
    return payload;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError("The backend health check timed out.");
    }
    throw new ApiError("The backend could not be reached.");
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function rewriteLiteraryText(
  text: string,
): Promise<LiteraryRewriteResponse> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), 190_000);

  try {
    const response = await fetch(`${apiBaseUrl}/api/features/literary-rewrite`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
      signal: controller.signal,
    });

    if (!response.ok) {
      let detail: unknown;
      try {
        const payload: unknown = await response.json();
        detail = isRecord(payload) ? payload.detail : undefined;
      } catch {
        detail = undefined;
      }

      const safeDetail = typeof detail === "string" ? detail : undefined;
      const message =
        safeDetail ??
        (response.status === 422
          ? "Please provide non-empty source text of no more than 5,000 characters."
          : response.status === 503
            ? "Ollama is unavailable. Start Ollama and confirm the selected model is installed."
            : response.status === 504
              ? "The rewrite took too long. Please try again."
              : "The local model could not complete the rewrite. Please try again.");
      throw new ApiError(message, response.status);
    }

    const payload: unknown = await response.json();
    if (!isLiteraryRewriteResponse(payload)) {
      throw new ApiError("The backend returned an invalid rewrite response.");
    }
    return payload;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError("The rewrite request timed out. Please try again.");
    }
    if (error instanceof SyntaxError) {
      throw new ApiError("The backend returned an unreadable rewrite response.");
    }
    throw new ApiError(
      "The backend could not be reached. Check that the application is running.",
    );
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function openWordCabinet(
  context: string,
  count: number,
): Promise<WordCabinetResponse> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), 190_000);

  try {
    const response = await fetch(`${apiBaseUrl}/api/features/word-cabinet`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ context, count }),
      signal: controller.signal,
    });

    if (!response.ok) {
      let detail: unknown;
      try {
        const payload: unknown = await response.json();
        detail = isRecord(payload) ? payload.detail : undefined;
      } catch {
        detail = undefined;
      }

      const safeDetail = typeof detail === "string" ? detail : undefined;
      const message =
        safeDetail ??
        (response.status === 422
          ? "Enter a context of no more than 2,000 characters and request 3 to 8 words."
          : response.status === 503
            ? "Ollama is unavailable. Start Ollama and confirm the selected model is installed."
            : response.status === 504
              ? "The vocabulary request took too long. Please try again."
              : "The local model could not prepare vocabulary. Please try again.");
      throw new ApiError(message, response.status);
    }

    const payload: unknown = await response.json();
    if (!isWordCabinetResponse(payload)) {
      throw new ApiError("The backend returned an invalid vocabulary response.");
    }
    return payload;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError("The vocabulary request timed out. Please try again.");
    }
    if (error instanceof SyntaxError) {
      throw new ApiError("The backend returned an unreadable vocabulary response.");
    }
    throw new ApiError(
      "The backend could not be reached. Check that the application is running.",
    );
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export async function generateInnerMonologue(
  scenario: string,
  perspective: "first_person" | "third_person",
  minWords: number,
  maxWords: number,
): Promise<InnerMonologueResponse> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), 190_000);

  try {
    const response = await fetch(`${apiBaseUrl}/api/features/inner-monologue`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        scenario,
        perspective,
        min_words: minWords,
        max_words: maxWords,
      }),
      signal: controller.signal,
    });

    if (!response.ok) {
      let detail: unknown;
      try {
        const payload: unknown = await response.json();
        detail = isRecord(payload) ? payload.detail : undefined;
      } catch {
        detail = undefined;
      }

      const safeDetail = typeof detail === "string" ? detail : undefined;
      const message =
        safeDetail ??
        (response.status === 422
          ? "Check the scenario and choose a valid word range between 50 and 500."
          : response.status === 503
            ? "Ollama is unavailable. Start Ollama and confirm the selected model is installed."
            : response.status === 504
              ? "The monologue request took too long. Please try again."
              : "The local model could not complete the monologue. Please try again.");
      throw new ApiError(message, response.status);
    }

    const payload: unknown = await response.json();
    if (!isInnerMonologueResponse(payload)) {
      throw new ApiError("The backend returned an invalid monologue response.");
    }
    return payload;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError("The monologue request timed out. Please try again.");
    }
    if (error instanceof SyntaxError) {
      throw new ApiError("The backend returned an unreadable monologue response.");
    }
    throw new ApiError(
      "The backend could not be reached. Check that the application is running.",
    );
  } finally {
    window.clearTimeout(timeoutId);
  }
}
