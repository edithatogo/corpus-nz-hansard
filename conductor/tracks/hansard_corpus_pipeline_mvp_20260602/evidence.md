# Evidence: Hansard Corpus Pipeline MVP

## Phase 1: Source Inventory and Storage Policy

Status: implementation complete; manual verification pending.

### Generated Output Policy

- Policy file: `docs/generated-output-policy.md`
- Generated multi-GB outputs are assigned to `generated/`.
- `generated/` is ignored by `.gitignore`.
- Lightweight manifests are tracked under `manifests/`.

### Red Phase

Command:

```powershell
python -m unittest tests.test_inventory_archive
```

Result:

- Failed as expected before implementation.
- Failure reason: `ModuleNotFoundError: No module named 'scripts.inventory_archive'`.

### Green Phase

Command:

```powershell
python -m unittest tests.test_inventory_archive
```

Result:

- Passed.
- Test count: 2.

### Source Inventory Command

Command:

```powershell
python scripts\inventory_archive.py --archive "2024-09-06 Hansard Extract from DocumentsDB.zip" --output manifests\source_inventory.json
```

Result:

- Output file: `manifests/source_inventory.json`
- Members: 8
- Total compressed bytes from ZIP members: 536,440,934
- Total uncompressed bytes from ZIP members: 2,456,546,357
- Source archive SHA-256: `2ac02c0042a4fb291fd8e401db5f469de2539e42c9e07c4c72eca16be9a17299`

Contained files:

| File | Uncompressed bytes | SHA-256 prefix |
| --- | ---: | --- |
| `2024-09-06 Hansard Extract from DocumentsDB/Hansard-47.csv` | 228,464,273 | `ca89faaf28d8198c` |
| `2024-09-06 Hansard Extract from DocumentsDB/Hansard-48.csv` | 455,157,236 | `cd5fe3cc544323e1` |
| `2024-09-06 Hansard Extract from DocumentsDB/Hansard-49.csv` | 519,596,192 | `cdc2c7641f618bbc` |
| `2024-09-06 Hansard Extract from DocumentsDB/Hansard-50.csv` | 496,126,794 | `2d390722113f2bbe` |
| `2024-09-06 Hansard Extract from DocumentsDB/Hansard-51.csv` | 379,702,876 | `7495ca5d62c87725` |
| `2024-09-06 Hansard Extract from DocumentsDB/Hansard-52.csv` | 166,567,364 | `a4a962540aae252f` |
| `2024-09-06 Hansard Extract from DocumentsDB/Hansard-53.csv` | 164,178,244 | `8774fa59978d7fb9` |
| `2024-09-06 Hansard Extract from DocumentsDB/Hansard-54.csv` | 46,753,378 | `5b12fb15d9b0e7a1` |

### Validation

Commands:

```powershell
Get-Content -Raw -LiteralPath manifests\source_inventory.json | Test-Json
python -m unittest tests.test_inventory_archive
```

Results:

- `manifests/source_inventory.json` parsed as valid JSON.
- Unit tests passed.

## Phase 2: CSV Schema Discovery

Status: implementation complete; manual verification pending.

### Red Phase

Command:

```powershell
python -m unittest tests.test_discover_schema
```

Result:

- Failed as expected before implementation.
- Failure reason: `ModuleNotFoundError: No module named 'scripts.discover_schema'`.

### Issue Found During Full-Source Run

The first full-source schema run revealed two real data handling issues:

- Python's default CSV field limit was too small for long Hansard `Content` values.
- `Hansard-48.csv` through `Hansard-54.csv` require UTF-16-aware decoding, while `Hansard-47.csv` decodes as `cp1252`.

Both issues were added to tests and fixed before producing the final schema report.

### Green Phase

Command:

```powershell
python -m unittest tests.test_inventory_archive tests.test_discover_schema
```

Result:

- Passed.
- Test count: 7.

### Schema Discovery Command

Command:

```powershell
python scripts\discover_schema.py --archive "2024-09-06 Hansard Extract from DocumentsDB.zip" --output manifests\schema_discovery.json --sample-rows 5
```

Result:

- Output file: `manifests/schema_discovery.json`
- Human-readable report: `docs/schema-discovery-report.md`
- Files inspected: 8
- Total rows counted: 193,922
- Header signatures: 1
- Columns per file: 11

Row counts:

| File | Encoding | Rows |
| --- | --- | ---: |
| `Hansard-47.csv` | `cp1252` | 24,378 |
| `Hansard-48.csv` | `utf-16` | 19,709 |
| `Hansard-49.csv` | `utf-16` | 23,877 |
| `Hansard-50.csv` | `utf-16` | 39,803 |
| `Hansard-51.csv` | `utf-16` | 34,808 |
| `Hansard-52.csv` | `utf-16` | 21,171 |
| `Hansard-53.csv` | `utf-16` | 23,402 |
| `Hansard-54.csv` | `utf-16` | 6,774 |

Candidate roles:

- Date: `DocumentContentDate`
- Speaker/member: `MemberOfParliament`
- Text: `Content`
- Topic/title: `Title`, `AbbreviatedTitle`
- Party: no explicit source column found

### Validation

Commands:

```powershell
Get-Content -Raw -LiteralPath manifests\schema_discovery.json | Test-Json
python -m unittest tests.test_inventory_archive tests.test_discover_schema
```

Results:

- `manifests/schema_discovery.json` parsed as valid JSON.
- Unit tests passed.

## Phase 3: Normalization Pipeline MVP

Status: implementation complete; manual verification pending.

### Red Phase

Command:

```powershell
python -m unittest tests.test_normalize_hansard
```

Result:

- Failed as expected before implementation.
- Failure reason: `ModuleNotFoundError: No module named 'scripts.normalize_hansard'`.

### Normalization Contract

- Contract file: `docs/normalization-contract.md`
- Output dataset: `generated/parquet/hansard.parquet`
- Manifest: `manifests/normalization_manifest.json`
- Validation report: `manifests/normalization_validation.json`
- Deferred: party inference, member entity resolution, portfolio normalization, and speech-turn segmentation.

### Green Phase

Command:

```powershell
python -m unittest tests.test_inventory_archive tests.test_discover_schema tests.test_normalize_hansard
```

Result:

- Passed.
- Test count: 10.

### Normalization Command

Command:

```powershell
python scripts\normalize_hansard.py --archive "2024-09-06 Hansard Extract from DocumentsDB.zip" --output-dir generated\parquet --manifest manifests\normalization_manifest.json --validation manifests\normalization_validation.json --batch-size 1000
```

Result:

- Parquet output: `generated/parquet/hansard.parquet`
- Parquet file size: 317,094,184 bytes
- Input rows: 193,922
- Output rows: 193,922
- Warning count: 0
- Parquet row groups: 194
- Parquet columns: 14

Rows by source file:

| File | Rows |
| --- | ---: |
| `Hansard-47.csv` | 24,378 |
| `Hansard-48.csv` | 19,709 |
| `Hansard-49.csv` | 23,877 |
| `Hansard-50.csv` | 39,803 |
| `Hansard-51.csv` | 34,808 |
| `Hansard-52.csv` | 21,171 |
| `Hansard-53.csv` | 23,402 |
| `Hansard-54.csv` | 6,774 |

### Validation

Commands:

```powershell
Get-Content -Raw -LiteralPath manifests\normalization_manifest.json | Test-Json
Get-Content -Raw -LiteralPath manifests\normalization_validation.json | Test-Json
python -c "import pyarrow.parquet as pq; pf=pq.ParquetFile('generated/parquet/hansard.parquet'); print(pf.metadata.num_rows, len(pf.schema.names))"
```

Results:

- Manifest and validation JSON parsed successfully.
- Parquet metadata reported 193,922 rows and 14 columns.

## Phase 4: DuckDB Analysis Surface

Status: implementation complete; manual verification pending.

### Dependency Setup

Command:

```powershell
python -m pip install duckdb
```

Result:

- Initial sandboxed install failed because no package versions were visible.
- Escalated install succeeded.
- Installed package: `duckdb-1.5.3`.

### Red Phase

Command:

```powershell
python -m unittest tests.test_build_duckdb
```

Result:

- Failed as expected before implementation.
- Failure reason: `ModuleNotFoundError: No module named 'scripts.build_duckdb'`.

### Green Phase

Command:

```powershell
python -m unittest tests.test_inventory_archive tests.test_discover_schema tests.test_normalize_hansard tests.test_build_duckdb
```

Result:

- Passed.
- Test count: 11.

### DuckDB Build Command

Command:

```powershell
python scripts\build_duckdb.py --parquet generated\parquet\hansard.parquet --database generated\duckdb\hansard.duckdb --validation manifests\duckdb_validation.json --expected-rows 193922
```

Result:

- Database: `generated/duckdb/hansard.duckdb`
- WAL file present: `generated/duckdb/hansard.duckdb.wal`
- Validation report: `manifests/duckdb_validation.json`
- Rows: 193,922
- Columns: 14
- Row count matches expected: true
- Checkpoint status: failed because DuckDB could not delete the WAL file on the OneDrive-backed path.

Rows by parliament number:

| Parliament | Rows |
| --- | ---: |
| 47 | 24,378 |
| 48 | 19,709 |
| 49 | 23,877 |
| 50 | 39,803 |
| 51 | 34,808 |
| 52 | 21,171 |
| 53 | 23,402 |
| 54 | 6,774 |

Top document types:

| Document type | Rows |
| --- | ---: |
| `Hansard - speech` | 133,616 |
| `Hansard - question` | 23,303 |
| `Hansard - debate` | 21,345 |
| `Hansard - vote` | 13,231 |
| `Hansard - daily` | 1,963 |

### Validation

Commands:

```powershell
Get-Content -Raw -LiteralPath manifests\duckdb_validation.json | Test-Json
python -c "import duckdb; con=duckdb.connect('generated/duckdb/hansard.duckdb', read_only=True); print(con.execute('select count(*) from hansard').fetchone()[0]); con.close()"
```

Results:

- `manifests/duckdb_validation.json` parsed as valid JSON.
- Direct DuckDB query returned 193,922 rows.
- Research readiness: row counts match normalized Parquet and source-schema discovery totals.
- Public dataset readiness: DuckDB remains a regenerable local derived artifact.
- Reporting readiness: aggregate queries by parliament number, document type, source file, status, and date fields are supported.

## Phase 5: Handoff and Readiness

Status: complete.

### Handoff Documentation

Created:

- `README.md`
- `requirements.txt`
- `docs/pipeline-handoff.md`
- `docs/readiness-review.md`

The handoff documents include:

- Dependency setup.
- Regeneration commands.
- Expected artifacts.
- Known limitations.
- Suggested next tracks.

### Final Readiness Review

Result:

- Research readiness: ready for local document-level analysis.
- Public dataset readiness: not ready; requires licensing, dataset card, limitations, and packaging track.
- Reporting readiness: partially ready; requires semantic/reporting model and refresh contract.

Final MVP evidence:

- Source ZIP hash recorded.
- 8 source CSV files inventoried.
- 193,922 source rows schema-discovered.
- 193,922 normalized Parquet rows generated.
- 193,922 DuckDB rows validated.
- Unit tests pass.
- `conductor/tracks.md` updated to move the MVP track to completed.

### Final Validation

Commands:

```powershell
python -m unittest tests.test_inventory_archive tests.test_discover_schema tests.test_normalize_hansard tests.test_build_duckdb
Get-Content -Raw -LiteralPath manifests\source_inventory.json | Test-Json
Get-Content -Raw -LiteralPath manifests\schema_discovery.json | Test-Json
Get-Content -Raw -LiteralPath manifests\normalization_manifest.json | Test-Json
Get-Content -Raw -LiteralPath manifests\normalization_validation.json | Test-Json
Get-Content -Raw -LiteralPath manifests\duckdb_validation.json | Test-Json
```

Results:

- All tests passed.
- All JSON manifests parsed successfully.
