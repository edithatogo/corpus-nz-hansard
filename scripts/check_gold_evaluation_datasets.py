"""Validate reviewed gold/evaluation fixtures and release gates."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/gold_evaluation_datasets.json"
MANIFEST_SCHEMA_PATH = ROOT / "schemas/gold_evaluation_datasets.schema.json"
FIXTURE_PATH = ROOT / "fixtures/gold_evaluation_samples.json"
SAMPLE_SCHEMA_PATH = ROOT / "schemas/gold_evaluation_sample.schema.json"
DOC_PATH = ROOT / "docs/gold-evaluation-datasets.md"
COMPONENT_DOC_PATH = ROOT / "docs/component-contracts.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
TRACK_PATH = ROOT / "conductor/tracks/gold_evaluation_datasets_20260609/evidence.md"

REQUIRED_DOMAINS = {
    "member_resolution",
    "party_attribution",
    "speech_turn",
    "vote",
    "topic_coding",
}
REQUIRED_CLASSES = {"positive", "negative", "ambiguous", "unresolved", "excluded"}
REQUIRED_METRICS = {
    "precision",
    "recall",
    "ambiguity_rate",
    "unresolved_rate",
    "exclusion_regression",
}
EXPECTED_LABEL_STATUS = {
    "positive": "gold_positive",
    "negative": "gold_negative",
    "ambiguous": "gold_ambiguous",
    "unresolved": "gold_unresolved",
    "excluded": "gold_excluded",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _validate_schema(path: Path, schema_path: Path) -> list[str]:
    failures: list[str] = []
    instance = _json(path)
    schema = _json(schema_path)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{path.relative_to(ROOT).as_posix()} {location}: {error.message}")
    return failures


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        MANIFEST_SCHEMA_PATH,
        FIXTURE_PATH,
        SAMPLE_SCHEMA_PATH,
        DOC_PATH,
        COMPONENT_DOC_PATH,
        ENDPOINT_DOC_PATH,
        RELEASE_LADDER_PATH,
        TRACK_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    failures.extend(_validate_schema(MANIFEST_PATH, MANIFEST_SCHEMA_PATH))
    failures.extend(_validate_schema(FIXTURE_PATH, SAMPLE_SCHEMA_PATH))

    manifest = _json(MANIFEST_PATH)
    fixtures = _json(FIXTURE_PATH)

    manifest_domains = {domain["domain"]: domain for domain in manifest["domains"]}
    if set(manifest_domains) != REQUIRED_DOMAINS:
        failures.append("gold evaluation manifest must cover exactly the required domains.")
    for domain, config in manifest_domains.items():
        if set(config["required_example_classes"]) != REQUIRED_CLASSES:
            failures.append(f"{domain} must require every example class.")
        if set(config["metrics_supported"]) != REQUIRED_METRICS:
            failures.append(f"{domain} must support every required metric.")

    samples = fixtures["samples"]
    sample_ids = [sample["sample_id"] for sample in samples]
    duplicate_ids = [sample_id for sample_id, count in Counter(sample_ids).items() if count > 1]
    if duplicate_ids:
        failures.append("duplicate gold sample IDs: " + ", ".join(sorted(duplicate_ids)))

    classes_by_domain: dict[str, set[str]] = defaultdict(set)
    for sample in samples:
        domain = sample["domain"]
        example_class = sample["example_class"]
        classes_by_domain[domain].add(example_class)
        expected_status = EXPECTED_LABEL_STATUS[example_class]
        if sample["label"]["status"] != expected_status:
            failures.append(f"{sample['sample_id']} label status must be {expected_status}.")
        review = sample["review"]
        if review["review_status"] != "reviewed":
            failures.append(f"{sample['sample_id']} must be reviewed.")
        if review["model_generated_label"]:
            failures.append(f"{sample['sample_id']} must not use a model-generated gold label.")
        if not sample["label"]["label_provenance"]:
            failures.append(f"{sample['sample_id']} must record label provenance.")
        if sample["source_reference"]["release_version"] != "0.1.0":
            failures.append(f"{sample['sample_id']} must reference release version 0.1.0.")

    for domain in REQUIRED_DOMAINS:
        missing_classes = REQUIRED_CLASSES - classes_by_domain[domain]
        if missing_classes:
            failures.append(f"{domain} is missing classes: " + ", ".join(sorted(missing_classes)))

    release_ladder = _json(RELEASE_LADDER_PATH)
    artifact_map = {item["artifact"]: item for item in release_ladder["artifact_map"]}
    if "gold evaluation datasets" not in artifact_map:
        failures.append("release ladder must map gold evaluation datasets.")
    elif artifact_map["gold evaluation datasets"]["release_level"] != "neutral-component":
        failures.append("gold evaluation datasets must map to neutral-component.")

    required_doc_terms = (
        "manifests/gold_evaluation_datasets.json",
        "fixtures/gold_evaluation_samples.json",
        "member_resolution",
        "party_attribution",
        "speech_turn",
        "vote",
        "topic_coding",
        "positive",
        "negative",
        "ambiguous",
        "unresolved",
        "excluded",
        "model-generated labels",
    )
    for relative_path, text in {
        "docs/gold-evaluation-datasets.md": _read(DOC_PATH),
        "docs/component-contracts.md": _read(COMPONENT_DOC_PATH),
        "docs/endpoint-contracts.md": _read(ENDPOINT_DOC_PATH),
    }.items():
        for term in required_doc_terms:
            if term not in text:
                failures.append(f"{relative_path} is missing gold evaluation term: {term}")

    track = _read(TRACK_PATH)
    for required in (
        "Evaluation Schema",
        "Reviewed Fixtures",
        "Regression Metrics",
        "Focused Validation",
    ):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"GOLD-EVALUATION: {failure}")
        return 1
    print("Gold evaluation datasets are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
