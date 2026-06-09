# Hosting Decision Matrix

## Status

GitHub has been selected for code, schemas, tests, docs, manifests, and the lightweight review package.

- Repository: `https://github.com/edithatogo/corpus-nz-hansard`
- Release: `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0`
- Hugging Face dataset publication has occurred.
- Hugging Face publication is complete at `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`.
- Zenodo archive publication has occurred at `https://zenodo.org/records/20595194`.
- DOI: `https://doi.org/10.5281/zenodo.20595194`
- Repository license/provenance boundary is documented in `LICENSE` and `NOTICE.md`.

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
3. Use Zenodo for DOI/archive citation.
4. Keep DuckDB and SQLite search as regenerated local outputs unless a reviewer explicitly needs prebuilt database files.
5. Do not redistribute the source ZIP by default; use `SOURCE_ARCHIVE_URL` plus SHA-256 verification for trusted rebuilds.

## Initial Distribution Decisions

- Hugging Face publishes `generated/huggingface/data/hansard.parquet` directly after credentialed publication.
- Zenodo hosts the staged archive from `generated/zenodo/` as the citable DOI record.
- The source ZIP is not redistributed by default.
- DuckDB and search SQLite are regenerated artifacts, not initial public dataset payloads.
- Non-authoritative speech-turn candidates are excluded from the initial public dataset.
- The current release is the canonical document-level `0.1.0` release.

## Cross-Corpus Hosting Alignment

Preferred family labels are `corpus-nz-hansard` and `corpus-nz-legislation`. Hansard already uses the preferred GitHub label. The legislation sibling may continue to expose existing published names until a migration track protects citations and redirects.

Environment requirements to track for both corpora:

- GitHub: repository description, homepage, topics, license detection, releases, Actions, CodeQL, Scorecard, Renovate, branch protection, README sibling links.
- Hugging Face: dataset card front matter, public/ungated access, Xet status, viewer health, file layout, DOI/GitHub/sibling links, manifest placement.
- Zenodo: canonical DOI, concept/version DOI, source-rights-safe license metadata, related identifiers to GitHub and Hugging Face, archive manifest and checksums.
- OSF: optional review or mirror bundle only after file-size, checksum, citation, and update cadence policy is documented.
- Other metadata registries: generate Croissant, RO-Crate, Frictionless, DCAT, and PROV-O metadata rather than hand-maintaining divergent descriptions.
