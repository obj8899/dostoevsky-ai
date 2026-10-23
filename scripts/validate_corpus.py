
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent

BOOKS = {
    "Crime and Punishment": {
        "raw": ROOT / "data/raw/crime_and_punishment_garnett.txt",
        "clean": ROOT / "data/processed/crime_and_punishment_clean.txt",
        "kind": "crime",
        "required_headings": [
            "TRANSLATOR’S PREFACE",
            "PART I",
            "PART II",
            "PART III",
            "PART IV",
            "PART V",
            "PART VI",
            "EPILOGUE",
        ],
    },
    "White Nights and Other Stories": {
        "raw": ROOT / "data/raw/white_nights_and_other_stories_garnett.txt",
        "clean": ROOT / "data/processed/white_nights_and_other_stories_clean.txt",
        "kind": "white_nights",
        "required_headings": [
            "WHITE NIGHTS",
            "NOTES FROM UNDERGROUND",
            "A FAINT HEART",
            "A CHRISTMAS TREE AND A WEDDING",
            "POLZUNKOV",
            "A LITTLE HERO",
            "MR. PROHARTCHIN",
        ],
    },
}

START_PATTERN = re.compile(
    r"^\s*\*\*\*\s+START\s+OF THE PROJECT GUTENBERG EBOOK\b",
    re.IGNORECASE,
)

END_PATTERN = re.compile(
    r"^\s*\*\*\*\s+END\s+OF THE PROJECT GUTENBERG EBOOK\b",
    re.IGNORECASE,
)

PUBLISHER_END = (
    "PRINTED IN GREAT BRITAIN BY RICHARD CLAY & SONS, LIMITED,"
)


def read_text(path):
    return path.read_text(encoding="utf-8-sig")


def extract_body(raw_text):
    """Extract only the lines between the Gutenberg marker lines."""
    lines = raw_text.splitlines()

    starts = [i for i, line in enumerate(lines) if START_PATTERN.search(line)]
    ends = [i for i, line in enumerate(lines) if END_PATTERN.search(line)]

    if len(starts) != 1 or len(ends) != 1:
        raise ValueError(
            f"Expected one start and end marker; "
            f"found {len(starts)} start and {len(ends)} end."
        )

    if starts[0] >= ends[0]:
        raise ValueError("Gutenberg markers are out of order.")

    return "\n".join(lines[starts[0] + 1:ends[0]])


def remove_crime_contents(text):
    lines = text.splitlines()

    contents = [
        i for i, line in enumerate(lines)
        if line.strip().casefold() == "contents"
    ]

    if not contents:
        raise ValueError("Crime and Punishment: CONTENTS heading missing.")

    headings = [
        i for i, line in enumerate(lines)
        if line.strip().casefold() == "translator’s preface"
        and i > contents[0]
    ]

    if len(headings) < 2:
        raise ValueError(
            "Crime and Punishment: expected two TRANSLATOR’S PREFACE "
            "headings after CONTENTS."
        )

    resume_at = headings[1]
    return "\n".join(lines[:contents[0]] + lines[resume_at:])


def remove_white_nights_contents(text):
    lines = text.splitlines()

    contents = [
        i for i, line in enumerate(lines)
        if line.strip().casefold() == "contents"
    ]

    if len(contents) != 1:
        raise ValueError(
            f"White Nights: expected one CONTENTS heading; found {len(contents)}."
        )

    headings = [
        i for i, line in enumerate(lines)
        if line.strip().casefold() == "white nights"
        and i > contents[0]
    ]

    if len(headings) != 1:
        raise ValueError(
            "White Nights: expected one actual WHITE NIGHTS heading "
            "after CONTENTS."
        )

    return "\n".join(lines[:contents[0]] + lines[headings[0]:])


def remove_publisher_material(text):
    pattern = re.compile(
        rf"(?im)^\s*{re.escape(PUBLISHER_END)}\s*$"
    )
    matches = list(pattern.finditer(text))

    if len(matches) != 1:
        raise ValueError(
            f"Expected one publisher boundary; found {len(matches)}."
        )

    return text[:matches[0].start()]


def normalize_text(text):
    paragraphs = re.split(r"\n\s*\n+", text)
    paragraphs = [
        re.sub(r"[ \t]+", " ", paragraph).strip()
        for paragraph in paragraphs
    ]
    paragraphs = [paragraph for paragraph in paragraphs if paragraph]
    return "\n\n".join(paragraphs).strip() + "\n"


def normalize_heading(line):
    line = re.sub(r"\[\d+\]", "", line.strip())
    return line.casefold().strip()


def audit_book(title, config):
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")

    raw_path = config["raw"]
    clean_path = config["clean"]

    for path in (raw_path, clean_path):
        if not path.is_file():
            print(f"FAIL: Missing file: {path}")
            return False

    try:
        raw_text = read_text(raw_path)
        clean_text = read_text(clean_path)
        source = extract_body(raw_text)

        if config["kind"] == "crime":
            source = remove_crime_contents(source)
        else:
            source = remove_white_nights_contents(source)
            source = remove_publisher_material(source)

        expected = normalize_text(source)

    except (OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}")
        return False

    checks = []

    checks.append((
        "Exact normalized-text comparison",
        expected == clean_text,
    ))

    checks.append((
        "No Unicode replacement characters",
        "\ufffd" not in clean_text,
    ))

    checks.append((
        "No Gutenberg marker lines",
        not START_PATTERN.search(clean_text)
        and not END_PATTERN.search(clean_text),
    ))

    checks.append((
        "No publisher printing notice",
        PUBLISHER_END.casefold() not in clean_text.casefold(),
    ))

    if config["kind"] == "white_nights":
        checks.append((
            "No transcriber notes",
            "transcriber's notes:" not in clean_text.casefold(),
        ))

    cleaned_headings = [
        normalize_heading(line) for line in clean_text.splitlines()
    ]

    for heading in config["required_headings"]:
        present = normalize_heading(heading) in cleaned_headings
        checks.append((f"Required heading: {heading}", present))

    # Verify the seven stories appear in the expected order.
    if config["kind"] == "white_nights":
        story_order = config["required_headings"]
        positions = []
        for heading in story_order:
            normalized = normalize_heading(heading)
            position = next(
                (
                    i for i, line in enumerate(cleaned_headings)
                    if line == normalized
                ),
                None,
            )
            positions.append(position)

        ordered = (
            all(position is not None for position in positions)
            and positions == sorted(positions)
        )
        checks.append(("Required story order", ordered))

    for label, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'}: {label}")

    print(f"Expected characters: {len(expected):,}")
    print(f"Cleaned characters:  {len(clean_text):,}")

    if expected != clean_text:
        limit = min(len(expected), len(clean_text))
        index = next(
            (
                i for i in range(limit)
                if expected[i] != clean_text[i]
            ),
            limit,
        )
        print(f"First text difference at character index: {index}")
        print(f"Expected: {expected[max(0, index - 50):index + 100]!r}")
        print(f"Actual:   {clean_text[max(0, index - 50):index + 100]!r}")

    passed_count = sum(passed for _, passed in checks)
    print(f"Checks passed: {passed_count}/{len(checks)}")

    return all(passed for _, passed in checks)


def main():
    results = [
        audit_book(title, config)
        for title, config in BOOKS.items()
    ]

    all_passed = all(results)

    print(f"\n{'=' * 72}")
    print(f"CORPUS VALIDATION: {'PASS' if all_passed else 'FAIL'}")
    print("Read-only audit: corpus files were not modified.")
    print(f"{'=' * 72}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())