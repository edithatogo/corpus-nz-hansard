# Evidence: SOTA Metadata Packages

## Initial Evidence

Status: opened on 2026-06-09.

Evidence should capture current and target public-surface behaviour across GitHub, Hugging Face, Zenodo, OSF, and future metadata environments.

## Current State

- Active public release metadata already exists in `manifests/public_dataset_release_manifest.json`, `manifests/public_surface_audit.json`, `.zenodo.json`, `CITATION.cff`, `DATASET_CARD.md`, and `schemas/hansard_record.schema.json`.
- GitHub, Hugging Face, and Zenodo are active public surfaces for release `0.1.0`.
- OSF remains optional and inactive.
- Croissant, RO-Crate, Frictionless, DCAT, and PROV-O package files are generated local release artifacts under `generated/metadata/`.

## Target State

- Added `manifests/metadata_packages_manifest.json` as the metadata-package contract for Croissant, RO-Crate, Frictionless Data Package, DCAT, and PROV-O.
- Added `schemas/metadata_packages_manifest.schema.json` for the contract shape.
- Added `docs/sota-metadata-packages.md` as the human-readable package policy and migration note.
- Added `scripts/check_metadata_packages.py` to validate package IDs, source-manifest references, active-public-surface URLs, checksum policy, planned output paths, documentation coverage, and publication-claim boundaries.
- Added `tests/test_metadata_packages.py` for focused validation.
- Added `scripts/build_metadata_packages.py` to generate Croissant, RO-Crate, Frictionless, DCAT, and PROV-O outputs from the public release manifest, `.zenodo.json`, and the record schema.

## Public Surface Implications

- GitHub: generated package files can be published from `generated/metadata/` once included in a normal release upload.
- Hugging Face: Croissant and Frictionless metadata may describe the hosted `default/train` dataset once generated.
- Zenodo: future package files must follow the existing sandbox-first, draft-update-only, protected-production-publish policy.
- OSF: remains null in the metadata-package manifest until the optional mirror track lands.
- Future metadata environments: publication claims remain disabled for any surface until generated files are uploaded to that surface and read back.

## Remaining Blockers

- Zenodo Sandbox upload/update/readback proof is now recorded in `manifests/zenodo_sandbox_proof.json` under `zenodo_rights_metadata_and_zenodraft_workflow_20260609`.

## Focused Validation

- Pre-implementation gap: no metadata-package manifest, checker, or focused test existed for this track.
- `python -m unittest tests.test_metadata_packages` passed.
- `python scripts\check_metadata_packages.py` passed.

## Coordination Completion - 2026-06-10

Central integration completed:

- Added shared quality-gate wiring for `python scripts\check_metadata_packages.py`.
- Registered this track as blocked in `conductor/tracks.md`.
- Blocker remains real package generation: Croissant, RO-Crate, Frictionless, DCAT, and PROV-O package files, checksums, and package-specific validators do not yet exist.

## Blocker Reduction - 2026-06-10

Repo-side metadata package blockers were addressed:

- Added deterministic metadata generation via `python scripts\build_metadata_packages.py`.
- Generated `generated/metadata/croissant.jsonld`, `generated/metadata/ro-crate-metadata.json`, `generated/metadata/datapackage.json`, `generated/metadata/dcat.ttl`, and `generated/metadata/prov-o.ttl`.
- Updated `manifests/metadata_packages_manifest.json` to mark all five packages `generated` and record SHA-256 checksums.
- Strengthened `scripts/check_metadata_packages.py` and `tests/test_metadata_packages.py` so the quality gate verifies output existence, checksums, JSON package structure, Turtle snippets, and generator provenance.

Focused validation after these changes:

- `python scripts\build_metadata_packages.py`
- `python scripts\check_metadata_packages.py`
- `python -m unittest tests.test_metadata_packages`

No metadata-package repo-side blocker remains. Live Zenodo Sandbox proof still requires `ZENODO_SANDBOX_TOKEN` and approval to create/update sandbox deposition state, and remains tracked by `zenodo_rights_metadata_and_zenodraft_workflow_20260609`.
