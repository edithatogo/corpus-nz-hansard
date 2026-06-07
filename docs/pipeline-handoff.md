# Pipeline Handoff

## What Exists

The workspace now has a reproducible source-to-analysis pipeline:

1. Source archive inventory.
2. CSV schema discovery.
3. Normalized document-level Parquet dataset.
4. DuckDB analytical database and validation report.

## Commands

Run all checks:

```powershell
python -m unittest tests.test_inventory_archive tests.test_discover_schema tests.test_normalize_hansard tests.test_build_duckdb
```

Regenerate all pipeline artifacts in order:

```powershell
python scripts\inventory_archive.py --archive "2024-09-06 Hansard Extract from DocumentsDB.zip" --output manifests\source_inventory.json
python scripts\discover_schema.py --archive "2024-09-06 Hansard Extract from DocumentsDB.zip" --output manifests\schema_discovery.json --sample-rows 5
python scripts\normalize_hansard.py --archive "2024-09-06 Hansard Extract from DocumentsDB.zip" --output-dir generated\parquet --manifest manifests\normalization_manifest.json --validation manifests\normalization_validation.json --batch-size 1000
python scripts\validate_hansard_records.py --parquet generated\parquet\hansard.parquet --schema schemas\hansard_record.schema.json --report manifests\record_schema_validation.json
python scripts\build_duckdb.py --parquet generated\parquet\hansard.parquet --database generated\duckdb\hansard.duckdb --validation manifests\duckdb_validation.json --expected-rows 193922
```

## Expected Outputs

| Artifact | Expected state |
| --- | --- |
| `manifests/source_inventory.json` | 8 archive members and source ZIP hash. |
| `manifests/schema_discovery.json` | 8 files, 193,922 rows, 1 header signature. |
| `generated/parquet/hansard.parquet` | 193,922 rows, 23 columns. |
| `manifests/normalization_validation.json` | 193,922 input rows, 193,922 output rows, 0 warnings. |
| `manifests/record_schema_validation.json` | 193,922 records validated against `schemas/hansard_record.schema.json`. |
| `generated/duckdb/hansard.duckdb` | Queryable `hansard` table with 193,922 rows. |
| `manifests/duckdb_validation.json` | DuckDB row count matches expected rows. |

## Known Limitations

- DuckDB may leave `generated/duckdb/hansard.duckdb.wal` on this OneDrive-backed workspace because checkpoint deletion can be denied.
- The pipeline has not performed public dataset licensing review.
- The pipeline has not inferred party, split speech turns, or resolved members to stable identities.
- `generated/` is local generated state and should be regenerated rather than committed.

## Suggested Next Tracks

- Public dataset publication readiness: dataset card, licensing assumptions, source limitations, and release packaging.
- Reporting/Power BI readiness: semantic model, refresh contract, and report-level measures.
- Search/RAG indexing: chunking strategy, embeddings or lexical search, source citation format, and retrieval validation.
- Speech-turn segmentation: split document-level `Content` into structured turns where the source text supports it.
