# Spec: Corpus-Wide Party Attribution Release

## Goal

Create a corpus-wide party attribution component with provenance, temporal validity, and explicit dependency on validated member identity.

## MoSCoW Requirements

### Must

- Join validated member identities to temporal party membership evidence.
- Preserve source document, member, party, date, and confidence/provenance fields.
- Represent independent, unknown, coalition, changed-party, and ambiguous cases explicitly.
- Emit schema, validation manifest, and coverage metrics.

### Should

- Reconcile party labels to canonical party identifiers and aliases.
- Include temporal boundary tests for party switches and parliamentary terms.
- Feed Popolo/Open Civic Data, RDF, ParlaMint, and topic endpoint tracks.

### Could

- Add a local review queue for unresolved party intervals.

### Won't

- Infer party from speech text alone.
- Override unresolved member identity statuses.

## Acceptance Criteria

- Party attribution output is generated only from auditable authority and document evidence.
- Temporal validation demonstrates that party labels are valid for the relevant sitting/speech date.
- Docs explain coverage gaps and uncertainty categories.
