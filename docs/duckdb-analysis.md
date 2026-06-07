# DuckDB Analysis Surface

## Build Command

```powershell
python scripts\build_duckdb.py --parquet generated\parquet\hansard.parquet --database generated\duckdb\hansard.duckdb --validation manifests\duckdb_validation.json --expected-rows 193922
```

## Outputs

- Database: `generated/duckdb/hansard.duckdb`
- Write-ahead log, when present: `generated/duckdb/hansard.duckdb.wal`
- Validation report: `manifests/duckdb_validation.json`
- Source dataset: `generated/parquet/hansard.parquet`

## Table

The database contains a physical table named `hansard` with the normalized Phase 3 columns.

Indexes:

- `parliament_document_id`
- `parliament_number`

## Example Queries

```sql
select count(*) from hansard;
```

```sql
select parliament_number, count(*) as rows
from hansard
group by parliament_number
order by parliament_number;
```

```sql
select document_type, count(*) as rows
from hansard
group by document_type
order by rows desc;
```

```sql
select parliament_document_id, title, length(content) as content_length
from hansard
order by content_length desc
limit 10;
```

## Readiness Notes

- Research readiness: table counts match the normalized Parquet dataset and source row totals.
- Public dataset readiness: generated database remains a local derived artifact and should be regenerated from tracked scripts and manifests.
- Reporting readiness: the table is suitable for aggregate checks by parliament number, document type, source file, status, and date fields.
- Environment note: on this OneDrive-backed workspace, DuckDB can create and query the database but checkpointing may fail to remove the `.wal` file because local deletion is denied. Keep both generated files together or regenerate from Parquet.
