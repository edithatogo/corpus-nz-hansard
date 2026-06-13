# Evidence: Akoma Ntoso Public Endpoint Release

Status: blocked.

Implemented artifacts:

- `schemas/akoma_ntoso_public_endpoint_validation.schema.json`
- `manifests/akoma_ntoso_public_endpoint_validation.json`
- `docs/akoma-ntoso-public-endpoint-release.md`
- `scripts/build_akoma_ntoso_public_endpoint.py`
- `scripts/check_akoma_ntoso_public_endpoint.py`
- `tests/test_akoma_ntoso_public_endpoint.py`

Validation evidence:

- `python scripts/build_akoma_ntoso_public_endpoint.py`
- `python scripts/check_akoma_ntoso_public_endpoint.py`
- `python -m unittest tests.test_akoma_ntoso_public_endpoint`

Release boundary:

- The current Akoma Ntoso package remains a maintainer-review sample, not a public endpoint release.
- Validated member identity, party attribution, speech-turn, motion, and vote components are not all available.
- Public endpoint publication remains deferred until the dependent component releases are validated.
