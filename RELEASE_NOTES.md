# Release Notes: 0.1.0-review.20260603

## Status

Published as a DOI-backed review-stage release. GitHub hosts the lightweight code/docs/manifests review package, Hugging Face hosts the normalized Parquet dataset, and Zenodo hosts the citable archive.

- GitHub repository: `https://github.com/edithatogo/corpus-nz-hansard`
- Review prerelease: `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0-review.20260603`
- Hugging Face dataset: `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`
- Zenodo DOI: `https://doi.org/10.5281/zenodo.20591997`

## Summary

This review release contains the first reproducible NZ Hansard corpus pipeline artifacts:

- Source archive inventory.
- Schema discovery.
- Normalized document-level Parquet generation.
- DuckDB analysis database generation.
- Public dataset readiness documentation.
- Release-readiness manifest.
- Hugging Face dataset card metadata.
- MIT license and provenance notice for original repository materials.

## Included In Review Package

The local review package includes lightweight tracked artifacts:

- Documentation.
- Manifests.
- Scripts.
- Tests.
- Conductor plans and evidence.
- Version and release notes.

## Excluded By Default

- Source ZIP archive.
- `generated/parquet/hansard.parquet`
- `generated/duckdb/hansard.duckdb`
- `generated/duckdb/hansard.duckdb.wal`

These large artifacts are reproducible from the source archive and scripts and should be packaged only after a hosting decision.

## Validation

Current validation:

- Unit tests: 35 passing.
- Source/schema/normalization/DuckDB/public-release manifests parse as JSON.
- Normalized rows: 193,922.
- Record schema validation errors: 0.
- DuckDB rows: 193,922.

## Release Posture

This remains a `0.1.0-review` prerelease because the dataset intentionally preserves document-level records and caveats around unresolved member identity, absent party attribution, and non-authoritative speech-turn segmentation. Promotion to a canonical `v0.1.0` should be a separate release decision after those review-stage limits are accepted or resolved.
