"""Validate repository-local Conductor learning-log entries."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "conductor" / "learning-log.md"
SCHEMA_PATH = ROOT / "conductor" / "templates" / "learning-entry.schema.json"
ENTRY_HEADING = re.compile(r"^##\s+(.+)$")
FIELD_LINE = re.compile(r"^-\s+`(?P<key>[^`]+)`:\s*(?P<value>.*)$")
LIST_ITEM = re.compile(r"^\s+-\s+(?P<value>.+)$")


def _strip_code_value(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        return value[1:-1]
    return value


def _parse_entries(text: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    current_list_key: str | None = None

    for raw_line in text.splitlines():
        if ENTRY_HEADING.match(raw_line):
            if current is not None:
                entries.append(current)
            current = {}
            current_list_key = None
            continue

        if current is None:
            continue

        field_match = FIELD_LINE.match(raw_line)
        if field_match:
            key = field_match.group("key")
            value = field_match.group("value").strip()
            if value:
                current[key] = _strip_code_value(value)
                current_list_key = None
            else:
                current[key] = []
                current_list_key = key
            continue

        list_match = LIST_ITEM.match(raw_line)
        if list_match and current_list_key:
            value = _strip_code_value(list_match.group("value"))
            current[current_list_key].append(value)

    if current is not None:
        entries.append(current)
    return entries


def _failures() -> list[str]:
    failures: list[str] = []
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    entries = _parse_entries(LOG_PATH.read_text(encoding="utf-8"))

    if not entries:
        return ["conductor/learning-log.md does not contain any learning entries."]

    for index, entry in enumerate(entries, start=1):
        entry_id = entry.get("entry_id", f"entry #{index}")
        for error in sorted(validator.iter_errors(entry), key=lambda item: item.path):
            path = ".".join(str(part) for part in error.path) or "<entry>"
            failures.append(f"{entry_id}: {path}: {error.message}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"LEARNING-LOG: {failure}")
        return 1
    print("Conductor learning log entries are schema-valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
