# Evidence: Speech-Turn Validated Artifact Decision

Status: complete.

Implemented artifacts:

- `docs/speech-turn-release-decision.md`
- `manifests/speech_turn_release_decision.json`
- `scripts/check_speech_turn_release_decision.py`
- `tests/test_speech_turn_release_decision.py`
- updates to `docs/speech-turn-segmentation-contract.md`
- updates to `docs/speech-turn-segmentation-report.md`
- updates to `docs/derived-fields-validation.md`

Validation evidence:

- `python scripts/check_speech_turn_release_decision.py`
- `python -m unittest tests.test_speech_turn_release_decision`
- `python scripts/validate_derived_fields.py`
- `python -m unittest tests.test_derived_fields_validation`

Release boundary:

- Candidate speech-turn output remains a local heuristic review artifact.
- The public final scope explicitly excludes speech-turn candidates.
- Any future promotion requires validated member identity and separate segmentation validation.
