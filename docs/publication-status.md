# Publication Status

Last verified: 2026-06-08

## Completed

- GitHub repository created: `https://github.com/edithatogo/corpus-nz-hansard`
- Main branch pushed at commit `368dacd`.
- GitHub Actions tests passed.
- GitHub review prerelease created: `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0-review.20260603`
- Review release assets uploaded:
  - `nz-hansard-corpus-0.1.0-review.20260603.zip`
  - `nz-hansard-corpus-0.1.0-review.20260603.manifest.json`
- GitHub repository secrets configured for publication workflows:
  - `HF_TOKEN`
  - `SOURCE_ARCHIVE_URL`
  - `ZENODO_TOKEN`
  - `ARCHIVE_CREATORS_JSON`
- Publication readiness workflow passed: `https://github.com/edithatogo/corpus-nz-hansard/actions/runs/27128195716`
- Hugging Face dataset published: `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`
- Hugging Face publish workflow passed: `https://github.com/edithatogo/corpus-nz-hansard/actions/runs/27130787565`
- Hugging Face remote files verified:
  - `data/hansard.parquet`
  - `manifests/`
  - `schemas/hansard_record.schema.json`
  - dataset card and documentation
- Zenodo deposition created: `https://zenodo.org/deposit/20591997`
- Zenodo archive workflow passed: `https://github.com/edithatogo/corpus-nz-hansard/actions/runs/27131023973`
- Zenodo draft files uploaded:
  - `nz-hansard-corpus-0.1.0-review.20260603.tar.gz`
  - `nz-hansard-corpus-0.1.0-review.20260603.manifest.json`
- Zenodo draft upload was initially verified from workflow response as `unsubmitted`, `published: false`.
- The same Zenodo deposition was later published by manual approval.
- Zenodo record published and verified: `https://zenodo.org/records/20591997`
- DOI resolves: `https://doi.org/10.5281/zenodo.20591997`
- Zenodo API status verified: `published`, `state: done`, `submitted: true`.
- Zenodo public files verified:
  - `nz-hansard-corpus-0.1.0-review.20260603.tar.gz`
  - `nz-hansard-corpus-0.1.0-review.20260603.manifest.json`

## Prepared Locally

- Hugging Face staging folder: `generated/huggingface`
- Zenodo archive: `generated/zenodo/nz-hansard-corpus-0.1.0-review.20260603.tar.gz`
- Zenodo archive SHA-256: `63a7182495b4a0c45d57caf288f279ef1c92ffd6fa78b497856445cbfe6d1d00`

## Initial Distribution Policy

- The source ZIP is not redistributed by default.
- Hugging Face is the intended host for the normalized document-level Parquet dataset.
- DuckDB and SQLite search outputs remain regenerated/local convenience artifacts by default.
- Non-authoritative speech-turn candidates are excluded from the initial public dataset.

## Remaining

- Review `DATASET_CARD.md` and `docs/licensing-and-provenance.md`.
- Confirm no official endorsement is implied.
- Confirm limitations around party, member identity, and speech-turn segmentation remain visible.
- Keep Hugging Face and GitHub release metadata synchronized with the Zenodo DOI.
- Keep source ZIP redistribution excluded unless a later explicit redistribution decision changes that policy.

## Readiness Check

Run this before dispatching upload workflows:

```powershell
python scripts/check_publication_readiness.py
```

The check reports whether local environment variables for Hugging Face and Zenodo publication are present without printing secret values. A nonzero exit means at least one selected publication target is not ready.

The same check is available in GitHub Actions:

```powershell
gh workflow run publication_readiness.yml --repo edithatogo/corpus-nz-hansard -f target=all
```

## Claim Boundary

The GitHub review prerelease, Hugging Face dataset, and Zenodo DOI record are public. The source ZIP is not redistributed in public dataset artifacts.
