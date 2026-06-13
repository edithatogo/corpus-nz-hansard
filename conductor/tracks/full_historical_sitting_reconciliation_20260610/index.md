# Full Historical Sitting Reconciliation

Track ID: `full_historical_sitting_reconciliation_20260610`

Status: blocked.

## Goal

Move from supplied-archive coverage auditing to official full historical
sitting/proceeding reconciliation before completeness claims.

## Primary Artifacts

- `spec.md`
- `plan.md`
- `evidence.md`

## Blocker

The repo now has a settled official sitting/proceeding inventory reference, but
it still does not have a completed comparison against corpus holdings. Until
that comparison exists, historical completeness remains explicitly
unreconciled. The ledger preparation step is now complete, the official PDF
export path is now recorded, but the actual comparison result is still blocked
on execution against that export surface.

A derived PDF export index now exists at
`derived/historical_sitting_official_exports/historical_sitting_official_export_index.json`,
which confirms the official export path is machine-readable and ready for the
next comparison pass.

A date-level comparison probe now exists at
`derived/historical_sitting_official_exports/historical_sitting_official_exports_coverage.json`
and currently shows 191 official unique header dates, 409 unique ledger sitting
dates, and 29 shared normalized dates. That is still not the row-by-row
reconciliation result, but it is the first measurable overlap on the official
PDF path.

Browser-crawled Weekly Journals Archive page indexes also now exist for pages
23, 22, 20, 16, and 14, with direct PDF resource hrefs captured for the weekly
archive ranges covering 2006-2007, 2007-2008, 2008-2009, 2012, and 2013. Those
artifacts are ready to be turned into cached PDF comparison inputs.

A combined weekly archive index now exists at
`derived/historical_sitting_official_exports/weekly_journals_archive_index.json`.
It consolidates the browser-discovered article URLs, titles, and PDF hrefs from
those weekly archive pages into a single machine-readable input set.

The official PDFs currently cover years 2010-2020 in the discovered export
surfaces, while the ledger spans 2003-2016. That boundary explains why the
current comparison is partial and why earlier years still need a different
official source surface if they are to be reconciled fully.

The remaining acquisition-priority years are 2003, 2004, 2007, 2008, 2009,
2012, and 2013.

## Contract

The comparison contract now lives in
`manifests/historical_sitting_reconciliation.json` and
`docs/historical-sitting-reconciliation.md`.
