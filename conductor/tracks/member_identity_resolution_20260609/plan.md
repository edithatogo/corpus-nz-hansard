# Plan: Member Identity Resolution

## Phase 1: Authority Source and Contract

- [x] Task: Identify authoritative member source(s).
    - [x] Document source URLs, access method, update cadence, and licensing/provenance.
    - [x] Define the member authority schema and version/hash contract.
- [x] Task: Define derived output contract.
    - [x] Specify output fields, statuses, confidence levels, and non-claims.
    - [x] Add schema documentation under `docs/`.

## Phase 2: Review Package and Tests

- [x] Task: Add fixture-driven tests.
    - [x] Exact raw-name match.
    - [x] Alias/honorific normalized match.
    - [x] Multiple members in one raw field.
    - [x] Unresolved raw member.
    - [x] Ambiguous raw member.
- [x] Task: Implement local review-package builder and checker.
    - [x] Read reviewed gold fixtures.
    - [x] Read authority table.
    - [x] Emit local member identity review output.
    - [x] Emit validation manifest.

## Phase 3: Review and Publication Gate

- [x] Task: Generate local review package.
    - [x] Record match, unresolved, ambiguous, and conflict counts.
    - [x] Produce review report for unresolved/ambiguous cases.
- [x] Task: Decide release readiness.
    - [x] Keep local-only until broader validation exists.
    - [x] Do not publish as a separate derived dataset yet.
