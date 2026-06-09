"""Discover CSV schema metadata inside a Hansard ZIP without full extraction."""

from __future__ import annotations

import argparse
import csv
import io
import json
import zipfile
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_ARCHIVE = Path("2024-09-06 Hansard Extract from DocumentsDB.zip")
DEFAULT_OUTPUT = Path("manifests/schema_discovery.json")
DEFAULT_SAMPLE_ROWS = 5
ENCODINGS = ("utf-8-sig", "utf-8", "cp1252", "latin-1")
DELIMITERS = ",\t;|"
csv.field_size_limit(1024 * 1024 * 1024)

ROLE_PATTERNS = {
    "date": ("date", "sitting", "day"),
    "speaker": ("speaker", "member", "person", "name"),
    "party": ("party", "political"),
    "topic": ("topic", "subject", "debate", "title", "business", "bill"),
    "text": ("text", "speech", "content", "body", "transcript", "hansard"),
}


def _decode_sample(raw: bytes) -> tuple[str, str]:
    if raw.startswith(b"\xff\xfe"):
        return raw.decode("utf-16"), "utf-16"
    if raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16"), "utf-16"
    prefix = raw[:2000]
    if prefix and prefix.count(b"\x00") / len(prefix) > 0.2:
        even_nulls = prefix[::2].count(b"\x00")
        odd_nulls = prefix[1::2].count(b"\x00")
        encoding = "utf-16-le" if odd_nulls >= even_nulls else "utf-16-be"
        return raw.decode(encoding), encoding
    for encoding in ENCODINGS:
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="replace"), "latin-1"


def _sniff_dialect(text: str) -> csv.Dialect:
    try:
        return csv.Sniffer().sniff(text, delimiters=DELIMITERS)
    except csv.Error:
        return csv.get_dialect("excel")


def _candidate_roles(headers: list[str]) -> dict[str, list[str]]:
    roles: dict[str, list[str]] = {role: [] for role in ROLE_PATTERNS}
    for header in headers:
        normalized = header.lower().replace("_", " ").replace("-", " ")
        for role, patterns in ROLE_PATTERNS.items():
            if role == "text" and "date" in normalized:
                continue
            if any(pattern in normalized for pattern in patterns):
                roles[role].append(header)
    return roles


def _empty_value(value: str | None) -> bool:
    return value is None or value.strip() == ""


def _read_prefix(archive: zipfile.ZipFile, info: zipfile.ZipInfo) -> bytes:
    with archive.open(info, "r") as stream:
        return stream.read(min(info.file_size, 1024 * 1024))


def _discover_member(
    archive: zipfile.ZipFile,
    info: zipfile.ZipInfo,
    sample_rows: int,
) -> dict[str, Any]:
    prefix = _read_prefix(archive, info)
    sample_text, encoding = _decode_sample(prefix)
    dialect = _sniff_dialect(sample_text)

    row_count = 0
    sample: list[dict[str, str]] = []
    null_counts: Counter[str] = Counter()
    headers: list[str] = []

    with archive.open(info, "r") as stream:
        wrapper = io.TextIOWrapper(stream, encoding=encoding, errors="replace", newline="")
        reader = csv.DictReader(wrapper, dialect=dialect)
        headers = list(reader.fieldnames or [])
        for row in reader:
            row_count += 1
            normalized_row = {header: row.get(header, "") or "" for header in headers}
            for header, value in normalized_row.items():
                if _empty_value(value):
                    null_counts[header] += 1
            if len(sample) < sample_rows:
                sample.append(normalized_row)

    return {
        "name": info.filename,
        "encoding": encoding,
        "delimiter": dialect.delimiter,
        "quotechar": dialect.quotechar,
        "headers": headers,
        "header_count": len(headers),
        "header_signature": "|".join(headers),
        "row_count": row_count,
        "sample_rows": sample,
        "null_counts": {header: null_counts.get(header, 0) for header in headers},
        "candidate_roles": _candidate_roles(headers),
    }


def build_schema_discovery(
    archive_path: Path | str,
    sample_rows: int = DEFAULT_SAMPLE_ROWS,
) -> dict[str, Any]:
    """Return CSV schema discovery metadata for every file in a ZIP archive."""
    archive_path = Path(archive_path)
    if not archive_path.exists():
        raise FileNotFoundError(f"Archive not found: {archive_path}")
    if not zipfile.is_zipfile(archive_path):
        raise ValueError(f"Not a valid ZIP archive: {archive_path}")

    files: list[dict[str, Any]] = []
    with zipfile.ZipFile(archive_path, "r") as archive:
        for info in archive.infolist():
            if info.is_dir() or not info.filename.lower().endswith(".csv"):
                continue
            files.append(_discover_member(archive, info, sample_rows))

    signature_counts = Counter(file_info["header_signature"] for file_info in files)
    column_files: dict[str, list[str]] = defaultdict(list)
    for file_info in files:
        for header in file_info["headers"]:
            column_files[header].append(file_info["name"])

    return {
        "discovery_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "source_archive": str(archive_path),
        "sample_rows_per_file": sample_rows,
        "summary": {
            "file_count": len(files),
            "total_rows": sum(file_info["row_count"] for file_info in files),
            "header_signatures": len(signature_counts),
            "all_columns": sorted(column_files),
            "columns_by_file_count": {
                column: len(paths) for column, paths in sorted(column_files.items())
            },
            "header_signature_counts": dict(signature_counts),
        },
        "files": files,
    }


def write_schema_discovery(discovery: dict[str, Any], output_path: Path | str) -> None:
    """Write schema discovery JSON with stable formatting."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(discovery, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover CSV schemas inside a source ZIP without full extraction."
    )
    parser.add_argument(
        "--archive",
        type=Path,
        default=DEFAULT_ARCHIVE,
        help=f"Source ZIP path. Default: {DEFAULT_ARCHIVE}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Schema discovery JSON output path. Default: {DEFAULT_OUTPUT}",
    )
    parser.add_argument(
        "--sample-rows",
        type=int,
        default=DEFAULT_SAMPLE_ROWS,
        help=f"Sample rows to retain per file. Default: {DEFAULT_SAMPLE_ROWS}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    discovery = build_schema_discovery(args.archive, sample_rows=args.sample_rows)
    write_schema_discovery(discovery, args.output)
    print(f"Wrote {args.output}")
    print(f"Files: {discovery['summary']['file_count']}")
    print(f"Rows: {discovery['summary']['total_rows']}")
    print(f"Header signatures: {discovery['summary']['header_signatures']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
