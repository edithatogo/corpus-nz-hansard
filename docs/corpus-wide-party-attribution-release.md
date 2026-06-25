# Corpus-Wide Party Attribution Release

## Purpose

This track promotes explicit party-vote attribution from explicit party-vote label extraction into a corpus-wide derived component. It does not change the canonical document-level v0.1.0 corpus.

## Current Release Gate

The current gate is `release-ready-explicit-party-labels-member-identity-triangulated`.

The member identity dependency is satisfied by `release-ready-triangulated-agent-review`. Party attribution release scope is limited to explicit party-vote labels extracted from vote text. Speech-text party inference and member-identity fallback rows are not authoritative party claims.

Current manifest: `manifests/corpus_wide_party_attribution_validation.json`

## Contract

The corpus-wide builder consumes normalized Hansard records and emits:

- `derived/corpus_wide_party_attribution/party_attribution.csv`
- `derived/corpus_wide_party_attribution/party_attribution_review_queue.csv`
- `derived/corpus_wide_party_attribution/party_attribution_review_overrides.csv`
- `schemas/corpus_wide_party_attribution.schema.json`
- `manifests/corpus_wide_party_attribution_validation.json`

The row contract preserves source evidence, party vote side, raw party label, normalized party label, party vote count, source hash, authority hash, and the member identity dependency state.

## Review Overrides

Review overrides remain separate and auditable in `derived/corpus_wide_party_attribution/party_attribution_review_overrides.csv`.

## Non-Claims

- Speech-text party inference is excluded from this release surface.
- Member-identity fallback rows are not authoritative party claims.
- The document-level corpus remains unchanged.
