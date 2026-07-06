# Parliament Video Ongoing Archive

Release posture: scheduled metadata refresh, gap monitoring, and no-download guard.

This track keeps the Parliament video archive moving without media downloads. It preserves prior snapshots, tracks source changes, and keeps the no-media boundary in force unless a later approved decision changes it.

## Refresh Policy

- Cadence: weekly
- Snapshot retention: 12
- Comparison basis: latest snapshot

## Thresholds

- Count regression: 1 source
- Stale-source threshold: 30 days
- Link-rot threshold: 1 failure
- Blocked-source threshold: 1 source

## Policy

- Metadata-first only.
- No media download.
- No public media release.
- No completeness claim.
- Rights review required before media acquisition.
- Fallbacks are validation only.

## Workflow

- Scheduled workflow: `.github/workflows/parliament-video-ongoing-archive.yml`
- Cron: `37 3 * * 0`

## Change Policy

- new_deletions
- new_sources
- deleted_sources
- changed_sources
- gap-ledger-updates-only

## Monitoring

| Metric | Count |
| --- | --- |
| Monitored sources | 19 |
| Monitored surfaces | 24 |
| New sources | 0 |
| Deleted sources | 0 |
| Changed sources | 0 |

## Operational Notes

- Stale sources are tracked from the fallback portion of the inventory and are reported even when access remains metadata-only.
- Link-rot watch covers archive-coverage surfaces and the metadata-only surfaces that are most likely to drift.
- The ongoing archive does not download Parliament video or audio files.
