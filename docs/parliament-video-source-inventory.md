# Parliament Video Source Inventory

Release posture: metadata-first/no-download source inventory.

This inventory records public NZ Parliament video source surfaces and validation fallbacks. It is an input to `parliament_video_seed_fetchers_20260705`; it is not a media archive and does not claim retrospective or ongoing completeness.

## Policy

- Metadata-first only.
- No media download, including video or audio files.
- No public media release.
- No completeness claim.
- Fallback resources are validation-only until a later rights decision says otherwise.
- Rights review is required before any media acquisition.

## Taxonomy

- Source families: house_video, select_committee_video, parliament_website_embeds, social_video_platform, broadcast_archive, audio_reporting, web_archive, adjacent_repo_evidence
- Platform classes: official_parliament_video, official_parliament_website, youtube, vimeo, parliament_on_demand, broadcast_catalogue, audio_reporting, web_archive, repository, search_or_sitemap
- Fallback roles: not_fallback, historical_broadcast_validation, catalogue_validation, audio_or_reporting_validation, link_rot_validation, boundary_evidence
- Rights statuses: rights_review_required, platform_terms_review_required, fallback_rights_review_required, web_archive_rights_review_required, not_media_source
- Archive statuses: external_source_identified, fallback_evidence_only, supporting_evidence_only, blocked_or_unknown

## Source Inventory

Official source surfaces:

- `official-parliament-video`: Official Parliament Video platform (official_parliament_video)
- `official-parliament-live-and-recorded`: Parliament website live and recorded video surface (official_parliament_website)
- `official-youtube-nz-parliament`: Official NZ Parliament YouTube channel (youtube)
- `parliament-on-demand-house-archive`: Parliament On Demand house video archive (parliament_on_demand)
- `select-committee-on-demand-archive`: Select Committees On Demand archive (parliament_on_demand)
- `select-committee-live-streams-current`: Current select committee livestream pages (official_parliament_website)
- `select-committee-vimeo-pages`: Vimeo pages linked from select committee livestream pages (vimeo)
- `parliament-website-embedded-video-pages`: Embedded Parliament website video pages (official_parliament_website)
- `parliament-site-search-and-sitemaps`: Parliament website search, sitemap, and feed discovery (search_or_sitemap)

| Source ID | Title | Role | Fallback role | Archive status |
| --- | --- | --- | --- | --- |
| `official-parliament-video` | Official Parliament Video platform | official | not_fallback | external_source_identified |
| `official-parliament-live-and-recorded` | Parliament website live and recorded video surface | official | not_fallback | external_source_identified |
| `official-youtube-nz-parliament` | Official NZ Parliament YouTube channel | official | not_fallback | external_source_identified |
| `parliament-on-demand-house-archive` | Parliament On Demand house video archive | official | not_fallback | external_source_identified |
| `select-committee-on-demand-archive` | Select Committees On Demand archive | official | not_fallback | external_source_identified |
| `select-committee-live-streams-current` | Current select committee livestream pages | official | not_fallback | external_source_identified |
| `select-committee-vimeo-pages` | Vimeo pages linked from select committee livestream pages | official | not_fallback | external_source_identified |
| `parliament-website-embedded-video-pages` | Embedded Parliament website video pages | official | not_fallback | external_source_identified |
| `parliament-site-search-and-sitemaps` | Parliament website search, sitemap, and feed discovery | official | not_fallback | external_source_identified |
| `tvnz-archive-looking-back` | TVNZ Archive / Looking Back historical footage references | fallback | historical_broadcast_validation | fallback_evidence_only |
| `nga-taonga-av-collection` | Nga Taonga Sound & Vision audiovisual collection search | fallback | catalogue_validation | fallback_evidence_only |
| `rnz-parliament` | RNZ Parliament reporting and audio evidence | fallback | audio_or_reporting_validation | fallback_evidence_only |
| `parliament-today-am-network` | Parliament Today and AM Network broadcast references | fallback | audio_or_reporting_validation | fallback_evidence_only |
| `archives-new-zealand-av-catalogue` | Archives New Zealand audiovisual catalogue evidence | fallback | catalogue_validation | fallback_evidence_only |
| `internet-archive-webcaptures` | Internet Archive web captures for Parliament video URLs | fallback | link_rot_validation | fallback_evidence_only |
| `memento-cdx-web-archives` | Memento/CDX web-archive discovery | fallback | link_rot_validation | fallback_evidence_only |
| `adjacent-sm-govt-nz` | Adjacent repo evidence: sm-govt-nz | supporting | boundary_evidence | supporting_evidence_only |
| `adjacent-hathi-nz` | Adjacent repo evidence: hathi-nz | supporting | boundary_evidence | supporting_evidence_only |
| `adjacent-corpus-law-nz` | Adjacent repo evidence: corpus-law-nz | supporting | boundary_evidence | supporting_evidence_only |

## Fallback Resources

- `tvnz-archive-looking-back`: historical_broadcast_validation (TVNZ Archive / New Zealand Parliament)
- `nga-taonga-av-collection`: catalogue_validation (Nga Taonga Sound & Vision)
- `rnz-parliament`: audio_or_reporting_validation (RNZ)
- `parliament-today-am-network`: audio_or_reporting_validation (Parliament Today / AM Network)
- `archives-new-zealand-av-catalogue`: catalogue_validation (Archives New Zealand)
- `internet-archive-webcaptures`: link_rot_validation (Internet Archive)
- `memento-cdx-web-archives`: link_rot_validation (Web archives)

## Adjacent Repo Boundaries

- `sm-govt-nz` can provide general NZ government YouTube metadata evidence, but not a complete Parliament video archive.
- `hathi-nz` is relevant to historical print/OCR evidence, not Parliament video.
- `corpus-law-nz` is the legislation/Gazette boundary and does not provide Parliament video coverage.

## Handoff

The next track must use this manifest to select bounded seed targets, preserve the no-download policy, record source-specific blocked states, and keep fallback resources separate from official acquisition sources.
