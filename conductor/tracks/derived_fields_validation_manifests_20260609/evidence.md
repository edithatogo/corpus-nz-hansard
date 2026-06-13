# Evidence: Derived Fields Validation Manifests

Status: complete.

Implemented artifacts:

- `docs/derived-fields-validation.md`
- `schemas/derived_fields_validation.schema.json`
- `scripts/validate_derived_fields.py`
- `manifests/member_identity_resolution_validation.json`
- `manifests/party_attribution_validation.json`
- `manifests/speech_turn_validated_artifact_validation.json`
- `tests/test_derived_fields_validation.py`

Validation evidence:

- `python scripts/validate_derived_fields.py`
- `python -m unittest tests.test_derived_fields_validation`
- `python scripts/check_quality_gate.py`
- `ruff check scripts/validate_derived_fields.py tests/test_derived_fields_validation.py`

Release gate status:

- Member identity validation remains blocked pending implementation.
- Party attribution validation remains blocked pending validated member identity and temporal authority inputs.
- Speech-turn validation remains blocked pending validated member identity and explicit release-decision handling.
