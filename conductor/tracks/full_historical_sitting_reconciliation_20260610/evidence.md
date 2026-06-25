# Evidence

Release status: release-ready-reconciliation-contract-agent-review.

Evidence added:

- scripts/build_full_historical_sitting_reconciliation.py generates the reconciliation sample.
- scripts/check_full_historical_sitting_reconciliation.py validates schema, release status, track metadata, and non-claims.
- tests/test_full_historical_sitting_reconciliation.py exercises build and validation.
- samples/full-historical-sitting-reconciliation/sitting-reconciliation.json and .csv provide sample date-level sitting records across historical periods.

The evidence uses agent-review fallback rather than human review. It does not claim full historical coverage, all dates reconciled, or an authoritative complete sitting calendar; the complete historical sitting calendar remains the external authority-data requirement.

## Historical Sitting Inventory Source Coverage

The reconciliation contract is tied to `manifests/historical_sitting_inventory.json` and its source inventory. Required authority-source labels remain in scope for future full historical reconciliation:

- Parliamentary Business
- Historic Journals of the House
- Weekly Journals Archive
- Sessional Journals archive
- Indexes to the Journals
- Daily progress in the House

These references do not claim full historical sitting reconciliation is complete; they preserve the authority-source coverage contract for the future complete historical sitting calendar.

## Historical Sitting Reconciliation Contract

The release-ready sample contract preserves the full historical reconciliation dependency chain: a comparison-ready official inventory, a corpus ledger, and an unresolved-exception log are required before corpus-wide historical completeness can be claimed.

The repository-side sample is not a full comparison execution. Full historical reconciliation remains blocked on comparison execution between the official inventory and the corpus ledger after the complete historical sitting calendar is available.
