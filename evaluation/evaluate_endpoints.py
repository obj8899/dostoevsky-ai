"""Rigorous endpoint-level evaluator for Dostoevsky AI.

Executes test cases from evaluation/endpoint_test_cases.json against the live
FastAPI application over HTTP using httpx.Client.

Enforces:
- Collision-resistant run IDs and atomic exclusive file creation (O_CREAT | O_EXCL).
- Incremental state saving so interrupted runs preserve completed cases with run_status="interrupted".
- Distinct failure taxonomy: transport_error, timeout_error, http_error, malformed_json,
  schema_violation, invariant_violation.
- Direct association of serving model digest with the model declared in the response,
  with explicit mismatch detection.
- Granular Word Cabinet completeness classification (full vs. warned partial vs. unexplained vs. excess).
- Diagnostic-only observation of Literary Rewrite word counts.
- Word-count and range invariant checks for Inner Monologue, leaving POV evaluation to human raters.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVALUATION_DIR = PROJECT_ROOT / "evaluation"
DEFAULT_SPEC_PATH = EVALUATION_DIR / "endpoint_test_cases.json"
DEFAULT_OUTPUT_DIR = EVALUATION_DIR / "endpoint_results"
DEFAULT_BASE_URL = "http://localhost:8000"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_REQUEST_TIMEOUT = 190.0

# Relevant source files whose SHA-256 hashes establish run provenance
PROVENANCE_SOURCE_FILES = [
    PROJECT_ROOT / "evaluation" / "endpoint_test_cases.json",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "main.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "config.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "api" / "features" / "literary_rewrite.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "api" / "features" / "word_cabinet.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "api" / "features" / "inner_monologue.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "prompts" / "literary_rewrite.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "prompts" / "word_cabinet.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "prompts" / "inner_monologue.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "schemas" / "word_cabinet.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "schemas" / "inner_monologue.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "services" / "literary_rewrite.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "services" / "word_cabinet.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "services" / "inner_monologue.py",
    PROJECT_ROOT / "backend" / "src" / "dostoevsky_ai" / "services" / "ollama_client.py",
]


def sha256_file(path: Path) -> str | None:
    """Return the SHA-256 hash of a file, or None if it cannot be read."""
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    try:
        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def get_git_provenance() -> dict[str, Any]:
    """Capture git commit SHA and dirty-worktree status without modifying git state."""
    provenance: dict[str, Any] = {
        "commit_hash": None,
        "branch": None,
        "is_dirty": None,
        "error": None,
    }
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if commit.returncode == 0:
            provenance["commit_hash"] = commit.stdout.strip()

        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if branch.returncode == 0:
            provenance["branch"] = branch.stdout.strip()

        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if status.returncode == 0:
            provenance["is_dirty"] = bool(status.stdout.strip())
    except Exception as exc:  # pragma: no cover
        provenance["error"] = f"Failed to read git provenance: {exc}"

    return provenance


def get_all_ollama_tags(ollama_url: str) -> tuple[dict[str, dict[str, Any]], str | None]:
    """Query Ollama /api/tags once to build a lookup table of installed models and digests.

    Returns:
        (tags_by_model_name, limitation_or_error_string)
    """
    base_url = ollama_url.rstrip("/")
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{base_url}/api/tags")
            if response.status_code != 200:
                return {}, f"Ollama /api/tags returned HTTP {response.status_code}."
            payload = response.json()
    except Exception as exc:
        return {}, f"Could not connect to Ollama at {base_url}/api/tags: {type(exc).__name__}."

    models = payload.get("models") if isinstance(payload, dict) else None
    if not isinstance(models, list):
        return {}, "Ollama /api/tags payload contained no 'models' list."

    tags_map: dict[str, dict[str, Any]] = {}
    for item in models:
        if isinstance(item, dict) and "name" in item:
            tags_map[item["name"]] = {
                "digest": item.get("digest"),
                "details": item.get("details"),
                "size_bytes": item.get("size"),
                "modified_at": item.get("modified_at"),
            }
    return tags_map, None


def resolve_model_provenance(
    actual_model: str | None,
    expected_model: str,
    ollama_tags_map: dict[str, dict[str, Any]],
    ollama_error: str | None,
) -> dict[str, Any]:
    """Resolve digest and mismatch flags for the model actually declared by the response."""
    result: dict[str, Any] = {
        "target_model_expected": expected_model,
        "actual_serving_model": actual_model,
        "model_match": None,
        "serving_model_digest": None,
        "serving_model_details": None,
        "limitation": None,
    }

    if not actual_model:
        result["model_match"] = False
        result["limitation"] = "Response did not declare a serving model field."
        return result

    result["model_match"] = actual_model == expected_model
    if not result["model_match"]:
        result["limitation"] = (
            f"Serving model mismatch: expected '{expected_model}', but application reported '{actual_model}'."
        )

    if actual_model in ollama_tags_map:
        info = ollama_tags_map[actual_model]
        result["serving_model_digest"] = info.get("digest")
        result["serving_model_details"] = info.get("details")
    else:
        limitation_suffix = (
            f" ({ollama_error})"
            if ollama_error
            else f" (Model '{actual_model}' not found in installed Ollama tags)."
        )
        if result["limitation"]:
            result["limitation"] += limitation_suffix
        else:
            result["limitation"] = f"Could not obtain digest for serving model '{actual_model}'{limitation_suffix}"

    return result


def generate_run_id() -> str:
    """Generate a collision-resistant run identifier with UTC timestamp and full UUID4 hex."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    unique_suffix = uuid.uuid4().hex
    return f"run_{timestamp}_{unique_suffix}"


def claim_result_file(output_path: Path, initial_document: dict[str, Any]) -> None:
    """Atomically claim the output file path using O_CREAT | O_EXCL.

    Guarantees race-safe collision protection against concurrent runs.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Mode 'x' opens for exclusive creation, failing with FileExistsError if existing
    with output_path.open("x", encoding="utf-8") as f:
        json.dump(initial_document, f, indent=2, ensure_ascii=False)


def save_atomic_results(output_path: Path, document: dict[str, Any]) -> None:
    """Safely update output document by writing to a unique temp file and replacing."""
    temp_path = output_path.parent / f".tmp_{output_path.stem}_{os.getpid()}_{uuid.uuid4().hex[:8]}.tmp"
    with temp_path.open("w", encoding="utf-8") as f:
        json.dump(document, f, indent=2, ensure_ascii=False)
    temp_path.replace(output_path)


def classify_word_cabinet_output(
    requested_count: int,
    words: list[Any],
    validation_warnings: list[str],
) -> tuple[str, list[str]]:
    """Classify Word Cabinet completeness distinguishing transparent partials from defects.

    Returns:
        (classification_status, diagnostic_messages)
    """
    actual_count = len(words)
    if actual_count == requested_count:
        return "full_count", []

    if actual_count < requested_count:
        # Check if the backend emitted a transparent partial warning.
        # Checks for presence of 'usable' and 'requested', or matching count numbers in warning.
        has_transparent_warning = any(
            ("usable" in w.casefold() and "requested" in w.casefold())
            or (str(actual_count) in w and str(requested_count) in w)
            for w in validation_warnings
        )
        if has_transparent_warning:
            return "partial_with_honest_warning", [
                f"Model returned {actual_count} usable entries; {requested_count} requested (honest warning present)."
            ]
        return "partial_unexplained", [
            f"Model returned {actual_count} usable entries; {requested_count} requested without transparent warning."
        ]

    # actual_count > requested_count
    return "excess_entries_unfiltered", [
        f"Model returned {actual_count} entries; {requested_count} requested (excess entries not capped)."
    ]


def run_automated_checks(
    feature: str,
    case: dict[str, Any],
    response_json: dict[str, Any],
) -> dict[str, Any]:
    """Execute deterministic invariant checks and collect non-failing diagnostic warnings."""
    checks: dict[str, Any] = {
        "status": "pass",
        "invariants": {},
        "diagnostic_warnings": [],
    }

    if feature == "literary_rewrite":
        rewritten = response_json.get("rewritten_text", "")
        reported_count = response_json.get("word_count")
        recalculated_count = len(rewritten.strip().split())
        count_matches = reported_count == recalculated_count
        checks["invariants"]["word_count_matches_whitespace_split"] = count_matches
        if not count_matches:
            checks["status"] = "fail"
            checks["diagnostic_warnings"].append(
                f"Word count mismatch: backend reported {reported_count}, calculated {recalculated_count}."
            )

        # Diagnostic word-count range check (does NOT fail contract status)
        diag_range = case.get("diagnostic_metrics", {}).get("reference_word_count_range")
        if diag_range and len(diag_range) == 2:
            min_ref, max_ref = diag_range
            in_range = min_ref <= recalculated_count <= max_ref
            checks["invariants"]["in_diagnostic_reference_range"] = in_range
            if not in_range:
                checks["diagnostic_warnings"].append(
                    f"Output word count {recalculated_count} outside reference range [{min_ref}, {max_ref}] (diagnostic only)."
                )

    elif feature == "word_cabinet":
        words = response_json.get("words", [])
        warnings = response_json.get("validation_warnings", [])
        requested_count = case.get("request_payload", {}).get("count", 6)

        # Check entry schemas and duplicate lemmas
        seen_words: set[str] = set()
        has_duplicates = False
        valid_entries = True
        allowed_pos = {"noun", "verb", "adjective", "adverb", "phrase"}

        if not isinstance(words, list) or not words:
            valid_entries = False
        else:
            for entry in words:
                if not isinstance(entry, dict):
                    valid_entries = False
                    break
                w_str = str(entry.get("word", "")).strip().casefold()
                if not w_str or w_str in seen_words:
                    has_duplicates = True
                seen_words.add(w_str)

                pos = entry.get("part_of_speech")
                intensity = entry.get("intensity")
                if (
                    pos not in allowed_pos
                    or not isinstance(intensity, int)
                    or not (1 <= intensity <= 5)
                    or not str(entry.get("definition", "")).strip()
                    or not str(entry.get("connotation", "")).strip()
                    or not str(entry.get("distinction", "")).strip()
                    or not str(entry.get("example", "")).strip()
                ):
                    valid_entries = False
                    break

        checks["invariants"]["entries_schema_valid"] = valid_entries
        checks["invariants"]["no_duplicate_lemmas"] = not has_duplicates

        if not valid_entries or has_duplicates:
            checks["status"] = "fail"
            if not valid_entries:
                checks["diagnostic_warnings"].append("One or more vocabulary entries failed schema validation.")
            if has_duplicates:
                checks["diagnostic_warnings"].append("Vocabulary entries contain duplicate words.")

        classification, diag_msgs = classify_word_cabinet_output(requested_count, words, warnings)
        checks["invariants"]["completeness_classification"] = classification
        checks["diagnostic_warnings"].extend(diag_msgs)

        if classification in {"partial_unexplained", "excess_entries_unfiltered"}:
            checks["status"] = "fail"

    elif feature == "inner_monologue":
        gen_text = response_json.get("generated_text", "")
        reported_count = response_json.get("word_count")
        recalculated_count = len(gen_text.strip().split())
        within_range = response_json.get("within_requested_range")
        min_words = response_json.get("requested_min_words")
        max_words = response_json.get("requested_max_words")
        warnings = response_json.get("validation_warnings", [])

        count_matches = reported_count == recalculated_count
        expected_within = (
            min_words is not None
            and max_words is not None
            and min_words <= recalculated_count <= max_words
        )
        range_flag_matches = within_range == expected_within

        # Warning consistency check
        range_warning_present = any(
            "requested minimum" in w.casefold() or "requested maximum" in w.casefold()
            for w in warnings
        )
        warning_consistent = (
            (not expected_within and range_warning_present)
            or (expected_within and not range_warning_present)
        )

        checks["invariants"]["word_count_matches_whitespace_split"] = count_matches
        checks["invariants"]["range_boolean_accurate"] = range_flag_matches
        checks["invariants"]["range_warning_consistent"] = warning_consistent

        if not count_matches or not range_flag_matches or not warning_consistent:
            checks["status"] = "fail"
            if not count_matches:
                checks["diagnostic_warnings"].append(
                    f"Word count mismatch: backend reported {reported_count}, calculated {recalculated_count}."
                )
            if not range_flag_matches:
                checks["diagnostic_warnings"].append(
                    f"Range boolean contradiction: backend reported {within_range}, expected {expected_within}."
                )
            if not warning_consistent:
                checks["diagnostic_warnings"].append(
                    "Warning inconsistency: range status does not match emitted warnings."
                )

        if not expected_within:
            checks["diagnostic_warnings"].append(
                f"Generated word count {recalculated_count} outside requested range [{min_words}, {max_words}] (honest warning present)."
            )

    return checks


def evaluate_case(
    client: httpx.Client,
    base_url: str,
    endpoint_path: str,
    case: dict[str, Any],
    expected_model: str,
    ollama_tags_map: dict[str, dict[str, Any]],
    ollama_error: str | None,
    timeout: float,
) -> dict[str, Any]:
    """Execute one endpoint test case over HTTP and record structured outcomes."""
    test_id = case["id"]
    feature = case["feature"]
    payload = case["request_payload"]
    url = f"{base_url.rstrip('/')}{endpoint_path}"

    result: dict[str, Any] = {
        "test_id": test_id,
        "feature": feature,
        "name": case.get("name"),
        "request_url": url,
        "request_payload": payload,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": None,
        "execution_status": "unexecuted",
        "contract_status": "fail",
        "failure_category": None,
        "automated_checks": {
            "status": "unexecuted",
            "invariants": {},
            "diagnostic_warnings": [],
        },
        "http_status": None,
        "response_body": None,
        "model_provenance": {
            "target_model_expected": expected_model,
            "actual_serving_model": None,
            "model_match": None,
            "serving_model_digest": None,
            "limitation": None,
        },
        "error_detail": None,
        "human_evaluation": {
            "criteria_scores": {
                crit_id: None
                for crit_id in case.get("human_evaluation", {}).get("criteria_guidance", {}).keys()
            },
            "criteria_guidance": case.get("human_evaluation", {}).get("criteria_guidance", {}),
            "failure_conditions": case.get("human_evaluation", {}).get("failure_conditions", []),
            "evidence_notes": None,
            "rater_id": None,
            "rated_at_utc": None,
        },
    }

    started = time.perf_counter()
    try:
        response = client.post(url, json=payload, timeout=timeout)
        elapsed = time.perf_counter() - started
        result["elapsed_seconds"] = round(elapsed, 3)
        result["http_status"] = response.status_code
        result["execution_status"] = "success"

        # 1. Parse JSON body
        try:
            body = response.json()
            result["response_body"] = body
        except Exception:
            result["response_body"] = response.text
            result["contract_status"] = "fail"
            result["failure_category"] = "malformed_json"
            result["automated_checks"]["status"] = "fail"
            result["error_detail"] = "Response body was not valid JSON."
            return result

        # 2. Check HTTP status code
        if response.status_code != 200:
            result["contract_status"] = "fail"
            result["failure_category"] = "http_error"
            result["automated_checks"]["status"] = "fail"
            detail = body.get("detail") if isinstance(body, dict) else str(body)
            result["error_detail"] = f"HTTP {response.status_code}: {detail}"
            return result

        # 3. Resolve model provenance from actual response
        actual_model = body.get("model") if isinstance(body, dict) else None
        result["model_provenance"] = resolve_model_provenance(
            actual_model, expected_model, ollama_tags_map, ollama_error
        )

        # 4. Run automated invariant and diagnostic checks
        auto_checks = run_automated_checks(feature, case, body)
        result["automated_checks"] = auto_checks

        if auto_checks["status"] == "fail":
            result["contract_status"] = "fail"
            result["failure_category"] = "invariant_violation"
            result["error_detail"] = "; ".join(auto_checks["diagnostic_warnings"])
        else:
            result["contract_status"] = "pass"
            result["failure_category"] = None

    except httpx.TimeoutException as exc:
        elapsed = time.perf_counter() - started
        result["elapsed_seconds"] = round(elapsed, 3)
        result["execution_status"] = "timeout_error"
        result["contract_status"] = "fail"
        result["failure_category"] = "timeout_error"
        result["automated_checks"]["status"] = "fail"
        result["error_detail"] = f"Request timed out after {timeout}s: {exc}"

    except httpx.RequestError as exc:
        elapsed = time.perf_counter() - started
        result["elapsed_seconds"] = round(elapsed, 3)
        result["execution_status"] = "transport_error"
        result["contract_status"] = "fail"
        result["failure_category"] = "transport_error"
        result["automated_checks"]["status"] = "fail"
        result["error_detail"] = f"HTTP request failed: {type(exc).__name__}: {exc}"

    return result


def run_evaluation(
    spec_path: Path,
    output_dir: Path,
    base_url: str = DEFAULT_BASE_URL,
    ollama_url: str = DEFAULT_OLLAMA_URL,
    feature_filter: str | None = None,
    case_ids_filter: list[str] | None = None,
    timeout: float = DEFAULT_REQUEST_TIMEOUT,
) -> Path:
    """Run the evaluation suite or subset, writing collision-proof results with incremental state."""
    if not spec_path.is_file():
        raise FileNotFoundError(f"Evaluation spec not found: {spec_path}")

    with spec_path.open("r", encoding="utf-8") as f:
        spec = json.load(f)

    target_model_expected = spec.get("target_model_expected", "dostoevsky-baseline:latest")
    endpoints: dict[str, str] = spec.get("endpoints", {})
    all_cases: list[dict[str, Any]] = spec.get("test_cases", [])

    # Filter test cases if requested
    selected_cases = all_cases
    if feature_filter:
        selected_cases = [c for c in selected_cases if c.get("feature") == feature_filter]
    if case_ids_filter:
        selected_set = {cid.strip() for cid in case_ids_filter}
        selected_cases = [c for c in selected_cases if c.get("id") in selected_set]

    if not selected_cases:
        raise ValueError("No test cases matched the specified filters.")

    run_id = generate_run_id()
    output_path = output_dir / f"{run_id}.json"

    # Query Ollama model tags table
    ollama_tags_map, ollama_error = get_all_ollama_tags(ollama_url)

    # Gather run provenance
    run_started_dt = datetime.now(timezone.utc)
    source_hashes = {
        path.name: sha256_file(path) for path in PROVENANCE_SOURCE_FILES if path.is_file()
    }
    git_provenance = get_git_provenance()

    metadata = {
        "run_id": run_id,
        "run_status": "in_progress",
        "started_at_utc": run_started_dt.isoformat(),
        "suite_name": spec.get("suite_name"),
        "suite_version": spec.get("suite_version"),
        "spec_sha256": sha256_file(spec_path),
        "target_model_expected": target_model_expected,
        "ollama_tags_captured": list(ollama_tags_map.keys()),
        "ollama_connection_error": ollama_error,
        "git_provenance": git_provenance,
        "source_hashes": source_hashes,
        "environment": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "base_url": base_url,
            "ollama_url": ollama_url,
        },
    }

    results: list[dict[str, Any]] = []
    initial_document = {
        "metadata": metadata,
        "completed_at_utc": None,
        "summary": {
            "total_cases_selected": len(selected_cases),
            "completed": 0,
            "is_complete": False,
            "contract_pass": 0,
            "contract_fail": 0,
            "transport_errors": 0,
            "timeout_errors": 0,
            "http_errors": 0,
            "invariant_violations": 0,
        },
        "results": results,
    }

    # Claim output path atomically with O_CREAT | O_EXCL
    claim_result_file(output_path, initial_document)

    print(f"\n========================================================")
    print(f" Dostoevsky AI Endpoint Evaluation")
    print(f" Run ID:   {run_id}")
    print(f" Target:   {base_url}")
    print(f" Cases:    {len(selected_cases)} selected")
    print(f" Output:   {output_path}")
    print(f"========================================================\n")

    run_succeeded = False
    try:
        with httpx.Client() as client:
            for idx, case in enumerate(selected_cases, start=1):
                cid = case["id"]
                feat = case["feature"]
                name = case.get("name", "")
                ep = endpoints.get(feat, f"/api/features/{feat.replace('_', '-')}")

                print(f"[{idx}/{len(selected_cases)}] Evaluating {cid} ({feat}: '{name}')...", end="", flush=True)
                case_result = evaluate_case(
                    client=client,
                    base_url=base_url,
                    endpoint_path=ep,
                    case=case,
                    expected_model=target_model_expected,
                    ollama_tags_map=ollama_tags_map,
                    ollama_error=ollama_error,
                    timeout=timeout,
                )
                results.append(case_result)

                exec_status = case_result["execution_status"]
                contract_status = case_result["contract_status"]
                elapsed = case_result["elapsed_seconds"]
                fail_cat = case_result.get("failure_category")
                status_suffix = f" ({fail_cat})" if fail_cat else ""
                print(f" [{exec_status.upper()} | Contract: {contract_status.upper()}{status_suffix}] ({elapsed}s)")

                # Incremental state save after every case
                interim_document = {
                    "metadata": metadata,
                    "completed_at_utc": None,
                    "summary": {
                        "total_cases_selected": len(selected_cases),
                        "completed": len(results),
                        "is_complete": len(results) == len(selected_cases),
                        "contract_pass": sum(r["contract_status"] == "pass" for r in results),
                        "contract_fail": sum(r["contract_status"] == "fail" for r in results),
                        "transport_errors": sum(r["execution_status"] == "transport_error" for r in results),
                        "timeout_errors": sum(r["execution_status"] == "timeout_error" for r in results),
                        "http_errors": sum(r.get("failure_category") == "http_error" for r in results),
                        "invariant_violations": sum(r.get("failure_category") == "invariant_violation" for r in results),
                    },
                    "results": results,
                }
                save_atomic_results(output_path, interim_document)

        run_succeeded = True
    finally:
        completed_dt = datetime.now(timezone.utc)
        final_status = "completed" if (run_succeeded and len(results) == len(selected_cases)) else "interrupted"
        metadata["run_status"] = final_status

        final_summary = {
            "total_cases_selected": len(selected_cases),
            "completed": len(results),
            "is_complete": final_status == "completed",
            "contract_pass": sum(r["contract_status"] == "pass" for r in results),
            "contract_fail": sum(r["contract_status"] == "fail" for r in results),
            "transport_errors": sum(r["execution_status"] == "transport_error" for r in results),
            "timeout_errors": sum(r["execution_status"] == "timeout_error" for r in results),
            "http_errors": sum(r.get("failure_category") == "http_error" for r in results),
            "invariant_violations": sum(r.get("failure_category") == "invariant_violation" for r in results),
        }

        final_document = {
            "metadata": metadata,
            "completed_at_utc": completed_dt.isoformat() if run_succeeded else None,
            "summary": final_summary,
            "results": results,
        }
        save_atomic_results(output_path, final_document)

    print(f"\nFinished run {run_id} (Status: {final_status}).")
    print(f"Summary: Completed {final_summary['completed']}/{final_summary['total_cases_selected']} cases. Contract Pass: {final_summary['contract_pass']}, Contract Fail: {final_summary['contract_fail']}")
    print(f"Results saved to: {output_path}\n")
    return output_path


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dostoevsky AI Endpoint-Level Evaluator"
    )
    parser.add_argument(
        "--spec",
        type=Path,
        default=DEFAULT_SPEC_PATH,
        help="Path to evaluation specification JSON.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to save evaluation results.",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default=DEFAULT_BASE_URL,
        help="FastAPI application base URL (default: http://localhost:8000).",
    )
    parser.add_argument(
        "--ollama-url",
        type=str,
        default=DEFAULT_OLLAMA_URL,
        help="Ollama base URL for metadata queries (default: http://localhost:11434).",
    )
    parser.add_argument(
        "--feature",
        choices=["literary_rewrite", "word_cabinet", "inner_monologue"],
        default=None,
        help="Filter evaluation to a single feature.",
    )
    parser.add_argument(
        "--cases",
        type=str,
        default=None,
        help="Comma-separated list of case IDs (e.g. LR01,WC01,IM01).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_REQUEST_TIMEOUT,
        help="Request timeout in seconds (default: 190.0).",
    )
    return parser.parse_args(args)


def main() -> int:
    args = parse_args()
    case_ids = [c.strip() for c in args.cases.split(",")] if args.cases else None
    try:
        run_evaluation(
            spec_path=args.spec,
            output_dir=args.output_dir,
            base_url=args.base_url,
            ollama_url=args.ollama_url,
            feature_filter=args.feature,
            case_ids_filter=case_ids,
            timeout=args.timeout,
        )
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
