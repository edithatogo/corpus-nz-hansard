# Track speech_turn_validated_artifact_20260609 Context

Promote speech-turn segmentation from candidate/non-authoritative output to a validated derived artifact, or explicitly keep it excluded from public final scope.

This track builds on `speech_turn_segmentation_20260603`, which produced conservative candidate tooling but did not support authoritative speech attribution.

Current implementation surface:

- `docs/speech-turn-release-decision.md`
- `manifests/speech_turn_release_decision.json`
- `scripts/check_speech_turn_release_decision.py`
- `tests/test_speech_turn_release_decision.py`
