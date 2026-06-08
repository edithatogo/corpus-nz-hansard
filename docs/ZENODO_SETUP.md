# Zenodo Setup

Zenodo should be used for an immutable DOI-bearing archive only after the release package and dataset card have been reviewed.

## Required Environment

```powershell
$env:ZENODO_TOKEN = "..."
$env:ZENODO_API_URL = "https://zenodo.org/api"
$env:ARCHIVE_CREATORS_JSON = '[{"name":"Maintainer"}]'
```

Use `https://sandbox.zenodo.org/api` for dry runs.

For GitHub Actions archive builds, configure repository secrets:

- `SOURCE_ARCHIVE_URL`: private/downloadable URL for `2024-09-06 Hansard Extract from DocumentsDB.zip`
- `HF_TOKEN`: required when `SOURCE_ARCHIVE_URL` points to a private Hugging Face source archive
- `ZENODO_TOKEN`: required only when `upload_to_zenodo=true`
- `ARCHIVE_CREATORS_JSON`: required only when `upload_to_zenodo=true`
- `ZENODO_DEPOSITION_ID`: optional existing draft deposition identifier

The workflow builds and uploads a GitHub Actions artifact for review by default. Set `upload_to_zenodo=true` to upload the archive and manifest to a Zenodo draft. It does not publish the draft.

`SOURCE_ARCHIVE_URL` downloads use `HF_TOKEN` when present and are verified against SHA-256 `2ac02c0042a4fb291fd8e401db5f469de2539e42c9e07c4c72eca16be9a17299` before the archive build continues.

Check GitHub Actions readiness before uploading a Zenodo draft:

```powershell
gh workflow run publication_readiness.yml --repo edithatogo/corpus-nz-hansard -f target=zenodo
```

## Archive Build

Build a local archive staged for Zenodo:

```powershell
python scripts\build_zenodo_archive.py --output-dir generated\zenodo
```

The archive includes:

- tracked code, docs, schemas, tests, and manifests;
- generated Parquet;
- release metadata.

It excludes the source ZIP unless a redistribution decision is made later.

## Upload Boundary

Zenodo publication must be explicit. Draft creation/upload is not the same as publication, and no publication should be claimed until a DOI exists and is verified.

Draft upload command:

```powershell
python scripts\upload_zenodo_archive.py --archive generated\zenodo\nz-hansard-corpus-0.1.0-review.20260603.tar.gz --manifest generated\zenodo\nz-hansard-corpus-0.1.0-review.20260603.manifest.json
```

The upload script rejects `--publish`; publication should happen as a separate reviewed step.
