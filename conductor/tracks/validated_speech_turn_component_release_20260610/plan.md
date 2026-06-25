# Plan: Validated Speech-Turn Component Release

## Status

Complete and release-ready under `release-ready-speech-turns-triangulated-speakers-agent-review`.

## Phase 1: Validation Design

- [x] Define evaluation sample, thresholds, and error taxonomy.
- [x] Define schema, selectors, and confidence/status fields.

## Phase 2: Implementation

- [x] Build validated turn artifact from candidate speech-turn parquet.
- [x] Resolve speaker candidates against the triangulated member authority.
- [x] Route unresolved or ambiguous speakers to agent-review fallback.
- [x] Generate manifest, metrics, and review queue.

## Phase 3: Release Gate

- [x] Accept `release-ready-triangulated-agent-review` as the member identity dependency gate.
- [x] Promote candidate speech-turn parquet with fallback non-claims.
- [x] Update speech-turn decision docs and downstream endpoint readiness.
