"""Validate the CAP / ParlaCAP topic sample package and readiness boundary."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CODEBOOK_PATH = ROOT / "manifests/cap_parlacap_topic_codebook.json"
MANIFEST_PATH = ROOT / "manifests/cap_parlacap_topic_validation_manifest.json"
FIXTURE_PATH = ROOT / "fixtures/neutral_components.json"
GOLD_PATH = ROOT / "fixtures/gold_evaluation_samples.json"
SAMPLE_PATH = ROOT / "samples/cap-parlacap/cap_parlacap_topics.csv"
README_PATH = ROOT / "samples/cap-parlacap/README.md"
MAPPING_DOC_PATH = ROOT / "docs/cap-parlacap-topic-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
DEPENDENCY_POLICY_PATH = ROOT / "manifests/dependency_extras_policy.json"
TRACK_PATH = ROOT / "conductor/tracks/cap_parlacap_topic_endpoint_20260609/evidence.md"

REQUIRED_DEPENDENCY_GROUPS = {"data", "ml", "nlp", "schema"}
REQUIRED_SAMPLE_COLUMNS = {
    "sample_id",
    "source_component_type",
    "source_component_id",
    "source_stable_id",
    "source_reference",
    "topic_scheme",
    "topic_code",
    "topic_label",
    "coding_method",
    "coder_or_model",
    "label_status",
    "validation_status",
    "review_status",
    "release_status",
    "source_text_excerpt",
    "notes",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _component_ids(fixtures: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for rows in fixtures["components"].values():
        ids.update(row["component_id"] for row in rows)
    return ids


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        CODEBOOK_PATH,
        MANIFEST_PATH,
        FIXTURE_PATH,
        GOLD_PATH,
        SAMPLE_PATH,
        README_PATH,
        MAPPING_DOC_PATH,
        ENDPOINT_DOC_PATH,
        RELEASE_LADDER_PATH,
        DEPENDENCY_POLICY_PATH,
        TRACK_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    codebook = _json(CODEBOOK_PATH)
    manifest = _json(MANIFEST_PATH)
    fixtures = _json(FIXTURE_PATH)
    rows = _csv_rows(SAMPLE_PATH)
    component_ids = _component_ids(fixtures)

    if manifest["codebook_version"] != codebook["codebook_version"]:
        failures.append("CAP manifest and codebook disagree on the declared version.")
    if manifest["codebook_metadata"] != "manifests/cap_parlacap_topic_codebook.json":
        failures.append("CAP manifest must reference the local codebook metadata file.")

    declared_codes = {row["topic_code"]: row for row in codebook["declared_codes"]}
    if manifest["release_status"] != "sample-not-release":
        failures.append("CAP manifest must remain sample-not-release.")
    if manifest["release_level"] != "upstream-contribution":
        failures.append("CAP sample package must be upstream-contribution level.")
    if set(manifest["dependency_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("CAP dependency groups must match dependency extras policy.")
    if manifest["validation_results"]["readiness_status"] != "blocked-pending-validated-components":
        failures.append("CAP readiness boundary must remain blocked on validated components.")
    if manifest["validation_results"]["blocking_errors"] != 0:
        failures.append("CAP sample integrity check must have zero blocking errors.")
    if not manifest["validation_results"]["human_rule_model_separated"]:
        failures.append("CAP manifest must keep human, rule, and model labels separated.")
    if not manifest["validation_results"]["codebook_codes_validate"]:
        failures.append("CAP sample codes must validate against the declared codebook.")

    if len(rows) != 3:
        failures.append("CAP sample CSV must contain exactly three representative rows.")
    if rows and set(rows[0]) != REQUIRED_SAMPLE_COLUMNS:
        failures.append("CAP sample CSV columns are incomplete or reordered unexpectedly.")

    row_methods = {row["coding_method"] for row in rows}
    if row_methods != {"human-coded", "rule-coded", "model-coded"}:
        failures.append("CAP sample must include human-coded, rule-coded, and model-coded rows.")

    for row in rows:
        if row["source_component_id"] not in component_ids:
            failures.append(
                f"CAP row {row['sample_id']} references an unknown neutral component ID."
            )
        if row["topic_code"] not in declared_codes:
            failures.append(f"CAP row {row['sample_id']} references an undeclared topic code.")
        if (
            row["coding_method"] == "model-coded"
            and row["validation_status"] != "exploratory-model"
        ):
            failures.append("CAP model-coded rows must remain exploratory-only.")
        if row["release_status"] != "sample-not-release":
            failures.append(f"CAP row {row['sample_id']} must remain sample-not-release.")

    dependency_policy = _json(DEPENDENCY_POLICY_PATH)
    cap_entry = next(
        item
        for item in dependency_policy["endpoint_requirements"]
        if item["endpoint_track"] == "cap_parlacap_topic_endpoint_20260609"
    )
    if set(cap_entry["required_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("Dependency extras policy and CAP manifest disagree.")

    release_ladder = _json(RELEASE_LADDER_PATH)
    artifacts = {item["artifact"]: item for item in release_ladder["artifact_map"]}
    if "CAP / ParlaCAP sample package" not in artifacts:
        failures.append("Release ladder missing CAP / ParlaCAP sample package mapping.")

    if "topic_coding" not in _read(GOLD_PATH):
        failures.append("Gold evaluation samples must include topic coding evidence.")

    required_terms_by_file = {
        "docs/cap-parlacap-topic-mapping.md": (
            "repository-declared review map",
            "human-coded",
            "rule-coded",
            "model-coded",
            "blocked-pending-validated-components",
        ),
        "docs/endpoint-contracts.md": (
            "CAP / ParlaCAP Topic Endpoint",
            "sample-not-release",
            "manifests/cap_parlacap_topic_validation_manifest.json",
            "manifests/cap_parlacap_topic_codebook.json",
        ),
        "samples/cap-parlacap/README.md": (
            "CAP / ParlaCAP Topic Sample Package",
            "sample-not-release",
            "fixtures/neutral_components.json",
            "fixtures/gold_evaluation_samples.json",
            "human-coded",
            "rule-coded",
            "model-coded",
            "blocked-pending-validated-components",
        ),
        "conductor/tracks/cap_parlacap_topic_endpoint_20260609/evidence.md": (
            "CAP / ParlaCAP Topic Sample Package",
            "sample-not-release",
            "manifests/cap_parlacap_topic_validation_manifest.json",
            "manifests/cap_parlacap_topic_codebook.json",
            "samples/cap-parlacap/cap_parlacap_topics.csv",
            "fixtures/neutral_components.json",
            "fixtures/gold_evaluation_samples.json",
            "human-coded",
            "rule-coded",
            "model-coded",
            "blocked-pending-validated-components",
        ),
    }
    for relative_path, required_terms in required_terms_by_file.items():
        text = _read(ROOT / relative_path)
        for term in required_terms:
            if term not in text:
                failures.append(f"{relative_path} is missing CAP term: {term}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"CAP-PARLACAP: {failure}")
        return 1
    print("CAP / ParlaCAP sample package is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
