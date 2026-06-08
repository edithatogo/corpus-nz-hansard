# Contracts

## Record Contract

Every normalized Hansard row must satisfy `schemas/hansard_record.schema.json`.

The Hansard contract intentionally mirrors the `corpus-law-nz` pattern while keeping Hansard-specific fields:

- stable record identity through `stable_id`;
- `jurisdiction` and `country` constants;
- source archive, source member, and source row provenance;
- document metadata from the source CSV;
- document-level `content`;
- `text_sha256` and `source_hash`;
- `pipeline_version`.

## Artifact Contract

Local generated layout:

```text
generated/
  parquet/hansard.parquet
  duckdb/hansard.duckdb
  search/hansard_search.sqlite
  release/nz-hansard-corpus-<version>.zip
manifests/
  source_inventory.json
  schema_discovery.json
  normalization_manifest.json
  normalization_validation.json
  record_schema_validation.json
  duckdb_validation.json
  search_index_validation.json
```

Potential public release layout should follow the `corpus-law-nz` split:

- GitHub stores code, schemas, tests, docs, small manifests, and lightweight review packages.
- Hugging Face stores the normalized document-level Parquet dataset if public release is approved.
- Zenodo stores a versioned immutable archive if DOI citation is required.
- DuckDB, SQLite search, and speech-turn candidate outputs are regenerated/local artifacts by default.

## Safety Contract

- Do not commit generated corpus data to GitHub.
- Do not claim Hugging Face or Zenodo publication without live remote proof.
- Do not treat the GitHub lightweight release package as the full dataset; Hugging Face and Zenodo host the normalized Parquet dataset.
- Do not publish Zenodo automatically.
- Do not claim speech-turn-level authority from document-level rows.
- Do not claim source completeness beyond the supplied DocumentsDB extract.
- Do not redistribute the source ZIP unless a later review explicitly approves it.
- Do not include non-authoritative speech-turn candidates in the initial public dataset.
