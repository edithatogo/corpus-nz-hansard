# Plan: Party Attribution With Provenance

## Phase 1: Dependency and Source Design

- [x] Task: Confirm dependency on member identity resolution.
    - [x] Define whether party attribution consumes `member_id`.
    - [x] Define fallback behavior for unresolved members.
- [x] Task: Select party authority source(s).
    - [x] Document source URLs, temporal granularity, and provenance limits.
    - [x] Define authority schema.

## Phase 2: Attribution Rules and Tests

- [x] Task: Define temporal attribution rules.
    - [x] Choose document date field(s).
    - [x] Define party-change and no-party behavior.
- [x] Task: Add tests.
    - [x] Date-bounded party match.
    - [x] Unknown party.
    - [x] Ambiguous member.
    - [x] Multiple members.
    - [x] Missing document date.

## Phase 3: Implementation and Validation

- [x] Task: Implement party attribution builder.
    - [x] Read member identity output and party authority table.
    - [x] Emit derived party output.
    - [x] Emit validation manifest.
- [x] Task: Review release readiness.
    - [x] Document assignment quality.
    - [x] Decide local-only vs derived public release.
