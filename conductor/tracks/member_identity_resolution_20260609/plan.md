# Plan: Member Identity Resolution

## Phase 1: Authority Source and Contract

- [ ] Task: Identify authoritative member source(s).
    - [ ] Document source URLs, access method, update cadence, and licensing/provenance.
    - [ ] Define the member authority schema and version/hash contract.
- [ ] Task: Define derived output contract.
    - [ ] Specify output fields, statuses, confidence levels, and non-claims.
    - [ ] Add schema documentation under `docs/`.

## Phase 2: Resolver Design and Tests

- [ ] Task: Add fixture-driven tests.
    - [ ] Exact raw-name match.
    - [ ] Alias/honorific normalized match.
    - [ ] Multiple members in one raw field.
    - [ ] Unresolved raw member.
    - [ ] Ambiguous raw member.
- [ ] Task: Implement resolver.
    - [ ] Read normalized Hansard Parquet.
    - [ ] Read authority table.
    - [ ] Emit derived member identity output.
    - [ ] Emit validation manifest.

## Phase 3: Review and Publication Gate

- [ ] Task: Generate full derived output.
    - [ ] Record match, unresolved, ambiguous, and conflict counts.
    - [ ] Produce review report for unresolved/ambiguous cases.
- [ ] Task: Decide release readiness.
    - [ ] Keep local-only if ambiguity is too high.
    - [ ] Publish as separate derived dataset only after validation acceptance.

