# Track popolo_opencivicdata_public_endpoint_release_20260610 Context

Move Popolo/Open Civic Data from endpoint contract/sample readiness to a scope-declared public release package.

Repo-side builder/checker are implemented with gate `release-ready-sample-public-endpoint` after validated member identity, validated party attribution, validated vote/motion extraction, validated speech-turn, and validated sitting/proceeding became available.
This remains sample-only evidence and is not a full Popolo/Open Civic Data corpus release.

Current implementation surface:

- `schemas/popolo_opencivicdata_public_endpoint_validation.schema.json`
- `manifests/popolo_opencivicdata_public_endpoint_validation.json`
- `docs/popolo-opencivicdata-public-endpoint-release.md`
- `scripts/build_popolo_opencivicdata_public_endpoint.py`
- `scripts/check_popolo_opencivicdata_public_endpoint.py`
