# Plan: Hugging Face Viewer Layout Fix

## Phase 1: Remote and staged layout audit

- [ ] Record current remote file list, dataset card metadata, `private`, `gated`, Xet status, and viewer error.
- [ ] Identify which JSON files Hugging Face treats as dataset splits.
- [ ] Decide whether to move manifests under a non-dataset path, add viewer `configs`, or otherwise constrain auto-detection.

## Phase 2: Implementation

- [ ] Update staging script so canonical Parquet is the only viewer dataset unless intentionally configured otherwise.
- [ ] Keep manifests, schemas, docs, CITATION, and NOTICE downloadable but not misdetected as incompatible splits.
- [ ] Add or update tests for staged Hugging Face layout.
- [ ] Republish and verify `private=false`, `gated=false`, populated `cardData`, and healthy viewer or intentional viewer-disable explanation.

## Phase 3: Cross-corpus alignment

- [ ] Document the chosen file layout as the family pattern for `corpus-nz-hansard` and `corpus-nz-legislation`.
- [ ] Add sibling-corpus links to the dataset card.

## Verification

- [ ] Dataset viewer loads or is intentionally disabled with documented rationale.
- [ ] Parquet file can be read through documented PyArrow/DuckDB examples.
- [ ] Track evidence records remote revision and access checks.
