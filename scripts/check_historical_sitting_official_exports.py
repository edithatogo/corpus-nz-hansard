"""Validate the discovered official PDF export surfaces for historical sitting comparison."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/historical_sitting_official_exports.json"
SCHEMA_PATH = ROOT / "schemas/historical_sitting_official_exports.schema.json"
DOC_PATH = ROOT / "docs/historical-sitting-official-exports.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH):
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

    doc = _read(DOC_PATH)
    for required in (
        "draft, weekly, and sessional",
        "official PDF export surfaces",
        "HTML challenge layer",
    ):
        if required not in doc:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    if len(manifest["sources"]) < 3:
        failures.append("at least three official export sources must be recorded.")
    if len(manifest["authoritative_statements"]) < 2:
        failures.append("authoritative standing-order statements must be recorded.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"HISTORICAL-SITTING-OFFICIAL-EXPORTS: {failure}")
        return 1
    print("Historical sitting official export surfaces are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
