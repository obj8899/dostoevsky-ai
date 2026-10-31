"""Unit tests for evaluation/evaluate_endpoints.py logic.

Tests all pure evaluation logic, classification rules, failure taxonomy, metadata
capture, model mismatch detection, interruption resilience, and atomic collision
protection without invoking live Ollama generation or requiring an active server.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest

# Ensure project root is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluation.evaluate_endpoints import (
    claim_result_file,
    classify_word_cabinet_output,
    evaluate_case,
    generate_run_id,
    get_all_ollama_tags,
    get_git_provenance,
    resolve_model_provenance,
    run_automated_checks,
    run_evaluation,
    sha256_file,
)


# --- 1. Word Cabinet Output Classification ---


def test_classify_word_cabinet_full_count():
    words = [{"word": "melancholy"}, {"word": "angst"}, {"word": "dread"}]
    warnings = []
    status, msgs = classify_word_cabinet_output(3, words, warnings)
    assert status == "full_count"
    assert msgs == []


def test_classify_word_cabinet_partial_with_honest_warning():
    words = [{"word": "melancholy"}, {"word": "angst"}]
    warnings = ["The model returned 2 usable entries; 4 requested."]
    status, msgs = classify_word_cabinet_output(4, words, warnings)
    assert status == "partial_with_honest_warning"
    assert len(msgs) == 1
    assert "2 usable entries; 4 requested" in msgs[0]


def test_classify_word_cabinet_partial_with_count_digits_in_warning():
    words = [{"word": "grief"}]
    warnings = ["Returned 1 out of 3 requested items."]
    status, msgs = classify_word_cabinet_output(3, words, warnings)
    assert status == "partial_with_honest_warning"


def test_classify_word_cabinet_partial_unexplained():
    words = [{"word": "melancholy"}, {"word": "angst"}]
    warnings = []  # No warning emitted!
    status, msgs = classify_word_cabinet_output(4, words, warnings)
    assert status == "partial_unexplained"
    assert len(msgs) == 1
    assert "without transparent warning" in msgs[0]


def test_classify_word_cabinet_excess_entries():
    words = [{"word": "a"}, {"word": "b"}, {"word": "c"}, {"word": "d"}]
    warnings = []
    status, msgs = classify_word_cabinet_output(3, words, warnings)
    assert status == "excess_entries_unfiltered"
    assert len(msgs) == 1


# --- 2. Automated Checks for Literary Rewrite ---


def test_literary_rewrite_checks_clean_match():
    case = {
        "diagnostic_metrics": {"reference_word_count_range": [10, 100]},
    }
    response = {
        "rewritten_text": "He walked into the dark quiet hall and hesitated.",
        "word_count": 9,
    }
    checks = run_automated_checks("literary_rewrite", case, response)
    assert checks["invariants"]["word_count_matches_whitespace_split"] is True
    # 9 is below [10, 100], so it flags a diagnostic warning but does NOT fail automated checks!
    assert checks["invariants"]["in_diagnostic_reference_range"] is False
    assert checks["status"] == "pass"
    assert any("diagnostic only" in w for w in checks["diagnostic_warnings"])


def test_literary_rewrite_checks_recalculation_mismatch():
    case = {}
    response = {
        "rewritten_text": "He walked into the hall.",
        "word_count": 99,  # False word count reported by backend!
    }
    checks = run_automated_checks("literary_rewrite", case, response)
    assert checks["status"] == "fail"
    assert checks["invariants"]["word_count_matches_whitespace_split"] is False
    assert any("Word count mismatch" in w for w in checks["diagnostic_warnings"])


# --- 3. Automated Checks for Word Cabinet ---


def test_word_cabinet_checks_clean_pass():
    case = {"request_payload": {"count": 3}}
    response = {
        "words": [
            {
                "word": "resentment",
                "part_of_speech": "noun",
                "definition": "A feeling of deep displeasure.",
                "connotation": "Bitter and persistent.",
                "intensity": 3,
                "distinction": "More enduring than anger.",
                "example": "He nursed his resentment in silence.",
            },
            {
                "word": "spite",
                "part_of_speech": "noun",
                "definition": "A desire to hurt or humiliate.",
                "connotation": "Petty and malicious.",
                "intensity": 4,
                "distinction": "Focuses on petty hurt rather than grievance.",
                "example": "She acted out of pure spite.",
            },
            {
                "word": "rancor",
                "part_of_speech": "noun",
                "definition": "Bitter, long-lasting resentment.",
                "connotation": "Deep-seated hostility.",
                "intensity": 5,
                "distinction": "Implies venomous persistence.",
                "example": "The dispute ended in lasting rancor.",
            },
        ],
        "validation_warnings": [],
    }
    checks = run_automated_checks("word_cabinet", case, response)
    assert checks["status"] == "pass"
    assert checks["invariants"]["entries_schema_valid"] is True
    assert checks["invariants"]["no_duplicate_lemmas"] is True
    assert checks["invariants"]["completeness_classification"] == "full_count"


def test_word_cabinet_checks_duplicate_words_fail():
    case = {"request_payload": {"count": 2}}
    response = {
        "words": [
            {
                "word": "Resentment",
                "part_of_speech": "noun",
                "definition": "Def 1",
                "connotation": "Con 1",
                "intensity": 3,
                "distinction": "Dist 1",
                "example": "Ex 1",
            },
            {
                "word": "resentment",  # Duplicate casefold lemma!
                "part_of_speech": "noun",
                "definition": "Def 2",
                "connotation": "Con 2",
                "intensity": 3,
                "distinction": "Dist 2",
                "example": "Ex 2",
            },
        ],
        "validation_warnings": [],
    }
    checks = run_automated_checks("word_cabinet", case, response)
    assert checks["status"] == "fail"
    assert checks["invariants"]["no_duplicate_lemmas"] is False


def test_word_cabinet_checks_partial_warned_passes_with_diag_warning():
    case = {"request_payload": {"count": 4}}
    response = {
        "words": [
            {
                "word": "grief",
                "part_of_speech": "noun",
                "definition": "Deep sorrow.",
                "connotation": "Heavy and quiet.",
                "intensity": 4,
                "distinction": "Distinction from sadness.",
                "example": "His grief was quiet.",
            }
        ],
        "validation_warnings": ["The model returned 1 usable entry; 4 requested."],
    }
    checks = run_automated_checks("word_cabinet", case, response)
    # Honest warning means contract status passes, but diagnostic warning is logged
    assert checks["status"] == "pass"
    assert checks["invariants"]["completeness_classification"] == "partial_with_honest_warning"
    assert any("honest warning present" in w for w in checks["diagnostic_warnings"])


# --- 4. Automated Checks for Inner Monologue ---


def test_inner_monologue_checks_clean_in_range():
    text = "Word " * 200
    case = {}
    response = {
        "generated_text": text.strip(),
        "word_count": 200,
        "requested_min_words": 180,
        "requested_max_words": 250,
        "within_requested_range": True,
        "validation_warnings": [],
    }
    checks = run_automated_checks("inner_monologue", case, response)
    assert checks["status"] == "pass"
    assert checks["invariants"]["word_count_matches_whitespace_split"] is True
    assert checks["invariants"]["range_boolean_accurate"] is True
    assert checks["invariants"]["range_warning_consistent"] is True


def test_inner_monologue_checks_out_of_range_with_honest_warning():
    text = "Word " * 120  # Under requested minimum 180
    case = {}
    response = {
        "generated_text": text.strip(),
        "word_count": 120,
        "requested_min_words": 180,
        "requested_max_words": 250,
        "within_requested_range": False,
        "validation_warnings": [
            "The response contains 120 whitespace-delimited words; the requested minimum is 180."
        ],
    }
    checks = run_automated_checks("inner_monologue", case, response)
    # The boolean and warning are consistent, so checks pass with a diagnostic note
    assert checks["status"] == "pass"
    assert checks["invariants"]["range_boolean_accurate"] is True
    assert checks["invariants"]["range_warning_consistent"] is True
    assert any("honest warning present" in w for w in checks["diagnostic_warnings"])


def test_inner_monologue_checks_range_flag_contradiction_fails():
    text = "Word " * 120
    case = {}
    response = {
        "generated_text": text.strip(),
        "word_count": 120,
        "requested_min_words": 180,
        "requested_max_words": 250,
        "within_requested_range": True,  # Contradiction: 120 is NOT in [180, 250]!
        "validation_warnings": [],
    }
    checks = run_automated_checks("inner_monologue", case, response)
    assert checks["status"] == "fail"
    assert checks["invariants"]["range_boolean_accurate"] is False


# --- 5. Ollama Metadata Capture & Serving Model Association ---


def test_get_all_ollama_tags_success():
    mock_payload = {
        "models": [
            {
                "name": "dostoevsky-baseline:latest",
                "digest": "c6fb3dc8d97a4e8cab26b0ea088705887efce3f582a01bfb9049f5ef8e1033c9",
                "size": 1929914040,
                "modified_at": "2026-10-23T22:19:54.8803105+05:30",
                "details": {"format": "gguf", "parameter_size": "3.1B"},
            },
            {
                "name": "dostoevsky-experiment1:latest",
                "digest": "e7cdbe1467f299b3900191f053b45c58f51fc0d0cbce1099cd6f5120fd3605fc",
                "size": 1929915327,
                "modified_at": "2026-10-24T10:28:44.9202882+05:30",
                "details": {"format": "gguf", "parameter_size": "3.1B"},
            },
        ]
    }
    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = mock_payload

    with patch.object(httpx.Client, "get", return_value=mock_response):
        tags_map, error = get_all_ollama_tags("http://fake-ollama:11434")
        assert error is None
        assert "dostoevsky-baseline:latest" in tags_map
        assert "dostoevsky-experiment1:latest" in tags_map


def test_resolve_model_provenance_clean_match():
    tags_map = {
        "dostoevsky-baseline:latest": {
            "digest": "digest_baseline_123",
            "details": {"family": "qwen2"},
        }
    }
    res = resolve_model_provenance("dostoevsky-baseline:latest", "dostoevsky-baseline:latest", tags_map, None)
    assert res["model_match"] is True
    assert res["actual_serving_model"] == "dostoevsky-baseline:latest"
    assert res["serving_model_digest"] == "digest_baseline_123"
    assert res["limitation"] is None


def test_resolve_model_provenance_mismatch_detected():
    tags_map = {
        "dostoevsky-baseline:latest": {"digest": "digest_baseline_123"},
        "dostoevsky-experiment1:latest": {"digest": "digest_exp1_456"},
    }
    # Expected baseline, but application served experiment1!
    res = resolve_model_provenance(
        "dostoevsky-experiment1:latest", "dostoevsky-baseline:latest", tags_map, None
    )
    assert res["model_match"] is False
    assert res["actual_serving_model"] == "dostoevsky-experiment1:latest"
    # Associates the digest with the ACTUAL serving model!
    assert res["serving_model_digest"] == "digest_exp1_456"
    assert "Serving model mismatch" in res["limitation"]


def test_resolve_model_provenance_missing_model_in_response():
    tags_map = {"dostoevsky-baseline:latest": {"digest": "digest_123"}}
    res = resolve_model_provenance(None, "dostoevsky-baseline:latest", tags_map, None)
    assert res["model_match"] is False
    assert res["actual_serving_model"] is None
    assert res["serving_model_digest"] is None
    assert "did not declare a serving model" in res["limitation"]


def test_get_git_provenance():
    prov = get_git_provenance()
    assert "commit_hash" in prov
    assert "is_dirty" in prov
    assert prov["error"] is None


def test_sha256_file_existing_and_missing(tmp_path: Path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("Hello Dostoevsky", encoding="utf-8")
    h = sha256_file(test_file)
    assert isinstance(h, str) and len(h) == 64

    missing_file = tmp_path / "nonexistent.txt"
    assert sha256_file(missing_file) is None


# --- 6. Execution Errors, Failure Taxonomy, and Atomic Collision Protection ---


def test_evaluate_case_transport_error():
    case = {
        "id": "LR01",
        "feature": "literary_rewrite",
        "request_payload": {"text": "Hello world."},
    }
    client = MagicMock()
    client.post.side_effect = httpx.ConnectError("Connection refused to :8000")

    result = evaluate_case(
        client, "http://localhost:8000", "/api/features/literary-rewrite", case,
        "dostoevsky-baseline:latest", {}, None, 5.0
    )
    assert result["execution_status"] == "transport_error"
    assert result["contract_status"] == "fail"
    assert result["failure_category"] == "transport_error"
    assert "HTTP request failed: ConnectError" in result["error_detail"]


def test_evaluate_case_timeout_error():
    case = {
        "id": "LR01",
        "feature": "literary_rewrite",
        "request_payload": {"text": "Hello world."},
    }
    client = MagicMock()
    client.post.side_effect = httpx.TimeoutException("Read timed out")

    result = evaluate_case(
        client, "http://localhost:8000", "/api/features/literary-rewrite", case,
        "dostoevsky-baseline:latest", {}, None, 5.0
    )
    assert result["execution_status"] == "timeout_error"
    assert result["contract_status"] == "fail"
    assert result["failure_category"] == "timeout_error"
    assert "Request timed out" in result["error_detail"]


def test_evaluate_case_http_502_error_not_processed_as_feature_response():
    case = {
        "id": "WC01",
        "feature": "word_cabinet",
        "request_payload": {"context": "Guilt.", "count": 3},
    }
    mock_response = MagicMock(status_code=502)
    mock_response.json.return_value = {"detail": "Ollama generation failed."}
    client = MagicMock()
    client.post.return_value = mock_response

    result = evaluate_case(
        client, "http://localhost:8000", "/api/features/word-cabinet", case,
        "dostoevsky-baseline:latest", {}, None, 5.0
    )
    assert result["execution_status"] == "success"
    assert result["contract_status"] == "fail"
    assert result["failure_category"] == "http_error"
    assert result["http_status"] == 502
    assert "HTTP 502: Ollama generation failed." in result["error_detail"]


def test_evaluate_case_malformed_json_response():
    case = {
        "id": "IM01",
        "feature": "inner_monologue",
        "request_payload": {"scenario": "A test.", "perspective": "first_person", "min_words": 180, "max_words": 250},
    }
    mock_response = MagicMock(status_code=200)
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_response.text = "This is not valid json {"
    client = MagicMock()
    client.post.return_value = mock_response

    result = evaluate_case(
        client, "http://localhost:8000", "/api/features/inner-monologue", case,
        "dostoevsky-baseline:latest", {}, None, 5.0
    )
    assert result["contract_status"] == "fail"
    assert result["failure_category"] == "malformed_json"
    assert "Response body was not valid JSON." in result["error_detail"]


def test_atomic_claim_refuses_overwrite(tmp_path: Path):
    target_file = tmp_path / "claimed_result.json"
    claim_result_file(target_file, {"initial": "data"})
    assert target_file.is_file()

    # Competing write must fail atomically with FileExistsError
    with pytest.raises(FileExistsError):
        claim_result_file(target_file, {"competing": "data"})


def test_run_evaluation_interrupted_run_preserves_records(tmp_path: Path):
    spec_file = tmp_path / "test_spec.json"
    spec_data = {
        "suite_name": "Test Suite",
        "suite_version": "1.0",
        "target_model_expected": "test-model:latest",
        "endpoints": {"literary_rewrite": "/api/features/literary-rewrite"},
        "test_cases": [
            {"id": "LR01", "feature": "literary_rewrite", "request_payload": {"text": "Case 1"}},
            {"id": "LR02", "feature": "literary_rewrite", "request_payload": {"text": "Case 2"}},
        ],
    }
    spec_file.write_text(json.dumps(spec_data), encoding="utf-8")
    output_dir = tmp_path / "results"

    call_count = 0

    def mock_post(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            resp = MagicMock(status_code=200)
            resp.json.return_value = {
                "original_text": "Case 1",
                "rewritten_text": "Rewritten 1",
                "word_count": 2,
                "model": "test-model:latest",
                "validation_warnings": [],
            }
            return resp
        # Simulate an abrupt crash on Case 2
        raise KeyboardInterrupt("Simulated user abort")

    with patch.object(httpx.Client, "post", side_effect=mock_post):
        with pytest.raises(KeyboardInterrupt):
            run_evaluation(
                spec_path=spec_file,
                output_dir=output_dir,
            )

    # Verify that the result file was preserved with run_status='interrupted' and Case 1 saved!
    result_files = list(output_dir.glob("run_*.json"))
    assert len(result_files) == 1
    saved_doc = json.loads(result_files[0].read_text(encoding="utf-8"))
    assert saved_doc["metadata"]["run_status"] == "interrupted"
    assert saved_doc["summary"]["is_complete"] is False
    assert saved_doc["summary"]["completed"] == 1
    assert len(saved_doc["results"]) == 1
    assert saved_doc["results"][0]["test_id"] == "LR01"
