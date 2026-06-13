# Speech Turn Release Decision

## Decision

Speech-turn candidate output is explicitly excluded from the public final scope.

## Basis

- The current speech-turn pipeline is a heuristic MVP and is not authoritative.
- Speaker names are not identity-resolved.
- Party and electorate details are not extracted.
- Documents without tab-colon markers emit no turns.
- Validated member identity is not yet available, so speaker attribution cannot be promoted to an authoritative derived artifact.

## Current Boundary

- Keep `generated/parquet/hansard_speech_turns.parquet` as a local candidate review artifact.
- Keep `manifests/speech_turn_segmentation_validation.json` as blocked validation evidence for the heuristic segmenter.
- Do not include speech-turn candidates in the canonical document-level `v0.1.0` release.

## Future Validation Requirements

- Validated member identity must exist before any speech-turn component can be authoritative.
- Segmentation correctness must be evaluated separately from identity attribution.
- Hand-reviewed stratified samples must cover hard colon-marker, embedded-heading, no-speaker fallback, and multi-speaker cases.
- A later derived-release track must re-evaluate whether a validated speech-turn artifact should be published.

## Future Track

The repository now carries a blocked future-track surface in `validated_speech_turn_component_release_20260610`, which keeps the candidate output excluded while documenting the path to a validated component release once member identity and candidate-artifact prerequisites are satisfied.
