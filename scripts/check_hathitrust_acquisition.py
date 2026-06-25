"""Validate the HathiTrust Hansard acquisition track evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/hathitrust_hansard_acquisition_inventory.json"
TRACK_DIR = ROOT / "conductor/tracks/hathitrust_hansard_acquisition_20260612"
PLAN_PATH = TRACK_DIR / "plan.md"
INDEX_PATH = TRACK_DIR / "index.md"
EVIDENCE_PATH = TRACK_DIR / "evidence.md"
METADATA_PATH = TRACK_DIR / "metadata.json"

REQUIRED_BLOCKER_SNIPPETS = (
    "OAuth",
    "hathifile",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _hathitrust_constants() -> tuple[str, int, tuple[str, ...]]:
    try:
        from scripts.fetch_hathitrust import (
            COLLECTION_ID,
            EXPECTED_VOLUMES,
            KNOWN_WAYBACK_SAMPLE_IDS,
        )
    except ModuleNotFoundError:
        import sys

        sys.path.insert(0, str(ROOT))
        from scripts.fetch_hathitrust import (
            COLLECTION_ID,
            EXPECTED_VOLUMES,
            KNOWN_WAYBACK_SAMPLE_IDS,
        )

    return COLLECTION_ID, EXPECTED_VOLUMES, KNOWN_WAYBACK_SAMPLE_IDS


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, PLAN_PATH, INDEX_PATH, EVIDENCE_PATH, METADATA_PATH):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    collection_id, expected_volumes, known_wayback_sample_ids = _hathitrust_constants()
    manifest = _json(MANIFEST_PATH)
    if manifest.get("artifact_name") != "hathitrust_hansard_acquisition_inventory":
        failures.append("HathiTrust inventory manifest artifact_name is incorrect.")
    if manifest.get("track_id") != "hathitrust_hansard_acquisition_20260612":
        failures.append("HathiTrust inventory manifest track_id is incorrect.")
    if manifest.get("collection_id") != collection_id:
        failures.append(f"HathiTrust inventory must use collection {collection_id}.")
    if manifest.get("expected_volumes") != expected_volumes:
        failures.append(f"HathiTrust inventory must expect {expected_volumes} volumes.")

    enumerated_ids = manifest.get("enumerated_ids", [])
    if len(enumerated_ids) != manifest.get("enumerated_count"):
        failures.append("HathiTrust inventory enumerated_count must match enumerated_ids length.")
    if set(known_wayback_sample_ids) - set(enumerated_ids):
        failures.append("HathiTrust inventory must include the committed Wayback sample IDs.")
    if manifest.get("pending_count", 0) <= 0:
        failures.append(
            "HathiTrust inventory must keep remaining full enumeration explicitly pending."
        )
    if manifest.get("acquisition_status") != "complete-deferred-hathifile-or-oauth-required":
        failures.append(
            "HathiTrust inventory must be complete-deferred without claiming acquisition completion."
        )
    if manifest.get("release_status") != "closed-deferred-external-access-required":
        failures.append(
            "HathiTrust release status must be closed-deferred-external-access-required."
        )

    blockers = " ".join(manifest.get("blockers", []))
    for snippet in REQUIRED_BLOCKER_SNIPPETS:
        if snippet not in blockers:
            failures.append(f"HathiTrust inventory blockers must mention {snippet}.")
    unblock_requirements = manifest.get("unblock_requirements", {})
    complete_inventory = unblock_requirements.get("complete_volume_inventory", {})
    if complete_inventory.get("required_count") != expected_volumes:
        failures.append("HathiTrust unblock requirements must require all 510 volumes.")
    if "hathi_full_YYYYMMDD.txt.gz" not in " ".join(
        complete_inventory.get("accepted_sources", [])
    ) and "local_hathi_full_YYYYMMDD.txt.gz" not in " ".join(
        complete_inventory.get("accepted_sources", [])
    ):
        failures.append("HathiTrust unblock requirements must name local hathifile intake.")
    if manifest.get("live_access_recheck", {}).get("result", "").find("Cloudflare") == -1:
        failures.append(
            "HathiTrust live access recheck must record the current Cloudflare blocker."
        )

    metadata = _json(METADATA_PATH)
    if metadata.get("status") != "complete":
        failures.append("HathiTrust track metadata status must be complete.")
    if metadata.get("release_status") != "closed-deferred-external-access-required":
        failures.append("HathiTrust metadata must record the closed deferred release status.")
    if metadata.get("blocked_on") != "external-hathifile-oauth-or-browser-backed-enumeration":
        failures.append("HathiTrust metadata must identify external unblock requirements.")

    plan = _read(PLAN_PATH)
    for required in (
        "Build deterministic inventory manifest from committed Wayback sample",
        "Document external unblock requirements",
        "39 sample IDs recovered",
        "enumerated_count == 510",
    ):
        if required not in plan:
            failures.append(f"Plan is missing task text: {required}")

    track_text = "\n".join((_read(INDEX_PATH), _read(EVIDENCE_PATH)))
    for required in (
        "closed-deferred-external-access-required",
        "manifests/hathitrust_hansard_acquisition_inventory.json",
        "510",
        "HathiTrust Data API",
    ):
        if required not in track_text:
            failures.append(f"HathiTrust track evidence is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"HATHITRUST-ACQUISITION: {failure}")
        return 1
    print("HathiTrust acquisition inventory is complete-deferred honestly and reproducibly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
