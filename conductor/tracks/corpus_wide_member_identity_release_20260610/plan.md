# Plan: Corpus-Wide Member Identity Release

## Status

Complete and release-ready under `release-ready-triangulated-agent-review`.

Triangulation is the required authority workflow. Agent-review fallback is used for unmatched authority records and unresolved row-level tokens; human review is not a release blocker.

## Phase 1: Inputs And Contract

- [x] Inventory all member-bearing fields in the corpus.
- [x] Freeze authority source snapshots and hashes.
- [x] Define corpus-wide schema, statuses, and review override format.

## Phase 2: Builder And Validation

- [x] Build corpus-wide resolver output from `generated/parquet/hansard.parquet`.
- [x] Emit member identity CSV, agent-review fallback queue, manifest, schema, and metrics.
- [x] Add validation checks for coverage, status values, source links, and conflicts.

## Phase 3: Triangulation And Fallback

- [x] Use Wikidata and NZ Parliament records as the authority triangulation basis.
- [x] Record 400 auto-derived authority records, 393 triangulated matches, and 7 unmatched fallback records.
- [x] Route 23 unresolved row-level member-token outputs to `agent-review-fallback`.
- [x] Refresh authority snapshot hash in the validation manifest.

## Phase 4: Release Decision

- [x] Set manifest `ok` to true with `validation_status` `ok`.
- [x] Set release gate to `release-ready-triangulated-agent-review`.
- [x] Update release and coverage docs with current triangulation facts.
- [x] Keep non-claims for unresolved fallback rows.
