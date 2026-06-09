# Spec: Member Identity Resolution

## Goal

Resolve raw `MemberOfParliament` source values into authoritative member identity fields suitable for a derived Hansard member-identity dataset.

## MoSCoW Requirements

### Must

- Preserve the canonical document-level corpus unchanged.
- Define an authoritative member authority table with source provenance.
- Normalize raw names without silently discarding ambiguous values.
- Support multiple raw members per document.
- Emit stable member identifiers, display names, source URLs, confidence, and resolution status.
- Keep unresolved, ambiguous, and conflicting identities explicit.
- Add fixture tests for exact match, alias match, multiple members, unresolved member, and ambiguous member cases.
- Emit a validation manifest with match counts, unresolved counts, ambiguity counts, and source authority version/hash.

### Should

- Support time-bounded identity resolution where official member records expose parliamentary service periods.
- Preserve raw source spelling and normalized comparison tokens.
- Provide a review table for low-confidence and ambiguous mappings.
- Document manual override rules and require provenance for every override.

### Could

- Add alternate-name and honorific stripping dictionaries.
- Add fuzzy matching as a review aid only.
- Add a small human-review UI/report for unresolved identities.

### Won't

- Infer identity from party, portfolio, title, or debate text without provenance.
- Claim authoritative identity where the source only provides raw text.
- Rewrite existing `stable_id` values.
- Publish derived member identity fields as part of `v0.1.0`.

## Design Amendments

- Add `derived/member_identity_authority.*` as a versioned authority artifact.
- Add a generated derived Parquet, for example `generated/derived/hansard_member_identity.parquet`.
- Add a tracked validation manifest, for example `manifests/member_identity_resolution_validation.json`.
- Candidate output fields:
  - `stable_id`
  - `member_of_parliament_raw`
  - `member_raw_token`
  - `member_id`
  - `member_display_name`
  - `member_authority_source`
  - `member_authority_url`
  - `member_resolution_method`
  - `member_resolution_confidence`
  - `member_resolution_status`
  - `member_resolution_notes`

## Acceptance Criteria

- The derived identity build is reproducible from tracked scripts plus documented authority inputs.
- Validation reports zero schema errors.
- Ambiguity and unresolved rates are visible before any publication decision.
- Dataset card and release docs clearly distinguish canonical document-level data from derived identity data.

