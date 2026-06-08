"""Build a lightweight local review package for release evaluation."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = Path("generated/release")
DEFAULT_PACKAGE_NAME = "nz-hansard-corpus-0.1.0.zip"
DEFAULT_SOURCE_ARCHIVE = "2024-09-06 Hansard Extract from DocumentsDB.zip"

INCLUDE_PREFIXES = (
    "conductor/",
    "docs/",
    "manifests/",
    "schemas/",
    "scripts/",
    "tests/",
)
INCLUDE_FILES = {
    ".gitignore",
    "CITATION.cff",
    "DATASET_CARD.md",
    "LICENSE",
    "NOTICE.md",
    "README.md",
    "RELEASE_NOTES.md",
    "VERSION",
    "requirements.txt",
}
EXCLUDE_PREFIXES = (
    ".tmp/",
    ".antigravitycli/",
    "generated/",
    "__pycache__/",
)
EXCLUDE_SUFFIXES = (".pyc",)


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _as_posix_relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _should_include(relative: str, source_archive_name: str) -> bool:
    if relative == source_archive_name:
        return False
    if relative in INCLUDE_FILES:
        return True
    if any(relative.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
        return False
    if any(relative.endswith(suffix) for suffix in EXCLUDE_SUFFIXES):
        return False
    return any(relative.startswith(prefix) for prefix in INCLUDE_PREFIXES)


def collect_release_files(
    project_dir: Path | str,
    source_archive_name: str = DEFAULT_SOURCE_ARCHIVE,
) -> list[Path]:
    """Collect lightweight files for the local review package."""
    project_dir = Path(project_dir)
    files: list[Path] = []
    for path in project_dir.rglob("*"):
        if not path.is_file():
            continue
        relative = _as_posix_relative(path, project_dir)
        if _should_include(relative, source_archive_name):
            files.append(path)
    return sorted(files, key=lambda item: _as_posix_relative(item, project_dir))


def build_release_package(
    project_dir: Path | str = Path("."),
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
    package_name: str = DEFAULT_PACKAGE_NAME,
    source_archive_name: str = DEFAULT_SOURCE_ARCHIVE,
) -> dict[str, Any]:
    """Write a local review ZIP and adjacent manifest with file checksums."""
    project_dir = Path(project_dir).resolve()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    package_path = output_dir / package_name
    manifest_path = output_dir / f"{package_path.stem}.manifest.json"

    files = collect_release_files(project_dir, source_archive_name=source_archive_name)
    manifest_files: dict[str, dict[str, Any]] = {}

    with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            relative = _as_posix_relative(path, project_dir)
            archive.write(path, relative)
            manifest_files[relative] = {
                "bytes": path.stat().st_size,
                "sha256": _sha256_path(path),
            }

    package_sha256 = _sha256_path(package_path)
    manifest = {
        "manifest_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "package": str(package_path),
        "package_sha256": package_sha256,
        "published": False,
        "publication_status": "local_review_package",
        "source_archive_excluded": source_archive_name,
        "large_generated_outputs_excluded": True,
        "file_count": len(manifest_files),
        "files": manifest_files,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {"package": str(package_path), "manifest": str(manifest_path), **manifest}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a local release package.")
    parser.add_argument("--project-dir", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--package-name", default=DEFAULT_PACKAGE_NAME)
    parser.add_argument("--source-archive-name", default=DEFAULT_SOURCE_ARCHIVE)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_release_package(
        project_dir=args.project_dir,
        output_dir=args.output_dir,
        package_name=args.package_name,
        source_archive_name=args.source_archive_name,
    )
    print(f"Wrote {result['package']}")
    print(f"Manifest: {result['manifest']}")
    print(f"Files: {result['file_count']}")
    print(f"Package SHA-256: {result['package_sha256']}")
    print("Published: False")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
