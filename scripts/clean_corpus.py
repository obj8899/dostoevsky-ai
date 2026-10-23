
from pathlib import Path
import json
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

BOOKS = {
    "crime_and_punishment_garnett.txt": {
        "output": "crime_and_punishment_clean.txt",
        "title": "Crime and Punishment",
        "translator": "Constance Garnett",
        "contents_end_heading": "TRANSLATOR’S PREFACE",
        "contents_end_occurrence": 2,
    },
    "white_nights_and_other_stories_garnett.txt": {
        "output": "white_nights_and_other_stories_clean.txt",
        "title": "White Nights and Other Stories",
        "translator": "Constance Garnett",
        "first_story_heading": "WHITE NIGHTS",
        "end_before": (
            "PRINTED IN GREAT BRITAIN BY RICHARD CLAY & SONS, LIMITED,"
        ),
    },
}


def find_gutenberg_marker(lines, marker_type):
    pattern = re.compile(
        rf"^\s*\*\*\*\s+{marker_type}\s+OF THE PROJECT GUTENBERG EBOOK\b",
        re.IGNORECASE,
    )
    matches = [
        i for i, line in enumerate(lines)
        if pattern.search(line)
    ]

    if len(matches) != 1:
        raise ValueError(
            f"Expected one Gutenberg {marker_type} marker; "
            f"found {len(matches)}"
        )

    return matches[0]


def extract_gutenberg_text(source_path):
    lines = source_path.read_text(encoding="utf-8-sig").splitlines()

    start = find_gutenberg_marker(lines, "START")
    end = find_gutenberg_marker(lines, "END")

    if start >= end:
        raise ValueError("Gutenberg start marker must precede end marker.")

    return "\n".join(lines[start + 1:end]), start + 1, end + 1


def remove_contents(text, heading, occurrence=1):
    lines = text.splitlines()

    contents_positions = [
        i for i, line in enumerate(lines)
        if line.strip().casefold() == "contents"
    ]

    if not contents_positions:
        raise ValueError("Could not find CONTENTS heading.")

    contents_start = contents_positions[0]

    heading_positions = [
        i for i, line in enumerate(lines)
        if line.strip().casefold() == heading.casefold()
        and i > contents_start
    ]

    if len(heading_positions) < occurrence:
        raise ValueError(
            f"Could not find occurrence {occurrence} of {heading!r} "
            "after CONTENTS."
        )

    contents_end = heading_positions[occurrence - 1]

    if contents_end <= contents_start:
        raise ValueError("Invalid contents-page boundaries.")

    # Remove the contents page, keeping the text before it and
    # resuming at the selected occurrence of the real heading.
    return "\n".join(
        lines[:contents_start] + lines[contents_end:]
    )


def remove_white_nights_contents(text, heading):
    lines = text.splitlines()

    contents_positions = [
        i for i, line in enumerate(lines)
        if line.strip().casefold() == "contents"
    ]

    if len(contents_positions) != 1:
        raise ValueError(
            f"Expected one CONTENTS heading; found {len(contents_positions)}"
        )

    contents_index = contents_positions[0]

    # Find the actual story heading AFTER the contents page.
    heading_positions = [
        i for i, line in enumerate(lines)
        if line.strip().casefold() == heading.casefold()
        and i > contents_index
    ]

    if len(heading_positions) != 1:
        raise ValueError(
            f"Expected one {heading!r} heading after CONTENTS; "
            f"found {len(heading_positions)}"
        )

    story_index = heading_positions[0]

    return "\n".join(
        lines[:contents_index] + lines[story_index:]
    )


def clean_book(filename, metadata):
    source_path = RAW_DIR / filename

    if not source_path.is_file():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    text, start_line, end_line = extract_gutenberg_text(source_path)

    if metadata["title"] == "Crime and Punishment":
        text = remove_contents(
            text,
            metadata["contents_end_heading"],
            metadata["contents_end_occurrence"],
        )

    elif metadata["title"] == "White Nights and Other Stories":
        text = remove_white_nights_contents(
            text,
            metadata["first_story_heading"],
        )

    # Remove publisher material and everything after it.
    end_before = metadata.get("end_before")

    if end_before:
        match = re.search(
            rf"(?im)^\s*{re.escape(end_before)}\s*$",
            text,
        )

        if not match:
            raise ValueError(
                f"Could not find ending marker: {end_before}"
            )

        text = text[:match.start()]

    # Normalize paragraph spacing without joining separate paragraphs.
    paragraphs = re.split(r"\n\s*\n+", text)
    paragraphs = [
        re.sub(r"[ \t]+", " ", paragraph).strip()
        for paragraph in paragraphs
    ]
    paragraphs = [p for p in paragraphs if p]

    cleaned = "\n\n".join(paragraphs).strip() + "\n"

    if len(cleaned) < 1000:
        raise ValueError(
            f"Cleaned output is unexpectedly short: "
            f"{len(cleaned)} characters"
        )

    # Basic checks before writing the output.
    if "\ufffd" in cleaned:
        raise ValueError("Output contains Unicode replacement characters.")

    if "*** START OF THE PROJECT GUTENBERG EBOOK" in cleaned:
        raise ValueError("Output still contains a Gutenberg start marker.")

    if "*** END OF THE PROJECT GUTENBERG EBOOK" in cleaned:
        raise ValueError("Output still contains a Gutenberg end marker.")

    if metadata["title"] == "White Nights and Other Stories":
        if end_before.casefold() in cleaned.casefold():
            raise ValueError("Publisher's printing notice remains in output.")

        if "Transcriber's Notes:" in cleaned:
            raise ValueError("Transcriber's notes remain in output.")

        if not re.search(r"(?m)^WHITE NIGHTS$", cleaned):
            raise ValueError("The White Nights story heading is missing.")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DIR / metadata["output"]
    output_path.write_text(cleaned, encoding="utf-8")

    return {
        "source_file": filename,
        "output_file": metadata["output"],
        "title": metadata["title"],
        "translator": metadata["translator"],
        "gutenberg_start_line": start_line,
        "gutenberg_end_line": end_line,
        "cleaned_characters": len(cleaned),
        "paragraph_count": len(paragraphs),
        "word_count_approx": len(re.findall(r"\b[\w'-]+\b", cleaned)),
        "first_200_characters": cleaned[:200],
        "last_200_characters": cleaned[-200:],
    }


def main():
    reports = []

    for filename, metadata in BOOKS.items():
        print(f"\nProcessing: {filename}")

        report = clean_book(filename, metadata)
        reports.append(report)

        print(f"  Characters: {report['cleaned_characters']:,}")
        print(f"  Approximate words: {report['word_count_approx']:,}")
        print(f"  Paragraphs: {report['paragraph_count']:,}")
        print(f"  First text: {report['first_200_characters']!r}")
        print(f"  Last text: {report['last_200_characters']!r}")
        print("  Validation: passed")

    report_path = PROCESSED_DIR / "corpus_report.json"
    report_path.write_text(
        json.dumps(reports, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"\nReport saved to: {report_path}")
    print("Original source files were not modified.")


if __name__ == "__main__":
    main()
