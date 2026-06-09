# Evidence: Public Surface Audit Evidence

## Initial Evidence

Status: opened on 2026-06-09.

Evidence should capture current and target public-surface behaviour across GitHub, Hugging Face, Zenodo, OSF, and future metadata environments.

## Hugging Face Surface - 2026-06-09

Read-only live checks against `edithatogo/nz-hansard-corpus` show:

- Repository access is public: `private: false`, `gated: false`.
- The staged public surface includes canonical `data/hansard.parquet` plus downloadable `docs/`, `manifests/`, and `schemas/`.
- The Hugging Face viewer currently fails because datasets-server appears to select the manifest JSON as a `validation` split and raises a cast error for manifest-style fields.
- `splits` returns only `validation`; `first-rows` for that split returns HTTP 500; `parquet` discovery returns no Parquet files.

Follow-up is tracked in `huggingface_viewer_layout_fix_20260609`: constrain data-files/config detection so `data/hansard.parquet` is the viewer dataset source, then republish and verify with datasets-server.

## GitHub Surface - 2026-06-09

Read-only live checks against `edithatogo/corpus-nz-hansard` show:

- The repository is public.
- Default branch is `main`.
- Repository homepage points to `https://doi.org/10.5281/zenodo.20595194`.
- Latest release is `v0.1.0`, published on `2026-06-08T13:34:29Z`, and is not a draft or prerelease.
- Release assets include `nz-hansard-corpus-0.1.0.zip` and `nz-hansard-corpus-0.1.0.manifest.json`.

Verified with GitHub CLI/API reads and the release page at `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0`.

## Zenodo Surface - 2026-06-09

Read-only live checks against `https://doi.org/10.5281/zenodo.20595194` and `https://zenodo.org/records/20595194` show:

- DOI redirects to the Zenodo record.
- Zenodo record page returns HTTP 200.
- Zenodo API reports title `NZ Hansard Corpus`, DOI `10.5281/zenodo.20595194`, `state: done`, `submitted: true`, and version `0.1.0`.
- Related identifiers link back to the GitHub repository, GitHub release, and Hugging Face dataset.
- Record headers expose items for `nz-hansard-corpus-0.1.0.manifest.json` and `nz-hansard-corpus-0.1.0.tar.gz`.

Audit note: Zenodo API fields such as `published` and `html` may be null even for the live record, so publication evidence should rely on DOI redirect, record-page HTTP 200, `state: done`, `submitted: true`, and related identifiers.

## OSF Surface - 2026-06-09

No OSF publication surface is currently claimed for `corpus-nz-hansard`.

Current policy status:

- GitHub, Hugging Face, and Zenodo are the active public surfaces for the document-level release.
- OSF is an optional future mirror or review-bundle host only after a dedicated policy decides scope, checksums, citation wording, version mapping, and maintenance responsibility.
- Until that policy exists, release/readiness claims should not describe OSF as published or complete.

Follow-up is tracked in `osf_optional_mirror_policy_20260609`.

## Public Surface Audit Ledger - 2026-06-10

Status: complete.

Repo-side audit implementation:

- Added `manifests/public_surface_audit.json` as the machine-readable public-surface ledger.
- Added `schemas/public_surface_audit.schema.json` for the ledger contract.
- Added `scripts/build_public_surface_audit.py` to rebuild the ledger from `manifests/public_dataset_release_manifest.json`.
- Added `scripts/check_public_surface_audit.py` to validate ledger schema, required surfaces, URL agreement with the public release manifest, OSF/future-metadata claim boundaries, and evidence/documentation coverage.
- Added `tests/test_build_public_surface_audit.py`.
- Added `docs/public-surface-audit.md` to document active GitHub/Hugging Face/Zenodo surfaces, inactive OSF status, future metadata status, migration constraints, and the `zenodraft` requirement for future Zenodo draft/archive workflow changes.
- Added `public-surface-audit` to `Makefile`, `.github/workflows/quality.yml`, `docs/quality-gate.md`, and `scripts/check_quality_gate.py`.

Ledger surface decisions:

- `github`: active; public claims allowed; authority URL is `https://github.com/edithatogo/corpus-nz-hansard`.
- `huggingface`: active; public claims allowed; authority URL is `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`; viewer health remains explicitly tracked by `huggingface_viewer_layout_fix_20260609`.
- `zenodo`: active; public claims allowed; authority URL is `https://zenodo.org/records/20595194`; DOI is `10.5281/zenodo.20595194`.
- `osf_optional`: inactive; public publication claims not allowed; follow-up track is `osf_optional_mirror_policy_20260609`.
- `future_metadata`: planned; public publication claims not allowed; follow-up track is `sota_metadata_packages_20260609`.

Current read-only live checks:

- GitHub repository API: `private=false`, default branch `main`, homepage `https://doi.org/10.5281/zenodo.20595194`.
- GitHub release API for `v0.1.0`: `draft=false`, `prerelease=false`, assets `nz-hansard-corpus-0.1.0.manifest.json` and `nz-hansard-corpus-0.1.0.zip`.
- Hugging Face dataset API: `private=false`, `gated=false`, id `edithatogo/nz-hansard-corpus`, revision `4d7ae9d560787c50588dfbdefad509165bc779d1`.
- Hugging Face datasets-server splits: `default:train`.
- Zenodo record API: DOI `10.5281/zenodo.20595194`, `state=done`, `submitted=true`, version `0.1.0`.
- DOI request for `https://doi.org/10.5281/zenodo.20595194` returned HTTP 200.

Validation:

- Red phase: `python -m unittest tests.test_build_public_surface_audit` failed before `scripts/build_public_surface_audit.py` existed.
- `python -m unittest tests.test_build_public_surface_audit tests.test_check_quality_gate` passed.
- `python scripts\check_public_surface_audit.py` passed.
- `make quality` passed with uv lock check, frozen sync, Ruff, Ruff format, ty strict type check, typos, zizmor, taplo, actionlint, quality configuration, release provenance policy, release version consistency, public-surface audit, and 48 unit tests.
