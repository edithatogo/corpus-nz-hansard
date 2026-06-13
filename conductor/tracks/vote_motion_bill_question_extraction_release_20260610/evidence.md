# Evidence: Vote Motion Bill Question Extraction Release

Status: blocked.

Implemented artifacts:

- `schemas/vote_motion_bill_question_extraction_validation.schema.json`
- `manifests/vote_motion_bill_question_extraction_validation.json`
- `derived/vote_motion_bill_question_extraction/extraction_coverage.json`
- `derived/vote_motion_bill_question_extraction/extraction_review.csv`
- `docs/vote-motion-bill-question-extraction-release.md`
- `scripts/build_vote_motion_bill_question_extraction.py`
- `scripts/check_vote_motion_bill_question_extraction.py`

Validation evidence:

- `python scripts/build_vote_motion_bill_question_extraction.py`
- `python scripts/check_vote_motion_bill_question_extraction.py`
- `python scripts/validate_derived_fields.py`
- `python -m unittest tests.test_vote_motion_bill_question_extraction tests.test_derived_fields_validation`
- `ruff check scripts/build_vote_motion_bill_question_extraction.py scripts/check_vote_motion_bill_question_extraction.py tests/test_vote_motion_bill_question_extraction.py`

Release boundary:

- Procedure samples are reviewed boundary evidence, not published extraction outputs.
- Vote rows remain blocked until validated member identity and party attribution exist.
- Question and procedural-decision rows remain blocked until sitting/proceeding validation is complete.
