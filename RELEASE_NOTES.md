# Release Notes: 0.1.0

## Status

Published as the first canonical document-level release of the NZ Hansard Corpus.
GitHub hosts the code, documentation, manifests, and lightweight release package;
Hugging Face hosts the normalized Parquet dataset; Zenodo hosts the citable archive.

- GitHub repository: `https://github.com/edithatogo/corpus-nz-hansard`
- GitHub release: `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0`
- Hugging Face dataset: `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`
- Zenodo DOI: `https://doi.org/10.5281/zenodo.20595194`

## Summary

This release contains the first reproducible document-level NZ Hansard corpus pipeline artifacts:

- Source archive inventory.
- Schema discovery.
- Normalized document-level Parquet generation.
- DuckDB analysis database generation.
- Public dataset release documentation.
- Release manifest.
- Hugging Face dataset card metadata.
- MIT license and provenance notice for original repository materials.

## Dataset Scope

This is a final release for the document-level corpus. It intentionally does not claim:

- resolved member identity;
- party attribution;
- authoritative speech-turn segmentation.

Those are later derived-data tracks and can be released as separate higher-level datasets without changing the canonical document-level contract.

## Included In GitHub Release Package

The GitHub release package includes lightweight tracked artifacts:

- Documentation.
- Manifests.
- Scripts.
- Tests.
- Conductor plans and evidence.
- Version and release notes.

## Excluded By Default

- Source ZIP archive.
- `generated/parquet/hansard.parquet` from the GitHub ZIP package.
- `generated/duckdb/hansard.duckdb`.
- `generated/duckdb/hansard.duckdb.wal`.

The normalized Parquet dataset is published on Hugging Face and included in the Zenodo archive. Large local database/search outputs remain reproducible convenience artifacts unless explicitly published later.

## Validation

Current validation:

- Unit tests: passing.
- Source/schema/normalization/DuckDB/public-release manifests parse as JSON.
- Normalized rows: 193,922.
- Record schema validation errors: 0.
- DuckDB rows: 193,922.
