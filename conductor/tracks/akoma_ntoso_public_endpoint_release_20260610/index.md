# Track akoma_ntoso_public_endpoint_release_20260610 Context

Move Akoma Ntoso from sample output to a scope-declared public endpoint release.

Repo-side builder/checker are implemented, but the release is blocked until validated member identity, validated party attribution, validated speech-turn, validated motion, and validated vote components exist. This remains sample-only evidence rather than a public endpoint release.

Current implementation surface:

- `schemas/akoma_ntoso_public_endpoint_validation.schema.json`
- `manifests/akoma_ntoso_public_endpoint_validation.json`
- `docs/akoma-ntoso-public-endpoint-release.md`
- `scripts/build_akoma_ntoso_public_endpoint.py`
- `scripts/check_akoma_ntoso_public_endpoint.py`
