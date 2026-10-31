import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ApiError } from "../api/client";
import LiteraryRewrite from "./LiteraryRewrite";

const mockRewrite = vi.hoisted(() => vi.fn());

vi.mock("../api/client", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../api/client")>();
  return {
    ...actual,
    rewriteLiteraryText: mockRewrite,
  };
});

describe("LiteraryRewrite component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the studio initial state correctly", () => {
    render(<LiteraryRewrite />);

    expect(
      screen.getByRole("region", { name: "Literary Rewrite workspace" }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText(/Your passage/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Rewrite" })).toBeInTheDocument();
    expect(screen.getByText("0 / 5,000")).toBeInTheDocument();
  });

  it("prevents empty submission with validation message", async () => {
    const user = userEvent.setup();
    render(<LiteraryRewrite />);

    const submitButton = screen.getByRole("button", { name: "Rewrite" });
    await user.click(submitButton);

    expect(mockRewrite).not.toHaveBeenCalled();
    expect(screen.getByRole("alert")).toHaveTextContent(
      "Enter a passage before asking for a rewrite.",
    );
  });

  it("enforces character length constraints", async () => {
    const user = userEvent.setup();
    render(<LiteraryRewrite />);

    const input = screen.getByLabelText(/Your passage/i);
    const longText = "a".repeat(5001);
    fireEvent.change(input, { target: { value: longText } });

    const submitButton = screen.getByRole("button", { name: "Rewrite" });
    await user.click(submitButton);

    expect(mockRewrite).not.toHaveBeenCalled();
    expect(screen.getByRole("alert")).toHaveTextContent(
      "The passage is 5,001 characters; shorten it to 5,000 characters or fewer.",
    );
  });

  it("displays loading state while generation is in flight", async () => {
    const user = userEvent.setup();
    let resolvePromise: (value: unknown) => void = () => {};
    mockRewrite.mockReturnValue(
      new Promise((resolve) => {
        resolvePromise = resolve;
      }),
    );

    render(<LiteraryRewrite />);

    const input = screen.getByLabelText(/Your passage/i);
    await user.type(input, "The street was silent and dark.");

    const submitButton = screen.getByRole("button", { name: "Rewrite" });
    await user.click(submitButton);

    expect(submitButton).toBeDisabled();
    expect(submitButton).toHaveTextContent("Attending to the passage…");

    resolvePromise({
      original_text: "The street was silent and dark.",
      rewritten_text: "The alleyway held its breath in deep gloom.",
      word_count: 8,
      model: "dostoevsky-baseline:latest",
      validation_warnings: [],
    });

    await waitFor(() => {
      expect(submitButton).toHaveTextContent("Rewrite");
      expect(submitButton).not.toBeDisabled();
    });
  });

  it("renders rewritten output successfully upon completion", async () => {
    const user = userEvent.setup();
    mockRewrite.mockResolvedValue({
      original_text: "The street was silent and dark.",
      rewritten_text: "The alleyway held its breath in deep gloom.",
      word_count: 8,
      model: "dostoevsky-baseline:latest",
      validation_warnings: ["Slightly elevated psychological tension."],
    });

    render(<LiteraryRewrite />);

    const input = screen.getByLabelText(/Your passage/i);
    await user.type(input, "The street was silent and dark.");

    const submitButton = screen.getByRole("button", { name: "Rewrite" });
    await user.click(submitButton);

    await waitFor(() => {
      expect(
        screen.getByText("The alleyway held its breath in deep gloom."),
      ).toBeInTheDocument();
      expect(screen.getByText("8 WORDS")).toBeInTheDocument();
      expect(
        screen.getByText("dostoevsky-baseline:latest"),
      ).toBeInTheDocument();
      expect(
        screen.getByText("Slightly elevated psychological tension."),
      ).toBeInTheDocument();
    });
  });

  it("displays understandable error when API request fails", async () => {
    const user = userEvent.setup();
    mockRewrite.mockRejectedValue(
      new ApiError("Ollama service is currently unavailable.", 503),
    );

    render(<LiteraryRewrite />);

    const input = screen.getByLabelText(/Your passage/i);
    await user.type(input, "A man walked across the bridge.");

    const submitButton = screen.getByRole("button", { name: "Rewrite" });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent(
        "Ollama service is currently unavailable.",
      );
      expect(
        screen.getByRole("button", { name: "Try again" }),
      ).toBeInTheDocument();
    });
  });

  it("provides copy button when rewritten output exists and copies content", async () => {
    const user = userEvent.setup();
    mockRewrite.mockResolvedValue({
      original_text: "He waited in agony.",
      rewritten_text: "He lingered in sharp, breathless torment.",
      word_count: 7,
      model: "dostoevsky-baseline:latest",
      validation_warnings: [],
    });

    render(<LiteraryRewrite />);

    const input = screen.getByLabelText(/Your passage/i);
    await user.type(input, "He waited in agony.");

    await user.click(screen.getByRole("button", { name: "Rewrite" }));

    await waitFor(() => {
      expect(
        screen.getByRole("button", { name: "Copy rewritten passage" }),
      ).toBeInTheDocument();
    });

    const copyButton = screen.getByRole("button", {
      name: "Copy rewritten passage",
    });
    await user.click(copyButton);

    await waitFor(() => {
      expect(screen.getByRole("status")).toHaveTextContent(
        "The rewrite has been copied.",
      );
    });
  });
});
