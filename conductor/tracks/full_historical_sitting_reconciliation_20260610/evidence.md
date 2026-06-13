# Evidence: Full Historical Sitting Reconciliation

Status: blocked.

Tracked artifacts:

- `spec.md`
- `plan.md`
- `metadata.json`
- `index.md`

What already exists:

- `manifests/historical_coverage_audit.json`
- `schemas/historical_coverage_audit.schema.json`
- `docs/historical-coverage-audit.md`
- `manifests/historical_sitting_reconciliation.json`
- `schemas/historical_sitting_reconciliation.schema.json`
- `docs/historical-sitting-reconciliation.md`
- `docs/historical-sitting-official-exports.md`
- `scripts/check_historical_coverage_audit.py`
- `scripts/check_historical_sitting_reconciliation.py`
- `scripts/check_historical_sitting_official_exports.py`
- `scripts/build_historical_sitting_official_exports.py`
- `conductor/tracks/historical_coverage_audit_20260609/`
- `conductor/tracks/sitting_proceeding_component_release_20260610/`

What this track would add:

- an official sitting/proceeding inventory reference
- comparison keys and tolerance rules
- a normalized sitting ledger derived from the corpus parquet
- missing, duplicate, partial, malformed, unavailable, inconsistent, and out-of-scope gap reporting
- acquisition priorities for unreconciled historical periods
- documentation language that can safely distinguish archive coverage from
  historical completeness
- a row-by-row comparison contract ready for execution
- a row by row execution note for the next reconciliation pass
- a missing, duplicate, partial, malformed, and unavailable gap taxonomy in the contract

Current blocker:

- The repo can prove supplied-archive coverage, and it now has an authoritative
  historical sitting inventory reference, but it still does not have a
  row-by-row comparison result against corpus holdings.
- The comparison ledger is now prepared and comparison-ready, but the
  historical comparison itself has not been executed.
- This remains blocked on comparison execution against the official PDF export
  surfaces.
- The live Parliament archive pages are reachable in desktop Chrome, and the
  browser DOM exposes direct PDF resource hrefs for weekly archive pages.
  Automated shell requests still hit the challenge layer on the HTML pages, so
  the remaining machine-readable step is to turn the browser-discovered article
  and PDF links into cached PDF inputs for the comparison pass.
- Without that comparison result, any claim of full historical NZ Hansard
  coverage would overstate the evidence.

Derived artifact now available:

- `derived/historical_sitting_official_exports/historical_sitting_official_export_index.json`
- `derived/historical_sitting_official_exports/historical_sitting_official_exports_coverage.json`
- `derived/historical_sitting_official_exports/weekly_journals_archive_index.json`
- cached PDF copies under `derived/historical_sitting_official_exports/pdf/`
- browser-crawled weekly archive page indexes:
  - `derived/historical_sitting_official_exports/weekly_journals_archive_page23.json`
  - `derived/historical_sitting_official_exports/weekly_journals_archive_page22.json`
  - `derived/historical_sitting_official_exports/weekly_journals_archive_page20.json`
  - `derived/historical_sitting_official_exports/weekly_journals_archive_page16.json`
  - `derived/historical_sitting_official_exports/weekly_journals_archive_page14.json`

Inventory discovery status:

- The official inventory now includes Parliamentary Business, Daily Progress,
  Order Paper, Weekly Journals Archive, Sessional Journals archive, Historic
  Journals of the House, Indexes to the Journals, and current Hansard.
- These source surfaces give the track a real historical reconciliation basis,
  and the repository now records the comparison contract for them.
- The blocker has narrowed from "no inventory" to "browser-discovered archive
  links have not yet been converted into a complete cached-PDF comparison set".

Date-level comparison probe result:

- official unique header dates: 191
- corpus unique sitting dates in the ledger: 409
- shared normalized dates: 29
- official years covered: 2010-2020
- ledger years covered: 2003-2016
- acquisition-priority years: 2003, 2004, 2007, 2008, 2009, 2012, 2013

Reference surfaces:

- `docs/historical-coverage-audit.md`
- `docs/historical-sitting-official-exports.md`
- `docs/interoperability-requirements-moscow.md`
- `docs/interoperability-design.md`
- `docs/endpoint-contracts.md`
- `manifests/authority_sources.json`
- `manifests/historical_sitting_inventory.json`
- `manifests/release_ladder.json`

Official inventory source IDs now recorded for the next reconciliation step:

- Parliamentary Business
- `nz-parliament-parliamentary-business-hub`
- Historic Journals of the House
- `nz-parliament-historic-journals-of-the-house`
- Daily progress in the House
- `nz-parliament-daily-progress`
- Indexes to the Journals
- `nz-parliament-journals-indexes`
- Order Paper
- `nz-parliament-order-paper`
- Weekly Journals Archive
- `nz-parliament-weekly-journals-archive`
- Sessional Journals archive
- `nz-parliament-sessional-journals-archive`
- Hansard
- `nz-parliament-hansard-current`

The inventory manifest is validated by `scripts/check_historical_sitting_inventory.py`.
The official export inventory is validated by
`scripts/check_historical_sitting_official_exports.py`.
The comparison contract is validated by `scripts/check_historical_sitting_reconciliation.py`.
The comparison-ready ledger is built by `scripts/build_historical_sitting_reconciliation.py`.
