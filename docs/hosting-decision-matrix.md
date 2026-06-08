# Hosting Decision Matrix

## Status

GitHub has been selected for code, schemas, tests, docs, manifests, and the lightweight review package.

- Repository: `https://github.com/edithatogo/corpus-nz-hansard`
- Review prerelease: `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0-review.20260603`
- Full dataset publication has not occurred.
- Hugging Face upload is blocked until `HF_TOKEN` is available.
- Zenodo draft/archive upload is blocked until `ZENODO_TOKEN` and creator metadata are available.

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
2. Use Hugging Face Datasets for browsable Parquet once `HF_TOKEN` is available.
3. Use Zenodo for DOI/archive once `ZENODO_TOKEN` and creator metadata are available.
4. Keep DuckDB as regenerated local output unless a reviewer explicitly needs a prebuilt database.

## Decisions Still Needed

- Whether Hugging Face should publish `generated/huggingface/data/hansard.parquet` directly.
- Whether Zenodo should use the staged archive in `generated/zenodo/`.
- Whether source ZIP can be redistributed.
- Whether DuckDB is included in any public dataset release or regenerated.
