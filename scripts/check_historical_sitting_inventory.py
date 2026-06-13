"""Validate the official sitting/proceeding inventory manifest."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/historical_sitting_inventory.json"
SCHEMA_PATH = ROOT / "schemas/historical_sitting_inventory.schema.json"
TRACK_PATH = ROOT / "conductor/tracks/full_historical_sitting_reconciliation_20260610/evidence.md"

EXPECTED_SOURCE_IDS = {
    "nz-parliament-parliamentary-business-hub",
    "nz-parliament-historic-journals-of-the-house",
    "nz-parliament-daily-progress",
    "nz-parliament-journals-indexes",
    "nz-parliament-order-paper",
    "nz-parliament-weekly-journals-archive",
    "nz-parliament-sessional-journals-archive",
    "nz-parliament-hansard-current",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, TRACK_PATH):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")

    source_ids = {item["id"] for item in manifest["sources"]}
    if source_ids != EXPECTED_SOURCE_IDS:
        failures.append(
            "historical sitting inventory source ids must match the official Parliament inventory."
        )

    track = _read(TRACK_PATH)
    for required in (
        "historical_sitting_inventory.json",
        "Parliamentary Business",
        "Historic Journals of the House",
        "Weekly Journals Archive",
        "Sessional Journals archive",
        "Indexes to the Journals",
        "Daily progress in the House",
    ):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"HISTORICAL-SITTING-INVENTORY: {failure}")
        return 1
    print("Historical sitting inventory manifest is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
