
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"

START_MARKERS = (
    "*** START OF THE PROJECT GUTENBERG",
    "*** START OF THIS PROJECT GUTENBERG",
)

END_MARKERS = (
    "*** END OF THE PROJECT GUTENBERG",
    "*** END OF THIS PROJECT GUTENBERG",
)


def read_text(path: Path) -> str:
    """Read a Gutenberg text file while tolerating a UTF-8 BOM."""
    return path.read_text(encoding="utf-8-sig", errors="replace")


def find_marker_line(text: str, markers: tuple[str, ...]):
    """Return the line index of the first matching marker, if present."""
    for index, line in enumerate(text.splitlines()):
        upper_line = line.upper()
        if any(marker in upper_line for marker in markers):
            return index
    return None


def inspect_file(path: Path) -> None:
    text = read_text(path)
    lines = text.splitlines()

    start_line = find_marker_line(text, START_MARKERS)
    end_line = find_marker_line(text, END_MARKERS)

    print(f"\n{'=' * 72}")
    print(f"FILE: {path.name}")
    print(f"{'=' * 72}")
    print(f"File size: {path.stat().st_size:,} bytes")
    print(f"Total lines: {len(lines):,}")
    print(f"Total characters: {len(text):,}")

    if start_line is None:
        print("Start marker: NOT FOUND")
    else:
        print(f"Start marker: line {start_line + 1}")

    if end_line is None:
        print("End marker: NOT FOUND")
    else:
        print(f"End marker: line {end_line + 1}")

    if (
        start_line is not None
        and end_line is not None
        and start_line < end_line
    ):
        body = "\n".join(lines[start_line + 1:end_line]).strip()
        print(f"Characters between markers: {len(body):,}")
    else:
        print("Body size: not estimated because valid boundaries were not found")

    paragraphs = [
        block.strip()
        for block in re.split(r"\n\s*\n", text)
        if block.strip()
    ]

    print(f"Non-empty paragraph blocks in full file: {len(paragraphs):,}")
    print("\nFirst 5 lines:")
    for line in lines[:5]:
        print(f"  {line[:160]}")


def main() -> None:
    if not RAW_DIR.exists():
        raise SystemExit(f"Raw data directory not found: {RAW_DIR}")

    files = sorted(RAW_DIR.glob("*.txt"))

    if not files:
        raise SystemExit(f"No .txt files found in {RAW_DIR}")

    print("DOSTOEVSKY AI — CORPUS INSPECTION")
    print(f"Raw data directory: {RAW_DIR}")
    print(f"Text files found: {len(files)}")

    for path in files:
        inspect_file(path)

    print("\nInspection complete. No source files were modified.")


if __name__ == "__main__":
    main()
