"""Validate sample-scoped W3C Time temporal model artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/w3c_time_temporal_model.json"
SCHEMA_PATH = ROOT / "schemas/w3c_time_temporal_model.schema.json"
TTL_PATH = ROOT / "samples/w3c-time-temporal-model/temporal-model.ttl"
JSON_PATH = ROOT / "samples/w3c-time-temporal-model/temporal-model.json"
README_PATH = ROOT / "samples/w3c-time-temporal-model/README.md"
DOC_PATH = ROOT / "docs/w3c-time-temporal-model.md"
TRACK_DIR = ROOT / "conductor/tracks/w3c_time_temporal_model_20260610"
INDEX_PATH = TRACK_DIR / "index.md"
PLAN_PATH = TRACK_DIR / "plan.md"
EVIDENCE_PATH = TRACK_DIR / "evidence.md"
METADATA_PATH = TRACK_DIR / "metadata.json"
TRACKS_PATH = ROOT / "conductor/tracks.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SCHEMA_PATH,
        TTL_PATH,
        JSON_PATH,
        README_PATH,
        DOC_PATH,
        INDEX_PATH,
        PLAN_PATH,
        EVIDENCE_PATH,
        METADATA_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures
    manifest = _json(MANIFEST_PATH)
    schema = _json(SCHEMA_PATH)
    for error in sorted(
        Draft202012Validator(schema).iter_errors(manifest), key=lambda item: list(item.path)
    ):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")
    if manifest["release_status"] != "release-ready-sample-temporal-model":
        failures.append("W3C Time release_status must be release-ready-sample-temporal-model.")
    claim = manifest["public_claim"]
    if claim.get("sample_only") is not True:
        failures.append("W3C Time public claim must be sample-only.")
    if claim.get("full_corpus_release") is not False:
        failures.append("W3C Time must not claim full corpus release.")
    if claim.get("full_historical_temporal_coverage") is not False:
        failures.append("W3C Time must not claim full historical temporal coverage.")
    if claim.get("proceeding_level_temporal_completeness") is not False:
        failures.append("W3C Time must not claim proceeding-level temporal completeness.")
    ttl = _read(TTL_PATH)
    for term in (
        "time:Instant",
        "time:Interval",
        "time:inXSDDate",
        "sample-only; not full corpus temporal coverage",
    ):
        if term not in ttl:
            failures.append(f"W3C Time Turtle is missing: {term}")
    payload = _json(JSON_PATH)
    if len(payload.get("contexts", [])) != 2:
        failures.append("W3C Time JSON sample must include one instant and one interval.")
    for path, terms in {
        DOC_PATH: (
            "release-ready-sample-temporal-model",
            "sample-only",
            "not full historical temporal coverage",
            "no proceeding-level temporal completeness claim",
        ),
        README_PATH: (
            "release-ready-sample-temporal-model",
            "sample-only",
            "not full corpus temporal coverage",
        ),
        INDEX_PATH: ("release-ready-sample-temporal-model", "not full corpus temporal coverage"),
        EVIDENCE_PATH: (
            "release-ready-sample-temporal-model",
            "Full historical sitting reconciliation",
            "no proceeding-level temporal completeness claim",
        ),
    }.items():
        text = _read(path)
        for term in terms:
            if term not in text:
                failures.append(f"{path.relative_to(ROOT).as_posix()} is missing: {term}")
    metadata = _json(METADATA_PATH)
    if metadata.get("status") != "complete":
        failures.append("W3C Time metadata status must be complete.")
    if "### [x] Track: W3C Time Temporal Model" not in _read(TRACKS_PATH):
        failures.append("Track registry must mark W3C Time Temporal Model complete.")
    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"W3C-TIME-TEMPORAL: {failure}")
        return 1
    print("W3C Time temporal model is sample-release consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
