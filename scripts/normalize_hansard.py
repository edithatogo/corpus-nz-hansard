"""Normalize Hansard CSV records from a source ZIP into Parquet."""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import zipfile
from collections import Counter, defaultdict
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

try:
    from scripts.discover_schema import _decode_sample, _sniff_dialect
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.discover_schema import _decode_sample, _sniff_dialect

# Ensure repo root is on sys.path so CI checkouts can import shared utilities.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import shared_utils  # noqa: E402

DEFAULT_ARCHIVE = Path("2024-09-06 Hansard Extract from DocumentsDB.zip")
DEFAULT_OUTPUT_DIR = Path("generated/parquet")
DEFAULT_MANIFEST = Path("manifests/normalization_manifest.json")
DEFAULT_VALIDATION = Path("manifests/normalization_validation.json")
DEFAULT_BATCH_SIZE = 1000

NORMALIZED_COLUMNS = [
    "stable_id",
    "jurisdiction",
    "country",
    "source",
    "source_archive",
    "source_file",
    "source_row_number",
    "parliament_number",
    "parliament_document_id",
    "document_type",
    "title",
    "abbreviated_title",
    "status",
    "content",
    "member_of_parliament_raw",
    "member_of_parliament_count",
    "portfolio_raw",
    "last_modified",
    "document_content_date",
    "language",
    "text_sha256",
    "source_hash",
    "pipeline_version",
]

PARQUET_SCHEMA = pa.schema(
    [
        ("stable_id", pa.string()),
        ("jurisdiction", pa.string()),
        ("country", pa.string()),
        ("source", pa.string()),
        ("source_archive", pa.string()),
        ("source_file", pa.string()),
        ("source_row_number", pa.int64()),
        ("parliament_number", pa.int64()),
        ("parliament_document_id", pa.string()),
        ("document_type", pa.string()),
        ("title", pa.string()),
        ("abbreviated_title", pa.string()),
        ("status", pa.string()),
        ("content", pa.string()),
        ("member_of_parliament_raw", pa.string()),
        ("member_of_parliament_count", pa.int64()),
        ("portfolio_raw", pa.string()),
        ("last_modified", pa.string()),
        ("document_content_date", pa.string()),
        ("language", pa.string()),
        ("text_sha256", pa.string()),
        ("source_hash", pa.string()),
        ("pipeline_version", pa.string()),
    ]
)

DEFAULT_PIPELINE_VERSION = "0.1.0"
DEFAULT_SOURCE = "New Zealand Parliament Hansard DocumentsDB extract"
PARQUET_COMPRESSION = "zstd"


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _parse_int(value: str | None) -> int | None:
    cleaned = _clean(value)
    if cleaned is None:
        return None
    return int(cleaned)


def _parse_timestamp(value: str | None) -> str | None:
    cleaned = _clean(value)
    if cleaned is None:
        return None
    trimmed = cleaned
    if "." in trimmed:
        head, tail = trimmed.split(".", 1)
        digits = "".join(char for char in tail if char.isdigit())[:6]
        trimmed = f"{head}.{digits}" if digits else head
    return datetime.fromisoformat(trimmed).isoformat()


def _member_count(value: str | None) -> int:
    cleaned = _clean(value)
    if cleaned is None:
        return 0
    return len([part for part in (item.strip() for item in cleaned.split(";")) if part])


def _stable_id(document_id: str | None, source_file: str, source_row_number: int) -> str:
    if document_id:
        return document_id
    return f"{source_file}#{source_row_number}"


def normalize_row(
    row: dict[str, str],
    source_file: str,
    source_row_number: int,
    source_archive: str | None = None,
    pipeline_version: str = DEFAULT_PIPELINE_VERSION,
) -> tuple[dict[str, Any], list[str]]:
    """Normalize one source CSV row and return warning codes."""
    warnings: list[str] = []

    try:
        parliament_number = _parse_int(row.get("ParliamentNumber"))
    except ValueError:
        parliament_number = None
        warnings.append("invalid_parliament_number")

    try:
        last_modified = _parse_timestamp(row.get("LastModified"))
    except ValueError:
        last_modified = None
        warnings.append("invalid_last_modified")

    try:
        document_content_date = _parse_timestamp(row.get("DocumentContentDate"))
    except ValueError:
        document_content_date = None
        warnings.append("invalid_document_content_date")

    content = _clean(row.get("Content"))
    if content is None:
        warnings.append("missing_content")

    member_raw = _clean(row.get("MemberOfParliament"))
    document_id = _clean(row.get("ParliamentDocumentId"))
    stable_id = _stable_id(document_id, source_file, source_row_number)
    abbreviated_title = _clean(row.get("AbbreviatedTitle"))
    title = _clean(row.get("Title")) or abbreviated_title or document_id or stable_id
    text_for_hash = content or ""
    source_hash_payload = json.dumps(
        {
            "source_archive": source_archive,
            "source_file": source_file,
            "source_row_number": source_row_number,
            "parliament_document_id": document_id,
            "content": text_for_hash,
        },
        ensure_ascii=False,
        sort_keys=True,
    )

    return (
        {
            "stable_id": stable_id,
            "jurisdiction": "New Zealand",
            "country": "NZ",
            "source": DEFAULT_SOURCE,
            "source_archive": source_archive,
            "source_file": source_file,
            "source_row_number": source_row_number,
            "parliament_number": parliament_number,
            "parliament_document_id": document_id,
            "document_type": _clean(row.get("DocumentType")),
            "title": title,
            "abbreviated_title": abbreviated_title,
            "status": _clean(row.get("Status")),
            "content": content,
            "member_of_parliament_raw": member_raw,
            "member_of_parliament_count": _member_count(member_raw),
            "portfolio_raw": _clean(row.get("Portfolio")),
            "last_modified": last_modified,
            "document_content_date": document_content_date,
            "language": "en",
            "text_sha256": shared_utils.sha256_text(text_for_hash),
            "source_hash": shared_utils.sha256_text(source_hash_payload),
            "pipeline_version": pipeline_version,
        },
        warnings,
    )


def _csv_infos(archive: zipfile.ZipFile) -> Iterable[zipfile.ZipInfo]:
    for info in archive.infolist():
        if not info.is_dir() and info.filename.lower().endswith(".csv"):
            yield info


def _member_reader(
    archive: zipfile.ZipFile, info: zipfile.ZipInfo
) -> tuple[csv.DictReader[str], io.TextIOWrapper]:
    with archive.open(info, "r") as prefix_stream:
        prefix = prefix_stream.read(min(info.file_size, 1024 * 1024))
    sample_text, encoding = _decode_sample(prefix)
    dialect = _sniff_dialect(sample_text)
    stream = archive.open(info, "r")
    wrapper = io.TextIOWrapper(stream, encoding=encoding, errors="replace", newline="")
    return csv.DictReader(wrapper, dialect=dialect), wrapper


def _write_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _table_from_batch(batch: list[dict[str, Any]]) -> pa.Table:
    columns = {column: [row.get(column) for row in batch] for column in NORMALIZED_COLUMNS}
    return pa.Table.from_pydict(columns, schema=PARQUET_SCHEMA)


def run_normalization(
    archive_path: Path | str = DEFAULT_ARCHIVE,
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
    manifest_path: Path | str = DEFAULT_MANIFEST,
    validation_path: Path | str = DEFAULT_VALIDATION,
    batch_size: int = DEFAULT_BATCH_SIZE,
    pipeline_version: str = DEFAULT_PIPELINE_VERSION,
) -> dict[str, Any]:
    """Stream source CSVs from the archive and write normalized Parquet."""
    archive_path = Path(archive_path)
    output_dir = Path(output_dir)
    manifest_path = Path(manifest_path)
    validation_path = Path(validation_path)
    parquet_path = output_dir / "hansard.parquet"
    output_dir.mkdir(parents=True, exist_ok=True)

    input_rows = 0
    output_rows = 0
    rows_by_file: Counter[str] = Counter()
    warnings_by_code: Counter[str] = Counter()
    warning_examples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    writer: pq.ParquetWriter | None = None
    batch: list[dict[str, Any]] = []

    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            for info in _csv_infos(archive):
                reader, wrapper = _member_reader(archive, info)
                try:
                    for source_row_number, row in enumerate(reader, start=1):
                        input_rows += 1
                        rows_by_file[info.filename] += 1
                        normalized, warnings = normalize_row(
                            row,
                            info.filename,
                            source_row_number,
                            source_archive=str(archive_path),
                            pipeline_version=pipeline_version,
                        )
                        for warning in warnings:
                            warnings_by_code[warning] += 1
                            examples = warning_examples[warning]
                            if len(examples) < 5:
                                examples.append(
                                    {
                                        "source_file": info.filename,
                                        "source_row_number": source_row_number,
                                    }
                                )
                        batch.append(normalized)
                        if len(batch) >= batch_size:
                            table = _table_from_batch(batch)
                            if writer is None:
                                writer = pq.ParquetWriter(
                                    parquet_path,
                                    PARQUET_SCHEMA,
                                    compression=PARQUET_COMPRESSION,
                                )
                            writer.write_table(table)
                            output_rows += len(batch)
                            batch.clear()
                finally:
                    wrapper.close()

        if batch:
            table = _table_from_batch(batch)
            if writer is None:
                writer = pq.ParquetWriter(
                    parquet_path,
                    PARQUET_SCHEMA,
                    compression=PARQUET_COMPRESSION,
                )
            writer.write_table(table)
            output_rows += len(batch)
            batch.clear()
    finally:
        if writer is not None:
            writer.close()

    manifest = {
        "manifest_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "source_archive": str(archive_path),
        "outputs": {
            "parquet": str(parquet_path),
            "validation": str(validation_path),
        },
        "schema": [{"name": field.name, "type": str(field.type)} for field in PARQUET_SCHEMA],
        "normalization_contract": "docs/normalization-contract.md",
        "record_schema": "schemas/hansard_record.schema.json",
        "pipeline_version": pipeline_version,
    }
    validation = {
        "validation_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "summary": {
            "input_rows": input_rows,
            "output_rows": output_rows,
            "warning_count": sum(warnings_by_code.values()),
            "warnings_by_code": dict(warnings_by_code),
        },
        "rows_by_file": dict(rows_by_file),
        "warning_examples": dict(warning_examples),
    }
    _write_json(manifest, manifest_path)
    _write_json(validation, validation_path)

    return {
        "outputs": manifest["outputs"],
        "summary": validation["summary"],
        "rows_by_file": validation["rows_by_file"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize Hansard CSVs from a source ZIP into Parquet."
    )
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--pipeline-version", default=DEFAULT_PIPELINE_VERSION)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_normalization(
        archive_path=args.archive,
        output_dir=args.output_dir,
        manifest_path=args.manifest,
        validation_path=args.validation,
        batch_size=args.batch_size,
        pipeline_version=args.pipeline_version,
    )
    print(f"Wrote {result['outputs']['parquet']}")
    print(f"Input rows: {result['summary']['input_rows']}")
    print(f"Output rows: {result['summary']['output_rows']}")
    print(f"Warnings: {result['summary']['warning_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
