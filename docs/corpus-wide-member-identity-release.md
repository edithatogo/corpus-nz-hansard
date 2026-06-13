# Corpus-Wide Member Identity Release

## Purpose

This release track promotes member identity resolution from the local reviewed sample package toward a corpus-wide derived component. It does not change the canonical document-level `v0.1.0` corpus.

## Current Release Gate

The current gate is blocked, not published.

- `blocked-pending-corpus-artifact`: the normalized corpus artifact `generated/parquet/hansard.parquet` is not present in this working tree.
- `blocked-pending-authority-coverage-review`: **Coverage review complete** — see [coverage review report](corpus-wide-member-identity-coverage-review.md). The authority snapshot is corpus-derived with some automated enhancements (reversed-name detection, authority URL generation, near-duplicate merging) but is NOT yet human-validated against official NZ Parliament sources. The review identifies **5 must-fix items** and **5 should-fix items** before the gate can advance.

Coverage review findings summary:
1. 403 records (not 4,505 as originally stated — discrepancy needs clarification)
2. 3 non-person entries remain (1 still in authority: `Ang`)
3. 1 honorific still embedded in canonical name (`Hon Aupito William Sio`)
4. 1 confirmed duplicate unmerged (`Tamati Coffey` ↔ `Tāmati Coffey`)
5. 100% authority URLs now populated (placeholder format)
6. 0% service periods populated
7. Near-duplicate groups (~10 groups) still require human consolidation
8. Zero cross-referencing done against official member-domain sources

The generated validation manifest is `manifests/corpus_wide_member_identity_validation.json`. Its release decision must remain `defer` until corpus input, authority coverage (must-fix items addressed), unresolved-case review, and validation gates pass.

## Contract

The corpus-wide builder consumes normalized Hansard records and emits:

- `derived/corpus_wide_member_identity/member_identity.csv`
- `derived/corpus_wide_member_identity/member_identity_review_queue.csv`
- `derived/corpus_wide_member_identity/member_identity_review_overrides.csv`
- `schemas/corpus_wide_member_identity.schema.json`
- `manifests/corpus_wide_member_identity_validation.json`

The row contract preserves source document evidence:

- `source_stable_id`
- `source_file`
- `source_row_number`
- `parliament_number`
- `parliament_document_id`
- `document_type`
- `document_content_date`
- `source_hash`
- `member_of_parliament_raw`
- `member_raw_token`

Resolution statuses distinguish:

- `exact`
- `alias`
- `multi-person`
- `unresolved`
- `ambiguous`
- `conflict`

## Review Overrides

Human review overrides are kept separate in `derived/corpus_wide_member_identity/member_identity_review_overrides.csv`. Overrides must be auditable and must not silently mutate the raw source token or canonical document records.

## Non-Claims

- The current output must not be published as a validated component.
- Unresolved, ambiguous, and conflict rows are not authoritative identity claims.
- The document-level corpus remains unchanged.
- Downstream party attribution, Popolo/Open Civic Data, ParlaMint-NZ, RDF, and speech-turn tracks must treat this layer as blocked until the validation manifest becomes release-ready.
