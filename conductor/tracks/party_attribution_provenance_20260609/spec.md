# Spec: Party Attribution With Provenance

## Goal

Create a derived party-attribution layer for Hansard records with documented authority sources, temporal validity, and validation gates.

## MoSCoW Requirements

### Must

- Treat party attribution as derived data, not a source column.
- Require provenance for every party assignment.
- Define temporal attribution rules using document date and party membership/service periods where available.
- Preserve cases where party attribution is unknown, not applicable, ambiguous, or conflicting.
- Emit attribution method, source URL, confidence, and validation status.
- Add tests for known party match, date-bounded party change, independent/no-party case, ambiguous member case, and missing date case.
- Emit a validation manifest with assigned, unknown, ambiguous, and conflict counts.

### Should

- Depend on validated `member_id` from the member identity track.
- Support multiple party assignments where multiple members are present in one document.
- Include a manual-review report for party conflicts and missing temporal data.
- Document exact assumptions for document date selection.

### Could

- Support parliamentary term-level fallback attribution when precise date ranges are unavailable.
- Compare derived counts against high-level external summaries as sanity checks.
- Add confidence tiers by attribution source quality.

### Won't

- Infer party directly from speech content.
- Collapse multiple members into one party without explicit rules.
- Claim party-level analysis is supported until the validation manifest passes release gates.
- Change the final document-level `v0.1.0` corpus.

## Design Amendments

- Add a party authority/provenance table, for example `derived/party_attribution_authority.*`.
- Add generated derived output, for example `generated/derived/hansard_party_attribution.parquet`.
- Add validation manifest `manifests/party_attribution_validation.json`.
- Candidate output fields:
  - `stable_id`
  - `member_id`
  - `document_content_date`
  - `party_id`
  - `party_name`
  - `party_attribution_start`
  - `party_attribution_end`
  - `party_attribution_source`
  - `party_attribution_url`
  - `party_attribution_method`
  - `party_attribution_confidence`
  - `party_attribution_status`

## Acceptance Criteria

- Party attribution can be reproduced from documented authority inputs.
- Unknown and ambiguous party values remain explicit.
- Tests and validation manifest pass.
- Release notes and dataset card describe provenance, limitations, and non-claims.

