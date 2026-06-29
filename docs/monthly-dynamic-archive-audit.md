# Monthly Dynamic Archive Audit

## Current Publication Surfaces

The repository currently has separate manual publication workflows:

- `.github/workflows/huggingface_publish.yml` rebuilds source inventory, schema discovery, normalized Parquet, validation reports, stages `generated/huggingface`, and uploads the staged folder to Hugging Face.
- `.github/workflows/zenodo_archive.yml` rebuilds source inventory, schema discovery, normalized Parquet, validation reports, builds `generated/zenodo/nz-hansard-corpus-<version>.tar.gz`, optionally uploads a Zenodo draft, uploads GitHub workflow artifacts, and attests archive provenance.
- `.github/workflows/zenodo_publish.yml` publishes an already prepared Zenodo draft through the protected `zenodo-production-publish` environment.
- `.github/workflows/publication_readiness.yml` checks required publication secrets and source archive access.

These workflows are manual-only. None currently runs on a monthly `schedule` event or records one cross-surface monthly release evidence manifest.

## Current Source And Build Inputs

- Governed source archive input: `SOURCE_ARCHIVE_URL`.
- Source archive local filename: `2024-09-06 Hansard Extract from DocumentsDB.zip`.
- Hugging Face token: `HF_TOKEN`, used both for publication and for protected source-archive download when the source archive URL requires it.
- Zenodo token: `ZENODO_TOKEN`.
- Zenodo creators metadata: `ARCHIVE_CREATORS_JSON`.
- Existing Zenodo record defaults are currently oriented around `0.1.0` and record `20591997` for new-version creation in the draft workflow.

## Existing Generated Outputs

The publication workflows rebuild or stage these outputs:

- `manifests/source_inventory.json`
- `manifests/schema_discovery.json`
- `generated/parquet/hansard.parquet`
- `manifests/normalization_manifest.json`
- `manifests/normalization_validation.json`
- `manifests/record_schema_validation.json`
- `generated/huggingface/`
- `generated/zenodo/nz-hansard-corpus-<version>.tar.gz`
- `generated/zenodo/nz-hansard-corpus-<version>.manifest.json`

## Monthly Archive Artifact Set

Each monthly archive should include:

- Canonical normalized Parquet: `data/hansard.parquet`.
- Repository documentation: `docs/`.
- Machine-readable manifests: `manifests/`.
- Machine-readable schemas: `schemas/`.
- Release and citation files: `README.md`, `DATASET_CARD.md`, `CITATION.cff`, `LICENSE`, `NOTICE.md`, `RELEASE_NOTES.md`, and `VERSION`.
- Reproducibility code and tests needed to inspect the release: `scripts/` and `tests/`.
- Conductor release context: `conductor/`.
- Archive manifest with SHA-256 hashes, byte sizes, row counts, publication status, and source archive exclusion status.

The source ZIP must remain excluded from committed files and public release artifacts unless a later rights-specific review approves publishing it.

## Gaps To Close

- Add a scheduled monthly GitHub Actions entrypoint.
- Ensure one dynamic workflow can perform dry-run validation, Hugging Face publication, Zenodo draft upload, and protected Zenodo publish handoff.
- Capture Hugging Face revision evidence after upload.
- Capture Zenodo draft/new-version metadata after upload.
- Add one machine-readable monthly evidence manifest that ties together GitHub run metadata, archive hashes, row counts, Hugging Face revision, Zenodo draft or DOI details, and rights boundaries.
- Add checker and tests that fail if the schedule, secrets checks, protected publication gate, or evidence fields are missing.
