# Technical Context

## Current State

This workspace currently contains a single ZIP archive of CSV extracts and no application, package, or pipeline metadata.

## Known Data Shape

Archive listing:

- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-47.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-48.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-49.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-50.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-51.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-52.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-53.csv`
- `2024-09-06 Hansard Extract from DocumentsDB/Hansard-54.csv`

## Preferred Tooling

Use conservative, scriptable tools that work well on Windows and large CSV files:

- PowerShell for local file inventory and orchestration.
- Python for archive inspection, CSV schema discovery, normalization, validation, and manifest generation.
- SQLite or DuckDB for local exploratory indexing once CSV schemas are known.
- Parquet for columnar derived outputs if publication or repeated analysis requires it.

## Repository Constraints

- The Git repository root appears to be higher than this project directory, so status output may include unrelated OneDrive-wide changes.
- Keep all generated project files scoped under `corpus-nz-hansard`.
- Avoid extracting multi-gigabyte data into the repository root without an explicit track and output policy.

## Data Handling

- Treat the ZIP as the immutable source artifact.
- Prefer derived-output directories that can be ignored or regenerated.
- Record source file hashes and row counts before transformation.
- Validate CSV dialect, encoding, headers, null handling, and date fields before building downstream models.

## Power BI Note

The local AGENTS instructions include Power BI CLI skill requirements for Power BI, DAX, semantic model, and report-layer work. This setup did not perform Power BI work. Invoke the relevant Power BI skill before future Power BI-specific changes.
