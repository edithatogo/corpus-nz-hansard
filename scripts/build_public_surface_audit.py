"""Build a machine-readable audit of public publication surfaces."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "manifests/public_dataset_release_manifest.json"
DEFAULT_OUTPUT = ROOT / "manifests/public_surface_audit.json"
AUDIT_VERSION = 1


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _surface(
    *,
    surface_id: str,
    label: str,
    status: str,
    url: str | None,
    role: str,
    evidence_source: str,
    claims_allowed: bool,
    follow_up_track: str | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": surface_id,
        "label": label,
        "status": status,
        "url": url,
        "role": role,
        "evidence_source": evidence_source,
        "claims_allowed": claims_allowed,
        "follow_up_track": follow_up_track,
        "notes": notes or [],
    }


def build_public_surface_audit(
    *,
    release_manifest: Path | str = DEFAULT_MANIFEST,
    output: Path | str | None = DEFAULT_OUTPUT,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build and optionally write a public-surface audit ledger."""
    release_manifest_path = Path(release_manifest)
    manifest = _read_json(release_manifest_path)
    publication = manifest["publication"]
    timestamp = generated_at or datetime.now(UTC).isoformat()

    audit = {
        "audit_version": AUDIT_VERSION,
        "generated_at": timestamp,
        "repository": "corpus-nz-hansard",
        "corpus_family_sibling": "corpus-nz-legislation",
        "publication_status": manifest["publication_status"],
        "release_manifest": release_manifest_path.relative_to(ROOT).as_posix(),
        "surfaces": [
            _surface(
                surface_id="github",
                label="GitHub",
                status="active",
                url=publication["github_repository"],
                role="Code, documentation, Actions, issues, and lightweight release assets.",
                evidence_source="GitHub repository API, release API, and release page readbacks.",
                claims_allowed=True,
                notes=[
                    f"Canonical release: {publication['github_release']}",
                    "Large normalized Parquet is hosted on Hugging Face and Zenodo, not GitHub.",
                ],
            ),
            _surface(
                surface_id="huggingface",
                label="Hugging Face",
                status="active",
                url=publication["huggingface_dataset"],
                role="Canonical normalized document-level Parquet dataset host.",
                evidence_source="Hugging Face dataset API and datasets-server viewer readbacks.",
                claims_allowed=True,
                follow_up_track="huggingface_viewer_layout_fix_20260609",
                notes=[
                    "Viewer health is an explicit audit item and must not be inferred from repository visibility alone.",
                    "The dataset is intended to remain public and ungated.",
                ],
            ),
            _surface(
                surface_id="zenodo",
                label="Zenodo",
                status="active",
                url=publication["zenodo_record"],
                role="Immutable citable archive and DOI-bearing snapshot.",
                evidence_source="DOI redirect, Zenodo record page, and Zenodo record API readbacks.",
                claims_allowed=True,
                notes=[
                    f"DOI: {publication['doi']}",
                    f"Concept DOI: {publication['conceptdoi']}",
                    "Publication evidence should rely on DOI redirect, record HTTP 200, state done, and submitted true.",
                ],
            ),
            _surface(
                surface_id="osf_optional",
                label="OSF",
                status="inactive",
                url=None,
                role="Optional future mirror or review-bundle host only after a dedicated policy.",
                evidence_source="Conductor OSF optional mirror policy and public-surface audit evidence.",
                claims_allowed=False,
                follow_up_track="osf_optional_mirror_policy_20260609",
                notes=[
                    "No OSF public surface is currently claimed.",
                    "Do not describe OSF as published or complete until policy, checksums, citation wording, and maintenance ownership are approved.",
                ],
            ),
            _surface(
                surface_id="future_metadata",
                label="Future metadata environments",
                status="planned",
                url=None,
                role="Croissant, RO-Crate, Frictionless, DCAT, PROV-O, and other machine-actionable metadata exports.",
                evidence_source="SOTA metadata packages and RDF linked-data endpoint tracks.",
                claims_allowed=False,
                follow_up_track="sota_metadata_packages_20260609",
                notes=[
                    "Future metadata surfaces must point back to the same GitHub, Hugging Face, and Zenodo authorities.",
                    "Do not claim external metadata publication before validated metadata packages exist.",
                ],
            ),
        ],
    }
    if output is not None:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return audit


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the public-surface audit ledger.")
    parser.add_argument("--release-manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    build_public_surface_audit(release_manifest=args.release_manifest, output=args.output)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
