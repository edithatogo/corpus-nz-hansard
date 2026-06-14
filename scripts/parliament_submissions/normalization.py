"""Schema normalization for parliament submission records."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError:
    pa = None
    pq = None


NORMALIZED_SCHEMA: pa.Schema | None = (
    pa.schema(
        [
            pa.field("submission_id", pa.string(), nullable=False),
            pa.field("submitter_name", pa.string()),
            pa.field("submitter_normalized", pa.string()),
            pa.field("date", pa.string()),
            pa.field("date_normalized", pa.string()),
            pa.field("committee", pa.string()),
            pa.field("committee_normalized", pa.string()),
            pa.field("bill_reference", pa.string()),
            pa.field("bill_reference_normalized", pa.string()),
            pa.field("text_content", pa.string()),
            pa.field("text_sha256", pa.string()),
            pa.field("source_url", pa.string()),
            pa.field("parliament_number", pa.int32()),
            pa.field("submission_year", pa.int32()),
        ]
    )
    if pa is not None
    else None
)


def normalize_submitter_name(raw: str | None) -> str | None:
    if not raw or not raw.strip():
        return None
    cleaned = raw.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.rstrip(".,;:-")
    cleaned = cleaned.strip()
    return cleaned if cleaned else None


def normalize_date(raw: str | None) -> str | None:
    if not raw or not raw.strip():
        return None
    raw = raw.strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", raw):
        return raw
    m = re.match(
        r"(\d{1,2})(?:st|nd|rd|th)?\s+"
        r"(January|February|March|April|May|June|July|"
        r"August|September|October|November|December)\s+(\d{4})",
        raw, re.IGNORECASE,
    )
    if m:
        from datetime import datetime
        try:
            dt = datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(3)}", "%d %B %Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass
    m = re.match(r"(\d{2})[/-](\d{2})[/-](\d{4})", raw)
    if m:
        from datetime import datetime
        try:
            dt = datetime.strptime(f"{m.group(1)}/{m.group(2)}/{m.group(3)}", "%d/%m/%Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None


def normalize_committee(raw: str | None) -> str | None:
    if not raw or not raw.strip():
        return None
    cleaned = raw.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned if cleaned else None


def normalize_bill_reference(raw: str | None) -> str | None:
    if not raw or not raw.strip():
        return None
    cleaned = raw.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.rstrip(".,;:")
    cleaned = cleaned.strip()
    return cleaned if cleaned else None


def normalize_text_content(raw: str | None) -> str:
    if not raw:
        return ""
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    text = text.strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def normalize_submission_entry(entry: dict[str, Any]) -> dict[str, Any]:
    submission_id = str(entry.get("id", "")) or ""
    submitter_name_raw = entry.get("submitter")
    submitter_name = normalize_submitter_name(submitter_name_raw)
    date_raw = entry.get("submission_date") or entry.get("date")
    date_normalized = normalize_date(date_raw)
    committee_raw = entry.get("committee")
    committee_normalized = normalize_committee(committee_raw)
    bill_ref_raw = entry.get("bill_reference")
    bill_ref_normalized = normalize_bill_reference(bill_ref_raw)
    text_raw = entry.get("text_content") or entry.get("text")
    text_content = normalize_text_content(text_raw)
    text_sha256 = hashlib.sha256(text_content.encode("utf-8")).hexdigest() if text_content else None
    source_url = entry.get("source_url") or entry.get("document_url")
    parliament_number = entry.get("parliament_number")

    submission_year: int | None = None
    if date_normalized and re.match(r"^\d{4}", date_normalized):
        try:
            submission_year = int(date_normalized[:4])
        except (ValueError, TypeError):
            pass

    return {
        "submission_id": submission_id,
        "submitter_name": submitter_name,
        "submitter_normalized": submitter_name,
        "date": date_raw.strip() if isinstance(date_raw, str) else date_raw,
        "date_normalized": date_normalized,
        "committee": committee_raw.strip() if isinstance(committee_raw, str) else committee_raw,
        "committee_normalized": committee_normalized,
        "bill_reference": bill_ref_raw.strip() if isinstance(bill_ref_raw, str) else bill_ref_raw,
        "bill_reference_normalized": bill_ref_normalized,
        "text_content": text_content,
        "text_sha256": text_sha256,
        "source_url": source_url,
        "parliament_number": parliament_number,
        "submission_year": submission_year,
    }


def write_normalized_parquet(
    records: list[dict[str, Any]],
    output_path: Path | str,
    *,
    schema: pa.Schema | None = None,
) -> str:
    if pa is None or pq is None:
        raise ImportError("pyarrow is required to write Parquet files")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    use_schema = schema or NORMALIZED_SCHEMA
    table = pa.Table.from_pylist(records, schema=use_schema)
    pq.write_table(table, str(output_path))
    return str(output_path.resolve())