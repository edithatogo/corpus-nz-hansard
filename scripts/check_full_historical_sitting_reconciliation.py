"""Validate the full historical sitting reconciliation release evidence."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RELEASE_STATUS = "release-ready-reconciliation-contract-agent-review"
MANIFEST = ROOT / "manifests" / "full_historical_sitting_reconciliation.json"
SCHEMA = ROOT / "schemas" / "full_historical_sitting_reconciliation.schema.json"
SAMPLE_JSON = (
    ROOT / "samples" / "full-historical-sitting-reconciliation" / "sitting-reconciliation.json"
)
SAMPLE_CSV = (
    ROOT / "samples" / "full-historical-sitting-reconciliation" / "sitting-reconciliation.csv"
)
README = ROOT / "samples" / "full-historical-sitting-reconciliation" / "README.md"
DOCS = ROOT / "docs" / "full-historical-sitting-reconciliation.md"
TRACK = ROOT / "conductor" / "tracks" / "full_historical_sitting_reconciliation_20260610"
TRACKS_MD = ROOT / "conductor" / "tracks.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    manifest = load_json(MANIFEST)
    sample = load_json(SAMPLE_JSON)
    schema = load_json(SCHEMA)
    jsonschema.validate(sample, schema)

    require(manifest["release_status"] == RELEASE_STATUS, "manifest release status is stale")
    require(sample["release_status"] == RELEASE_STATUS, "sample release status is stale")
    require(len(sample["sittings"]) >= 5, "sample must cover multiple historical periods")
    require(SAMPLE_CSV.exists(), "CSV reconciliation artifact is missing")

    claims = sample["public_claims"]
    require(
        claims["reconciliation_contract_release_ready"] is True,
        "contract readiness must be explicit",
    )
    require(
        claims["sample_reconciliation_release_ready"] is True, "sample readiness must be explicit"
    )
    require(claims["full_historical_coverage"] is False, "must not claim full historical coverage")
    require(claims["all_dates_reconciled"] is False, "must not claim all dates reconciled")
    require(
        claims["authoritative_complete_sitting_calendar"] is False,
        "must not claim an authoritative complete sitting calendar",
    )

    contract = sample["coverage_contract"]
    require(contract["grain"] == "date-level sitting identity", "wrong reconciliation grain")
    require(contract["requires_agent_review_fallback"] is True, "agent-review fallback is required")
    require(
        contract["requires_human_review"] is False, "human-review dependency must not block release"
    )

    combined = "\n".join(
        [
            README.read_text(encoding="utf-8"),
            DOCS.read_text(encoding="utf-8"),
            (TRACK / "plan.md").read_text(encoding="utf-8"),
            (TRACK / "evidence.md").read_text(encoding="utf-8"),
            (TRACK / "index.md").read_text(encoding="utf-8"),
        ]
    )
    for phrase in (
        RELEASE_STATUS,
        "agent-review fallback",
        "does not claim full historical coverage",
        "complete historical sitting calendar",
    ):
        require(phrase in combined, f"missing required phrase: {phrase}")

    metadata = load_json(TRACK / "metadata.json")
    require(metadata.get("status") == "complete", "track metadata must be complete")
    tracks_md = TRACKS_MD.read_text(encoding="utf-8")
    require(
        "### [x] Track: Full Historical Sitting Reconciliation" in tracks_md,
        "conductor/tracks.md checkbox is not complete",
    )


if __name__ == "__main__":
    main()
