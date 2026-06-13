"""Build the historical sitting reconciliation ledger from normalized Hansard rows."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PARQUET = ROOT / "generated/parquet/hansard.parquet"
DEFAULT_OUTPUT_DIR = ROOT / "derived/historical_sitting_reconciliation"
DEFAULT_LEDGER = DEFAULT_OUTPUT_DIR / "historical_sitting_ledger.parquet"
DEFAULT_SUMMARY = DEFAULT_OUTPUT_DIR / "historical_sitting_ledger_summary.json"

SITTING_DATE_RE = re.compile(r"Sitting date:\s*([0-9]{1,2} [A-Za-z]+ [0-9]{4})")
VOLUME_PAGE_RE = re.compile(r"Volume:([0-9]+);Page:([0-9]+)")


def _write_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _normalize_title(value: str | None) -> str:
    if not value:
        return ""
    normalized = re.sub(r"[^0-9A-Za-z]+", " ", value).strip().lower()
    return re.sub(r"\s+", " ", normalized)


def _publication_surface(document_type: str | None, content: str | None) -> str:
    text = f"{document_type or ''} {content or ''}".lower()
    if "order paper" in text:
        return "Order Paper"
    if "daily progress" in text:
        return "Daily Progress"
    if "sessional journal" in text:
        return "Sessional Journals"
    if "weekly journal" in text:
        return "Weekly Journals"
    if "journals of the house" in text or "historic journal" in text or "journal" in text:
        return "Journals"
    if "hansard" in text:
        return "Hansard"
    return "Unknown"


def _extract_sitting_date(content: str | None) -> str:
    if not content:
        return ""
    match = SITTING_DATE_RE.search(content)
    return match.group(1) if match else ""


def _extract_volume_page(content: str | None) -> tuple[str, str]:
    if not content:
        return "", ""
    match = VOLUME_PAGE_RE.search(content)
    if not match:
        return "", ""
    return match.group(1), match.group(2)


def _comparison_key(row: dict[str, Any]) -> str:
    parts = [
        str(row["sitting_date"]),
        str(row["parliament_number"]),
        str(row["publication_surface"]),
        str(row["stable_id"]),
        str(row["publication_title_normalized"]),
        str(row["issue_or_volume"]),
        str(row["entry_sequence"]),
    ]
    return "|".join(parts)


def _records_from_parquet(parquet_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    columns = [
        "stable_id",
        "source_file",
        "source_row_number",
        "parliament_number",
        "document_type",
        "title",
        "content",
    ]
    ledger_rows: list[dict[str, Any]] = []
    summary = {
        "source_row_count": 0,
        "sitting_date_extracted_rows": 0,
        "sitting_date_missing_rows": 0,
        "volume_page_extracted_rows": 0,
        "volume_page_missing_rows": 0,
        "publication_surface_counts": Counter(),
        "document_type_counts": Counter(),
        "parliament_counts": Counter(),
        "source_file_counts": Counter(),
    }

    parquet_file = pq.ParquetFile(parquet_path)
    for batch in parquet_file.iter_batches(batch_size=4096, columns=columns):
        for record in batch.to_pylist():
            content = record.get("content") or ""
            sitting_date = _extract_sitting_date(content)
            volume, page = _extract_volume_page(content)
            publication_surface = _publication_surface(record.get("document_type"), content)
            entry_sequence = int(record.get("source_row_number") or 0)
            row = {
                "stable_id": record.get("stable_id") or "",
                "source_file": record.get("source_file") or "",
                "source_row_number": entry_sequence,
                "parliament_number": int(record.get("parliament_number") or 0),
                "document_type": record.get("document_type") or "",
                "title": record.get("title") or "",
                "publication_title_normalized": _normalize_title(record.get("title")),
                "sitting_date_raw": sitting_date,
                "sitting_date": sitting_date,
                "volume": volume,
                "page": page,
                "issue_or_volume": volume,
                "entry_sequence": entry_sequence,
                "publication_surface": publication_surface,
                "comparison_key": "",
                "extraction_status": "complete"
                if sitting_date and volume and page
                else "partial"
                if sitting_date or volume or page
                else "missing",
                "content_length": len(content),
            }
            row["comparison_key"] = _comparison_key(row)
            ledger_rows.append(row)

            summary["source_row_count"] += 1
            if sitting_date:
                summary["sitting_date_extracted_rows"] += 1
            else:
                summary["sitting_date_missing_rows"] += 1
            if volume and page:
                summary["volume_page_extracted_rows"] += 1
            else:
                summary["volume_page_missing_rows"] += 1
            summary["publication_surface_counts"][publication_surface] += 1
            summary["document_type_counts"][row["document_type"]] += 1
            summary["parliament_counts"][str(row["parliament_number"])] += 1
            summary["source_file_counts"][row["source_file"]] += 1

    return ledger_rows, summary


def build_historical_sitting_ledger(
    *,
    parquet_path: Path = DEFAULT_PARQUET,
    ledger_path: Path = DEFAULT_LEDGER,
    summary_path: Path = DEFAULT_SUMMARY,
    generated_at: str | None = None,
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    if not parquet_path.exists():
        raise FileNotFoundError(f"Normalized corpus artifact not found: {parquet_path}")

    rows, summary = _records_from_parquet(parquet_path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), ledger_path)

    summary_payload = {
        "artifact_name": "historical_sitting_reconciliation",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "source_parquet": parquet_path.relative_to(ROOT).as_posix()
        if parquet_path.is_relative_to(ROOT)
        else str(parquet_path),
        "ledger_parquet": ledger_path.relative_to(ROOT).as_posix()
        if ledger_path.is_relative_to(ROOT)
        else str(ledger_path),
        "ledger_summary": summary_path.relative_to(ROOT).as_posix()
        if summary_path.is_relative_to(ROOT)
        else str(summary_path),
        "row_count": len(rows),
        "source_row_count": summary["source_row_count"],
        "sitting_date_extracted_rows": summary["sitting_date_extracted_rows"],
        "sitting_date_missing_rows": summary["sitting_date_missing_rows"],
        "volume_page_extracted_rows": summary["volume_page_extracted_rows"],
        "volume_page_missing_rows": summary["volume_page_missing_rows"],
        "publication_surface_counts": dict(
            sorted(summary["publication_surface_counts"].items())
        ),
        "document_type_counts": dict(
            sorted(summary["document_type_counts"].items(), key=lambda item: (-item[1], item[0]))
        ),
        "parliament_counts": dict(sorted(summary["parliament_counts"].items())),
        "source_file_counts": dict(sorted(summary["source_file_counts"].items())),
        "notes": [
            "This ledger is a normalized comparison input, not a completed official reconciliation.",
            "Comparison against official inventory surfaces still happens in the next pass.",
        ],
    }
    _write_json(summary_payload, summary_path)
    return {
        "ledger_parquet": summary_payload["ledger_parquet"],
        "summary": summary_payload,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the historical sitting reconciliation ledger."
    )
    parser.add_argument("--parquet", type=Path, default=DEFAULT_PARQUET)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_historical_sitting_ledger(
        parquet_path=args.parquet,
        ledger_path=args.ledger,
        summary_path=args.summary,
    )
    print(f"Wrote {result['ledger_parquet']}")
    print(f"Rows: {result['summary']['row_count']}")
    print(f"Published sittings: {result['summary']['sitting_date_extracted_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
