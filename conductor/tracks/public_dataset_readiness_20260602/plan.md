# Plan: Public Dataset Readiness

## Phase 1: Provenance and Dataset Card

- [x] Task: Write licensing and provenance note.
    - [x] Cite official Parliament source material.
    - [x] Separate Hansard text status from website/coverage reuse terms.
- [x] Task: Write dataset card and public release checklist.
    - [x] Include scope, source, schema, outputs, limitations, and intended uses.
    - [x] Keep publication decision and upload out of scope.

## Phase 2: Release Manifest

- [x] Task: Implement release manifest generator.
    - [x] Read existing source, schema, normalization, and DuckDB manifests.
    - [x] Emit machine-readable public dataset release manifest.
    - [x] Add fixture-based tests.
- [x] Task: Validate readiness artifacts.
    - [x] Run tests.
    - [x] Parse generated JSON.
    - [x] Record evidence.

## Phase 3: Track Closure

- [x] Task: Final readiness review.
    - [x] Confirm no upload/publication occurred.
    - [x] Mark publication status explicitly.
    - [x] Update `conductor/tracks.md`.
