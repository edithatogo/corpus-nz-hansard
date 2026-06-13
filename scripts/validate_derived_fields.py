"""Shared helpers for derived-field validation manifests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SCHEMA_PATH = ROOT / "schemas/derived_fields_validation.schema.json"

COMMON_REQUIRED_FIELDS = (
    "artifact_name",
    "artifact_version",
    "generated_at",
    "ok",
    "validation_status",
    "release_gate_status",
    "counts",
    "errors",
    "warnings",
    "source_hashes",
    "source_manifests",
)

VALIDATION_STATUSES = {"blocked", "ok", "excluded"}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for field in COMMON_REQUIRED_FIELDS:
        if field not in manifest:
            failures.append(f"missing required field: {field}")
    if failures:
        return failures

    if not isinstance(manifest["ok"], bool):
        failures.append("ok must be a boolean.")
    if manifest["validation_status"] not in VALIDATION_STATUSES:
        failures.append("validation_status must be blocked, ok, or excluded.")
    if not isinstance(manifest["counts"], dict) or not manifest["counts"]:
        failures.append("counts must be a non-empty object.")
    else:
        for key, value in manifest["counts"].items():
            if not isinstance(key, str):
                failures.append("counts keys must be strings.")
            if not isinstance(value, int):
                failures.append(f"count {key} must be an integer.")
    for field in ("errors", "warnings", "source_manifests"):
        if not isinstance(manifest[field], list):
            failures.append(f"{field} must be an array.")
        elif not all(isinstance(item, str) for item in manifest[field]):
            failures.append(f"{field} must contain strings only.")
    if not isinstance(manifest["source_hashes"], dict) or not manifest["source_hashes"]:
        failures.append("source_hashes must be a non-empty object.")
    else:
        for key, value in manifest["source_hashes"].items():
            if not isinstance(key, str) or not isinstance(value, str) or not value:
                failures.append("source_hashes must map string keys to non-empty strings.")
    return failures


def gold_sample_counts(domain: str) -> dict[str, int]:
    samples = load_json(ROOT / "fixtures/gold_evaluation_samples.json")["samples"]
    filtered = [sample for sample in samples if sample["domain"] == domain]
    counts: dict[str, int] = {"sample_total": len(filtered)}
    for sample in filtered:
        counts[sample["example_class"]] = counts.get(sample["example_class"], 0) + 1
    return counts


def segmentation_counts() -> dict[str, int]:
    validation = load_json(ROOT / "manifests/speech_turn_segmentation_validation.json")
    summary = validation["summary"]
    return {
        "documents_read": summary["documents_read"],
        "documents_with_turns": summary["documents_with_turns"],
        "documents_without_turns": summary["documents_without_turns"],
        "turns_written": summary["turns_written"],
        "medium_confidence": summary["confidence_counts"].get("medium", 0),
    }


def main() -> int:
    manifests = [
        ROOT / "manifests/member_identity_resolution_validation.json",
        ROOT / "manifests/corpus_wide_member_identity_validation.json",
        ROOT / "manifests/corpus_wide_party_attribution_validation.json",
        ROOT / "manifests/party_attribution_validation.json",
        ROOT / "manifests/sitting_proceeding_component_validation.json",
        ROOT / "manifests/vote_motion_bill_question_extraction_validation.json",
        ROOT / "manifests/validated_speech_turn_component_validation.json",
        ROOT / "manifests/speech_turn_validated_artifact_validation.json",
    ]
    failures: list[str] = []
    for path in manifests:
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
            continue
        failures.extend(
            f"{path.relative_to(ROOT).as_posix()}: {failure}"
            for failure in validate_manifest(load_json(path))
        )
    if (
        MANIFEST_SCHEMA_PATH.exists()
        and "derived fields validation manifest schema" not in _read(MANIFEST_SCHEMA_PATH).lower()
    ):
        failures.append("schema file is missing the expected title.")

    if failures:
        for failure in failures:
            print(f"DERIVED-FIELDS: {failure}")
        return 1
    print("Derived fields validation manifests are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
