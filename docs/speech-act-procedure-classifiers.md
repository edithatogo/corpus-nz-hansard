# Speech-Act And Procedure Classifiers

## Scope

This track defines the future classifier surface for speech acts, question/answer structure, interjections, procedural rulings, and debate segments. The track is release-ready as a baseline plan because validated speech-turn components are available.

## Gate

- Validated speech-turn component release
- NZ parliamentary procedure model
- Human validation required before authoritative classifier outputs

## Label Families

- speech_act
- question_answer_structure
- interjection
- procedural_ruling
- debate_segment

## Planned Models

The initial release candidate is intended to use optional ML dependencies from
`requirements/ml.txt` with scikit-learn baselines for reproducible review tooling.

## Evaluation Design

- Reviewed procedure fixtures will seed the first benchmark set.
- Correction files will capture reviewer overrides and false positives.
- Confusion analysis will remain tied to the procedure model rather than raw text.
- `derived/speech-act-procedure-classifiers/evaluation.json` records a reviewed-fixture smoke evaluation and selector checks.

## Boundaries

- No authoritative procedural classification may be published from unvalidated
  speech-turn output.
- Speech-turn readiness is a hard gate, not a soft preference.
- The fixture evaluation is not a corpus-wide accuracy claim or an authoritative classifier release.
