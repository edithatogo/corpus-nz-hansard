# Evidence: ParlaMint-NZ Public Endpoint Release

Status: blocked.

Implemented artifacts:

- `schemas/parlamint_nz_public_endpoint_validation.schema.json`
- `manifests/parlamint_nz_public_endpoint_validation.json`
- `docs/parlamint-nz-public-endpoint-release.md`
- `scripts/build_parlamint_nz_public_endpoint.py`
- `scripts/check_parlamint_nz_public_endpoint.py`

Validation evidence:

- `python scripts/build_parlamint_nz_public_endpoint.py`
- `python scripts/check_parlamint_nz_public_endpoint.py`
- `python -m unittest tests.test_parlamint_nz_public_endpoint`

Release boundary:

- The current ParlaMint-NZ package remains a maintainer-review sample, not a public endpoint release.
- Validated member identity, party attribution, speech-turn, and sitting/proceeding components are not all available.
- Public endpoint publication remains deferred until the dependent component releases are validated.
