# Evidence: Popolo/Open Civic Data Public Endpoint Release

Status: blocked.

Implemented artifacts:

- `schemas/popolo_opencivicdata_public_endpoint_validation.schema.json`
- `manifests/popolo_opencivicdata_public_endpoint_validation.json`
- `docs/popolo-opencivicdata-public-endpoint-release.md`
- `scripts/build_popolo_opencivicdata_public_endpoint.py`
- `scripts/check_popolo_opencivicdata_public_endpoint.py`
- `tests/test_popolo_opencivicdata_public_endpoint.py`

Validation evidence:

- `python scripts/build_popolo_opencivicdata_public_endpoint.py`
- `python scripts/check_popolo_opencivicdata_public_endpoint.py`
- `python -m unittest tests.test_popolo_opencivicdata_public_endpoint`

Release boundary:

- The current Popolo/Open Civic Data package remains a maintainer-review sample, not a public endpoint release.
- Validated member identity, party attribution, vote/motion extraction, and speech-turn components are not all available.
- Public endpoint publication remains deferred until the dependent component releases are validated.
