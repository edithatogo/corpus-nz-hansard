# Plan: Hugging Face Viewer Layout Fix

## Phase 1: Remote and staged layout audit

- [x] Record current remote file list, dataset card metadata, `private`, `gated`, Xet status, and viewer error.
- [x] Identify which JSON files Hugging Face treats as dataset splits.
- [x] Decide whether to move manifests under a non-dataset path, add viewer `configs`, or otherwise constrain auto-detection.

## Phase 2: Implementation

- [x] Update staging script so canonical Parquet is the only viewer dataset unless intentionally configured otherwise.
- [x] Keep manifests, schemas, docs, CITATION, and NOTICE downloadable but not misdetected as incompatible splits.
- [x] Add or update tests for staged Hugging Face layout.
- [x] Republish and verify `private=false`, `gated=false`, populated `cardData`, and healthy viewer or intentional viewer-disable explanation.

## Phase 3: Cross-corpus alignment

- [x] Document the chosen file layout as the family pattern for `corpus-nz-hansard` and `corpus-nz-legislation`.
- [x] Add sibling-corpus links to the dataset card.

## Verification

- [x] Dataset viewer loads or is intentionally disabled with documented rationale.
- [x] Parquet file can be read through documented PyArrow/DuckDB examples.
- [x] Track evidence records remote revision and access checks.
