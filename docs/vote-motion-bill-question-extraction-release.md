# Vote Motion Bill Question Extraction Release

## Decision

This track is release-ready for reviewed fixture extractions under `release-ready-fixture-reviewed-extraction-agent-review`.

## Basis

- Procedure fixtures cover party vote, personal vote, question, stage, ruling, and interjection boundaries.
- validated member identity, validated party attribution, and validated sitting/proceeding components are all available at release time.
- Five extractable procedure fixture rows are validated fixture extractions; the interjection row remains excluded-by-design.
- This is not a corpus-wide extraction completeness claim.

## Current Boundary

- Publish `derived/vote_motion_bill_question_extraction/extraction_review.csv` as the reviewed fixture extraction and boundary report.
- Keep `derived/vote_motion_bill_question_extraction/extraction_coverage.json` as the local coverage summary.
- Preserve authority-source, uncertainty, and exclusion boundaries for every vote, motion, bill, question, answer, and procedural decision sample.
- Do not infer full corpus-wide vote, motion, bill, question, answer, or procedural-decision coverage from the fixture release.

## Future Validation Requirements

- Corpus-wide extraction must be run against normalized Hansard inputs before broad release claims are made.
- Row-level sitting/proceeding reconciliation must mature before proceeding-level completeness is claimed.
- Motion, bill, vote, question, answer, and procedural decision claims must preserve the authority-source and uncertainty boundary recorded in the procedure model.

## Outputs

- `schemas/vote_motion_bill_question_extraction_validation.schema.json`
- `manifests/vote_motion_bill_question_extraction_validation.json`
- `derived/vote_motion_bill_question_extraction/extraction_coverage.json`
- `derived/vote_motion_bill_question_extraction/extraction_review.csv`
