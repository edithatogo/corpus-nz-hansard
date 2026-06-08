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
- `manifests/record_schema_validation.json`
- `manifests/duckdb_validation.json`
- `manifests/search_index_validation.json`
- `docs/schema-discovery-report.md`
- `docs/normalization-contract.md`
- `docs/duckdb-analysis.md`

Generated outputs:

- `generated/parquet/hansard.parquet`
- `generated/duckdb/hansard.duckdb`
- `generated/search/hansard_search.sqlite`
- `generated/huggingface/`
- `generated/zenodo/`
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

Validate records:

```powershell
python scripts\validate_hansard_records.py --parquet generated\parquet\hansard.parquet --schema schemas\hansard_record.schema.json --report manifests\record_schema_validation.json
```

Run tests:

```powershell
python -m unittest discover tests
```

## Current Validation

- Source inventory members: 8
- Schema-discovered rows: 193,922
- Normalized Parquet rows: 193,922
- Record schema validation errors: 0
- DuckDB rows: 193,922
- Search index chunks: 1,018,955
- Normalization warnings: 0

## Publication Status

- GitHub repository: `https://github.com/edithatogo/corpus-nz-hansard`
- GitHub review prerelease: `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0-review.20260603`
- Hugging Face dataset upload: blocked until `HF_TOKEN` is available.
- Zenodo archive upload: blocked until `ZENODO_TOKEN` and `ARCHIVE_CREATORS_JSON` are available.

## Limits

- Party is not present as a source column.
- `MemberOfParliament` is retained as a raw semicolon-separated source field plus a count; entity resolution is deferred.
- `Content` remains document-level text; speech-turn segmentation is deferred.
- Full public dataset publication, final licensing review, and Power BI/reporting models are deferred tracks.
