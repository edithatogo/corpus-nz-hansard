# Evidence: Historical Coverage Audit

## Coverage Manifest

- Added `manifests/historical_coverage_audit.json`.
- Added `schemas/historical_coverage_audit.schema.json`.
- Recorded verified supplied-archive claims, partial Parliament 47-54 source-file coverage, unknown full historical NZ Hansard completeness, and excluded out-of-extract periods.

## Archive Versus Historical Claims

- Verified the supplied DocumentsDB archive SHA-256 against `manifests/source_inventory.json`.
- Verified eight source members and 193,922 normalized rows against `manifests/normalization_validation.json`.
- Kept every Parliament 47-54 coverage row marked `partial`, because file presence and row preservation do not prove complete sitting or proceeding coverage.

## Authority Cross-Check

- Linked historical reconciliation to authority-source candidates in `manifests/authority_sources.json`.
- Recorded that `nz-parliament-hansard-current`, `nz-parliament-order-paper`, and `nz-parliament-daily-progress` are available but not yet reconciled to source rows.
- Kept pre-47, within-47-54, and post-snapshot gaps explicit.

## Release And Endpoint Language

- Updated `README.md`, `DATASET_CARD.md`, and `docs/endpoint-contracts.md` so public and endpoint language cites `manifests/historical_coverage_audit.json`.
- Added `docs/historical-coverage-audit.md` as the human-readable coverage report.
- Added a quality-gate checker and unittest so future edits cannot silently claim full historical NZ Hansard coverage.

## Focused Validation

- `python scripts\check_historical_coverage_audit.py`
- `python -m unittest tests.test_historical_coverage_audit`
