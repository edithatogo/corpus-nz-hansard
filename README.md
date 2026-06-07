# corpus-nz-hansard

Reproducible local corpus workspace for New Zealand Hansard data extracted from a DocumentsDB source archive.

## Source

- Source archive: `2024-09-06 Hansard Extract from DocumentsDB.zip`
- Source archive SHA-256: `2ac02c0042a4fb291fd8e401db5f469de2539e42c9e07c4c72eca16be9a17299`
- Source CSV files: `Hansard-47.csv` through `Hansard-54.csv`

## Pipeline Outputs

Tracked manifests and reports:

- `manifests/source_inventory.json`
- `manifests/schema_discovery.json`
- `manifests/normalization_manifest.json`
- `manifests/normalization_validation.json`
- `manifests/duckdb_validation.json`
- `docs/schema-discovery-report.md`
- `docs/normalization-contract.md`
- `docs/duckdb-analysis.md`

Generated outputs:

- `generated/parquet/hansard.parquet`
- `generated/duckdb/hansard.duckdb`
- `generated/duckdb/hansard.duckdb.wal` when DuckDB cannot checkpoint away the write-ahead log on OneDrive.

`generated/` is ignored by Git and can be regenerated from the source archive and scripts.

## Regeneration

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Build source inventory:

```powershell
python scripts\inventory_archive.py --archive "2024-09-06 Hansard Extract from DocumentsDB.zip" --output manifests\source_inventory.json
```

Discover schema:

```powershell
python scripts\discover_schema.py --archive "2024-09-06 Hansard Extract from DocumentsDB.zip" --output manifests\schema_discovery.json --sample-rows 5
```

Normalize to Parquet:

```powershell
python scripts\normalize_hansard.py --archive "2024-09-06 Hansard Extract from DocumentsDB.zip" --output-dir generated\parquet --manifest manifests\normalization_manifest.json --validation manifests\normalization_validation.json --batch-size 1000
```

Build DuckDB:

```powershell
python scripts\build_duckdb.py --parquet generated\parquet\hansard.parquet --database generated\duckdb\hansard.duckdb --validation manifests\duckdb_validation.json --expected-rows 193922
```

Run tests:

```powershell
python -m unittest tests.test_inventory_archive tests.test_discover_schema tests.test_normalize_hansard tests.test_build_duckdb
```

## Current Validation

- Source inventory members: 8
- Schema-discovered rows: 193,922
- Normalized Parquet rows: 193,922
- DuckDB rows: 193,922
- Normalization warnings: 0

## Limits

- Party is not present as a source column.
- `MemberOfParliament` is retained as a raw semicolon-separated source field plus a count; entity resolution is deferred.
- `Content` remains document-level text; speech-turn segmentation is deferred.
- Public dataset publication, licensing review, and Power BI/reporting models are deferred tracks.
