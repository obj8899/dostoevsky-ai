import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ApiError } from "../api/client";
import InnerMonologue from "./InnerMonologue";

const mockMonologue = vi.hoisted(() => vi.fn());

vi.mock("../api/client", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../api/client")>();
  return {
    ...actual,
    generateInnerMonologue: mockMonologue,
  };
});

describe("InnerMonologue component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the studio initial state correctly", () => {
    render(<InnerMonologue />);

    expect(
      screen.getByRole("region", { name: "Inner Monologue workspace" }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText(/The situation/i)).toBeInTheDocument();
    expect(screen.getByLabelText("Point of view")).toHaveValue("first_person");
    expect(screen.getByLabelText("Minimum words")).toHaveValue(180);
    expect(screen.getByLabelText("Maximum words")).toHaveValue(250);
    expect(
      screen.getByRole("button", { name: "Begin the Monologue" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        /Shorter ranges \(e\.g\. 100–180 words\) may produce more reliable results/i,
      ),
    ).toBeInTheDocument();
  });

  it("allows updating perspective and word range settings", async () => {
    const user = userEvent.setup();
    render(<InnerMonologue />);

    const perspective = screen.getByLabelText("Point of view");
    await user.selectOptions(perspective, "third_person");
    expect(perspective).toHaveValue("third_person");

    const minInput = screen.getByLabelText("Minimum words");
    await user.clear(minInput);
    await user.type(minInput, "100");
    expect(minInput).toHaveValue(100);

    const maxInput = screen.getByLabelText("Maximum words");
    await user.clear(maxInput);
    await user.type(maxInput, "200");
    expect(maxInput).toHaveValue(200);
  });

  it("prevents empty submission with validation alert", async () => {
    const user = userEvent.setup();
    render(<InnerMonologue />);

    await user.click(
      screen.getByRole("button", { name: "Begin the Monologue" }),
    );

    expect(mockMonologue).not.toHaveBeenCalled();
    expect(screen.getByRole("alert")).toHaveTextContent(
      "Describe the situation for the inner monologue.",
    );
  });

  it("validates that minimum words do not exceed maximum words", async () => {
    const user = userEvent.setup();
    render(<InnerMonologue />);

    const textarea = screen.getByLabelText(/The situation/i);
    await user.type(textarea, "A dilemma at dusk.");

    const minInput = screen.getByLabelText("Minimum words");
    const maxInput = screen.getByLabelText("Maximum words");
    await user.clear(minInput);
    await user.type(minInput, "300");
    await user.clear(maxInput);
    await user.type(maxInput, "200");

    await user.click(
      screen.getByRole("button", { name: "Begin the Monologue" }),
    );

    expect(mockMonologue).not.toHaveBeenCalled();
    expect(screen.getByRole("alert")).toHaveTextContent(
      /Choose a word range from 50 to 500, with the maximum at least the minimum/i,
    );
  });

  it("displays loading state while generating monologue", async () => {
    const user = userEvent.setup();
    let resolvePromise: (value: unknown) => void = () => {};
    mockMonologue.mockReturnValue(
      new Promise((resolve) => {
        resolvePromise = resolve;
      }),
    );

    render(<InnerMonologue />);

    const textarea = screen.getByLabelText(/The situation/i);
    await user.type(textarea, "Waiting for the verdict.");

    const submitButton = screen.getByRole("button", {
      name: "Begin the Monologue",
    });
    await user.click(submitButton);

    expect(submitButton).toBeDisabled();
    expect(submitButton).toHaveTextContent("Listening for the inner voice…");

    resolvePromise({
      scenario: "Waiting for the verdict.",
      generated_text:
        "The gavel has not struck yet, but my conscience has already sentenced me.",
      word_count: 12,
      requested_min_words: 180,
      requested_max_words: 250,
      within_requested_range: false,
      model: "dostoevsky-baseline:latest",
      validation_warnings: ["Slightly under length target."],
    });

    await waitFor(() => {
      expect(submitButton).toHaveTextContent("Begin the Monologue");
      expect(submitButton).not.toBeDisabled();
    });
  });

  it("renders successful monologue output and word count information", async () => {
    const user = userEvent.setup();
    mockMonologue.mockResolvedValue({
      scenario: "A clerk considers confessing an error.",
      generated_text:
        "If I speak now, they will call it foolishness. If I remain silent, the silence will fester inside me.",
      word_count: 18,
      requested_min_words: 50,
      requested_max_words: 100,
      within_requested_range: true,
      model: "dostoevsky-baseline:latest",
      validation_warnings: [],
    });

    render(<InnerMonologue />);

    const textarea = screen.getByLabelText(/The situation/i);
    await user.type(textarea, "A clerk considers confessing an error.");

    await user.click(
      screen.getByRole("button", { name: "Begin the Monologue" }),
    );

    await waitFor(() => {
      expect(
        screen.getByText(/If I speak now, they will call it foolishness/i),
      ).toBeInTheDocument();
      expect(screen.getByText("18 words")).toBeInTheDocument();
      expect(screen.getByText("Within range")).toBeInTheDocument();
      expect(
        screen.getByText("LOCAL GENERATION"),
      ).toBeInTheDocument();
    });
  });

  it("displays clear error and retry action when monologue generation fails", async () => {
    const user = userEvent.setup();
    mockMonologue.mockRejectedValue(
      new ApiError("Inference request timed out.", 504),
    );

    render(<InnerMonologue />);

    const textarea = screen.getByLabelText(/The situation/i);
    await user.type(textarea, "Crisis of faith");

    await user.click(
      screen.getByRole("button", { name: "Begin the Monologue" }),
    );

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent(
        "Inference request timed out.",
      );
      expect(
        screen.getByRole("button", { name: "Try again" }),
      ).toBeInTheDocument();
    });
  });

  it("copies generated monologue to clipboard", async () => {
    const user = userEvent.setup();
    mockMonologue.mockResolvedValue({
      scenario: "Doubt",
      generated_text: "Am I a trembling creature or have I the right?",
      word_count: 10,
      requested_min_words: 50,
      requested_max_words: 100,
      within_requested_range: true,
      model: "dostoevsky-baseline:latest",
      validation_warnings: [],
    });

    render(<InnerMonologue />);

    const textarea = screen.getByLabelText(/The situation/i);
    await user.type(textarea, "Doubt");

    await user.click(
      screen.getByRole("button", { name: "Begin the Monologue" }),
    );

    await waitFor(() => {
      expect(
        screen.getByRole("button", { name: "Copy generated monologue" }),
      ).toBeInTheDocument();
    });

    await user.click(
      screen.getByRole("button", { name: "Copy generated monologue" }),
    );

    await waitFor(() => {
      expect(
        screen.getByText("The monologue has been copied."),
      ).toBeInTheDocument();
    });
  });
});
