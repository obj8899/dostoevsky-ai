
"""Run the fixed Dostoevsky AI baseline evaluation using local Ollama."""

import argparse
import hashlib
import json
import os
import platform
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVALUATION_DIR = PROJECT_ROOT / "evaluation"
SPEC_PATH = EVALUATION_DIR / "test_cases.json"
RESULTS_DIR = EVALUATION_DIR / "results"
MODELFILE_PATH = PROJECT_ROOT / "Modelfile"

OLLAMA_URL = "http://localhost:11434/api/generate"
REQUEST_TIMEOUT_SECONDS = 600


def sha256_file(path: Path) -> str:
    """Return the SHA-256 hash of a file."""
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)

    return digest.hexdigest()


def post_json(url: str, payload: dict) -> dict:
    """Send a JSON POST request and return the decoded JSON response."""
    body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(
        request, timeout=REQUEST_TIMEOUT_SECONDS
    ) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    if not SPEC_PATH.is_file():
        print(f"ERROR: Evaluation specification not found: {SPEC_PATH}")
        return 1

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    with SPEC_PATH.open("r", encoding="utf-8") as file:
        specification = json.load(file)
    parser = argparse.ArgumentParser(
        description="Run a controlled Dostoevsky AI experiment."
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Exact Ollama model name, e.g. dostoevsky-candidate:latest",
    )
    parser.add_argument(
        "--experiment",
        required=True,
        help="Short experiment label used in the result filename.",
    )
    parser.add_argument(
        "--modelfile",
        required=True,
        help="Path to the Modelfile used to create the candidate model.",
    )
    args = parser.parse_args()

    modelfile_path = Path(args.modelfile)
    if not modelfile_path.is_absolute():
        modelfile_path = PROJECT_ROOT / modelfile_path
    modelfile_path = modelfile_path.resolve()

    if not modelfile_path.is_file():
        print(f"ERROR: Modelfile not found: {modelfile_path}")
        return 1

    experiment_name = args.experiment.strip()

    if (
        not experiment_name
        or any(
            character not in
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
            for character in experiment_name
        )
    ):
        print("ERROR: Experiment name may contain only letters, numbers, _ and -.")
        return 1

    test_cases = specification["test_cases"]
    settings = specification["generation_settings"]
    model_name = args.model
    if not test_cases:
        print("ERROR: No test cases found.")
        return 1

    # Verify that Ollama is reachable before starting the suite.
    try:
        with urllib.request.urlopen(
            "http://localhost:11434/api/tags", timeout=10
        ) as response:
            available_models = json.loads(
                response.read().decode("utf-8")
            ).get("models", [])

    except Exception as exc:
        print(f"ERROR: Could not connect to local Ollama: {exc}")
        print("Check that Ollama is running, then try again.")
        return 1

    matching_models = [
        model
        for model in available_models
        if model.get("name") == model_name
    ]

    if not matching_models:
        print(f"ERROR: Model not found in Ollama: {model_name}")
        print("Available models:")
        for model in available_models:
            print(f"  - {model.get('name', 'unknown')}")
        return 1

    model_digest = matching_models[0].get("digest")

    # Record the configuration used for this run.
    run_started = datetime.now(timezone.utc)
    run_id = run_started.strftime("%Y%m%dT%H%M%SZ")
    output_path = RESULTS_DIR / f"{experiment_name}_{run_id}.json"

    metadata = {
        "run_id": run_id,
        "experiment_name": experiment_name,
        "experiment_type": "controlled_candidate",
        "started_at_utc": run_started.isoformat(),
        "suite_name": specification["suite_name"],
        "suite_version": specification["suite_version"],
        "test_spec_sha256": sha256_file(SPEC_PATH),
        "modelfile_path": os.path.relpath(modelfile_path, PROJECT_ROOT),
        "modelfile_sha256": sha256_file(modelfile_path),
        "model": model_name,
        "model_digest": model_digest,
        "ollama_version_declared_in_spec": specification.get(
            "ollama_version"
        ),
        "python_version": sys.version,
        "platform": platform.platform(),
        "generation_settings": settings,
        "system_prompt_override": None,
        "note": (
            "Controlled experiment using the specified Ollama model. "
            "Ollama uses the stored model configuration. Each test "
            "is an independent generation request."
        ),
    }

    results = []

    print(f"Model: {model_name}")
    print(f"Tests: {len(test_cases)}")
    print(f"Results: {output_path}")
    print("\nStarting evaluation...\n")

    for index, test_case in enumerate(test_cases, start=1):
        test_id = test_case["id"]
        prompt = test_case["prompt"]

        print(f"[{index}/{len(test_cases)}] {test_id}: "
              f"{test_case['name']}")

        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "options": settings,
        }

        started = time.perf_counter()

        try:
            response = post_json(OLLAMA_URL, payload)
            elapsed_seconds = time.perf_counter() - started

            result = {
                "test_id": test_id,
                "feature": test_case["feature"],
                "name": test_case["name"],
                "prompt": prompt,
                "status": "success",
                "output": response.get("response", ""),
                "elapsed_seconds": round(elapsed_seconds, 3),
                "ollama_metrics": {
                    "total_duration_ns": response.get("total_duration"),
                    "load_duration_ns": response.get("load_duration"),
                    "prompt_eval_count": response.get("prompt_eval_count"),
                    "prompt_eval_duration_ns": response.get(
                        "prompt_eval_duration"
                    ),
                    "eval_count": response.get("eval_count"),
                    "eval_duration_ns": response.get("eval_duration"),
                },
                "done_reason": response.get("done_reason"),
                "scores": None,
                "review_notes": None,
            }

            print(f"    Completed in {elapsed_seconds:.1f}s")

        except Exception as exc:
            elapsed_seconds = time.perf_counter() - started

            result = {
                "test_id": test_id,
                "feature": test_case["feature"],
                "name": test_case["name"],
                "prompt": prompt,
                "status": "error",
                "output": None,
                "elapsed_seconds": round(elapsed_seconds, 3),
                "error": f"{type(exc).__name__}: {exc}",
                "scores": None,
                "review_notes": None,
            }

            print(f"    FAILED: {result['error']}")

        results.append(result)

        # Save after every test so completed outputs survive interruptions.
        document = {
            "metadata": metadata,
            "progress": {
                "completed": len(results),
                "total": len(test_cases),
                "successful": sum(
                    item["status"] == "success" for item in results
                ),
                "failed": sum(
                    item["status"] == "error" for item in results
                ),
            },
            "results": results,
        }

        temporary_path = output_path.with_suffix(".tmp")
        temporary_path.write_text(
            json.dumps(document, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary_path.replace(output_path)

    successful = sum(item["status"] == "success" for item in results)
    failed = len(results) - successful

    print("\nEvaluation run finished.")
    print(f"Successful: {successful}/{len(results)}")
    print(f"Failed:     {failed}/{len(results)}")
    print(f"Saved to:   {output_path}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
