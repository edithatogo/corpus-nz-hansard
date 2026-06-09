"""Validate the Popolo/Open Civic Data sample endpoint package."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/popolo_opencivicdata_validation_manifest.json"
FIXTURE_PATH = ROOT / "fixtures/neutral_components.json"
MAPPING_DOC_PATH = ROOT / "docs/popolo-opencivicdata-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DEPENDENCY_MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
TRACK_PATH = ROOT / "conductor/tracks/popolo_opencivicdata_endpoint_20260609/evidence.md"
SAMPLE_DIR = ROOT / "samples/popolo-opencivicdata"

JSON_OUTPUTS = {
    "people": SAMPLE_DIR / "people.json",
    "organizations": SAMPLE_DIR / "organizations.json",
    "memberships": SAMPLE_DIR / "memberships.json",
    "motions": SAMPLE_DIR / "motions.json",
    "vote_events": SAMPLE_DIR / "vote-events.json",
}
JSONL_OUTPUTS = {
    "votes": SAMPLE_DIR / "votes.jsonl",
    "speeches": SAMPLE_DIR / "speeches.jsonl",
}
REQUIRED_DEPENDENCY_GROUPS = {"data", "schema", "authority"}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> Any:
    return json.loads(_read(path))


def _jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(_read(path).splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"{path.relative_to(ROOT).as_posix()} line {line_number}: {exc}"
            ) from exc
    return rows


def _component_ids(fixtures: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for rows in fixtures["components"].values():
        ids.update(row["component_id"] for row in rows)
    return ids


def _valid_date_range(start_date: str | None, end_date: str | None) -> bool:
    if start_date is None:
        return False
    start = date.fromisoformat(start_date)
    if end_date is None:
        return True
    return start <= date.fromisoformat(end_date)


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        FIXTURE_PATH,
        MAPPING_DOC_PATH,
        ENDPOINT_DOC_PATH,
        DEPENDENCY_MANIFEST_PATH,
        RELEASE_LADDER_PATH,
        TRACK_PATH,
        SAMPLE_DIR / "README.md",
        *JSON_OUTPUTS.values(),
        *JSONL_OUTPUTS.values(),
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    fixtures = _json(FIXTURE_PATH)
    fixture_ids = _component_ids(fixtures)
    output_rows = {key: _json(path) for key, path in JSON_OUTPUTS.items()}
    try:
        jsonl_rows = {key: _jsonl(path) for key, path in JSONL_OUTPUTS.items()}
    except ValueError as exc:
        return [str(exc)]

    people_ids = {row["id"] for row in output_rows["people"]}
    organization_ids = {row["id"] for row in output_rows["organizations"]}
    motion_ids = {row["id"] for row in output_rows["motions"]}
    vote_event_ids = {row["id"] for row in output_rows["vote_events"]}
    proceeding_ids = {
        row["proceeding_item_id"] for row in fixtures["components"]["proceeding_items"]
    }

    for membership in output_rows["memberships"]:
        if membership["person_id"] not in people_ids:
            failures.append("membership person_id must reference people.json.")
        if membership["organization_id"] not in organization_ids:
            failures.append("membership organization_id must reference organizations.json.")
        if not _valid_date_range(membership["start_date"], membership["end_date"]):
            failures.append("membership date range must be valid.")
        if "provenance" not in membership:
            failures.append("membership must preserve provenance.")

    for vote_event in output_rows["vote_events"]:
        if vote_event["motion_id"] not in motion_ids:
            failures.append("vote event must reference motions.json.")
        if vote_event["classification"] != "party_vote":
            failures.append("sample vote event must distinguish party_vote classification.")
        if "provenance" not in vote_event:
            failures.append("vote event must preserve provenance.")

    for vote in jsonl_rows["votes"]:
        if vote["vote_event_id"] not in vote_event_ids:
            failures.append("vote row must reference vote-events.json.")
        if vote["motion_id"] not in motion_ids:
            failures.append("vote row must reference motions.json.")
        if vote["voter_type"] == "organization" and vote["voter_id"] not in organization_ids:
            failures.append("organization vote row must reference organizations.json.")
        if vote["voter_type"] == "person" and vote["voter_id"] not in people_ids:
            failures.append("person vote row must reference people.json.")
        if vote["voter_type"] not in {"organization", "person"}:
            failures.append("vote row must distinguish organization/person voter_type.")
        if "provenance" not in vote:
            failures.append("vote row must preserve provenance.")

    for speech in jsonl_rows["speeches"]:
        if speech["speaker_id"] not in people_ids:
            failures.append("speech row speaker_id must reference people.json.")
        if speech["proceeding_item_id"] not in proceeding_ids:
            failures.append("speech row proceeding_item_id must reference neutral proceeding item.")
        if "provenance" not in speech:
            failures.append("speech row must preserve provenance.")

    if manifest["release_status"] != "sample-not-release":
        failures.append("Popolo/Open Civic Data manifest must remain sample-not-release.")
    if manifest["release_level"] != "upstream-contribution":
        failures.append(
            "Popolo/Open Civic Data sample package must be upstream-contribution level."
        )
    if set(manifest["dependency_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("Popolo/Open Civic Data dependency groups must match policy.")
    if manifest["validation_results"]["component_metadata_validated"]:
        failures.append(
            "Popolo/Open Civic Data sample must not claim validated component metadata yet."
        )
    if manifest["validation_results"]["readiness_status"] != "blocked-pending-validated-components":
        failures.append("Popolo/Open Civic Data readiness boundary must remain blocked.")
    if manifest["validation_results"]["blocking_errors"] != 0:
        failures.append(
            "Popolo/Open Civic Data sample integrity check must have zero blocking errors."
        )

    traced_ids = set(manifest["traceability"][0]["neutral_component_ids"])
    if not traced_ids.issubset(fixture_ids):
        failures.append("Popolo/Open Civic Data traceability cites unknown neutral component IDs.")

    dependency_manifest = _json(DEPENDENCY_MANIFEST_PATH)
    popolo_entry = next(
        item
        for item in dependency_manifest["endpoint_requirements"]
        if item["endpoint_track"] == "popolo_opencivicdata_endpoint_20260609"
    )
    if set(popolo_entry["required_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("Dependency extras policy and Popolo/Open Civic Data manifest disagree.")

    release_ladder = _json(RELEASE_LADDER_PATH)
    artifacts = {item["artifact"]: item for item in release_ladder["artifact_map"]}
    if "Popolo / Open Civic Data sample package" not in artifacts:
        failures.append("Release ladder missing Popolo / Open Civic Data sample package mapping.")

    required_terms = (
        "Popolo / Open Civic Data",
        "sample-not-release",
        "manifests/popolo_opencivicdata_validation_manifest.json",
        "samples/popolo-opencivicdata/vote-events.json",
        "fixtures/neutral_components.json",
        "party_vote",
        "organization",
        "person",
        "blocked-pending-validated-components",
        "member identity",
        "party attribution",
        "vote/motion extraction",
        "speech-turn validation",
    )
    for relative_path, text in {
        "docs/popolo-opencivicdata-mapping.md": _read(MAPPING_DOC_PATH),
        "docs/endpoint-contracts.md": _read(ENDPOINT_DOC_PATH),
        "samples/popolo-opencivicdata/README.md": _read(SAMPLE_DIR / "README.md"),
    }.items():
        for term in required_terms:
            if term not in text:
                failures.append(f"{relative_path} is missing Popolo/Open Civic Data term: {term}")

    track_text = _read(TRACK_PATH)
    for required in (
        "Civic-Data Mapping",
        "Sample Package",
        "Referential Integrity",
        "Readiness Boundary",
    ):
        if required not in track_text:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"POPOLO-OCD: {failure}")
        return 1
    print("Popolo/Open Civic Data sample endpoint is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
