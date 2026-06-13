# Track member_identity_resolution_20260609 Context

Resolve `member_of_parliament_raw` into authoritative member identity fields as a derived dataset layer.

This track starts from the final document-level `v0.1.0` corpus and must not rewrite the canonical document-level release. It should produce derived identity artifacts with clear provenance, confidence, validation, and claim boundaries.

Current implementation surface:

- `derived/member_identity_authority.json`
- `samples/member-identity/member_identity_review.csv`
- `samples/member-identity/README.md`
- `docs/member-identity-resolution.md`
- `manifests/member_identity_resolution_package.json`
- `scripts/build_member_identity_review.py`
- `scripts/check_member_identity_resolution.py`
