# Readiness Review

## Summary

The initial Hansard corpus pipeline MVP is research-ready for local document-level analysis. It is not yet public-dataset-release ready or report-production ready without the next tracks listed below.

## Evidence

- Source archive SHA-256 is recorded in `manifests/source_inventory.json`.
- Source inventory validates 8 contained CSV files.
- Schema discovery validates 193,922 rows and one consistent source header signature.
- Normalization writes 193,922 Parquet rows from 193,922 source rows with 0 warnings.
- DuckDB validates 193,922 table rows and representative aggregate queries.
- Unit tests pass across inventory, schema discovery, normalization, and DuckDB build scripts.

## Research Readiness

Status: ready for local document-level research use.

Supported:

- Querying by parliament number, document type, title, status, source file, content date, and member field.
- Document-level text analysis over `Content`.
- Reproducible regeneration from the source archive.

Deferred:

- Speaker-turn segmentation.
- Party inference.
- Member identity resolution.
- Detailed licensing/public release review.

## Public Dataset Readiness

Status: not ready.

Required next work:

- Dataset card.
- Licensing and redistribution assumptions.
- Provenance and limitations statement.
- Generated artifact packaging policy.
- Public release checks for sensitive or malformed records.

## Reporting Readiness

Status: partially ready.

Supported:

- Aggregate checks from DuckDB.
- Counts by parliament number and document type.

Required next work:

- Formal semantic/reporting model.
- Date field validation for reporting periods.
- Measure definitions and refresh procedures.
- Power BI or equivalent reporting build.

## Final MVP Decision

The MVP acceptance criteria are met for a local reproducible corpus pipeline:

- Source ZIP remained unmodified.
- Source inventory and schema discovery are documented.
- Normalization rules are documented before and alongside full output generation.
- Parquet and DuckDB outputs are generated and validated.
- Research, public-dataset, and reporting readiness are separated.
