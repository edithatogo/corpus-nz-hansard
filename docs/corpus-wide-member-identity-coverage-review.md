# Corpus-Wide Member Identity Authority Coverage Review

Track ID: `corpus_wide_member_identity_release_20260610`

Status: release-ready under `release-ready-triangulated-agent-review`

## Current Finding

The old coverage review was based on a stale 408-record authority snapshot before triangulation. The current authority artifact contains 400 auto-derived records and a triangulation summary against Wikidata and NZ Parliament sources.

Current metrics:

- Authority records: 400
- Triangulated matches: 393
- Unmatched fallback records: 7
- Match rate: 98.2%
- Wikidata matches: 352
- NZ Parliament matches: 41
- Wikidata records available: 1,514
- NZ Parliament records available: 125

## Resolution Policy

Triangulation is the required authority workflow. Fallback goes to agent review, not human review. The component is not blocked by the seven currently unmatched authority records because fallback rows are explicitly flagged and non-authoritative until resolved.

## Resolved Stale Issues

- The normalized corpus artifact is present: `generated/parquet/hansard.parquet`.
- The authority snapshot hash is refreshed in the validation manifest.
- The old 408-record, zero-URL, zero-cross-reference review is superseded by the current 400-record triangulated authority.
- The release gate no longer depends on human review.

## Remaining Fallback Work

- Seven authority records remain unmatched by triangulation.
- Twenty-three row-level member-token outputs are routed to `agent-review-fallback`.
- Fallback rows must be resolved or excluded by downstream consumers that require fully authoritative member identity.
