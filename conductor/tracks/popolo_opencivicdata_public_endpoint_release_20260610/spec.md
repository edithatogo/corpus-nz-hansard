# Spec: Popolo/Open Civic Data Public Endpoint Release

## Goal

Publish a validated civic-data endpoint release after people, organisations, memberships, motions, votes, and events are mature enough.

## MoSCoW Requirements

### Must

- Generate Popolo/Open Civic Data-compatible people, organisations, memberships, posts, events, motions, votes, and source links when evidence exists.
- Preserve uncertainty with status fields and avoid filling absent evidence silently.
- Validate JSON structure, ID stability, temporal memberships, and provenance.

### Should

- Align identifiers with member identity, party attribution, and canonical URI policy.
- Include import examples for civic-data consumers.

### Could

- Release identity/organisation subsets before votes and motions if clearly scoped.

### Won't

- Invent memberships, offices, or vote records from incomplete evidence.

## Acceptance Criteria

- Package, schema checks, validation manifest, docs, and coverage metrics exist.
- Release state is blocked until required upstream components are validated.
