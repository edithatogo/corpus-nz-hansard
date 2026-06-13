"""Validate the speech-turn release decision boundary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DECISION_DOC_PATH = ROOT / "docs/speech-turn-release-decision.md"
DECISION_MANIFEST_PATH = ROOT / "manifests/speech_turn_release_decision.json"
GOLD_FIXTURE_PATH = ROOT / "fixtures/gold_evaluation_samples.json"
SEGMENTATION_CONTRACT_PATH = ROOT / "docs/speech-turn-segmentation-contract.md"
SEGMENTATION_REPORT_PATH = ROOT / "docs/speech-turn-segmentation-report.md"
SEGMENTATION_VALIDATION_PATH = ROOT / "manifests/speech_turn_segmentation_validation.json"

REQUIRED_DECISION_FIELDS = (
    "artifact_name",
    "artifact_version",
    "generated_at",
    "decision",
    "status",
    "release_scope",
    "release_gate_status",
    "decision_basis",
    "source_manifests",
    "source_hashes",
    "future_validation_requirements",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for field in REQUIRED_DECISION_FIELDS:
        if field not in manifest:
            failures.append(f"missing required field: {field}")
    if failures:
        return failures

    if manifest["artifact_name"] != "speech_turn_release_decision":
        failures.append("artifact_name must be speech_turn_release_decision.")
    if manifest["decision"] != "explicitly excluded":
        failures.append("decision must be explicitly excluded.")
    if manifest["status"] != "excluded":
        failures.append("status must be excluded.")
    if manifest["release_scope"] != "public final scope":
        failures.append("release_scope must be public final scope.")
    if manifest["release_gate_status"] != "excluded":
        failures.append("release_gate_status must be excluded.")

    for field in ("decision_basis", "source_manifests", "future_validation_requirements"):
        if not isinstance(manifest[field], list) or not manifest[field]:
            failures.append(f"{field} must be a non-empty array.")
        elif not all(isinstance(item, str) and item for item in manifest[field]):
            failures.append(f"{field} must contain non-empty strings only.")

    if not isinstance(manifest["source_hashes"], dict) or not manifest["source_hashes"]:
        failures.append("source_hashes must be a non-empty object.")

    return failures


def _doc_contains(path: Path, required_terms: tuple[str, ...]) -> list[str]:
    text = _read(path)
    return [
        f"{path.relative_to(ROOT).as_posix()} is missing: {term}"
        for term in required_terms
        if term not in text
    ]


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        DECISION_DOC_PATH,
        DECISION_MANIFEST_PATH,
        GOLD_FIXTURE_PATH,
        SEGMENTATION_CONTRACT_PATH,
        SEGMENTATION_REPORT_PATH,
        SEGMENTATION_VALIDATION_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    failures.extend(validate_manifest(load_json(DECISION_MANIFEST_PATH)))

    decision_doc_terms = (
        "explicitly excluded",
        "heuristic MVP",
        "not authoritative",
        "Future Validation Requirements",
    )
    failures.extend(_doc_contains(DECISION_DOC_PATH, decision_doc_terms))

    contract_terms = (
        "Heuristic MVP. Not authoritative.",
        "Release Decision",
        "explicitly excluded",
    )
    failures.extend(_doc_contains(SEGMENTATION_CONTRACT_PATH, contract_terms))

    report_terms = (
        "Heuristic MVP. Not authoritative.",
        "Release Decision",
        "explicitly excluded",
    )
    failures.extend(_doc_contains(SEGMENTATION_REPORT_PATH, report_terms))

    validation = load_json(SEGMENTATION_VALIDATION_PATH)
    summary = validation.get("summary", {})
    if summary.get("authoritative") is not False:
        failures.append("segmentation validation must remain non-authoritative.")
    if summary.get("confidence_counts", {}).get("medium") != 439:
        failures.append("segmentation validation medium confidence count must remain 439.")

    gold_samples = [
        sample
        for sample in load_json(GOLD_FIXTURE_PATH)["samples"]
        if sample.get("domain") == "speech_turn"
    ]
    expected_classes = {
        "gold-speech-turn-01": "positive",
        "gold-speech-turn-02": "negative",
        "gold-speech-turn-03": "ambiguous",
        "gold-speech-turn-04": "unresolved",
        "gold-speech-turn-05": "excluded",
    }
    if len(gold_samples) != len(expected_classes):
        failures.append("gold speech-turn fixture must contain five reviewed samples.")
    for sample in gold_samples:
        sample_id = sample.get("sample_id")
        if sample_id not in expected_classes:
            failures.append(f"unexpected speech-turn sample id: {sample_id}")
            continue
        if sample.get("example_class") != expected_classes[sample_id]:
            failures.append(f"{sample_id} must remain {expected_classes[sample_id]}.")

    expected_fragments = {
        "gold-speech-turn-01": "positive segmentation case",
        "gold-speech-turn-02": "heading-like text",
        "gold-speech-turn-03": "identity remains ambiguous",
        "gold-speech-turn-04": "no turn boundary",
        "gold-speech-turn-05": "Exclude vote-procedure text",
    }
    for sample in gold_samples:
        sample_id = sample.get("sample_id")
        fragment = expected_fragments.get(sample_id)
        if fragment and fragment not in sample.get("label", {}).get("expected_behavior", ""):
            failures.append(f"{sample_id} must preserve the reviewed expected behavior text.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"SPEECH-TURN-DECISION: {failure}")
        return 1
    print("Speech-turn release decision is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
