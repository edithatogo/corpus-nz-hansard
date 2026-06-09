"""Build a local Zenodo archive package for the Hansard corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = Path("generated/zenodo")
DEFAULT_VERSION = "0.1.0"
DEFAULT_PARQUET = Path("generated/parquet/hansard.parquet")

INCLUDE_DIRS = ("conductor", "docs", "manifests", "schemas", "scripts", "tests")
INCLUDE_FILES = (
    ".gitignore",
    "CITATION.cff",
    "DATASET_CARD.md",
    "LICENSE",
    "NOTICE.md",
    "README.md",
    "RELEASE_NOTES.md",
    "VERSION",
    "requirements.txt",
)


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _add_file(
    archive: tarfile.TarFile,
    manifest_files: list[dict[str, Any]],
    path: Path,
    arcname: str,
) -> None:
    archive.add(path, arcname=arcname)
    manifest_files.append(
        {
            "path": arcname,
            "bytes": path.stat().st_size,
            "sha256": _sha256_path(path),
        }
    )


def build_zenodo_archive(
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
    version: str = DEFAULT_VERSION,
    parquet_path: Path | str = DEFAULT_PARQUET,
) -> dict[str, Any]:
    """Build a tar.gz archive for DOI deposition review."""
    output_dir = Path(output_dir)
    parquet_path = Path(parquet_path)
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet input not found: {parquet_path}")
    output_dir.mkdir(parents=True, exist_ok=True)

    archive_path = output_dir / f"nz-hansard-corpus-{version}.tar.gz"
    manifest_path = output_dir / f"nz-hansard-corpus-{version}.manifest.json"
    root_name = f"nz-hansard-corpus-{version}"
    manifest_files: list[dict[str, Any]] = []

    with tarfile.open(archive_path, "w:gz") as archive:
        for file_name in INCLUDE_FILES:
            path = Path(file_name)
            if path.exists():
                _add_file(archive, manifest_files, path, f"{root_name}/{file_name}")

        for dir_name in INCLUDE_DIRS:
            base = Path(dir_name)
            if not base.exists():
                continue
            for path in sorted(base.rglob("*")):
                if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                    continue
                _add_file(archive, manifest_files, path, f"{root_name}/{path.as_posix()}")

        _add_file(
            archive,
            manifest_files,
            parquet_path,
            f"{root_name}/data/hansard.parquet",
        )

    manifest = {
        "manifest_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "version": version,
        "archive": str(archive_path),
        "archive_sha256": _sha256_path(archive_path),
        "published": False,
        "publication_status": "zenodo_archive_ready_for_draft_upload",
        "source_archive_included": False,
        "files": manifest_files,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {**manifest, "manifest": str(manifest_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a local Zenodo archive package.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--parquet", type=Path, default=DEFAULT_PARQUET)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_zenodo_archive(args.output_dir, args.version, args.parquet)
    print(f"Wrote {result['archive']}")
    print(f"Manifest: {result['manifest']}")
    print(f"Archive SHA-256: {result['archive_sha256']}")
    print("Published: False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
