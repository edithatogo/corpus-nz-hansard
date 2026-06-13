# Evidence: Member Identity Resolution

Status: complete.

Implemented artifacts:

- `derived/member_identity_authority.json`
- `samples/member-identity/member_identity_review.csv`
- `samples/member-identity/README.md`
- `docs/member-identity-resolution.md`
- `manifests/member_identity_resolution_package.json`
- `scripts/build_member_identity_review.py`
- `scripts/check_member_identity_resolution.py`

Validation evidence:

- `python scripts/build_member_identity_review.py`
- `python scripts/check_member_identity_resolution.py`
- `python -m unittest tests.test_member_identity_resolution`
- `python -m unittest tests.test_member_identity_resolution tests.test_derived_fields_validation`
- `ruff check scripts/build_member_identity_review.py scripts/check_member_identity_resolution.py tests/test_member_identity_resolution.py`

Release boundary:

- Exact and honorific-normalized historical member matches are resolved from official Parliament sources.
- Office titles and generic headings remain unresolved or excluded.
- The review package is local-only and does not claim a published corpus-wide member identity release.
