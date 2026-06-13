# Track popolo_opencivicdata_public_endpoint_release_20260610 Context

Move Popolo/Open Civic Data from maintainer-review sample output to a scope-declared public endpoint release.

Repo-side builder/checker are implemented, but the release is blocked until validated member identity, validated party attribution, validated vote/motion extraction, and validated speech-turn components exist. This remains sample-only evidence rather than a public endpoint release.

Current implementation surface:

- `schemas/popolo_opencivicdata_public_endpoint_validation.schema.json`
- `manifests/popolo_opencivicdata_public_endpoint_validation.json`
- `docs/popolo-opencivicdata-public-endpoint-release.md`
- `scripts/build_popolo_opencivicdata_public_endpoint.py`
- `scripts/check_popolo_opencivicdata_public_endpoint.py`
