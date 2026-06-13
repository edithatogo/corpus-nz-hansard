# Evidence: Corpus-Wide Member Identity Release

## Status

Blocked — coverage review complete, builder enhanced, but release still blocked.

## Coverage Review (2026-06-12)

A full coverage audit was performed against the auto-derived member identity authority. See the full report at `docs/corpus-wide-member-identity-coverage-review.md`.

**Key findings:**

| Finding | Detail |
|---------|--------|
| Records in authority | 403 (down from 408 after builder enhancements merged near-duplicates and corrected reversed names) |
| Record count discrepancy | Task brief stated 4,505; actual is 403 (~90% less) |
| Authority URLs | 100% populated (placeholder URLs via NZ Parliament former-members pattern) |
| Service periods | 0% populated |
| Records with aliases | 20 (up from 2 after builder enhancements merged near-duplicates) |
| Non-person entries | `Ang` still present (was 3, now 1 — `Presiding Officer` and `The Clerk` filtered) |
| Honorific in canonical name | `Hon Aupito William Sio` still present |
| Reversed names | Fixed: `Foster-Bell Paul` → `Paul Foster-Bell` (builder enhancement) |
| Confirmed duplicate | `Tamati Coffey` ↔ `Tāmati Coffey` still unmerged |
| Near-duplicate groups | ~10 groups still need human consolidation |
| Cross-referenced vs official sources | 0 of 5 official sources checked |

**Verdict:** ⛔ BLOCKED — 5 must-fix items and 5 should-fix items remain.

## Builder Enhancements (2026-06-12)

`scripts/expand_member_authority.py` was enhanced with:

1. **Extended IGNORED_TOKENS** — `Presiding Officer`, `The Clerk`, `Clerk` now filtered
2. **Reversed-name detection** — `Foster-Bell Paul` corrected to `Paul Foster-Bell`
3. **Authority URL generation** — placeholder URLs using NZ Parliament former-members URL pattern
4. **Near-duplicate merging** — records differing only by middle name merged (e.g., `Hilary Jane Calvert` + `Hilary Calvert`)
5. **20 new tests** added to `tests/test_corpus_wide_member_identity.py` (all passing)

Authority rebuilt: **403 records**, **20 with aliases**, all with placeholder URLs.

## Implemented

- `scripts/build_corpus_wide_member_identity.py`
- `scripts/check_corpus_wide_member_identity.py`
- `scripts/expand_member_authority.py` (enhanced)
- `schemas/corpus_wide_member_identity.schema.json`
- `docs/corpus-wide-member-identity-release.md`
- `docs/corpus-wide-member-identity-coverage-review.md`
- `tests/test_corpus_wide_member_identity.py`
- `manifests/corpus_wide_member_identity_validation.json`
- `derived/corpus_wide_member_identity/member_identity.csv`
- `derived/corpus_wide_member_identity/member_identity_review_queue.csv`
- `derived/corpus_wide_member_identity/member_identity_review_overrides.csv`
- `derived/corpus_wide_member_identity_authority.json` (rebuilt)

## Release Decision

Decision: defer.

Reasons:

- Coverage review identified 5 must-fix items: remove `Ang`, strip honorific from `Hon Aupito William Sio`, merge `Tamati Coffey` ↔ `Tāmati Coffey`, review near-duplicate groups, human-validate against official sources.
- Authority snapshot is corpus-derived and not yet human-validated against official sources.
- Any generated corpus-wide output must remain `blocked-pending-authority-coverage-review` until authority coverage and unresolved-case review are complete.
- The produced CSV contains blocked derived rows and is not a validated public release.

## Validation Commands

- `python scripts\expand_member_authority.py` (rebuild authority)
- `python scripts\build_corpus_wide_member_identity.py` (rebuild from parquet)
- `python scripts\check_corpus_wide_member_identity.py`
- `python scripts\validate_derived_fields.py`
- `python -m unittest tests.test_corpus_wide_member_identity -v`
- `ruff check scripts\expand_member_authority.py scripts\build_corpus_wide_member_identity.py scripts\check_corpus_wide_member_identity.py tests\test_corpus_wide_member_identity.py`
