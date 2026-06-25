# Corpus-Wide Member Identity Release

## Purpose

This release track promotes member identity resolution from the local review package into a corpus-wide derived component. It does not change the canonical document-level v0.1.0 corpus.

## Current Release Gate

The current gate is `release-ready-triangulated-agent-review`.

Triangulation is the required authority workflow. The authority snapshot is cross-referenced against Wikidata and NZ Parliament records, with agent-review fallback for unmatched authority records and unresolved row-level member tokens. There is no human-review blocking gate in this workflow.

Current manifest: `manifests/corpus_wide_member_identity_validation.json`

Current metrics:

- Source rows read: 193,922
- Source rows with member field: 157,640
- Derived member-token rows: 308,437
- Exact rows: 78,574
- Alias rows: 3,924
- Multi-person rows: 225,916
- Unresolved agent-review fallback rows: 23
- Ambiguous rows: 0
- Conflict rows: 0
- Authority records: 400
- Triangulated authority matches: 393/400 (98.2%)
- Wikidata matches: 352
- NZ Parliament matches: 41
- Unmatched authority records routed to fallback: 7

## Contract

The corpus-wide builder consumes normalized Hansard records from `generated/parquet/hansard.parquet` and emits:

- `derived/corpus_wide_member_identity/member_identity.csv`
- `derived/corpus_wide_member_identity/member_identity_review_queue.csv`
- `derived/corpus_wide_member_identity/member_identity_review_overrides.csv`
- `schemas/corpus_wide_member_identity.schema.json`
- `manifests/corpus_wide_member_identity_validation.json`

The row contract preserves source document evidence, raw member strings, authority hashes, and resolution status. Resolved rows carry `release-ready`; fallback rows carry `agent-review-fallback`.

## Agent-Review Fallback

The review queue is now an agent-review fallback queue. Fallback rows are isolated for later agent resolution and must not be treated as authoritative identity claims until resolved. review overrides remain separate and auditable in `derived/corpus_wide_member_identity/member_identity_review_overrides.csv`.

## Non-Claims

- unresolved fallback rows are not authoritative identity claims.
- The document-level corpus remains unchanged.
- Downstream consumers must respect `member_resolution_status` and `release_status` when excluding fallback rows.
