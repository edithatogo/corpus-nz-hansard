# Plan: Party Attribution With Provenance

## Phase 1: Dependency and Source Design

- [ ] Task: Confirm dependency on member identity resolution.
    - [ ] Define whether party attribution consumes `member_id`.
    - [ ] Define fallback behavior for unresolved members.
- [ ] Task: Select party authority source(s).
    - [ ] Document source URLs, temporal granularity, and provenance limits.
    - [ ] Define authority schema.

## Phase 2: Attribution Rules and Tests

- [ ] Task: Define temporal attribution rules.
    - [ ] Choose document date field(s).
    - [ ] Define party-change and no-party behavior.
- [ ] Task: Add tests.
    - [ ] Date-bounded party match.
    - [ ] Unknown party.
    - [ ] Ambiguous member.
    - [ ] Multiple members.
    - [ ] Missing document date.

## Phase 3: Implementation and Validation

- [ ] Task: Implement party attribution builder.
    - [ ] Read member identity output and party authority table.
    - [ ] Emit derived party output.
    - [ ] Emit validation manifest.
- [ ] Task: Review release readiness.
    - [ ] Document assignment quality.
    - [ ] Decide local-only vs derived public release.

