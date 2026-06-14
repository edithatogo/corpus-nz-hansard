"""Validate normalized Hansard Parquet records against the record schema."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq
from jsonschema import Draft202012Validator

# Ensure repo root is on sys.path so CI checkouts can import shared utilities.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import shared_utils  # noqa: E402

DEFAULT_PARQUET = Path("generated/parquet/hansard.parquet")
DEFAULT_SCHEMA = Path("schemas/hansard_record.schema.json")
DEFAULT_REPORT = Path("manifests/record_schema_validation.json")


def validate_hansard_records(
    parquet_path: Path | str = DEFAULT_PARQUET,
    schema_path: Path | str = DEFAULT_SCHEMA,
    report_path: Path | str | None = DEFAULT_REPORT,
    batch_size: int = 1000,
) -> dict[str, Any]:
    """Validate normalized Parquet rows and write a machine-readable report."""
    parquet_path = Path(parquet_path)
    schema_path = Path(schema_path)
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet input not found: {parquet_path}")
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    stable_ids: Counter[str] = Counter()
    document_ids: Counter[str] = Counter()
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    record_count = 0

    parquet_file = pq.ParquetFile(parquet_path)
    for record_batch in parquet_file.iter_batches(batch_size=batch_size):
        for record in record_batch.to_pylist():
            row_number = record_count
            record_count += 1
            stable_id = str(record.get("stable_id") or "")
            document_id = str(record.get("parliament_document_id") or "")
            if stable_id:
                stable_ids[stable_id] += 1
            if document_id:
                document_ids[document_id] += 1

            for err in validator.iter_errors(record):
                errors.append(
                    {
                        "type": "schema_error",
                        "row": row_number,
                        "stable_id": stable_id,
                        "path": list(err.path),
                        "message": err.message,
                    }
                )

            content = str(record.get("content") or "")
            if record.get("text_sha256") != shared_utils.sha256_text(content):
                errors.append(
                    {
                        "type": "text_hash_mismatch",
                        "row": row_number,
                        "stable_id": stable_id,
                    }
                )
            if not record.get("document_content_date"):
                warnings.append(
                    {
                        "type": "missing_document_content_date",
                        "row": row_number,
                        "stable_id": stable_id,
                    }
                )

    for value, count in stable_ids.items():
        if value and count > 1:
            errors.append({"type": "duplicate_stable_id", "stable_id": value, "count": count})
    for value, count in document_ids.items():
        if value and count > 1:
            warnings.append(
                {
                    "type": "duplicate_parliament_document_id",
                    "parliament_document_id": value,
                    "count": count,
                }
            )

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "parquet_path": str(parquet_path),
        "schema_path": str(schema_path),
        "record_count": record_count,
        "errors": errors,
        "warnings": warnings,
        "ok": not errors,
    }
    if report_path:
        shared_utils.write_json(Path(report_path), report)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate normalized Hansard Parquet records against the JSON schema."
    )
    parser.add_argument("--parquet", type=Path, default=DEFAULT_PARQUET)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--batch-size", type=int, default=1000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = validate_hansard_records(
        parquet_path=args.parquet,
        schema_path=args.schema,
        report_path=args.report,
        batch_size=args.batch_size,
    )
    print(f"Validated {report['record_count']} records")
    print(f"Errors: {len(report['errors'])}")
    print(f"Warnings: {len(report['warnings'])}")
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
