# Track cap_parlacap_public_endpoint_release_20260610 Context

Move CAP / ParlaCAP topic outputs from sample readiness to a scope-declared public endpoint package.

Repo-side builder/checker are implemented with gate `release-ready-sample-public-endpoint` after validated speech-turn became available.
This remains sample-only evidence; the codebook is not maintainer-confirmed and this is not a full CAP / ParlaCAP corpus release.

Current implementation surface:

- `schemas/cap_parlacap_public_endpoint_validation.schema.json`
- `manifests/cap_parlacap_public_endpoint_validation.json`
- `docs/cap-parlacap-public-endpoint-release.md`
- `scripts/build_cap_parlacap_public_endpoint.py`
- `scripts/check_cap_parlacap_public_endpoint.py`
