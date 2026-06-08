# Zenodo Setup

Zenodo should be used for an immutable DOI-bearing archive only after the release package and dataset card have been reviewed.

## Required Environment

```powershell
$env:ZENODO_TOKEN = "..."
$env:ZENODO_API_URL = "https://zenodo.org/api"
$env:ARCHIVE_CREATORS_JSON = '[{"name":"Maintainer"}]'
```

Use `https://sandbox.zenodo.org/api` for dry runs.

For GitHub Actions archive builds, configure:

- `SOURCE_ARCHIVE_URL`: private/downloadable URL for `2024-09-06 Hansard Extract from DocumentsDB.zip`

The current workflow builds and uploads a GitHub Actions artifact for review. It does not publish to Zenodo.

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
