# Evidence: Gold Evaluation Datasets

## Evaluation Schema

- Added `schemas/gold_evaluation_sample.schema.json`.
- Added `schemas/gold_evaluation_datasets.schema.json`.
- Added `manifests/gold_evaluation_datasets.json` to define domains, required example classes, metrics, quality gates, and publication posture.

## Reviewed Fixtures

- Added `fixtures/gold_evaluation_samples.json`.
- Covered `member_resolution`, `party_attribution`, `speech_turn`, `vote`, and `topic_coding`.
- Included `positive`, `negative`, `ambiguous`, `unresolved`, and `excluded` examples for every domain.
- Recorded sampling frame, review status, reviewer, reviewed date, label provenance, source reference, and expected behavior for every sample.
- Prohibited model-generated labels from being treated as gold.

## Regression Metrics

- Recorded support for precision, recall, ambiguity rate, unresolved rate, and exclusion regression checks.
- Kept the fixture set compact and text-excerpt based so it remains Git-friendly.

## Release Gate Links

- Updated `docs/component-contracts.md`, `docs/endpoint-contracts.md`, `manifests/release_ladder.json`, `README.md`, and `docs/gold-evaluation-datasets.md`.
- Added `scripts/check_gold_evaluation_datasets.py` and `tests/test_gold_evaluation_datasets.py`.
- Wired the checker into `Makefile`, `.github/workflows/quality.yml`, `scripts/check_quality_gate.py`, and `docs/quality-gate.md`.

## Focused Validation

- `python scripts\check_gold_evaluation_datasets.py`
- `python -m unittest tests.test_gold_evaluation_datasets`
