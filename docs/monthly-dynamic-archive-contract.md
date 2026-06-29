# Monthly Dynamic Archive Publication Contract

## Purpose

This contract defines the monthly dynamic publication surface for `corpus-nz-hansard`. It governs the archive rebuilt by GitHub Actions, the Hugging Face dataset update, the Zenodo draft/new-version upload, and the evidence that ties those surfaces together.

## Cadence

- Scheduled cadence: monthly.
- Required manual trigger: `workflow_dispatch`.
- Scheduled runs must be able to run as validation-only dry runs.
- Network publication steps must run only when their explicit publish inputs or scheduled defaults permit them and required secrets are present.

## Source Inputs

Required inputs:

- `SOURCE_ARCHIVE_URL`: governed source archive location.
- `HF_TOKEN`: Hugging Face token, also used for protected source archive downloads when needed.
- `ZENODO_TOKEN`: Zenodo draft/upload/publish token.
- `ARCHIVE_CREATORS_JSON`: Zenodo creator metadata JSON.
- Repository commit SHA and GitHub run metadata from the workflow environment.

Optional inputs:

- Hugging Face dataset repo ID, default `edithatogo/nz-hansard-corpus`.
- Zenodo API URL, default `https://zenodo.org/api`.
- Existing Zenodo record ID for new-version creation.
- Release version or monthly version label.

## Generated Outputs

The monthly workflow must rebuild or stage:

- `manifests/source_inventory.json`
- `manifests/schema_discovery.json`
- `generated/parquet/hansard.parquet`
- `manifests/normalization_manifest.json`
- `manifests/normalization_validation.json`
- `manifests/record_schema_validation.json`
- `generated/huggingface/`
- `generated/zenodo/nz-hansard-corpus-<version>.tar.gz`
- `generated/zenodo/nz-hansard-corpus-<version>.manifest.json`
- `manifests/monthly_dynamic_archive_publication_evidence.json`

## Public Surfaces

Hugging Face:

- Target repo: `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus` unless overridden.
- Must include `data/hansard.parquet`.
- Must include supporting `docs/`, `manifests/`, `schemas/`, and dataset card metadata.
- Must record the resulting revision SHA or URL in evidence.

Zenodo:

- Target: a new draft or new version derived from the latest governed Zenodo record.
- Must upload the full monthly tarball and matching manifest.
- Must not publish automatically outside the protected `zenodo-production-publish` environment.
- Must record draft ID, draft URL, or DOI/version URL when available.

GitHub:

- Must record workflow run ID, run URL, commit SHA, branch/ref, and artifact names.
- Must upload generated release archive artifacts for dry-run and review.

## Evidence Manifest Fields

The monthly evidence manifest must include:

- `manifest_version`
- `track_id`
- `generated_at`
- `run`
- `source`
- `archive`
- `huggingface`
- `zenodo`
- `validation`
- `rights_boundary`

The evidence must include archive SHA-256 hashes, manifest hashes, row counts, source archive exclusion status, publication mode, and public URLs or draft identifiers when available.

## Rights-Safe Exclusions

- The source ZIP is not committed.
- The source ZIP is not included in public monthly artifacts.
- Publication does not imply New Zealand Parliament endorsement.
- Monthly publication does not claim full historical completeness beyond the governed DocumentsDB source archive and validated authority evidence.

## Failure Policy

- Missing required secrets fail closed before publication steps.
- Failed validation prevents Hugging Face upload, Zenodo draft upload, and Zenodo publish handoff.
- Zenodo draft upload and protected Zenodo publish remain separate steps.
- Dependency-update PRs must never publish datasets or Zenodo records.
