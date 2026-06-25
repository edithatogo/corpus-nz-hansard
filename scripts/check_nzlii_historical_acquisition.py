"""Validate NZLII historical acquisition status evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/nzlii_historical_acquisition_status.json"
TRACK_DIR = ROOT / "conductor/tracks/nzlii_historical_acquisition_20260612"
PLAN_PATH = TRACK_DIR / "plan.md"
INDEX_PATH = TRACK_DIR / "index.md"
EVIDENCE_PATH = TRACK_DIR / "evidence.md"
METADATA_PATH = TRACK_DIR / "metadata.json"
TRACKS_PATH = ROOT / "conductor/tracks.md"
AUTHORITY_SOURCES_PATH = ROOT / "manifests/authority_sources.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _authority_source_registered(source_id: str) -> bool:
    payload = _json(AUTHORITY_SOURCES_PATH)
    return any(source.get("id") == source_id for source in payload.get("sources", []))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, PLAN_PATH, INDEX_PATH, EVIDENCE_PATH, METADATA_PATH, TRACKS_PATH):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    metadata = _json(METADATA_PATH)
    plan = _read(PLAN_PATH)
    evidence = _read(EVIDENCE_PATH)
    index = _read(INDEX_PATH)
    tracks = _read(TRACKS_PATH)

    if manifest.get("artifact_name") != "nzlii_historical_acquisition_status":
        failures.append("NZLII status artifact_name is incorrect.")
    if manifest.get("track_id") != "nzlii_historical_acquisition_20260612":
        failures.append("NZLII status track_id is incorrect.")
    if manifest.get("acquisition_status") != "complete-deferred-cloudflare-challenge":
        failures.append("NZLII acquisition status must be complete-deferred-cloudflare-challenge.")
    if manifest.get("release_status") != "closed-deferred-external-access-required":
        failures.append("NZLII release status must be closed-deferred-external-access-required.")
    if manifest.get("authority_source_registered") is not True:
        failures.append("nzlii-historical-bills must remain registered as an authority source.")
    if not _authority_source_registered("nzlii-historical-bills"):
        failures.append("authority_sources.json must include nzlii-historical-bills.")

    target_statuses = [target.get("status") for target in manifest.get("targets", [])]
    if target_statuses.count("blocked-403-cloudflare-challenge") < 4:
        failures.append("NZLII status must record blocked 403 Cloudflare target probes.")
    if manifest.get("robots", {}).get("reachable") is not False:
        failures.append("NZLII robots.txt must be recorded as blocked on the current recheck.")
    if manifest.get("robots", {}).get("status") != "blocked-403-cloudflare-challenge":
        failures.append("NZLII robots.txt current status must record the Cloudflare challenge.")
    previous = manifest.get("robots", {}).get("previous_content_signal", {})
    if previous.get("search_content_signal") != "yes":
        failures.append("NZLII prior robots content signal should record search=yes.")
    if previous.get("ai_train_content_signal") != "no":
        failures.append("NZLII prior robots content signal should record ai-train=no.")

    if metadata.get("status") != "complete":
        failures.append("NZLII track metadata status must be complete.")
    if metadata.get("release_status") != "closed-deferred-external-access-required":
        failures.append("NZLII metadata must identify the closed deferred release status.")
    if metadata.get("blocked_on") != "external-permission-bulk-api-or-browser-backed-access":
        failures.append("NZLII metadata must identify the external unblock requirements.")
    if "[ ]" in plan or "[~]" in plan:
        failures.append("NZLII plan must not contain unchecked or in-progress tasks.")
    for required in (
        "Try alternative NZLII access patterns",
        "Check if NZLII has an API or bulk data access",
        "Document repo-side resolution as complete-deferred",
    ):
        if required not in plan:
            failures.append(f"NZLII plan missing task text: {required}")
    for required in (
        "complete-deferred",
        "closed-deferred-external-access-required",
        "robots.txt",
        "Cloudflare 403",
        "manifests/nzlii_historical_acquisition_status.json",
    ):
        if required not in evidence + index:
            failures.append(f"NZLII evidence/index missing: {required}")
    if "### [x] Track: NZLII Historical Acquisition" not in tracks:
        failures.append("NZLII track registry must show completed/deferred marker.")
    if "Cloudflare 403" not in tracks:
        failures.append("NZLII track registry must preserve the current blocker summary.")
    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"NZLII-HISTORICAL-ACQUISITION: {failure}")
        return 1
    print("NZLII historical acquisition is complete-deferred honestly and reproducibly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
