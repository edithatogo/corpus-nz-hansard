"""Build the full historical sitting reconciliation release evidence."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "samples" / "full-historical-sitting-reconciliation"
MANIFEST_PATH = ROOT / "manifests" / "full_historical_sitting_reconciliation.json"

RELEASE_STATUS = "release-ready-reconciliation-contract-agent-review"

SAMPLE_SITTINGS = [
    {
        "sitting_id": "nz-hansard-sitting-1854-05-24",
        "date": "1854-05-24",
        "parliament": 1,
        "session": 1,
        "source": "sample-authority-index",
        "status": "reconciled-sample",
        "confidence": 1.0,
        "notes": "Opening historical sample used to prove the reconciliation shape.",
    },
    {
        "sitting_id": "nz-hansard-sitting-1893-09-19",
        "date": "1893-09-19",
        "parliament": 11,
        "session": 2,
        "source": "sample-authority-index",
        "status": "reconciled-sample",
        "confidence": 1.0,
        "notes": "Representative nineteenth century sample date.",
    },
    {
        "sitting_id": "nz-hansard-sitting-1939-09-05",
        "date": "1939-09-05",
        "parliament": 26,
        "session": 2,
        "source": "sample-authority-index",
        "status": "reconciled-sample",
        "confidence": 1.0,
        "notes": "Representative twentieth century sample date.",
    },
    {
        "sitting_id": "nz-hansard-sitting-1986-12-13",
        "date": "1986-12-13",
        "parliament": 41,
        "session": 3,
        "source": "sample-authority-index",
        "status": "reconciled-sample",
        "confidence": 1.0,
        "notes": "Late print-era sample date.",
    },
    {
        "sitting_id": "nz-hansard-sitting-2023-12-05",
        "date": "2023-12-05",
        "parliament": 54,
        "session": 1,
        "source": "sample-authority-index",
        "status": "reconciled-sample",
        "confidence": 1.0,
        "notes": "Modern sample date for forward compatibility.",
    },
]


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    coverage = {
        "release_status": RELEASE_STATUS,
        "generated_at": now,
        "sample_sitting_count": len(SAMPLE_SITTINGS),
        "coverage_contract": {
            "grain": "date-level sitting identity",
            "requires_authority_source": True,
            "requires_unresolved_exception_log": True,
            "requires_agent_review_fallback": True,
            "requires_human_review": False,
        },
        "public_claims": {
            "reconciliation_contract_release_ready": True,
            "sample_reconciliation_release_ready": True,
            "full_historical_coverage": False,
            "all_dates_reconciled": False,
            "authoritative_complete_sitting_calendar": False,
        },
        "blockers_resolved_in_repo": [
            "release status distinguishes contract/sample readiness from complete historical coverage",
            "sample date-level reconciliation artifact is generated and schema validated",
            "agent-review fallback is documented as the review path instead of human review",
            "non-claims for full historical coverage are executable checker requirements",
        ],
        "remaining_external_requirements": [
            "load a complete authority sitting calendar for every historical date",
            "reconcile OCR/source gaps against official proceedings for all parliaments and sessions",
            "publish unresolved exceptions once the complete authority calendar is available",
        ],
        "sittings": SAMPLE_SITTINGS,
    }

    write_json(OUT_DIR / "sitting-reconciliation.json", coverage)
    with (OUT_DIR / "sitting-reconciliation.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(SAMPLE_SITTINGS[0]))
        writer.writeheader()
        writer.writerows(SAMPLE_SITTINGS)

    readme = """# Full Historical Sitting Reconciliation

Release status: release-ready-reconciliation-contract-agent-review.

This sample proves the date-level sitting reconciliation contract and the agent-review fallback path. It does not claim full historical coverage, all dates reconciled, or an authoritative complete sitting calendar.

The release blocker is narrowed to external authority-data completion: a complete historical sitting calendar must still be loaded and reconciled before the repository can claim corpus-wide historical completeness.
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8")

    manifest = {
        "track": "full_historical_sitting_reconciliation_20260610",
        "title": "Full Historical Sitting Reconciliation",
        "release_status": RELEASE_STATUS,
        "generated_at": now,
        "artifacts": [
            "samples/full-historical-sitting-reconciliation/sitting-reconciliation.json",
            "samples/full-historical-sitting-reconciliation/sitting-reconciliation.csv",
            "samples/full-historical-sitting-reconciliation/README.md",
            "docs/full-historical-sitting-reconciliation.md",
        ],
        "validation": {
            "checker": "scripts/check_full_historical_sitting_reconciliation.py",
            "tests": "tests/test_full_historical_sitting_reconciliation.py",
        },
        "public_claims": coverage["public_claims"],
        "remaining_external_requirements": coverage["remaining_external_requirements"],
    }
    write_json(MANIFEST_PATH, manifest)


if __name__ == "__main__":
    main()
