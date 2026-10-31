import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import App from "./App";
import * as client from "./api/client";

vi.mock("./api/client", async (importOriginal) => {
  const actual = await importOriginal<typeof import("./api/client")>();
  return {
    ...actual,
    fetchHealth: vi.fn(),
    rewriteLiteraryText: vi.fn(),
    openWordCabinet: vi.fn(),
    generateInnerMonologue: vi.fn(),
  };
});

describe("App integration, state preservation and hash navigation", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    window.location.hash = "";
    vi.mocked(client.fetchHealth).mockResolvedValue({
      status: "ok",
      ollama: {
        status: "connected",
        model: "dostoevsky-baseline:latest",
        model_available: true,
        error: null,
      },
    });
  });

  function getNavButton(nameRegex: RegExp): HTMLElement {
    return screen.getAllByRole("button", { name: nameRegex })[0];
  }

  it("renders the application shell and defaults to Literary Rewrite studio", async () => {
    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Backend connected")).toBeInTheDocument();
    });

    const rewriteButton = getNavButton(/Literary Rewrite/i);
    expect(rewriteButton).toHaveAttribute("aria-current", "page");

    const rewritePanel = document.getElementById("studio-panel-rewrite");
    const cabinetPanel = document.getElementById("studio-panel-cabinet");
    const monologuePanel = document.getElementById("studio-panel-monologue");

    expect(rewritePanel).not.toHaveAttribute("hidden");
    expect(cabinetPanel).toHaveAttribute("hidden");
    expect(monologuePanel).toHaveAttribute("hidden");
  });

  it("renders degraded and error health states correctly", async () => {
    vi.mocked(client.fetchHealth).mockResolvedValueOnce({
      status: "degraded",
      ollama: {
        status: "unavailable",
        model: "dostoevsky-baseline:latest",
        model_available: null,
        error: "Ollama not running",
      },
    });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText("Ollama unavailable")).toBeInTheDocument();
      expect(screen.getByRole("button", { name: /retry/i })).toBeInTheDocument();
    });
  });

  it("preserves Literary Rewrite drafts and output across tab switches without duplicate API calls", async () => {
    const user = userEvent.setup();
    vi.mocked(client.rewriteLiteraryText).mockResolvedValue({
      original_text: "A gloomy evening in Petersburg.",
      rewritten_text: "Petersburg crouched in yellow fog and damp silence.",
      word_count: 8,
      model: "dostoevsky-baseline:latest",
      validation_warnings: [],
    });

    render(<App />);

    const textarea = screen.getByLabelText(/Your passage/i);
    await user.type(textarea, "A gloomy evening in Petersburg.");

    await user.click(
      screen.getByRole("button", { name: "Rewrite" }),
    );

    await waitFor(() => {
      expect(
        screen.getByText("Petersburg crouched in yellow fog and damp silence."),
      ).toBeInTheDocument();
    });

    expect(client.rewriteLiteraryText).toHaveBeenCalledTimes(1);

    // Switch to Word Cabinet
    await user.click(getNavButton(/Word Cabinet/i));

    const cabinetPanel = document.getElementById("studio-panel-cabinet");
    const rewritePanel = document.getElementById("studio-panel-rewrite");
    expect(cabinetPanel).not.toHaveAttribute("hidden");
    expect(rewritePanel).toHaveAttribute("hidden");

    // Switch back to Literary Rewrite
    await user.click(getNavButton(/Literary Rewrite/i));

    expect(rewritePanel).not.toHaveAttribute("hidden");
    // User draft and output are preserved!
    expect(textarea).toHaveValue("A gloomy evening in Petersburg.");
    expect(
      screen.getByText("Petersburg crouched in yellow fog and damp silence."),
    ).toBeInTheDocument();

    // No additional API requests were dispatched
    expect(client.rewriteLiteraryText).toHaveBeenCalledTimes(1);
    expect(client.openWordCabinet).not.toHaveBeenCalled();
  });

  it("preserves Word Cabinet context, count selection, and cards across navigation", async () => {
    const user = userEvent.setup();
    vi.mocked(client.openWordCabinet).mockResolvedValue({
      context: "Guilt and pride",
      words: [
        {
          word: "contrition",
          part_of_speech: "noun",
          definition: "Repentance for sin.",
          connotation: "Sincere sorrow.",
          intensity: 4,
          distinction: "Focuses on moral sorrow rather than fear of punishment.",
          example: "He felt genuine contrition in the quiet room.",
        },
      ],
      model: "dostoevsky-baseline:latest",
      validation_warnings: [],
    });

    render(<App />);

    // Switch to Word Cabinet
    await user.click(getNavButton(/Word Cabinet/i));

    const contextInput = screen.getByLabelText(/The feeling or situation/i);
    await user.type(contextInput, "Guilt and pride");

    const countSelect = screen.getByRole("combobox", {
      name: "Number of suggestions",
    });
    await user.selectOptions(countSelect, "5");

    await user.click(screen.getByRole("button", { name: "Open the Cabinet" }));

    await waitFor(() => {
      expect(screen.getByText("contrition")).toBeInTheDocument();
    });

    // Navigate to Inner Monologue
    await user.click(getNavButton(/Inner Monologue/i));

    // Return to Word Cabinet
    await user.click(getNavButton(/Word Cabinet/i));

    expect(contextInput).toHaveValue("Guilt and pride");
    expect(countSelect).toHaveValue("5");
    expect(screen.getByText("contrition")).toBeInTheDocument();
  });

  it("preserves Inner Monologue scenario, perspective, length settings, and generated output", async () => {
    const user = userEvent.setup();
    vi.mocked(client.generateInnerMonologue).mockResolvedValue({
      scenario: "Contemplating confession",
      generated_text: "Can a crime ever remain purely a thought?",
      word_count: 8,
      requested_min_words: 120,
      requested_max_words: 220,
      within_requested_range: false,
      model: "dostoevsky-baseline:latest",
      validation_warnings: [],
    });

    render(<App />);

    // Switch to Inner Monologue
    await user.click(getNavButton(/Inner Monologue/i));

    const scenarioInput = screen.getByLabelText(/The situation/i);
    await user.type(scenarioInput, "Contemplating confession");

    const perspectiveSelect = screen.getByLabelText("Point of view");
    await user.selectOptions(perspectiveSelect, "third_person");

    const minWords = screen.getByLabelText("Minimum words");
    await user.clear(minWords);
    await user.type(minWords, "120");

    const maxWords = screen.getByLabelText("Maximum words");
    await user.clear(maxWords);
    await user.type(maxWords, "220");

    await user.click(
      screen.getByRole("button", { name: "Begin the Monologue" }),
    );

    await waitFor(() => {
      expect(
        screen.getByText("Can a crime ever remain purely a thought?"),
      ).toBeInTheDocument();
    });

    // Switch to Rewrite and then return
    await user.click(getNavButton(/Literary Rewrite/i));
    await user.click(getNavButton(/Inner Monologue/i));

    expect(scenarioInput).toHaveValue("Contemplating confession");
    expect(perspectiveSelect).toHaveValue("third_person");
    expect(minWords).toHaveValue(120);
    expect(maxWords).toHaveValue(220);
    expect(
      screen.getByText("Can a crime ever remain purely a thought?"),
    ).toBeInTheDocument();
  });

  it("preserves user draft when API request fails", async () => {
    const user = userEvent.setup();
    vi.mocked(client.rewriteLiteraryText).mockRejectedValue(
      new client.ApiError("Server exploded", 500),
    );

    render(<App />);

    const textarea = screen.getByLabelText(/Your passage/i);
    await user.type(textarea, "My precious draft passage");

    await user.click(
      screen.getByRole("button", { name: "Rewrite" }),
    );

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("Server exploded");
    });

    // Draft is still in textarea
    expect(textarea).toHaveValue("My precious draft passage");

    // Switch away and back
    await user.click(getNavButton(/Word Cabinet/i));
    await user.click(getNavButton(/Literary Rewrite/i));

    expect(textarea).toHaveValue("My precious draft passage");
  });

  it("synchronizes navigation clicks with URL hash and avoids redundant updates", async () => {
    const user = userEvent.setup();
    render(<App />);

    expect(window.location.hash).toBe("");

    // Clicking Word Cabinet sets #word-cabinet
    await user.click(getNavButton(/Word Cabinet/i));
    expect(window.location.hash).toBe("#word-cabinet");

    // Clicking again on already active Word Cabinet does not change or duplicate
    await user.click(getNavButton(/Word Cabinet/i));
    expect(window.location.hash).toBe("#word-cabinet");

    // Clicking Inner Monologue sets #inner-monologue
    await user.click(getNavButton(/Inner Monologue/i));
    expect(window.location.hash).toBe("#inner-monologue");

    // Clicking Literary Rewrite sets #rewrite
    await user.click(getNavButton(/Literary Rewrite/i));
    expect(window.location.hash).toBe("#rewrite");
  });

  it("activates the studio matching initial URL hash on mount", () => {
    window.location.hash = "#word-cabinet";
    render(<App />);

    const cabinetPanel = document.getElementById("studio-panel-cabinet");
    const rewritePanel = document.getElementById("studio-panel-rewrite");

    expect(cabinetPanel).not.toHaveAttribute("hidden");
    expect(rewritePanel).toHaveAttribute("hidden");
  });

  it("responds to browser Back / Forward hashchange events", async () => {
    render(<App />);

    const cabinetPanel = document.getElementById("studio-panel-cabinet");
    const rewritePanel = document.getElementById("studio-panel-rewrite");

    expect(rewritePanel).not.toHaveAttribute("hidden");
    expect(cabinetPanel).toHaveAttribute("hidden");

    // Simulate browser Back/Forward changing hash
    act(() => {
      window.location.hash = "#word-cabinet";
      fireEvent(window, new HashChangeEvent("hashchange"));
    });

    expect(cabinetPanel).not.toHaveAttribute("hidden");
    expect(rewritePanel).toHaveAttribute("hidden");

    act(() => {
      window.location.hash = "#inner-monologue";
      fireEvent(window, new HashChangeEvent("hashchange"));
    });

    const monologuePanel = document.getElementById("studio-panel-monologue");
    expect(monologuePanel).not.toHaveAttribute("hidden");
    expect(cabinetPanel).toHaveAttribute("hidden");
  });

  it("falls back to Literary Rewrite studio on unknown or invalid hash", () => {
    window.location.hash = "#completely-unknown-route";
    render(<App />);

    const rewritePanel = document.getElementById("studio-panel-rewrite");
    expect(rewritePanel).not.toHaveAttribute("hidden");
  });
});
