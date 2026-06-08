# Publication Status

Last verified: 2026-06-08

## Completed

- GitHub repository created: `https://github.com/edithatogo/corpus-nz-hansard`
- GitHub repository secrets configured for publication workflows:
  - `HF_TOKEN`
  - `SOURCE_ARCHIVE_URL`
  - `ZENODO_TOKEN`
  - `ARCHIVE_CREATORS_JSON`
- Hugging Face dataset published: `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`
- Zenodo concept DOI created: `https://doi.org/10.5281/zenodo.20591996`
- Repository `LICENSE` and `NOTICE.md` added for original repository materials and source provenance boundaries.

## Final Document-Level Release

- Version: `0.1.0`
- GitHub release target: `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0`
- Hugging Face dataset target: `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`
- Zenodo concept DOI: `https://doi.org/10.5281/zenodo.20591996`

This is the canonical document-level dataset release. Member identity resolution, party attribution, and authoritative speech-turn segmentation are intentionally out of scope for this release and should be handled as later derived-data releases.

## Prepared Locally

- Hugging Face staging folder: `generated/huggingface`
- Zenodo archive: `generated/zenodo/nz-hansard-corpus-0.1.0.tar.gz`

## Distribution Policy

- The source ZIP is not redistributed by default.
- Hugging Face is the intended host for the normalized document-level Parquet dataset.
- Zenodo stores the citable archive and DOI.
- DuckDB and SQLite search outputs remain regenerated/local convenience artifacts by default.
- Non-authoritative speech-turn candidates are excluded from the canonical document-level dataset.

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

The GitHub release, Hugging Face dataset, and Zenodo DOI record are public release surfaces. The source ZIP is not redistributed in public dataset artifacts.
