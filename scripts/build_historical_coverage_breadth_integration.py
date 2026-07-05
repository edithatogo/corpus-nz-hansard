"""Build the cross-repo historical coverage breadth integration manifest."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "historical_coverage_breadth_integration.json"
DOC_PATH = ROOT / "docs" / "historical-coverage-breadth-integration.md"
EVIDENCE_PATH = (
    ROOT
    / "conductor"
    / "archive"
    / "historical_coverage_breadth_integration_20260705"
    / "evidence.md"
)


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_manifest(now: str) -> dict[str, object]:
    return {
        "manifest_version": 1,
        "repository": "corpus-nz-hansard",
        "track_id": "historical_coverage_breadth_integration_20260705",
        "generated_at": now,
        "bridge_status": "evidence-only",
        "policy": {
            "no_completeness_claim": True,
            "no_bulk_acquisition": True,
            "official_sources_first": True,
            "legislation_and_gazette_excluded": True,
        },
        "coverage_taxonomy": {
            "official": ["official"],
            "fallback": ["fallback"],
            "supporting": ["supporting"],
            "evidence_only": ["evidence_only"],
            "excluded": ["excluded"],
        },
        "adjacent_repos": [
            {
                "repo": "hathi-nz",
                "path": str((ROOT.parent / "hathi-nz").resolve()),
                "role": "HathiTrust Hansard discovery and archive evidence",
            },
            {
                "repo": "corpus-law-nz",
                "path": str((ROOT.parent / "corpus-law-nz").resolve()),
                "role": "Legislation and Gazette boundary reference",
            },
        ],
        "boundary_rules": [
            "corpus-law-nz keeps NZ legislation and Gazette out of scope.",
            "HathiTrust may be cited only as discovery or gap-detection evidence.",
            "Supporting sources can narrow historical gaps but cannot replace official Parliament coverage.",
        ],
        "source_map": [
            {
                "source_id": "nz-parliament-hansard-current",
                "family": "hansard_debates",
                "posture": "official",
                "role": "primary",
                "notes": "Official debates surface remains the anchor source.",
            },
            {
                "source_id": "papers-past-hansard",
                "family": "hansard_debates",
                "posture": "fallback",
                "role": "gap-detection",
                "notes": "Useful for older debate references and OCR cross-checks.",
            },
            {
                "source_id": "google-books-hansard-volumes",
                "family": "hansard_debates",
                "posture": "fallback",
                "role": "gap-detection",
                "notes": "Discovery and triangulation only, not a bulk dependency.",
            },
            {
                "source_id": "library-catalogue-hansard-holdings",
                "family": "hansard_debates",
                "posture": "fallback",
                "role": "gap-detection",
                "notes": "Physical holdings and catalogue metadata for unresolved gaps.",
            },
            {
                "source_id": "nz-parliament-weekly-journals-archive",
                "family": "journals",
                "posture": "official",
                "role": "primary",
                "notes": "Weekly journals remain an official reconciliation input.",
            },
            {
                "source_id": "papers-past-ajhr",
                "family": "papers_presented_ajhr",
                "posture": "fallback",
                "role": "gap-detection",
                "notes": "Historical AJHR discovery input with rights and coverage notes.",
            },
            {
                "source_id": "o-nehera-british-parliamentary-papers-context",
                "family": "papers_presented_ajhr",
                "posture": "supporting",
                "role": "contextual-triangulation",
                "notes": "Contextual only; helps locate British Parliamentary Papers relationships.",
            },
            {
                "source_id": "data-govt-parliament-dataset-requests",
                "family": "parliamentary_rules_procedure",
                "posture": "evidence_only",
                "role": "demand-signal",
                "notes": "Evidence of user demand or gap discussion only.",
            },
            {
                "source_id": "excluded-nz-legislation",
                "family": "parliamentary_rules_procedure",
                "posture": "excluded",
                "role": "boundary",
                "notes": "Legislation is handled in the adjacent corpus-law-nz repo.",
            },
            {
                "source_id": "excluded-nz-gazette",
                "family": "papers_presented_ajhr",
                "posture": "excluded",
                "role": "boundary",
                "notes": "Gazette records are outside this Parliament bridge.",
            },
        ],
        "historical_gap_model": {
            "grains": ["family", "time_period", "source_pair"],
            "statuses": ["open", "narrowed", "resolved", "excluded"],
            "notes": "Gap status distinguishes uncovered historical periods from narrowed source pairs and explicitly excluded domains.",
        },
        "linked_manifests": [
            "manifests/parliament_dataset_inventory.json",
            "manifests/historical_coverage_audit.json",
            "manifests/historical_sitting_inventory.json",
            "../hathi-nz/manifests/hathitrust-nz/nz_parliamentary_debates_hansard.json",
            "../corpus-law-nz/docs/cross_corpus_interoperability_hansard.md",
        ],
        "no_completeness_claims": [
            "This bridge is evidence-only, not a completeness claim.",
            "Historical completeness requires official reconciliation plus adjacent evidence.",
            "NZ legislation and Gazette remain excluded from this track.",
        ],
    }


def main() -> None:
    now = datetime.now(UTC).replace(microsecond=0).date().isoformat()
    manifest = build_manifest(now)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    DOC_PATH.write_text(
        """# Historical Coverage Breadth Integration

Release posture: evidence-only.

This bridge manifest makes a no completeness claim. It links the Parliament website inventory to adjacent historical evidence sources without claiming completeness. It keeps NZ legislation and the Gazette out of scope, and it treats HathiTrust and other historical resources as gap-detection evidence and discovery evidence while preserving the distinction between discovery evidence and acquisition evidence.

## Coverage model

- Official: Parliament website sources that remain the anchor.
- Fallback: Papers Past, Google Books, and library catalogues used only to narrow historical gaps.
- Supporting: Contextual sources such as O Nehera for British Parliamentary Papers relationships.
- Evidence-only: Data.govt.nz requests and similar demand signals.
- Excluded: NZ legislation and Gazette, plus other non-primary baselines.

## Adjacent repos

- `hathi-nz` supplies HathiTrust-side Hansard discovery and archive evidence.
- `corpus-law-nz` remains the legislation/Gazette boundary reference.

## Guardrails

- Do not claim full historical completeness.
- Do not promote fallback sources to official sources without manifest changes.
- Do not use this bridge as a bulk-acquisition dependency.
""",
        encoding="utf-8",
    )
    EVIDENCE_PATH.write_text(
        """# Evidence

Release posture: evidence-only.

Evidence added:

- `scripts/build_historical_coverage_breadth_integration.py` generates the bridge manifest and docs.
- `scripts/check_historical_coverage_breadth_integration.py` validates schema, posture, boundary rules, and adjacent-repo references.
- `tests/test_historical_coverage_breadth_integration.py` exercises build and validation.
- `manifests/historical_coverage_breadth_integration.json` records the cross-repo coverage model.
- The bridge makes a no completeness claim.
- The coverage posture uses gap-detection evidence and discovery evidence instead of bulk-acquisition claims.
- HathiTrust remains a historical Hansard evidence companion, not a completeness source.

## Repository boundary summary

- `corpus-nz-hansard` remains the Parliament website anchor.
- `hathi-nz` is cited only for historical Hansard discovery and archive evidence.
- `corpus-law-nz` remains the legislation/Gazette boundary reference.

This bridge does not claim historical completeness or bulk-acquisition readiness.
""",
        encoding="utf-8",
    )
    write_json(MANIFEST_PATH, manifest)


if __name__ == "__main__":
    main()
