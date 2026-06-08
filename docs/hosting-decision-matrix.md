# Hosting Decision Matrix

## Status

GitHub has been selected for code, schemas, tests, docs, manifests, and the lightweight review package.

- Repository: `https://github.com/edithatogo/corpus-nz-hansard`
- Review prerelease: `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0-review.20260603`
- Hugging Face dataset publication has occurred; Zenodo publication has not.
- Hugging Face publication is complete at `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`.
- Zenodo draft/archive upload is complete at `https://zenodo.org/deposit/20591997`.
- Zenodo publication remains gated on explicit approval.

## Options

| Option | Strengths | Tradeoffs | Fit |
| --- | --- | --- | --- |
| Hugging Face Datasets | Good dataset card support, discoverability, Parquet-friendly. | Needs account/token and explicit dataset repo decision. | Strong candidate for public data release. |
| Zenodo | DOI support, archival citation, versioned deposits. | Less ergonomic for iterative dataset browsing. | Strong candidate for citable release. |
| OSF | Research-project friendly, good for review bundles. | Less optimized for dataset browsing/querying. | Good review/handoff option. |
| GitHub Releases | Convenient for code-adjacent artifacts. | Large data and long-term dataset discovery are weaker. | Suitable for lightweight review package only. |
| Local only | No external dependency. | Not a public release. | Superseded for code/review package by GitHub; still true for generated full dataset artifacts. |

## Recommended Path

1. Keep GitHub as the code and lightweight review-package host.
2. Use Hugging Face Datasets for browsable document-level Parquet.
3. Use Zenodo for DOI/archive after explicit publication approval.
4. Keep DuckDB and SQLite search as regenerated local outputs unless a reviewer explicitly needs prebuilt database files.
5. Do not redistribute the source ZIP by default; use `SOURCE_ARCHIVE_URL` plus SHA-256 verification for trusted rebuilds.

## Initial Distribution Decisions

- Hugging Face publishes `generated/huggingface/data/hansard.parquet` directly after credentialed publication.
- Zenodo uses the staged archive in `generated/zenodo/`; draft upload is complete, publication is pending approval.
- The source ZIP is not redistributed by default.
- DuckDB and search SQLite are regenerated artifacts, not initial public dataset payloads.
- Non-authoritative speech-turn candidates are excluded from the initial public dataset.
