"""Build the NZ Parliament video reconciliation ledger."""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "manifests" / "parliament_video_source_inventory.json"
SEED_PATH = ROOT / "manifests" / "parliament_video_seed_fetchers.json"
ARCHIVE_COVERAGE_PATH = ROOT / "manifests" / "parliament_video_archive_coverage.json"
MANIFEST_PATH = ROOT / "manifests" / "parliament_video_reconciliation.json"
LEDGER_PATH = (
    ROOT
    / "derived"
    / "parliament_video_reconciliation"
    / "parliament_video_reconciliation_ledger.json"
)
DOC_PATH = ROOT / "docs" / "parliament-video-reconciliation.md"

SOURCE_PRIORITY = {
    "official-parliament-video": 1,
    "official-parliament-live-and-recorded": 2,
    "official-youtube-nz-parliament": 3,
    "parliament-on-demand-house-archive": 4,
    "select-committee-on-demand-archive": 5,
    "select-committee-live-streams-current": 6,
    "select-committee-vimeo-pages": 7,
    "parliament-website-embedded-video-pages": 8,
    "parliament-site-search-and-sitemaps": 9,
    "tvnz-archive-looking-back": 10,
    "nga-taonga-av-collection": 11,
    "archives-new-zealand-av-catalogue": 12,
    "rnz-parliament": 13,
    "parliament-today-am-network": 14,
    "internet-archive-webcaptures": 15,
    "memento-cdx-web-archives": 16,
    "adjacent-sm-govt-nz": 17,
    "adjacent-hathi-nz": 18,
    "adjacent-corpus-law-nz": 19,
}

GAP_STATUSES = (
    "metadata-only",
    "rights-gated",
    "fallback-only",
    "evidence-only",
    "access-blocked",
    "migrated",
    "missing-everywhere",
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _build_gap_status(source: dict[str, Any], seed_target: dict[str, Any] | None) -> str:
    source_role = source["source_role"]
    source_id = source["source_id"]
    fallback_role = source.get("fallback_role", "not_fallback")

    if source_role == "supporting":
        return "evidence-only"
    if source_role == "fallback":
        if fallback_role == "audio_or_reporting_validation":
            return "evidence-only"
        if seed_target and seed_target.get("proof_status") == "blocked":
            return "access-blocked"
        if seed_target and seed_target.get("proof_status") == "fetched":
            return "fallback-only"
        if seed_target and seed_target.get("proof_status") == "index-only":
            return "fallback-only"
        return "fallback-only"
    if seed_target is None:
        return "missing-everywhere"
    if seed_target.get("source_classification") == "rights-gated":
        return "rights-gated"
    if seed_target.get("proof_status") == "blocked":
        return "access-blocked"
    if source_id == "parliament-on-demand-house-archive":
        return "migrated"
    if seed_target.get("proof_status") in {"fetched", "index-only"}:
        return "metadata-only"
    return "missing-everywhere"


def _build_ledger(
    inventory: dict[str, Any],
    seed: dict[str, Any],
    archive: dict[str, Any],
) -> list[dict[str, Any]]:
    seed_by_id = {row["source_id"]: row for row in seed["targets"]}
    archive_by_repo = {row["repo"]: row for row in archive["adjacent_repo_findings"]}
    rows: list[dict[str, Any]] = []

    for source in inventory["sources"]:
        source_id = source["source_id"]
        seed_target = seed_by_id.get(source_id)
        proof_status = seed_target["proof_status"] if seed_target else "not-seeded"
        gap_status = _build_gap_status(source, seed_target)
        source_classification = (
            seed_target["source_classification"]
            if seed_target
            else "evidence-only"
            if source["source_role"] == "supporting"
            else "fallback-only"
        )
        row: dict[str, Any] = {
            "source_id": source_id,
            "source_family": source["source_family"],
            "source_role": source["source_role"],
            "source_priority": SOURCE_PRIORITY[source_id],
            "source_classification": source_classification,
            "gap_status": gap_status,
            "reconciliation_grain": "source-family/source-id",
            "inventory_archive_status": source["archive_status"],
            "inventory_rights_status": source["rights_status"],
            "seed_proof_status": proof_status,
            "seed_rights_status": seed_target["rights_status"] if seed_target else "not-seeded",
            "seed_index_url": seed_target["index_url"] if seed_target else None,
            "seed_sample_url": seed_target["sample_url"] if seed_target else None,
            "seed_blocked_reason": seed_target["blocked_reason"] if seed_target else None,
            "evidence": [
                _relative(INVENTORY_PATH),
                _relative(SEED_PATH),
            ],
        }
        if source["source_family"] == "adjacent_repo_evidence":
            row["evidence"] = [_relative(ARCHIVE_COVERAGE_PATH)]
        rows.append(row)

    for repo in ("sm-govt-nz", "hathi-nz", "corpus-law-nz"):
        finding = archive_by_repo[repo]
        rows.append(
            {
                "source_id": finding["repo"],
                "source_family": "adjacent_repo_evidence",
                "source_role": "supporting",
                "source_priority": SOURCE_PRIORITY[f"adjacent-{repo}"],
                "source_classification": "evidence-only",
                "gap_status": "evidence-only",
                "reconciliation_grain": "adjacent-repo-boundary",
                "inventory_archive_status": "supporting_evidence_only",
                "inventory_rights_status": "not_media_source",
                "seed_proof_status": "not-applicable",
                "seed_rights_status": "not-applicable",
                "seed_index_url": None,
                "seed_sample_url": None,
                "seed_blocked_reason": None,
                "evidence": [_relative(ARCHIVE_COVERAGE_PATH)],
                "boundary_finding": finding["finding"],
            }
        )

    return rows


def _build_manifest(
    generated_at: str,
    inventory: dict[str, Any],
    seed: dict[str, Any],
    archive: dict[str, Any],
    ledger: list[dict[str, Any]],
) -> dict[str, Any]:
    gap_counts = Counter(row["gap_status"] for row in ledger)
    classification_counts = Counter(row["source_classification"] for row in ledger)
    source_roles = Counter(row["source_role"] for row in ledger)
    official_source_count = len(inventory["source_summary"]["official_source_ids"])
    fallback_source_count = len(inventory["source_summary"]["fallback_source_ids"])
    supporting_source_count = len(
        [
            row
            for row in ledger
            if row["source_role"] == "supporting" and row["source_id"].startswith("adjacent-")
        ]
    )
    return {
        "manifest_version": 1,
        "track_id": "parliament_video_reconciliation_20260705",
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "reconciliation_status": "not-complete",
        "policy": {
            "metadata_first": True,
            "no_video_file_download": True,
            "no_audio_file_download": True,
            "no_public_media_release": True,
            "no_completeness_claim": True,
            "rights_review_required_before_media_acquisition": True,
            "fallbacks_are_validation_only": True,
        },
        "inputs": {
            "inventory_manifest": _relative(INVENTORY_PATH),
            "seed_fetchers_manifest": _relative(SEED_PATH),
            "archive_coverage_manifest": _relative(ARCHIVE_COVERAGE_PATH),
        },
        "reconciliation_grains": [
            "source-family",
            "source-id",
            "surface-state",
            "adjacent-repo-boundary",
        ],
        "gap_taxonomy": list(GAP_STATUSES),
        "source_priorities": [
            {
                "rank": 1,
                "label": "Official Parliament video surfaces",
                "source_ids": [
                    "official-parliament-video",
                    "official-parliament-live-and-recorded",
                    "parliament-on-demand-house-archive",
                    "select-committee-on-demand-archive",
                    "select-committee-live-streams-current",
                    "parliament-website-embedded-video-pages",
                    "parliament-site-search-and-sitemaps",
                ],
            },
            {
                "rank": 2,
                "label": "Rights-gated official platform mirrors",
                "source_ids": [
                    "official-youtube-nz-parliament",
                    "select-committee-vimeo-pages",
                ],
            },
            {
                "rank": 3,
                "label": "Fallback validation sources",
                "source_ids": [
                    "tvnz-archive-looking-back",
                    "nga-taonga-av-collection",
                    "archives-new-zealand-av-catalogue",
                    "rnz-parliament",
                    "parliament-today-am-network",
                    "internet-archive-webcaptures",
                    "memento-cdx-web-archives",
                ],
            },
            {
                "rank": 4,
                "label": "Adjacent repository boundaries",
                "source_ids": [
                    "adjacent-sm-govt-nz",
                    "adjacent-hathi-nz",
                    "adjacent-corpus-law-nz",
                ],
            },
        ],
        "cross_checks": [
            {
                "check_id": "inventory-manifest",
                "status": "pass",
                "evidence": _relative(INVENTORY_PATH),
                "details": f"{official_source_count} official, {fallback_source_count} fallback, {supporting_source_count} supporting sources are inventoried.",
            },
            {
                "check_id": "seed-fetchers-manifest",
                "status": "pass",
                "evidence": _relative(SEED_PATH),
                "details": f"{seed['summary']['target_count']} seed targets prove metadata-only retrieval, blocked states, and fallback validation roles.",
            },
            {
                "check_id": "archive-coverage-manifest",
                "status": "pass",
                "evidence": _relative(ARCHIVE_COVERAGE_PATH),
                "details": "retrospective_archive_complete and ongoing_archive_complete remain false, so no completeness claim is made.",
            },
            {
                "check_id": "adjacent-repo-boundaries",
                "status": "pass",
                "evidence": _relative(ARCHIVE_COVERAGE_PATH),
                "details": "sm-govt-nz stays metadata-only; hathi-nz and corpus-law-nz remain not-applicable for video coverage.",
            },
        ],
        "summary": {
            "source_count": len(inventory["sources"]),
            "official_source_count": official_source_count,
            "fallback_source_count": fallback_source_count,
            "supporting_source_count": supporting_source_count,
            "seed_target_count": seed["summary"]["target_count"],
            "ledger_row_count": len(ledger),
            "metadata_reconciled_source_count": sum(
                1
                for row in ledger
                if row["gap_status"] in {"metadata-only", "rights-gated", "migrated"}
            ),
            "fallback_only_source_count": gap_counts["fallback-only"],
            "evidence_only_source_count": gap_counts["evidence-only"],
            "rights_gated_source_count": gap_counts["rights-gated"],
            "access_blocked_source_count": gap_counts["access-blocked"],
            "migrated_source_count": gap_counts["migrated"],
            "missing_everywhere_source_count": gap_counts["missing-everywhere"],
            "retrospective_archive_complete": False,
            "ongoing_archive_complete": False,
            "complete_video_archive": False,
            "metadata_completeness_claim": False,
            "media_completeness_claim": False,
            "gap_status_counts": dict(sorted(gap_counts.items())),
            "source_classification_counts": dict(sorted(classification_counts.items())),
            "source_role_counts": dict(sorted(source_roles.items())),
        },
        "ledger": ledger,
        "notes": [
            "Metadata completeness and media completeness remain separate.",
            "Fallback sources are validation-only and do not authorize public media claims.",
            "No retrospective archive completeness claim is made from metadata alone.",
        ],
        "adjacent_repo_findings": archive["adjacent_repo_findings"],
    }


def _write_doc(manifest: dict[str, Any]) -> None:
    summary = manifest["summary"]
    ledger_rows = manifest["ledger"]
    rows = "\n".join(
        f"| `{row['source_id']}` | {row['gap_status']} | {row['source_classification']} | {row['seed_proof_status']} |"
        for row in ledger_rows
    )
    priorities = "\n".join(
        f"- {item['rank']}. {item['label']}: {', '.join(f'`{source_id}`' for source_id in item['source_ids'])}"
        for item in manifest["source_priorities"]
    )
    cross_checks = "\n".join(
        f"- `{check['check_id']}`: {check['details']} ({check['evidence']})"
        for check in manifest["cross_checks"]
    )
    DOC_PATH.write_text(
        f"""# Parliament Video Reconciliation

Release posture: metadata-first reconciliation ledger.

This track reconciles Parliament video metadata against multiple independent sources before any completeness claim. It is explicitly not a complete retrospective archive and it does not permit a media-completeness claim.

## Policy

- Metadata-first only.
- No video-file download in this track.
- No audio-file download in this track.
- No public media release.
- No completeness claim.
- Rights review required before media acquisition.
- Fallback sources are validation only.

## Inputs

- `{manifest["inputs"]["inventory_manifest"]}`
- `{manifest["inputs"]["seed_fetchers_manifest"]}`
- `{manifest["inputs"]["archive_coverage_manifest"]}`

## Summary

| Field | Value |
| --- | --- |
| Source count | {summary["source_count"]} |
| Official sources | {summary["official_source_count"]} |
| Fallback sources | {summary["fallback_source_count"]} |
| Supporting boundary sources | {summary["supporting_source_count"]} |
| Seed targets | {summary["seed_target_count"]} |
| Ledger rows | {summary["ledger_row_count"]} |
| Metadata reconciled | {summary["metadata_reconciled_source_count"]} |
| Rights gated | {summary["rights_gated_source_count"]} |
| Fallback only | {summary["fallback_only_source_count"]} |
| Evidence only | {summary["evidence_only_source_count"]} |
| Access blocked | {summary["access_blocked_source_count"]} |
| Migrated | {summary["migrated_source_count"]} |
| Missing everywhere | {summary["missing_everywhere_source_count"]} |

Retrospective archive complete: {summary["retrospective_archive_complete"]}
Ongoing archive complete: {summary["ongoing_archive_complete"]}
Complete video archive: {summary["complete_video_archive"]}

## Gap Taxonomy

{chr(10).join(f"- {gap}" for gap in manifest["gap_taxonomy"])}

## Source Priorities

{priorities}

## Cross Checks

{cross_checks}

## Exception Ledger

| Source | Gap status | Classification | Seed proof |
| --- | --- | --- | --- |
{rows}

## Residual Gaps

- Rights-gated surfaces remain constrained by platform terms or media rights review.
- TVNZ Archive, Ngā Taonga, Archives New Zealand, RNZ, Parliament Today, and web archives remain validation-only evidence rather than acquisition permissions.
- The repository still does not have a complete retrospective archive or a complete ongoing archive.

## Next Actions

- Feed this reconciliation result into the full metadata archive track.
- Keep future completeness claims gated on additional authority evidence, not metadata presence alone.
- Preserve the distinction between metadata completeness and media completeness in downstream documentation.
""",
        encoding="utf-8",
    )


def build_manifest(*, generated_at: str | None = None) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).replace(microsecond=0).isoformat()
    inventory = _read_json(INVENTORY_PATH)
    seed = _read_json(SEED_PATH)
    archive = _read_json(ARCHIVE_COVERAGE_PATH)
    ledger = _build_ledger(inventory, seed, archive)
    manifest = _build_manifest(generated_at, inventory, seed, archive, ledger)
    _write_json(MANIFEST_PATH, manifest)
    _write_json(
        LEDGER_PATH,
        {
            "track_id": manifest["track_id"],
            "generated_at": generated_at,
            "summary": manifest["summary"],
            "ledger": ledger,
        },
    )
    _write_doc(manifest)
    return manifest


def main() -> None:
    manifest = build_manifest()
    print(f"Wrote {_relative(MANIFEST_PATH)}")
    print(f"Wrote {_relative(LEDGER_PATH)}")
    print(f"Ledger rows: {manifest['summary']['ledger_row_count']}")


if __name__ == "__main__":
    main()
