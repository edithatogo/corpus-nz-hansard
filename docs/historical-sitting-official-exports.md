# Historical Sitting Official Exports

This note records the official PDF export surfaces discovered for historical
sitting reconciliation.

## What Is Confirmed

- Parliament publishes Journals of the House in draft, weekly, and sessional stages.
- The Journals are the official record of proceedings.
- Weekly and sessional journal PDFs are directly reachable on `www3.parliament.nz`.

## Confirmed PDF Surfaces

- 49th Parliament weekly journal PDF
- 51st Parliament sessional schedules PDF
- 52nd Parliament sessional schedules PDF

## Boundary

These official PDF export surfaces are evidence for a stable machine-readable
export path.
They are not, by themselves, the completed row-by-row reconciliation result.

The remaining work is to drive the compare against these PDF exports rather than
against the HTML challenge layer on the archive pages.

The repository also now has a date-level comparison probe at
`derived/historical_sitting_official_exports/historical_sitting_official_exports_coverage.json`.

That probe currently shows the discovered official PDF surfaces covering
2010-2020, while the normalized ledger spans 2003-2016. The uncovered ledger
years are 2003, 2004, 2007, 2008, 2009, 2012, and 2013.

In addition, browser-based crawling of the Weekly Journals Archive now has
saved page indexes for archive pages covering 2006-2007, 2007-2008, 2008-2009,
2012, and 2013:

- `derived/historical_sitting_official_exports/weekly_journals_archive_page23.json`
- `derived/historical_sitting_official_exports/weekly_journals_archive_page22.json`
- `derived/historical_sitting_official_exports/weekly_journals_archive_page20.json`
- `derived/historical_sitting_official_exports/weekly_journals_archive_page16.json`
- `derived/historical_sitting_official_exports/weekly_journals_archive_page14.json`

Those browser-discovered archive links expose direct PDF resource hrefs, but
they still need to be turned into cached comparison inputs before the row-by-row
reconciliation can run.

A combined weekly archive index now exists at
`derived/historical_sitting_official_exports/weekly_journals_archive_index.json`
for the browser-crawled pages above. It records the article URLs, titles, and
PDF hrefs from the weekly archive surface and provides a reproducible input set
for future cached PDF acquisition.
