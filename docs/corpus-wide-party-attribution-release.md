# Corpus-Wide Party Attribution Release

## Purpose

This track promotes party attribution from the sample review package toward a corpus-wide derived component. It does not change the canonical document-level `v0.1.0` corpus.

## Current Release Gate

The current gate is blocked, not published.

- `blocked-pending-validated-member-identity`: the repository still lacks a validated corpus-wide member identity release.
- The current party authority snapshot supports provenance and explicit vote-label extraction, but it is not enough to publish member-linked party attribution as a validated corpus-wide component.
- Explicit party-vote labels can be extracted in blocked-review mode, but that does not change the release gate.

The generated validation manifest is `manifests/corpus_wide_party_attribution_validation.json`. Its release decision must remain `defer` until validated member identity exists.

## Contract

The corpus-wide builder consumes normalized Hansard records and emits:

- `derived/corpus_wide_party_attribution/party_attribution.csv`
- `derived/corpus_wide_party_attribution/party_attribution_review_queue.csv`
- `derived/corpus_wide_party_attribution/party_attribution_review_overrides.csv`
- `schemas/corpus_wide_party_attribution.schema.json`
- `manifests/corpus_wide_party_attribution_validation.json`

The row contract preserves source evidence:

- `source_stable_id`
- `source_file`
- `source_row_number`
- `parliament_number`
- `parliament_document_id`
- `document_type`
- `document_content_date`
- `party_vote_side`
- `party_label_raw`
- `party_label_normalized`
- `party_vote_count`
- `party_id`
- `source_hash`

Resolution statuses distinguish:

- `authoritative`
- `alias`
- `ambiguous`
- `unresolved`
- `blocked`

## Review Overrides

Human review overrides are kept separate in `derived/corpus_wide_party_attribution/party_attribution_review_overrides.csv`. Overrides must remain auditable and must not silently rewrite source text.

## Non-Claims

- The current output must not be published as a validated component.
- Member-linked party attribution is blocked until validated member identity exists.
- Speech-text party inference remains excluded from the public release surface.
- The document-level corpus remains unchanged.
