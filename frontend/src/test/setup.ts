import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach, beforeEach, vi } from "vitest";

beforeEach(() => {
  if (!navigator.clipboard) {
    Object.assign(navigator, {
      clipboard: {
        writeText: vi.fn().mockResolvedValue(undefined),
      },
    });
  } else if (!navigator.clipboard.writeText) {
    navigator.clipboard.writeText = vi.fn().mockResolvedValue(undefined);
  }

  if (!document.execCommand) {
    document.execCommand = vi.fn().mockReturnValue(true);
  }
});

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

