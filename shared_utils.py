"""Shared utilities for corpus-nz-hansard scripts.

This module is intentionally repo-local so GitHub Actions checkouts do not
depend on a parent workspace helper file.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any


def sha256_bytes(data: bytes) -> str:
    """Return the SHA-256 hex digest of *data*."""
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    """Return the SHA-256 hex digest of the UTF-8 encoding of *text*."""
    return sha256_bytes(text.encode("utf-8"))


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Return the SHA-256 hex digest of the file at *path*."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path, default: Any = None) -> Any:
    """Deserialize JSON from *path*, or return *default* when missing."""
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any, *, sort_keys: bool = True) -> None:
    """Serialize *data* as sorted, indented JSON to *path*."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, sort_keys=sort_keys, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def append_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    """Append rows as JSON Lines to *path* and return the row count."""
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("a", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
            count += 1
    return count


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    """Write rows as JSON Lines to *path* and return the row count."""
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
            count += 1
    return count


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read all JSON Lines from *path*, returning an empty list when missing."""
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def content_sha256(payload: dict[str, Any]) -> str:
    """Compute a stable content-only SHA-256 for manifest comparisons."""
    content_payload = {
        "schema_version": payload.get("schema_version"),
        "record_count": payload.get("record_count"),
        "files": [
            {"path": item["path"], "size_bytes": item["size_bytes"], "sha256": item["sha256"]}
            for item in payload.get("files", [])
        ],
    }
    return sha256_text(json.dumps(content_payload, sort_keys=True, ensure_ascii=False))


def manifest_sha256(payload: dict[str, Any], *, exclude_keys: set[str] | None = None) -> str:
    """Compute a SHA-256 of the manifest payload minus transient keys."""
    excluded = set(exclude_keys or {"generated_at_utc", "manifest_sha256"})
    manifest_payload = {key: value for key, value in payload.items() if key not in excluded}
    return sha256_text(json.dumps(manifest_payload, sort_keys=True, ensure_ascii=False))


def build_change_report(
    previous: dict[str, Any] | None,
    current: dict[str, Any],
) -> dict[str, Any]:
    """Compare two manifests and return added, removed, and changed files."""
    previous_files = {item["path"]: item for item in (previous or {}).get("files", [])}
    current_files = {item["path"]: item for item in current.get("files", [])}

    added = sorted(set(current_files) - set(previous_files))
    removed = sorted(set(previous_files) - set(current_files))
    changed = sorted(
        path
        for path in set(current_files) & set(previous_files)
        if current_files[path].get("sha256") != previous_files[path].get("sha256")
    )

    previous_content = (previous or {}).get("content_sha256") or (previous or {}).get(
        "manifest_sha256"
    )
    current_content = current.get("content_sha256") or current.get("manifest_sha256")

    return {
        "schema_version": "1.0",
        "previous_manifest_sha256": (previous or {}).get("manifest_sha256"),
        "current_manifest_sha256": current.get("manifest_sha256"),
        "previous_content_sha256": previous_content,
        "current_content_sha256": current_content,
        "added": added,
        "removed": removed,
        "changed": changed,
        "has_changes": bool(added or removed or changed or previous_content != current_content),
    }
