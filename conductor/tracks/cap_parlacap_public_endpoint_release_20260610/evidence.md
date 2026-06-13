# Evidence: CAP/ParlaCAP Public Endpoint Release

Status: blocked.

Implemented artifacts:

- `schemas/cap_parlacap_public_endpoint_validation.schema.json`
- `manifests/cap_parlacap_public_endpoint_validation.json`
- `docs/cap-parlacap-public-endpoint-release.md`
- `scripts/build_cap_parlacap_public_endpoint.py`
- `scripts/check_cap_parlacap_public_endpoint.py`
- `tests/test_cap_parlacap_public_endpoint.py`

Validation evidence:

- `python scripts/build_cap_parlacap_public_endpoint.py`
- `python scripts/check_cap_parlacap_public_endpoint.py`
- `python -m unittest tests.test_cap_parlacap_public_endpoint`

Release boundary:

- The current CAP/ParlaCAP package remains a maintainer-review sample, not a public endpoint release.
- Validated speech-turn exports are not yet available for public ParlaCAP-compatible speech/topic output.
- The repository-declared review map still awaits maintainer confirmation.
