# Track vote_motion_bill_question_extraction_release_20260610 Context

Implement validated corpus-wide extraction for votes, motions, bills, oral/written questions, answers, and procedural decisions.

Repo-side builder/checker are implemented, but the release is blocked until validated member identity, validated party attribution, and validated sitting/proceeding components exist.

Current implementation surface:

- `schemas/vote_motion_bill_question_extraction_validation.schema.json`
- `manifests/vote_motion_bill_question_extraction_validation.json`
- `derived/vote_motion_bill_question_extraction/extraction_coverage.json`
- `derived/vote_motion_bill_question_extraction/extraction_review.csv`
- `docs/vote-motion-bill-question-extraction-release.md`
- `scripts/build_vote_motion_bill_question_extraction.py`
- `scripts/check_vote_motion_bill_question_extraction.py`
