# Evidence: Speech-Act And Procedure Classifiers

## Blocked

The track depends on validated speech-turn components that are not yet available.

## Dependencies

- `manifests/validated_speech_turn_component_validation.json`
- `manifests/nz_parliamentary_procedure_model.json`
- `fixtures/nz_parliamentary_procedure_samples.json`

## Label Families

- speech_act
- question_answer_structure
- interjection
- procedural_ruling
- debate_segment

## Planned Models

- Speech-act classifier outputs
- Question/answer structure classifier outputs
- Interjection classifier outputs
- Procedural ruling classifier outputs
- Debate-segment classifier outputs
- Review correction files
- Confusion analysis and benchmark notes

## Validation Commands

- `python scripts/build_speech_act_procedure_classifiers.py`
- `python scripts/check_speech_act_procedure_classifiers.py`
- `python -m unittest tests.test_speech_act_procedure_classifiers`
