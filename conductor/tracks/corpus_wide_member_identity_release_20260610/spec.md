# Spec: Corpus-Wide Member Identity Release

## Goal

Promote the local member identity review package into a corpus-wide validated derived component without changing the canonical document-level release.

## MoSCoW Requirements

### Must

- Generate a corpus-wide member identity artifact from the full available Hansard corpus.
- Preserve raw speaker/member strings and source document identifiers.
- Include authority source hashes, source URLs, access dates, and transformation provenance.
- Distinguish exact, alias, multi-person, unresolved, ambiguous, and conflict statuses.
- Emit schema, validation manifest, review queue, and release-readiness decision.

### Should

- Include coverage metrics by parliament, year, document type, and source archive.
- Support human-reviewed overrides as a separate auditable input.
- Feed downstream party attribution and civic-data endpoint tracks.

### Could

- Publish a preview subset before a full derived release if coverage is uneven.

### Won't

- Claim authoritative identity for unresolved or ambiguous rows.
- Mutate the document-level `v0.1.0` corpus.

## Acceptance Criteria

- Corpus-wide output, schema, validation manifest, docs, and tests exist.
- Public docs clearly state status, coverage, limitations, and non-claims.
- Downstream tracks can consume stable member identifiers and resolution statuses.
