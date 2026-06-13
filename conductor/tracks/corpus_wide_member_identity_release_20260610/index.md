# Corpus-Wide Member Identity Release

Track ID: `corpus_wide_member_identity_release_20260610`

Status: blocked.

## Goal

Promote the local member identity review package into a corpus-wide validated
derived component without changing the canonical document-level release.

## Primary Artifacts

- `spec.md`
- `plan.md`
- `evidence.md`
- `docs/corpus-wide-member-identity-coverage-review.md`

## Coverage Review

The authority coverage review is complete. Full report at
`docs/corpus-wide-member-identity-coverage-review.md`.

**Summary:**
- Authority rebuilt with enhancements: 403 records, 20 with aliases, all with placeholder URLs
- Fixes applied: reversed-name detection, near-duplicate merging, non-person token filtering
- Remaining issues: `Ang` still present, `Hon Aupito William Sio` honorific not stripped,
  `Tamati Coffey`/`Tāmati Coffey` duplicate unmerged, ~10 near-duplicate groups unconsolidated
- Human validation against official sources: NOT yet performed

## Blocker

The release remains blocked on authority coverage review. The coverage review
identified **5 must-fix items** and **5 should-fix items** that must be addressed
before the gate can advance. The corpus-wide builder produces a derived CSV from
the normalized parquet, but the result remains a blocked derived component rather
than a validated public release.
