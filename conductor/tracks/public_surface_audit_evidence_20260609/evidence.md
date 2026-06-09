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
