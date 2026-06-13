"""Compare official historical sitting PDF export dates against the corpus ledger."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX_PATH = ROOT / "derived/historical_sitting_official_exports/historical_sitting_official_export_index.json"
DEFAULT_LEDGER_PATH = ROOT / "derived/historical_sitting_reconciliation/historical_sitting_ledger.parquet"
DEFAULT_OUTPUT_PATH = ROOT / "derived/historical_sitting_official_exports/historical_sitting_official_exports_coverage.json"

HEADER_DATE_RE = re.compile(
    r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}"
)
LEDGER_DATE_RE = re.compile(r"^[0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}$")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _extract_pdf_dates(pdf_path: Path) -> list[str]:
    reader = PdfReader(str(pdf_path))
    dates: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        match = HEADER_DATE_RE.search(text)
        if match:
            dates.append(match.group(0))
    return dates


def _normalize_date(value: str) -> str:
    for fmt in ("%A, %d %B %Y", "%d %B %Y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue
    return value


def _load_ledger_dates(ledger_path: Path) -> set[str]:
    table = pq.read_table(ledger_path, columns=["sitting_date"])
    return {
        _normalize_date(value)
        for value in table.column("sitting_date").to_pylist()
        if value and isinstance(value, str) and LEDGER_DATE_RE.match(value)
    }


def _year(value: str) -> str:
    return value[:4] if len(value) >= 4 else value


def build_historical_sitting_official_exports_coverage(
    *,
    index_path: Path = DEFAULT_INDEX_PATH,
    ledger_path: Path = DEFAULT_LEDGER_PATH,
    output_path: Path = DEFAULT_OUTPUT_PATH,
    generated_at: str | None = None,
) -> dict[str, Any]:
    index = _json(index_path)
    if not ledger_path.exists():
        raise FileNotFoundError(f"Ledger parquet not found: {ledger_path}")

    ledger_dates = _load_ledger_dates(ledger_path)
    source_reports: list[dict[str, Any]] = []
    official_dates: set[str] = set()
    total_page_dates = 0
    year_summary: dict[str, dict[str, set[str]]] = {}

    for source in index["sources"]:
        pdf_path = ROOT / source["cached_pdf"]
        if not pdf_path.exists():
            raise FileNotFoundError(f"Cached PDF not found: {pdf_path}")
        dates = _extract_pdf_dates(pdf_path)
        normalized_dates = [_normalize_date(value) for value in dates]
        date_counts = Counter(normalized_dates)
        unique_dates = set(normalized_dates)
        official_dates |= unique_dates
        total_page_dates += len(normalized_dates)
        for date in unique_dates:
            year_summary.setdefault(
                _year(date), {"official_dates": set(), "ledger_dates": set()}
            )
            year_summary[_year(date)]["official_dates"].add(date)
        source_reports.append(
            {
                "id": source["id"],
                "title": source["title"],
                "publication_stage": source["publication_stage"],
                "page_count": source["page_count"],
                "header_date_count": len(normalized_dates),
                "unique_header_date_count": len(unique_dates),
                "shared_dates_with_ledger": len(unique_dates & ledger_dates),
                "missing_in_ledger": sorted(unique_dates - ledger_dates)[:25],
                "missing_in_official": sorted(ledger_dates - unique_dates)[:25],
                "most_common_header_dates": date_counts.most_common(10),
            }
        )

    for date in ledger_dates:
        year_summary.setdefault(_year(date), {"official_dates": set(), "ledger_dates": set()})
        year_summary[_year(date)]["ledger_dates"].add(date)

    year_rows = [
        {
            "year": year,
            "official_dates": len(counts["official_dates"]),
            "ledger_dates": len(counts["ledger_dates"]),
            "shared_dates": len(counts["official_dates"] & counts["ledger_dates"]),
            "status": (
                "covered"
                if counts["official_dates"] and counts["ledger_dates"]
                else "official-only"
                if counts["official_dates"]
                else "ledger-only"
            ),
        }
        for year, counts in sorted(year_summary.items())
    ]
    acquisition_priority_years = [
        row["year"] for row in year_rows if row["status"] == "ledger-only"
    ]

    report = {
        "artifact_name": "historical_sitting_official_exports_coverage",
        "artifact_version": "0.1.0",
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "index_path": index_path.relative_to(ROOT).as_posix()
        if index_path.is_relative_to(ROOT)
        else str(index_path),
        "ledger_path": ledger_path.relative_to(ROOT).as_posix()
        if ledger_path.is_relative_to(ROOT)
        else str(ledger_path),
        "official_date_count": len(official_dates),
        "ledger_date_count": len(ledger_dates),
        "shared_date_count": len(official_dates & ledger_dates),
        "official_years": sorted({_year(value) for value in official_dates}),
        "ledger_years": sorted({_year(value) for value in ledger_dates}),
        "year_summary": year_rows,
        "acquisition_priority_years": acquisition_priority_years,
        "page_header_date_count": total_page_dates,
        "sources": source_reports,
        "notes": [
            "This is a date-level comparison probe, not the final row-by-row historical reconciliation.",
            "It uses page-header dates extracted from the confirmed official PDF exports.",
            "Years marked ledger-only are acquisition priorities for the next reconciliation pass.",
        ],
    }
    _write_json(report, output_path)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare official historical sitting PDF export dates against the corpus ledger."
    )
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX_PATH)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_historical_sitting_official_exports_coverage(
        index_path=args.index,
        ledger_path=args.ledger,
        output_path=args.output,
    )
    print(f"Wrote {args.output}")
    print(f"Official date count: {result['official_date_count']}")
    print(f"Shared dates: {result['shared_date_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
