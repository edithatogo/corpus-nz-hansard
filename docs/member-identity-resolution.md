# Member Identity Resolution

## Purpose

This repository keeps member identity as a derived layer with explicit provenance.

The local review package resolves reviewed gold fixtures only. It does not claim a
published corpus-wide member identity release.

## Authority Sources

The current review package uses official Parliament historical sources:

- Former Members of Parliament
- Roll of members of the New Zealand House of Representatives, 1854 onwards

These sources provide historical service periods and canonical member names for
exact and honorific-normalized resolution.

## Review Rules

- Exact raw-name matches resolve to canonical member records.
- Honorifics are stripped before matching aliases.
- Semicolon-delimited raw values are split into separate candidate member tokens.
- Office titles and generic headings remain unresolved or excluded.
- Ambiguous variants remain explicit and require authority matching before
  canonical publication.

## Sample Boundary

- `derived/member_identity_authority.json`
- `samples/member-identity/member_identity_review.csv`
- `samples/member-identity/README.md`
- `manifests/member_identity_resolution_validation.json`
- `manifests/member_identity_resolution_package.json`

## Corpus-Wide Release Gate

The corpus-wide release track is separate from the sample package:

- Builder: `scripts/build_corpus_wide_member_identity.py`
- Checker: `scripts/check_corpus_wide_member_identity.py`
- Schema: `schemas/corpus_wide_member_identity.schema.json`
- Validation manifest: `manifests/corpus_wide_member_identity_validation.json`
- Release-gate docs: `docs/corpus-wide-member-identity-release.md`

The current corpus-wide gate is blocked until `generated/parquet/hansard.parquet`
is available and authority coverage review passes. Any generated corpus-wide rows
must remain `blocked-pending-validation` until the validation manifest becomes
release-ready.

## Known Limits

- The package is local-review-only.
- No public derived member identity dataset is published here.
- Broader validation and historical coverage are still required for a full release.
