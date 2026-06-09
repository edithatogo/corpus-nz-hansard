# Evidence: SOTA Metadata Packages

## Initial Evidence

Status: opened on 2026-06-09.

Evidence should capture current and target public-surface behaviour across GitHub, Hugging Face, Zenodo, OSF, and future metadata environments.

## Current State

- Active public release metadata already exists in `manifests/public_dataset_release_manifest.json`, `manifests/public_surface_audit.json`, `.zenodo.json`, `CITATION.cff`, `DATASET_CARD.md`, and `schemas/hansard_record.schema.json`.
- GitHub, Hugging Face, and Zenodo are active public surfaces for release `0.1.0`.
- OSF remains optional and inactive.
- Croissant, RO-Crate, Frictionless, DCAT, and PROV-O package files are not yet generated release artifacts.

## Target State

- Added `manifests/metadata_packages_manifest.json` as the metadata-package contract for Croissant, RO-Crate, Frictionless Data Package, DCAT, and PROV-O.
- Added `schemas/metadata_packages_manifest.schema.json` for the contract shape.
- Added `docs/sota-metadata-packages.md` as the human-readable package policy and migration note.
- Added `scripts/check_metadata_packages.py` to validate package IDs, source-manifest references, active-public-surface URLs, checksum policy, planned output paths, documentation coverage, and publication-claim boundaries.
- Added `tests/test_metadata_packages.py` for focused validation.

## Public Surface Implications

- GitHub: future generated package files may be published from `generated/metadata/` once checksums and package validators are added.
- Hugging Face: Croissant and Frictionless metadata may describe the hosted `default/train` dataset once generated.
- Zenodo: future package files must follow the existing sandbox-first, draft-update-only, protected-production-publish policy.
- OSF: remains null in the metadata-package manifest until the optional mirror track lands.
- Future metadata environments: publication claims remain disabled until generated files, checksums, and package-specific validators exist.

## Remaining Blockers

- Package exporters are not yet implemented.
- Generated package files under `generated/metadata/` do not yet exist.
- Package-specific validators for Croissant, RO-Crate, Frictionless, DCAT, and PROV-O are not yet wired into shared quality gates.
- This worker did not edit `conductor/tracks.md`, `Makefile`, CI, or shared quality-gate files by ownership instruction.

## Focused Validation

- Pre-implementation gap: no metadata-package manifest, checker, or focused test existed for this track.
- `python -m unittest tests.test_metadata_packages` passed.
- `python scripts\check_metadata_packages.py` passed.

## Coordination Completion - 2026-06-10

Central integration completed:

- Added shared quality-gate wiring for `python scripts\check_metadata_packages.py`.
- Registered this track as blocked in `conductor/tracks.md`.
- Blocker remains real package generation: Croissant, RO-Crate, Frictionless, DCAT, and PROV-O package files, checksums, and package-specific validators do not yet exist.
