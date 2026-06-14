"""Download caching and incremental update logic for select committee reports."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


@dataclass
class CacheManifest:
    """Tracks which reports have been downloaded and their integrity metadata."""

    version: int = 1
    entries: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"version": self.version, "entries": self.entries}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CacheManifest:
        return cls(
            version=data.get("version", 1),
            entries=data.get("entries", {}),
        )


def load_manifest(path: Path | str) -> CacheManifest:
    """Load a cache manifest from a JSON file.

    Returns an empty ``CacheManifest`` if the file does not exist
    or is corrupt.
    """
    path = Path(path)
    if not path.exists():
        return CacheManifest()

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return CacheManifest.from_dict(data)
    except (json.JSONDecodeError, KeyError, TypeError):
        return CacheManifest()


def save_manifest(manifest: CacheManifest, path: Path | str) -> None:
    """Save a cache manifest to a JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def is_cached(manifest: CacheManifest, report_id: str) -> bool:
    """Check if a report ID is present in the cache manifest."""
    return report_id in manifest.entries


def mark_cached(
    manifest: CacheManifest,
    report_id: str,
    *,
    url: str,
    file_hash: str,
    size: int,
    fmt: str,
) -> None:
    """Record a report as cached in the manifest."""
    manifest.entries[report_id] = {
        "url": url,
        "sha256": file_hash,
        "size": size,
        "format": fmt,
        "cached_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
    }


def compute_file_hash(path: Path | str) -> str:
    """Compute SHA-256 hash of a file. Returns empty string if file not found."""
    path = Path(path)
    if not path.exists():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def get_stale_entries(
    manifest: CacheManifest,
    max_age_days: int = 7,
    reference_date: str | None = None,
) -> list[str]:
    """Return a list of report IDs whose cache is older than *max_age_days*.

    Parameters
    ----------
    manifest:
        The cache manifest to check.
    max_age_days:
        Maximum allowed age in days before an entry is considered stale.
    reference_date:
        ISO date string for "now" (defaults to today UTC).

    Returns
    -------
    list of str
        Report IDs that are stale and should be re-fetched.
    """
    if reference_date:
        now = datetime.strptime(reference_date, "%Y-%m-%d")
    else:
        now = datetime.utcnow()

    stale: list[str] = []
    for report_id, info in manifest.entries.items():
        cached_at = info.get("cached_at")
        if not cached_at:
            continue
        try:
            cache_time = datetime.strptime(cached_at, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
        age = now - cache_time
        if age > timedelta(days=max_age_days):
            stale.append(report_id)
    return stale
