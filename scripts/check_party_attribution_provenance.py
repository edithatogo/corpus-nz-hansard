"""Validate the party attribution with provenance review package."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_MANIFEST_PATH = ROOT / "manifests/party_attribution_provenance_package.json"
VALIDATION_MANIFEST_PATH = ROOT / "manifests/party_attribution_validation.json"
AUTHORITATIVE_SOURCE_PATH = ROOT / "derived/party_attribution_authority.json"
REVIEW_CSV_PATH = ROOT / "samples/party-attribution/party_attribution_review.csv"
README_PATH = ROOT / "samples/party-attribution/README.md"
DOC_PATH = ROOT / "docs/party-attribution-provenance.md"
GOLD_PATH = ROOT / "fixtures/gold_evaluation_samples.json"

REQUIRED_EXAMPLE_CLASSES = {"positive", "negative", "ambiguous", "unresolved", "excluded"}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        PACKAGE_MANIFEST_PATH,
        VALIDATION_MANIFEST_PATH,
        AUTHORITATIVE_SOURCE_PATH,
        REVIEW_CSV_PATH,
        README_PATH,
        DOC_PATH,
        GOLD_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    package_manifest = _json(PACKAGE_MANIFEST_PATH)
    validation_manifest = _json(VALIDATION_MANIFEST_PATH)
    authority = _json(AUTHORITATIVE_SOURCE_PATH)
    review_rows = _csv_rows(REVIEW_CSV_PATH)
    gold_samples = [
        sample for sample in _json(GOLD_PATH)["samples"] if sample["domain"] == "party_attribution"
    ]

    if package_manifest["release_status"] != "sample-not-release":
        failures.append("Party attribution package must remain sample-not-release.")
    if package_manifest["submission_status"] != "not-submitted":
        failures.append("Party attribution package must not claim external submission.")
    if package_manifest["readiness_status"] != "blocked-pending-validated-components":
        failures.append("Party attribution package must remain blocked on validated components.")
    if validation_manifest["ok"] is not False:
        failures.append("Party attribution validation manifest must remain blocked.")
    if validation_manifest["release_gate_status"] != "blocked-pending-validated-components":
        failures.append(
            "Party attribution validation manifest must remain blocked-pending-validated-components."
        )
    if validation_manifest["counts"]["sample_total"] != 5:
        failures.append("Party attribution validation manifest must record five gold samples.")
    if validation_manifest["counts"]["derived_rows"] != 0:
        failures.append("Party attribution validation manifest must not claim derived rows yet.")

    if len(authority["authority_sources"]) != 4:
        failures.append("Party attribution authority table must list four source references.")
    if "validated member identity" not in authority["temporal_rules"][2].lower():
        failures.append(
            "Party attribution authority table must state the member-identity dependency."
        )

    if len(review_rows) != 5:
        failures.append("Party attribution review table must contain five reviewed rows.")
    review_classes = {row["example_class"] for row in review_rows}
    if review_classes != REQUIRED_EXAMPLE_CLASSES:
        failures.append("Party attribution review table must cover all gold example classes.")

    gold_ids = {sample["sample_id"] for sample in gold_samples}
    if {row["sample_id"] for row in review_rows} != gold_ids:
        failures.append(
            "Party attribution review table must align with the gold evaluation samples."
        )

    if any(row["release_status"] != "sample-not-release" for row in review_rows):
        failures.append("Party attribution review rows must remain sample-not-release.")
    if any(row["review_status"] != "reviewed" for row in review_rows):
        failures.append("Party attribution review rows must be reviewed.")

    required_terms = {
        "samples/party-attribution/README.md": (
            "Party Attribution With Provenance Sample Package",
            "sample-not-release",
            "blocked pending validated member identity",
        ),
        "docs/party-attribution-provenance.md": (
            "Party attribution is derived data",
            "validated member identity",
            "No derived party attribution output is promoted",
        ),
    }
    for relative_path, terms in required_terms.items():
        text = _read(ROOT / relative_path)
        for term in terms:
            if term not in text:
                failures.append(f"{relative_path} is missing term: {term}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARTY-ATTRIBUTION: {failure}")
        return 1
    print("Party attribution with provenance package is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
