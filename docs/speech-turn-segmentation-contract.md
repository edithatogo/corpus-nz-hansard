# Speech Turn Segmentation Contract

## Purpose

Create a derived candidate speech-turn dataset from document-level Hansard `Content`.

## Status

Heuristic MVP. Not authoritative.

## Release Decision

Speech-turn candidates are explicitly excluded from the public final scope. See `docs/speech-turn-release-decision.md`.

## Inputs

- `generated/parquet/hansard.parquet`

Required columns:

- `parliament_document_id`
- `parliament_number`
- `document_type`
- `title`
- `content`
- `source_file`
- `source_row_number`

## Output

Output path:

- `generated/parquet/hansard_speech_turns.parquet`

Tracked validation:

- `manifests/speech_turn_segmentation_validation.json`

Output columns:

- `parliament_document_id`
- `parliament_number`
- `document_type`
- `title`
- `source_file`
- `source_row_number`
- `turn_index`
- `speaker_candidate`
- `speech_text`
- `confidence`
- `method`

## Heuristic

The MVP splits document content into tab-delimited fragments and looks for `speaker : speech` patterns. It emits one candidate turn per detected marker. Documents without detected turns are recorded in validation but do not emit fallback rows.

## Confidence

- `medium`: a speaker-like fragment and following speech fragment were detected.
- `low`: reserved for future fallback or weak extraction logic.

## Limitations

- Speaker candidates are raw text, not resolved member identities.
- Party and electorate details are not extracted.
- Procedural headings and question text may be mixed with speaker turns.
- Hansard editorial structure is not fully parsed.
- This output is suitable for exploratory review, not definitive quotation attribution.
- Candidate speech-turn output remains local and non-authoritative until a later track can validate member identity and segmentation separately.
