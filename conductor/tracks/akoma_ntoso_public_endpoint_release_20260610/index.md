# Track akoma_ntoso_public_endpoint_release_20260610 Context

Move Akoma Ntoso from endpoint contract/sample readiness to a scope-declared public release package.

Repo-side builder/checker are implemented with gate `release-ready-sample-public-endpoint` after validated member identity, validated party attribution, validated speech-turn, validated motion, and validated vote became available.
This remains sample-only evidence and is not full Akoma Ntoso corpus or schema coverage.

Current implementation surface:

- `schemas/akoma_ntoso_public_endpoint_validation.schema.json`
- `manifests/akoma_ntoso_public_endpoint_validation.json`
- `docs/akoma-ntoso-public-endpoint-release.md`
- `scripts/build_akoma_ntoso_public_endpoint.py`
- `scripts/check_akoma_ntoso_public_endpoint.py`
