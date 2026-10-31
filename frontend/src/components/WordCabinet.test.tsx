import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ApiError } from "../api/client";
import WordCabinet from "./WordCabinet";

const mockCabinet = vi.hoisted(() => vi.fn());

vi.mock("../api/client", async (importOriginal) => {
  const actual = await importOriginal<typeof import("../api/client")>();
  return {
    ...actual,
    openWordCabinet: mockCabinet,
  };
});

describe("WordCabinet component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the studio initial state correctly", () => {
    render(<WordCabinet />);

    expect(
      screen.getByRole("region", { name: "Word Cabinet workspace" }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText(/The feeling or situation/i)).toBeInTheDocument();
    expect(
      screen.getByRole("combobox", { name: "Number of suggestions" }),
    ).toHaveValue("6");
    expect(
      screen.getByRole("button", { name: "Open the Cabinet" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        /Fewer suggestions can reduce generation time on local hardware/i,
      ),
    ).toBeInTheDocument();
  });

  it("allows selecting requested suggestions count", async () => {
    const user = userEvent.setup();
    render(<WordCabinet />);

    const select = screen.getByRole("combobox", {
      name: "Number of suggestions",
    });
    await user.selectOptions(select, "4");
    expect(select).toHaveValue("4");
  });

  it("prevents empty submission with validation alert", async () => {
    const user = userEvent.setup();
    render(<WordCabinet />);

    await user.click(screen.getByRole("button", { name: "Open the Cabinet" }));

    expect(mockCabinet).not.toHaveBeenCalled();
    expect(screen.getByRole("alert")).toHaveTextContent(
      "Describe the feeling or state of mind you want to name.",
    );
  });

  it("displays loading state while waiting for vocabulary", async () => {
    const user = userEvent.setup();
    let resolvePromise: (value: unknown) => void = () => {};
    mockCabinet.mockReturnValue(
      new Promise((resolve) => {
        resolvePromise = resolve;
      }),
    );

    render(<WordCabinet />);

    const textarea = screen.getByLabelText(/The feeling or situation/i);
    await user.type(textarea, "An intense sense of shame and humiliation.");

    const submitButton = screen.getByRole("button", {
      name: "Open the Cabinet",
    });
    await user.click(submitButton);

    expect(submitButton).toBeDisabled();
    expect(submitButton).toHaveTextContent("Turning the words…");

    resolvePromise({
      context: "An intense sense of shame and humiliation.",
      words: [],
      model: "dostoevsky-baseline:latest",
      validation_warnings: [],
    });

    await waitFor(() => {
      expect(submitButton).toHaveTextContent("Open the Cabinet");
      expect(submitButton).not.toBeDisabled();
    });
  });

  it("renders valid vocabulary cards with full details", async () => {
    const user = userEvent.setup();
    mockCabinet.mockResolvedValue({
      context: "Pride wounded by condescension",
      words: [
        {
          word: "mortification",
          part_of_speech: "noun",
          definition: "Great embarrassment and shame.",
          connotation: "Carries a sense of injured vanity.",
          intensity: 4,
          distinction: "Deeper and more paralyzing than simple embarrassment.",
          example: "He endured the patron's smirk with silent mortification.",
        },
      ],
      model: "dostoevsky-baseline:latest",
      validation_warnings: [],
    });

    render(<WordCabinet />);

    const textarea = screen.getByLabelText(/The feeling or situation/i);
    await user.type(textarea, "Pride wounded by condescension");

    await user.click(screen.getByRole("button", { name: "Open the Cabinet" }));

    await waitFor(() => {
      expect(screen.getByText("mortification")).toBeInTheDocument();
      expect(screen.getByText("noun")).toBeInTheDocument();
      expect(
        screen.getByText("Great embarrassment and shame."),
      ).toBeInTheDocument();
      expect(
        screen.getByText("Carries a sense of injured vanity."),
      ).toBeInTheDocument();
      expect(
        screen.getByText(
          "Deeper and more paralyzing than simple embarrassment.",
        ),
      ).toBeInTheDocument();
      expect(
        screen.getByText(
          "He endured the patron's smirk with silent mortification.",
        ),
      ).toBeInTheDocument();
      expect(screen.getByText("4 / 5")).toBeInTheDocument();
    });
  });

  it("renders graceful empty state fallback when words array is empty", async () => {
    const user = userEvent.setup();
    mockCabinet.mockResolvedValue({
      context: "Uncommon scenario",
      words: [],
      model: "dostoevsky-baseline:latest",
      validation_warnings: [],
    });

    render(<WordCabinet />);

    const textarea = screen.getByLabelText(/The feeling or situation/i);
    await user.type(textarea, "Uncommon scenario");

    await user.click(screen.getByRole("button", { name: "Open the Cabinet" }));

    await waitFor(() => {
      expect(
        screen.getByText(
          "No usable vocabulary entries were returned. Try refining the context and request again.",
        ),
      ).toBeInTheDocument();
      expect(screen.getByText("0 entries")).toBeInTheDocument();
    });
  });

  it("communicates API errors clearly with retry action", async () => {
    const user = userEvent.setup();
    mockCabinet.mockRejectedValue(
      new ApiError("Backend failed to process prompt.", 500),
    );

    render(<WordCabinet />);

    const textarea = screen.getByLabelText(/The feeling or situation/i);
    await user.type(textarea, "Conflicted motives");

    await user.click(screen.getByRole("button", { name: "Open the Cabinet" }));

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent(
        "Backend failed to process prompt.",
      );
      expect(
        screen.getByRole("button", { name: "Try again" }),
      ).toBeInTheDocument();
    });
  });

  it("allows copying individual word to clipboard", async () => {
    const user = userEvent.setup();
    mockCabinet.mockResolvedValue({
      context: "Resentment",
      words: [
        {
          word: "rancor",
          part_of_speech: "noun",
          definition: "Bitterness or resentfulness.",
          connotation: "Deep-seated and enduring.",
          intensity: 4,
          distinction: "Implies lingering malice rather than a passing temper.",
          example: "He spoke without rancor, yet forgot nothing.",
        },
      ],
      model: "dostoevsky-baseline:latest",
      validation_warnings: [],
    });

    render(<WordCabinet />);

    const textarea = screen.getByLabelText(/The feeling or situation/i);
    await user.type(textarea, "Resentment");

    await user.click(screen.getByRole("button", { name: "Open the Cabinet" }));

    await waitFor(() => {
      expect(
        screen.getByRole("button", { name: "Copy the word rancor" }),
      ).toBeInTheDocument();
    });

    await user.click(
      screen.getByRole("button", { name: "Copy the word rancor" }),
    );

    await waitFor(() => {
      expect(screen.getByRole("status")).toHaveTextContent("rancor copied.");
    });
  });
});
