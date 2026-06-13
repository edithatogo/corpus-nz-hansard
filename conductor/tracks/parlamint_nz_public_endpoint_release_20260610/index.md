# Track parlamint_nz_public_endpoint_release_20260610 Context

Move ParlaMint-NZ from endpoint contract/sample readiness to a scope-declared public release package.

Repo-side builder/checker are implemented, but the release is blocked until validated member identity, validated party attribution, validated speech-turn, and validated sitting/proceeding components exist.
This remains sample-only evidence rather than a public endpoint release.

Current implementation surface:

- `schemas/parlamint_nz_public_endpoint_validation.schema.json`
- `manifests/parlamint_nz_public_endpoint_validation.json`
- `docs/parlamint-nz-public-endpoint-release.md`
- `scripts/build_parlamint_nz_public_endpoint.py`
- `scripts/check_parlamint_nz_public_endpoint.py`
