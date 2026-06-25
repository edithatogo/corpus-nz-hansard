# Plan: Corpus-Wide Party Attribution Release

## Status

Complete and release-ready under `release-ready-explicit-party-labels-member-identity-triangulated`.

## Phase 1: Dependencies

- [x] Confirm member identity release gate state.
- [x] Inventory party membership authority sources and temporal fields.
- [x] Define schema and unresolved/ambiguous status handling.

## Phase 2: Implementation

- [x] Build explicit party-vote label extraction and validation checks.
- [x] Limit release scope to explicit party-vote labels.
- [x] Exclude speech-text party inference and member-identity fallback rows from authoritative party claims.

## Phase 3: Release Decision

- [x] Accept `release-ready-triangulated-agent-review` as the member identity dependency gate.
- [x] Update docs and manifest with release-ready explicit-party-label scope.
- [x] Record release decision with validation evidence.
