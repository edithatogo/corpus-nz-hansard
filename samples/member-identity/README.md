# Member Identity Resolution Sample Package

Maintainer-review package for the derived member-identity layer.
This package is sample-not-release and is not release-readiness evidence.

- `member_identity_review.csv`

Validation and traceability:

- Manifest: `manifests/member_identity_resolution_validation.json`
- Package manifest: `manifests/member_identity_resolution_package.json`
- Authority table: `derived/member_identity_authority.json`
- Review table: `samples/member-identity/member_identity_review.csv`
- Gold evaluation fixtures: `fixtures/gold_evaluation_samples.json`
- Authority source discovery: `manifests/authority_sources.json`

Rules:

- Member identity is derived data, not a source column.
- Exact-name and honorific-normalized matches are resolved only against official Parliament authority sources.
- Semicolon-delimited raw values are split before matching.
- Office titles and generic headings remain unresolved or excluded.
- Ambiguous and unresolved cases remain explicit.

Known limitations:

- The package is local-review-only.
- The repo does not claim a published corpus-wide member identity release.
- Full publication still requires broader validation and historical authority coverage.
