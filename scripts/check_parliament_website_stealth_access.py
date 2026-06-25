"""Validate saved Parliament website stealth-access artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "parliament_website_stealth_access_20260612"
TRACK_DIR = ROOT / "conductor/tracks" / TRACK_ID
DERIVED_DIR = ROOT / "derived/parliament_stealth"
RUN_LOG_PATH = DERIVED_DIR / "run_log.json"
TRACKS_INDEX_PATH = ROOT / "conductor/tracks.md"

TARGETS = {
    "members-current": "Members of Parliament",
    "former-members": "Former Members of Parliament",
    "daily-progress": "Daily progress in the House",
    "order-paper": "Order Paper",
    "hansard-current": "Hansard",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    required_paths = [
        RUN_LOG_PATH,
        TRACK_DIR / "plan.md",
        TRACK_DIR / "evidence.md",
        TRACK_DIR / "metadata.json",
        TRACKS_INDEX_PATH,
    ]
    for path in required_paths:
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    run_log = _json(RUN_LOG_PATH)
    if run_log.get("successful") != len(TARGETS):
        failures.append("Parliament stealth run_log must record all target pages as successful.")
    if run_log.get("total") != len(TARGETS):
        failures.append("Parliament stealth run_log total must match expected target count.")
    if set(run_log.get("targets", [])) != set(TARGETS):
        failures.append("Parliament stealth run_log target labels do not match expected labels.")

    results = run_log.get("results", [])
    if not isinstance(results, list) or len(results) != len(TARGETS):
        failures.append("Parliament stealth run_log must contain one result per target.")
        results = []

    for target, expected_title in TARGETS.items():
        for suffix in ("html", "txt", "png"):
            artifact = DERIVED_DIR / f"{target}.{suffix}"
            if not artifact.exists():
                failures.append(f"{artifact.relative_to(ROOT).as_posix()} must exist.")
            elif artifact.stat().st_size <= 0:
                failures.append(f"{artifact.relative_to(ROOT).as_posix()} must not be empty.")

        text_path = DERIVED_DIR / f"{target}.txt"
        if text_path.exists() and expected_title not in _read(text_path):
            failures.append(
                f"{text_path.relative_to(ROOT).as_posix()} is missing {expected_title}."
            )

    titles = {str(result.get("title", "")) for result in results if isinstance(result, dict)}
    for expected_title in TARGETS.values():
        if not any(expected_title in title for title in titles):
            failures.append(f"run_log result titles are missing {expected_title}.")

    metadata = _json(TRACK_DIR / "metadata.json")
    if metadata.get("status") != "completed":
        failures.append("Parliament stealth track metadata must be completed.")

    plan = _read(TRACK_DIR / "plan.md")
    if "- [ ]" in plan:
        failures.append("Parliament stealth plan must not contain unchecked tasks.")
    for required in (
        "Run Playwright stealth script - SUCCESS",
        "Wayback fallback documented as not required",
    ):
        if required not in plan:
            failures.append(f"Parliament stealth plan is missing: {required}")

    evidence = _read(TRACK_DIR / "evidence.md")
    for required in (
        "Successful Stealth Access",
        "All 5 target pages were successfully fetched",
        "derived/parliament_stealth/",
        "scripts/check_parliament_website_stealth_access.py",
    ):
        if required not in evidence:
            failures.append(f"Parliament stealth evidence is missing: {required}")

    tracks_index = _read(TRACKS_INDEX_PATH)
    if "### [x] Track: Parliament Website Stealth Access" not in tracks_index:
        failures.append("tracks.md must mark Parliament Website Stealth Access complete.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLIAMENT-STEALTH: {failure}")
        return 1
    print("Parliament website stealth-access artifacts are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
