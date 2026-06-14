"""Canonical ID and URI helpers for NZ Hansard derived artifacts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

# Ensure workspace root is on sys.path so we can import shared utilities
_WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
if str(_WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(_WORKSPACE_ROOT))

import shared_utils  # noqa: E402

NAMESPACE = "https://w3id.org/nz-hansard/"
ID_PATTERN = re.compile(r"^nzhc-[a-z][a-z0-9-]*-[a-f0-9]{16}$")
SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")
CLASS_SLUG_ALIASES = {"neutral-component": "component"}


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    if not slug or not SLUG_PATTERN.fullmatch(slug):
        raise ValueError(f"invalid canonical slug source: {value!r}")
    return slug


def _digest(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return shared_utils.sha256_text(encoded)[:16]


def canonical_id(artifact_class: str, payload: dict[str, Any]) -> str:
    """Return a deterministic corpus-local ID for a validated payload."""
    slug = CLASS_SLUG_ALIASES.get(artifact_class, _slug(artifact_class))
    return f"nzhc-{slug}-{_digest(payload)}"


def canonical_uri(kind: str, identifier: str) -> str:
    """Return the planned canonical URI for an ID in the NZ Hansard namespace."""
    kind_slug = _slug(kind)
    if not ID_PATTERN.fullmatch(identifier):
        raise ValueError(f"identifier does not match canonical ID pattern: {identifier!r}")
    return f"{NAMESPACE}{kind_slug}/{identifier}"


def component_payload(
    *,
    release_version: str,
    component_type: str,
    source_stable_id: str,
    local_key: str,
    validation_manifest: str,
) -> dict[str, str]:
    """Build the required payload for neutral component IDs."""
    return {
        "release_version": release_version,
        "component_type": component_type,
        "source_stable_id": source_stable_id,
        "local_key": local_key,
        "validation_manifest": validation_manifest,
    }
