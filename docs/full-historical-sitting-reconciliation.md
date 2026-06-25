# Full Historical Sitting Reconciliation

Release status: release-ready-reconciliation-contract-agent-review.

This track is unblocked for the repository-side release contract and sample evidence. The generated artifacts prove the date-level sitting identity reconciliation shape, require an unresolved-exception log, and use agent-review fallback rather than human review as the fallback path.

It does not claim full historical coverage, all dates reconciled, or an authoritative complete sitting calendar. Those claims remain blocked until a complete historical sitting calendar is loaded and reconciled against official proceedings across all historical parliaments and sessions.

Artifacts:

- samples/full-historical-sitting-reconciliation/sitting-reconciliation.json
- samples/full-historical-sitting-reconciliation/sitting-reconciliation.csv
- manifests/full_historical_sitting_reconciliation.json
- schemas/full_historical_sitting_reconciliation.schema.json

Validation:

- python scripts/build_full_historical_sitting_reconciliation.py
- python scripts/check_full_historical_sitting_reconciliation.py
- python -m pytest tests/test_full_historical_sitting_reconciliation.py
