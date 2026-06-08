# Publication Status

Last verified: 2026-06-07

## Completed

- GitHub repository created: `https://github.com/edithatogo/corpus-nz-hansard`
- Main branch pushed at commit `44e8121`.
- GitHub Actions tests passed.
- GitHub review prerelease created: `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0-review.20260603`
- Review release assets uploaded:
  - `nz-hansard-corpus-0.1.0-review.20260603.zip`
  - `nz-hansard-corpus-0.1.0-review.20260603.manifest.json`

## Prepared Locally

- Hugging Face staging folder: `generated/huggingface`
- Zenodo archive: `generated/zenodo/nz-hansard-corpus-0.1.0-review.20260603.tar.gz`
- Zenodo archive SHA-256: `63a7182495b4a0c45d57caf288f279ef1c92ffd6fa78b497856445cbfe6d1d00`

## Blocked

- Hugging Face upload is blocked by missing/invalid Hugging Face authentication. The attempted dataset repo creation for `edithatogo/nz-hansard-corpus` returned `401 Unauthorized`.
- Hugging Face and Zenodo GitHub workflows also need `SOURCE_ARCHIVE_URL` because the source ZIP is intentionally ignored.
- Zenodo draft upload is blocked because `ZENODO_TOKEN` and `ARCHIVE_CREATORS_JSON` are not configured. The workflow can build a GitHub Actions artifact without those secrets and can upload a draft when `upload_to_zenodo=true`.

## Claim Boundary

The GitHub review prerelease is public. The full dataset has not been published to Hugging Face or Zenodo, and no DOI has been minted.
