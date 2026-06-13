# Vote Motion Bill Question Extraction Release

## Decision

This track is implemented as a blocked extraction release surface.

## Basis

- Procedure fixtures cover party vote, personal vote, question, stage, ruling, and interjection boundaries.
- Neutral fixtures cover the related motion, vote, and bill component families.
- validated member identity, validated party attribution, and validated sitting/proceeding components are not all available at release time.

## Current Boundary

- Keep `derived/vote_motion_bill_question_extraction/extraction_review.csv` as a local review queue and boundary report.
- Keep `derived/vote_motion_bill_question_extraction/extraction_coverage.json` as a local coverage summary.
- Keep `manifests/vote_motion_bill_question_extraction_validation.json` blocked until the dependent component releases are validated.

## Future Validation Requirements

- validated member identity and validated party attribution must exist before releasing vote rows that depend on named members or party labels.
- validated sitting/proceeding reconciliation must be complete before releasing question and procedural decision rows.
- Motion, bill, vote, question, answer, and procedural decision claims must preserve the authority-source and uncertainty boundary recorded in the procedure model.

## Outputs

- `schemas/vote_motion_bill_question_extraction_validation.schema.json`
- `manifests/vote_motion_bill_question_extraction_validation.json`
- `derived/vote_motion_bill_question_extraction/extraction_coverage.json`
- `derived/vote_motion_bill_question_extraction/extraction_review.csv`
