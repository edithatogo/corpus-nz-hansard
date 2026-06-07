# Hosting Decision Matrix

## Status

No hosting target has been selected and no upload has occurred.

## Options

| Option | Strengths | Tradeoffs | Fit |
| --- | --- | --- | --- |
| Hugging Face Datasets | Good dataset card support, discoverability, Parquet-friendly. | Needs account/token and explicit dataset repo decision. | Strong candidate for public data release. |
| Zenodo | DOI support, archival citation, versioned deposits. | Less ergonomic for iterative dataset browsing. | Strong candidate for citable release. |
| OSF | Research-project friendly, good for review bundles. | Less optimized for dataset browsing/querying. | Good review/handoff option. |
| GitHub Releases | Convenient for code-adjacent artifacts. | Large data and long-term dataset discovery are weaker. | Suitable for lightweight review package only. |
| Local only | No external dependency. | Not a public release. | Current state. |

## Recommended Path

1. Keep current state local-only for review.
2. Use Hugging Face Datasets for browsable Parquet if public release is approved.
3. Use Zenodo for DOI/archive if a citable release is required.
4. Keep DuckDB as regenerated local output unless a reviewer explicitly needs a prebuilt database.

## Decisions Still Needed

- Hosting target.
- Dataset versioning scheme beyond `0.1.0-review.20260603`.
- Whether source ZIP can be redistributed.
- Whether Parquet is uploaded directly.
- Whether DuckDB is included or regenerated.
