# Generated Output Policy

## Purpose

This project uses the source ZIP as the immutable seed artifact. Extracted files, normalized datasets, DuckDB databases, and caches are generated outputs and must be reproducible from scripts.

## Generated Folder

Use `generated/` for multi-GB or regenerable local outputs:

- `generated/extracted/` for temporary extracted CSVs if a later task requires extraction.
- `generated/parquet/` for normalized Parquet outputs.
- `generated/duckdb/` for local DuckDB databases.
- `generated/validation/` for large validation byproducts that can be regenerated.

The `generated/` folder is ignored by Git.

## Tracked Lightweight Artifacts

Track lightweight artifacts that document reproducibility and source state:

- `manifests/source_inventory.json`
- Future schema discovery reports where file size remains reasonable.
- Future validation summaries where they are suitable for review.
- Conductor evidence files under `conductor/tracks/`.

## Regeneration Rule

Generated outputs must be rebuildable from:

1. `2024-09-06 Hansard Extract from DocumentsDB.zip`
2. Scripts under `scripts/`
3. Documented commands in the active Conductor evidence file
4. Tracked manifests and configuration

Do not manually edit generated corpus data.
