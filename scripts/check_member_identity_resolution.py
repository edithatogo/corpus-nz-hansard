"""Validate the member identity resolution review package."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.build_member_identity_review import _member_id
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.build_member_identity_review import _member_id

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_MANIFEST_PATH = ROOT / "manifests/member_identity_resolution_package.json"
VALIDATION_MANIFEST_PATH = ROOT / "manifests/member_identity_resolution_validation.json"
AUTHORITY_PATH = ROOT / "derived/member_identity_authority.json"
REVIEW_CSV_PATH = ROOT / "samples/member-identity/member_identity_review.csv"
README_PATH = ROOT / "samples/member-identity/README.md"
DOC_PATH = ROOT / "docs/member-identity-resolution.md"
GOLD_PATH = ROOT / "fixtures/gold_evaluation_samples.json"
AUTHORITY_SOURCES_PATH = ROOT / "manifests/authority_sources.json"


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
        AUTHORITY_PATH,
        REVIEW_CSV_PATH,
        README_PATH,
        DOC_PATH,
        GOLD_PATH,
        AUTHORITY_SOURCES_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    package_manifest = _json(PACKAGE_MANIFEST_PATH)
    validation_manifest = _json(VALIDATION_MANIFEST_PATH)
    authority = _json(AUTHORITY_PATH)
    review_rows = _csv_rows(REVIEW_CSV_PATH)
    if package_manifest["release_status"] != "sample-not-release":
        failures.append("Member identity package must remain sample-not-release.")
    if package_manifest["submission_status"] != "not-submitted":
        failures.append("Member identity package must not claim external submission.")
    if package_manifest["readiness_status"] != "blocked-pending-validated-components":
        failures.append("Member identity package must remain blocked on validated components.")
    if validation_manifest["ok"] is not False:
        failures.append("Member identity validation manifest must remain blocked.")
    if validation_manifest["release_gate_status"] != "blocked-pending-validation":
        failures.append(
            "Member identity validation manifest must remain blocked-pending-validation."
        )
    if validation_manifest["counts"]["sample_total"] != 5:
        failures.append("Member identity validation manifest must record five gold samples.")
    if validation_manifest["counts"]["derived_rows"] != 0:
        failures.append("Member identity validation manifest must not claim derived rows yet.")

    if len(authority["authority_sources"]) != 2:
        failures.append("Member identity authority table must list two source references.")
    if len(authority["member_records"]) != 2:
        failures.append("Member identity authority table must list two reviewed member records.")

    expected_member_ids = {
        "Clayton Cosgrove": _member_id("nz-parliament-former-members", "clayton-cosgrove"),
        "Roger Morrison Sowry": _member_id("nz-parliament-roll-of-members", "roger-morrison-sowry"),
    }
    if {record["display_name"] for record in authority["member_records"]} != set(
        expected_member_ids
    ):
        failures.append(
            "Member identity authority table must cover Clayton Cosgrove and Roger Morrison Sowry."
        )
    for record in authority["member_records"]:
        if record["member_id"] != expected_member_ids[record["display_name"]]:
            failures.append(f"{record['display_name']} must use the canonical member ID helper.")

    if len(review_rows) != 5:
        failures.append("Member identity review table must contain five reviewed rows.")
    review_classes = [row["example_class"] for row in review_rows]
    if review_classes != ["positive", "negative", "ambiguous", "unresolved", "excluded"]:
        failures.append(
            "Member identity review table must preserve the reviewed gold sample order and classes."
        )
    if any(row["review_status"] != "reviewed" for row in review_rows):
        failures.append("Member identity review rows must be reviewed.")
    if any(row["release_status"] != "sample-not-release" for row in review_rows):
        failures.append("Member identity review rows must remain sample-not-release.")

    positive = review_rows[0]
    if (
        positive["member_display_name"] != "Clayton Cosgrove"
        or positive["member_resolution_status"] != "authoritative"
    ):
        failures.append("Positive member-resolution row must remain authoritative.")
    ambiguous = review_rows[2]
    if (
        ambiguous["member_display_name"] != "Roger Morrison Sowry"
        or ambiguous["member_resolution_status"] != "ambiguous-match"
    ):
        failures.append(
            "Ambiguous member-resolution row must preserve the honorific-normalized match."
        )
    if review_rows[1]["member_resolution_status"] != "unresolved":
        failures.append("Office-title case must remain unresolved.")
    if review_rows[4]["member_resolution_status"] != "excluded":
        failures.append("Generic heading case must remain excluded.")

    required_terms = {
        "samples/member-identity/README.md": (
            "Member Identity Resolution Sample Package",
            "sample-not-release",
            "local-review-only",
        ),
        "docs/member-identity-resolution.md": (
            "Member Identity Resolution",
            "Former Members",
            "Roll of members",
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
            print(f"MEMBER-IDENTITY: {failure}")
        return 1
    print("Member identity resolution review package is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
