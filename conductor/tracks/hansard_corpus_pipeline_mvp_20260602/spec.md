# Spec: Hansard Corpus Pipeline MVP

## Goal

Create the first reproducible, evidence-backed pipeline for the NZ Hansard corpus, covering source archive inventory, CSV schema discovery, normalization design, generated Parquet outputs, and a DuckDB analysis database.

## Inputs

- Source archive: `2024-09-06 Hansard Extract from DocumentsDB.zip`
- Known contained files: `Hansard-47.csv` through `Hansard-54.csv`

## Required Outputs

- Machine-readable source inventory with archive metadata, contained CSV metadata, hashes, and sizes.
- Schema discovery report covering headers, encoding, delimiter, sample rows, row counts, and schema drift.
- Repeatable scripts for inventory, schema discovery, normalization, and output validation.
- Generated-output policy using a project-local generated folder.
- Normalized Parquet outputs.
- DuckDB database or build script that can query the normalized outputs.
- Validation report with row counts, warnings, failures, and known limitations.
- Human-readable evidence in the track folder.

## Acceptance Criteria

- The source ZIP is not modified.
- The source archive hash and contained-file metadata are recorded.
- CSV schema discovery runs without full manual extraction into the repo root.
- Normalization rules are documented before full output generation.
- Generated Parquet and DuckDB outputs can be recreated from the source archive and scripts.
- Validation reports identify row counts, schema drift, parse failures, and limitations.
- Research corpus readiness is documented separately from public dataset readiness and reporting readiness.

## Non-Goals

- No public dataset publication in this track.
- No Power BI semantic model or report in this track.
- No claim of complete public-release readiness unless licensing and source-coverage evidence is added in a later track.
