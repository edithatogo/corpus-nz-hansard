# Parliament Video Seed Fetchers

Release posture: metadata-first/no-download seed evidence.

This track records bounded seed proofs for the video surfaces identified by `parliament_video_source_inventory_20260705`. It is not a video archive and does not claim retrospective or ongoing completeness.

## Policy

- Metadata-first only.
- No media download, including video or audio files.
- No public media release.
- No completeness claim.
- Fallback resources are validation-only until a later rights decision says otherwise.
- Rights review is required before any media acquisition.

## Target Inventory

Official source surfaces:

- `official-parliament-video`: Official Parliament Video platform (official-video-platform)
- `official-parliament-live-and-recorded`: Parliament website live and recorded video surface (official-website-video)
- `official-youtube-nz-parliament`: Official NZ Parliament YouTube channel (official-youtube-channel)
- `parliament-on-demand-house-archive`: Parliament On Demand house video archive (legacy-house-archive)
- `select-committee-on-demand-archive`: Select Committees On Demand archive (select-committee-archive)
- `select-committee-live-streams-current`: Current select committee livestream pages (current-committee-streams)
- `select-committee-vimeo-pages`: Vimeo pages linked from select committee livestream pages (vimeo-era-committee-pages)
- `parliament-website-embedded-video-pages`: Embedded Parliament website video pages (embedded-website-video)
- `parliament-site-search-and-sitemaps`: Parliament website search, sitemap, and feed discovery (site-discovery)

Fallback resources:

- `tvnz-archive-looking-back`: catalogue-only (TVNZ Archive / Looking Back historical footage references)
- `nga-taonga-av-collection`: catalogue-only (Nga Taonga Sound & Vision audiovisual collection search)
- `rnz-parliament`: evidence-only (RNZ Parliament reporting and audio evidence)
- `parliament-today-am-network`: evidence-only (Parliament Today and AM Network broadcast references)
- `archives-new-zealand-av-catalogue`: catalogue-only (Archives New Zealand audiovisual catalogue evidence)
- `internet-archive-webcaptures`: fallback-validation (Internet Archive web captures for Parliament video URLs)
- `memento-cdx-web-archives`: fallback-validation (Memento/CDX web-archive discovery)

| Source ID | Title | Role | Classification | Proof status |
| --- | --- | --- | --- | --- |
| `official-parliament-video` | Official Parliament Video platform | official | official | index-only |
| `official-parliament-live-and-recorded` | Parliament website live and recorded video surface | official | official | index-only |
| `official-youtube-nz-parliament` | Official NZ Parliament YouTube channel | official | rights-gated | fetched |
| `parliament-on-demand-house-archive` | Parliament On Demand house video archive | official | official | fetched |
| `select-committee-on-demand-archive` | Select Committees On Demand archive | official | official | index-only |
| `select-committee-live-streams-current` | Current select committee livestream pages | official | official | index-only |
| `select-committee-vimeo-pages` | Vimeo pages linked from select committee livestream pages | official | rights-gated | index-only |
| `parliament-website-embedded-video-pages` | Embedded Parliament website video pages | official | official | index-only |
| `parliament-site-search-and-sitemaps` | Parliament website search, sitemap, and feed discovery | official | official | index-only |
| `tvnz-archive-looking-back` | TVNZ Archive / Looking Back historical footage references | fallback | catalogue-only | index-only |
| `nga-taonga-av-collection` | Nga Taonga Sound & Vision audiovisual collection search | fallback | catalogue-only | fetched |
| `rnz-parliament` | RNZ Parliament reporting and audio evidence | fallback | evidence-only | fetched |
| `parliament-today-am-network` | Parliament Today and AM Network broadcast references | fallback | evidence-only | fetched |
| `archives-new-zealand-av-catalogue` | Archives New Zealand audiovisual catalogue evidence | fallback | catalogue-only | index-only |
| `internet-archive-webcaptures` | Internet Archive web captures for Parliament video URLs | fallback | fallback-validation | fetched |
| `memento-cdx-web-archives` | Memento/CDX web-archive discovery | fallback | fallback-validation | blocked |

## Fallback Resources

- `tvnz-archive-looking-back`: historical broadcast validation only.
- `nga-taonga-av-collection`: catalogue validation only.
- `rnz-parliament`: evidence-only reporting surface.
- `parliament-today-am-network`: evidence-only reporting surface.
- `archives-new-zealand-av-catalogue`: catalogue validation only.
- `internet-archive-webcaptures`: link-rot validation only.
- `memento-cdx-web-archives`: link-rot validation only.

## Output Layout

Seed artifacts are written beneath:

`derived/parliament_video_seed_fetchers/<source_family>/<source_id>/`

Each target writes bounded raw response artifacts plus the manifest entry describing request URLs, hashes, sample counts, and proof status.

## Handoff

The full metadata archive track should reuse these source IDs, request URLs, and rights boundaries.

The handoff requirements are:

1. keep request counts bounded in seed mode;
2. preserve hashes and timestamps;
3. promote only the approved sources with stable retrieval behavior;
4. keep blocked or deferred sources explicitly marked until the archive strategy changes.

No seed artifact in this track should be interpreted as a final corpus snapshot.
