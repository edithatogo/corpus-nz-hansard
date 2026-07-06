"""Build the NZ Parliament video ongoing archive snapshot and change ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INVENTORY_PATH = ROOT / "manifests" / "parliament_video_source_inventory.json"
SEED_FETCHERS_PATH = ROOT / "manifests" / "parliament_video_seed_fetchers.json"
RECONCILIATION_PATH = ROOT / "manifests" / "parliament_video_reconciliation.json"
ARCHIVE_COVERAGE_PATH = ROOT / "manifests" / "parliament_video_archive_coverage.json"
MEDIA_DECISION_PATH = ROOT / "manifests" / "parliament_video_media_acquisition_decision.json"
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_ongoing_archive.json"
DOC_PATH = ROOT / "docs" / "parliament-video-ongoing-archive.md"
SCHEMA_PATH = ROOT / "schemas" / "parliament_video_ongoing_archive.schema.json"
SNAPSHOT_DIR = ROOT / "derived" / "parliament_video_ongoing_archive" / "snapshots"
SNAPSHOT_PATH = (
    ROOT
    / "derived"
    / "parliament_video_ongoing_archive"
    / "parliament_video_ongoing_archive_snapshot.json"
)
CHANGES_PATH = (
    ROOT
    / "derived"
    / "parliament_video_ongoing_archive"
    / "parliament_video_ongoing_archive_changes.json"
)

DEFAULT_RETENTION = 12
DEFAULT_CRON = "37 3 * * 0"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _stable_digest(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def _latest_snapshot() -> Path | None:
    if not SNAPSHOT_DIR.exists():
        return None
    snapshots = sorted(SNAPSHOT_DIR.glob("*.json"))
    return snapshots[-1] if snapshots else None


def _source_records(
    inventory: dict[str, Any],
    reconciliation: dict[str, Any],
    archive_coverage: dict[str, Any],
) -> list[dict[str, Any]]:
    ledger_by_id = {row["source_id"]: row for row in reconciliation["ledger"]}
    records: list[dict[str, Any]] = []
    for source in inventory["sources"]:
        ledger_row = ledger_by_id.get(source["source_id"], {})
        record = {
            "record_id": source["source_id"],
            "record_type": "source",
            "source_family": source["source_family"],
            "source_role": source["source_role"],
            "source_posture": source.get("archive_status", source.get("rights_status")),
            "surface_status": ledger_row.get("gap_status", "metadata-only"),
            "rights_status": source["rights_status"],
            "evidence": [
                "manifests/parliament_video_source_inventory.json",
                "manifests/parliament_video_reconciliation.json",
                "manifests/parliament_video_seed_fetchers.json",
            ],
        }
        record["digest"] = _stable_digest(record)
        records.append(record)

    for surface in archive_coverage["surfaces"]:
        record = {
            "record_id": surface["surface_id"],
            "record_type": "surface",
            "source_family": "coverage_surface",
            "source_role": "supporting",
            "source_posture": surface["local_status"],
            "surface_status": surface["rights_boundary"],
            "rights_status": surface["rights_boundary"],
            "evidence": ["manifests/parliament_video_archive_coverage.json"],
        }
        record["digest"] = _stable_digest(record)
        records.append(record)
    return records


def compare_snapshots(
    previous: dict[str, Any] | None,
    current: dict[str, Any],
) -> dict[str, list[str]]:
    def _record_id(record: dict[str, Any]) -> str:
        return str(record.get("record_id") or record.get("source_id"))

    previous_records = (
        {_record_id(record): record for record in previous.get("records", [])} if previous else {}
    )
    current_records = {_record_id(record): record for record in current.get("records", [])}
    previous_ids = set(previous_records)
    current_ids = set(current_records)
    new_ids = sorted(current_ids - previous_ids)
    deleted_ids = sorted(previous_ids - current_ids)
    changed_ids = sorted(
        record_id
        for record_id in current_ids & previous_ids
        if current_records[record_id].get("digest") != previous_records[record_id].get("digest")
    )
    return {
        "new_source_ids": new_ids,
        "deleted_source_ids": deleted_ids,
        "changed_source_ids": changed_ids,
    }


def _load_previous_snapshot() -> dict[str, Any] | None:
    latest = _latest_snapshot()
    if latest is None:
        return None
    return _read_json(latest)


def _build_manifest(
    generated_at: str, current: dict[str, Any], diff: dict[str, list[str]]
) -> dict[str, Any]:
    monitored_source_count = len(
        [record for record in current["records"] if record["record_type"] == "source"]
    )
    monitored_surface_count = len(current["records"])
    blocked_source_ids = [
        record["record_id"]
        for record in current["records"]
        if "blocked" in record["surface_status"] or "blocked" in record["source_posture"]
    ]
    stale_source_ids = [
        record["record_id"]
        for record in current["records"]
        if record["record_type"] == "source" and record["source_role"] == "fallback"
    ]
    link_rot_watch_ids = [
        record["record_id"]
        for record in current["records"]
        if record["record_type"] == "surface"
        or record["source_posture"] in {"external-only", "metadata-inventory-only"}
    ]
    return {
        "manifest_version": 1,
        "track_id": "parliament_video_ongoing_archive_20260705",
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "workflow": {
            "path": ".github/workflows/parliament-video-ongoing-archive.yml",
            "schedule_cron": DEFAULT_CRON,
            "dispatch_modes": ["dry-run", "refresh"],
            "runner": "scripts/build_parliament_video_ongoing_archive.py",
        },
        "refresh_policy": {
            "cadence": "weekly",
            "snapshot_retention": DEFAULT_RETENTION,
            "comparison_basis": "latest_snapshot",
            "preserve_history": True,
        },
        "policy": {
            "metadata_first": True,
            "no_media_download": True,
            "no_video_file_download": True,
            "no_audio_file_download": True,
            "no_public_media_release": True,
            "no_completeness_claim": True,
            "rights_review_required_before_media_acquisition": True,
            "fallbacks_are_validation_only": True,
        },
        "alert_thresholds": {
            "count_regression_sources": 1,
            "stale_source_days": 30,
            "link_rot_failures": 1,
            "blocked_source_threshold": 1,
        },
        "change_policy": [
            "new_deletions",
            "new_sources",
            "deleted_sources",
            "changed_sources",
            "gap-ledger-updates-only",
        ],
        "monitored_source_count": monitored_source_count,
        "monitored_surface_count": monitored_surface_count,
        "source_count": monitored_source_count,
        "source_inventory_manifest": "manifests/parliament_video_source_inventory.json",
        "seed_fetchers_manifest": "manifests/parliament_video_seed_fetchers.json",
        "reconciliation_manifest": "manifests/parliament_video_reconciliation.json",
        "archive_coverage_manifest": "manifests/parliament_video_archive_coverage.json",
        "media_acquisition_decision_manifest": "manifests/parliament_video_media_acquisition_decision.json",
        "monitoring": {
            "stale_source_ids": stale_source_ids,
            "link_rot_watch_ids": link_rot_watch_ids,
            "blocked_source_ids": blocked_source_ids,
        },
        "snapshot": {
            "path": "derived/parliament_video_ongoing_archive/parliament_video_ongoing_archive_snapshot.json",
            "previous_snapshot_path": current.get("previous_snapshot_path"),
            "retention_directory": "derived/parliament_video_ongoing_archive/snapshots",
        },
        "change_summary": {
            "new_source_count": len(diff["new_source_ids"]),
            "deleted_source_count": len(diff["deleted_source_ids"]),
            "changed_source_count": len(diff["changed_source_ids"]),
        },
        "comparison": diff,
        "notes": [
            "Scheduled refresh remains metadata-first and never downloads media by default.",
            "Snapshot retention preserves history so changes can be audited over time.",
            "Fallback sources stay validation-only and cannot be promoted to acquisition sources here.",
        ],
    }


def _write_doc(manifest: dict[str, Any]) -> None:
    doc = f"""# Parliament Video Ongoing Archive

Release posture: scheduled metadata refresh, gap monitoring, and no-download guard.

This track keeps the Parliament video archive moving without media downloads. It preserves prior snapshots, tracks source changes, and keeps the no-media boundary in force unless a later approved decision changes it.

## Refresh Policy

- Cadence: {manifest["refresh_policy"]["cadence"]}
- Snapshot retention: {manifest["refresh_policy"]["snapshot_retention"]}
- Comparison basis: latest snapshot

## Thresholds

- Count regression: {manifest["alert_thresholds"]["count_regression_sources"]} source
- Stale-source threshold: {manifest["alert_thresholds"]["stale_source_days"]} days
- Link-rot threshold: {manifest["alert_thresholds"]["link_rot_failures"]} failure
- Blocked-source threshold: {manifest["alert_thresholds"]["blocked_source_threshold"]} source

## Policy

- Metadata-first only.
- No media download.
- No public media release.
- No completeness claim.
- Rights review required before media acquisition.
- Fallbacks are validation only.

## Workflow

- Scheduled workflow: `{manifest["workflow"]["path"]}`
- Cron: `{manifest["workflow"]["schedule_cron"]}`

## Change Policy

{chr(10).join(f"- {item}" for item in manifest["change_policy"])}

## Monitoring

| Metric | Count |
| --- | --- |
| Monitored sources | {manifest["monitored_source_count"]} |
| Monitored surfaces | {manifest["monitored_surface_count"]} |
| New sources | {manifest["change_summary"]["new_source_count"]} |
| Deleted sources | {manifest["change_summary"]["deleted_source_count"]} |
| Changed sources | {manifest["change_summary"]["changed_source_count"]} |

## Operational Notes

- Stale sources are tracked from the fallback portion of the inventory and are reported even when access remains metadata-only.
- Link-rot watch covers archive-coverage surfaces and the metadata-only surfaces that are most likely to drift.
- The ongoing archive does not download Parliament video or audio files.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def build_manifest(
    *, write_outputs: bool = True, snapshot_dir: Path = SNAPSHOT_DIR
) -> dict[str, Any]:
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    inventory = _read_json(SOURCE_INVENTORY_PATH)
    seed = _read_json(SEED_FETCHERS_PATH)
    reconciliation = _read_json(RECONCILIATION_PATH)
    archive_coverage = _read_json(ARCHIVE_COVERAGE_PATH)
    media_decision = _read_json(MEDIA_DECISION_PATH)

    current_records = _source_records(inventory, reconciliation, archive_coverage)
    current_snapshot: dict[str, Any] = {
        "manifest_version": 1,
        "track_id": "parliament_video_ongoing_archive_20260705",
        "generated_at": generated_at,
        "records": current_records,
    }
    previous_snapshot = _load_previous_snapshot()
    diff = compare_snapshots(previous_snapshot, current_snapshot)
    manifest = _build_manifest(
        generated_at,
        {
            **current_snapshot,
            "previous_snapshot_path": _latest_snapshot().as_posix() if _latest_snapshot() else None,
        },
        diff,
    )
    manifest["seed_target_count"] = seed["summary"]["target_count"]
    manifest["reconciliation_ledger_count"] = reconciliation["summary"]["ledger_row_count"]
    manifest["archive_surface_count"] = archive_coverage["summary"]["surface_count"]
    manifest["media_acquisition_decision_state"] = media_decision["decision_state"]
    manifest["no_media_download_guard"] = media_decision["policy"]["no_media_download"] is True
    manifest["summary"] = {
        "monitored_source_count": manifest["monitored_source_count"],
        "monitored_surface_count": manifest["monitored_surface_count"],
        "new_source_count": manifest["change_summary"]["new_source_count"],
        "deleted_source_count": manifest["change_summary"]["deleted_source_count"],
        "changed_source_count": manifest["change_summary"]["changed_source_count"],
        "retention_limit": manifest["refresh_policy"]["snapshot_retention"],
        "no_media_download": True,
        "stale_source_watch_count": len(manifest["monitoring"]["stale_source_ids"]),
        "link_rot_watch_count": len(manifest["monitoring"]["link_rot_watch_ids"]),
        "blocked_source_watch_count": len(manifest["monitoring"]["blocked_source_ids"]),
    }

    if write_outputs:
        _write_json(MANIFEST_PATH, manifest)
        _write_json(
            SNAPSHOT_PATH,
            {
                "manifest_version": 1,
                "track_id": manifest["track_id"],
                "generated_at": generated_at,
                "records": current_records,
                "previous_snapshot_path": manifest["snapshot"]["previous_snapshot_path"],
            },
        )
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        _write_json(snapshot_dir / f"{generated_at.replace(':', '-')}.json", current_snapshot)
        _write_json(
            CHANGES_PATH, {"track_id": manifest["track_id"], "generated_at": generated_at, **diff}
        )
        _write_doc(manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-write", action="store_true", help="Compute outputs without writing files."
    )
    args = parser.parse_args()
    manifest = build_manifest(write_outputs=not args.no_write)
    print(f"Wrote {MANIFEST_PATH.relative_to(ROOT).as_posix()}")
    print(f"Monitored sources: {manifest['monitored_source_count']}")


if __name__ == "__main__":
    main()
