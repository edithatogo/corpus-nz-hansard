# Parliament Video Reconciliation

Release posture: metadata-first reconciliation ledger.

This track reconciles Parliament video metadata against multiple independent sources before any completeness claim. It is explicitly not a complete retrospective archive and it does not permit a media-completeness claim.

## Policy

- Metadata-first only.
- No video-file download in this track.
- No audio-file download in this track.
- No public media release.
- No completeness claim.
- Rights review required before media acquisition.
- Fallback sources are validation only.

## Inputs

- `manifests/parliament_video_source_inventory.json`
- `manifests/parliament_video_seed_fetchers.json`
- `manifests/parliament_video_archive_coverage.json`

## Summary

| Field | Value |
| --- | --- |
| Source count | 19 |
| Official sources | 9 |
| Fallback sources | 7 |
| Supporting boundary sources | 3 |
| Seed targets | 16 |
| Ledger rows | 22 |
| Metadata reconciled | 9 |
| Rights gated | 2 |
| Fallback only | 4 |
| Evidence only | 8 |
| Access blocked | 1 |
| Migrated | 1 |
| Missing everywhere | 0 |

Retrospective archive complete: False
Ongoing archive complete: False
Complete video archive: False

## Gap Taxonomy

- metadata-only
- rights-gated
- fallback-only
- evidence-only
- access-blocked
- migrated
- missing-everywhere

## Source Priorities

- 1. Official Parliament video surfaces: `official-parliament-video`, `official-parliament-live-and-recorded`, `parliament-on-demand-house-archive`, `select-committee-on-demand-archive`, `select-committee-live-streams-current`, `parliament-website-embedded-video-pages`, `parliament-site-search-and-sitemaps`
- 2. Rights-gated official platform mirrors: `official-youtube-nz-parliament`, `select-committee-vimeo-pages`
- 3. Fallback validation sources: `tvnz-archive-looking-back`, `nga-taonga-av-collection`, `archives-new-zealand-av-catalogue`, `rnz-parliament`, `parliament-today-am-network`, `internet-archive-webcaptures`, `memento-cdx-web-archives`
- 4. Adjacent repository boundaries: `adjacent-sm-govt-nz`, `adjacent-hathi-nz`, `adjacent-corpus-law-nz`

## Cross Checks

- `inventory-manifest`: 9 official, 7 fallback, 3 supporting sources are inventoried. (manifests/parliament_video_source_inventory.json)
- `seed-fetchers-manifest`: 16 seed targets prove metadata-only retrieval, blocked states, and fallback validation roles. (manifests/parliament_video_seed_fetchers.json)
- `archive-coverage-manifest`: retrospective_archive_complete and ongoing_archive_complete remain false, so no completeness claim is made. (manifests/parliament_video_archive_coverage.json)
- `adjacent-repo-boundaries`: sm-govt-nz stays metadata-only; hathi-nz and corpus-law-nz remain not-applicable for video coverage. (manifests/parliament_video_archive_coverage.json)

## Exception Ledger

| Source | Gap status | Classification | Seed proof |
| --- | --- | --- | --- |
| `official-parliament-video` | metadata-only | official | index-only |
| `official-parliament-live-and-recorded` | metadata-only | official | index-only |
| `official-youtube-nz-parliament` | rights-gated | rights-gated | fetched |
| `parliament-on-demand-house-archive` | migrated | official | fetched |
| `select-committee-on-demand-archive` | metadata-only | official | index-only |
| `select-committee-live-streams-current` | metadata-only | official | index-only |
| `select-committee-vimeo-pages` | rights-gated | rights-gated | index-only |
| `parliament-website-embedded-video-pages` | metadata-only | official | index-only |
| `parliament-site-search-and-sitemaps` | metadata-only | official | index-only |
| `tvnz-archive-looking-back` | fallback-only | catalogue-only | index-only |
| `nga-taonga-av-collection` | fallback-only | catalogue-only | fetched |
| `rnz-parliament` | evidence-only | evidence-only | fetched |
| `parliament-today-am-network` | evidence-only | evidence-only | fetched |
| `archives-new-zealand-av-catalogue` | fallback-only | catalogue-only | index-only |
| `internet-archive-webcaptures` | fallback-only | fallback-validation | fetched |
| `memento-cdx-web-archives` | access-blocked | fallback-validation | blocked |
| `adjacent-sm-govt-nz` | evidence-only | evidence-only | not-seeded |
| `adjacent-hathi-nz` | evidence-only | evidence-only | not-seeded |
| `adjacent-corpus-law-nz` | evidence-only | evidence-only | not-seeded |
| `sm-govt-nz` | evidence-only | evidence-only | not-applicable |
| `hathi-nz` | evidence-only | evidence-only | not-applicable |
| `corpus-law-nz` | evidence-only | evidence-only | not-applicable |

## Residual Gaps

- Rights-gated surfaces remain constrained by platform terms or media rights review.
- TVNZ Archive, Ngā Taonga, Archives New Zealand, RNZ, Parliament Today, and web archives remain validation-only evidence rather than acquisition permissions.
- The repository still does not have a complete retrospective archive or a complete ongoing archive.

## Next Actions

- Feed this reconciliation result into the full metadata archive track.
- Keep future completeness claims gated on additional authority evidence, not metadata presence alone.
- Preserve the distinction between metadata completeness and media completeness in downstream documentation.
