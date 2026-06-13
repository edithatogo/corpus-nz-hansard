# Track cap_parlacap_public_endpoint_release_20260610 Context

Move CAP/ParlaCAP from sample topic output to a scope-declared public endpoint release.

Repo-side builder/checker are implemented, but the release is blocked until validated speech-turn components exist and maintainer-confirmed codebook intake is available. This remains sample-only evidence rather than a public endpoint release.

Current implementation surface:

- `schemas/cap_parlacap_public_endpoint_validation.schema.json`
- `manifests/cap_parlacap_public_endpoint_validation.json`
- `docs/cap-parlacap-public-endpoint-release.md`
- `scripts/build_cap_parlacap_public_endpoint.py`
- `scripts/check_cap_parlacap_public_endpoint.py`
