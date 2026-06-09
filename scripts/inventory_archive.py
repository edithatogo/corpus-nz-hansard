"""Inventory a Hansard source ZIP without extracting it to disk."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import IO, Any

DEFAULT_ARCHIVE = Path("2024-09-06 Hansard Extract from DocumentsDB.zip")
DEFAULT_OUTPUT = Path("manifests/source_inventory.json")
BUFFER_SIZE = 1024 * 1024


def _sha256_stream(stream: IO[bytes]) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(BUFFER_SIZE), b""):
        digest.update(chunk)
    return digest.hexdigest()


def _sha256_path(path: Path) -> str:
    with path.open("rb") as stream:
        return _sha256_stream(stream)


def _zip_datetime(info: zipfile.ZipInfo) -> str:
    return datetime(*info.date_time, tzinfo=UTC).isoformat()


def _file_modified_time(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=UTC).isoformat()


def build_inventory(archive_path: Path | str) -> dict[str, Any]:
    """Return source archive and member metadata for a ZIP archive."""
    archive_path = Path(archive_path)
    if not archive_path.exists():
        raise FileNotFoundError(f"Archive not found: {archive_path}")
    if not zipfile.is_zipfile(archive_path):
        raise ValueError(f"Not a valid ZIP archive: {archive_path}")

    stat = archive_path.stat()
    members: list[dict[str, Any]] = []

    with zipfile.ZipFile(archive_path, "r") as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            with archive.open(info, "r") as member_stream:
                member_sha256 = _sha256_stream(member_stream)
            members.append(
                {
                    "name": info.filename,
                    "compressed_size": info.compress_size,
                    "uncompressed_size": info.file_size,
                    "modified_time": _zip_datetime(info),
                    "crc32": f"{info.CRC:08x}",
                    "sha256": member_sha256,
                }
            )

    total_compressed_size = sum(member["compressed_size"] for member in members)
    total_uncompressed_size = sum(member["uncompressed_size"] for member in members)

    return {
        "inventory_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "source_archive": {
            "path": str(archive_path),
            "name": archive_path.name,
            "size": stat.st_size,
            "modified_time": _file_modified_time(archive_path),
            "sha256": _sha256_path(archive_path),
        },
        "summary": {
            "member_count": len(members),
            "total_compressed_size": total_compressed_size,
            "total_uncompressed_size": total_uncompressed_size,
        },
        "members": members,
    }


def write_inventory(inventory: dict[str, Any], output_path: Path | str) -> None:
    """Write inventory JSON with stable formatting."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory a source ZIP and contained files without extraction."
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
        help=f"Inventory JSON output path. Default: {DEFAULT_OUTPUT}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inventory = build_inventory(args.archive)
    write_inventory(inventory, args.output)
    print(f"Wrote {args.output}")
    print(f"Members: {inventory['summary']['member_count']}")
    print(f"Uncompressed bytes: {inventory['summary']['total_uncompressed_size']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
