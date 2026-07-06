# Parliament Video Media Acquisition Decision

Release posture: metadata-only, no media download.

This track records the decision gate that keeps Parliament video/audio acquisition blocked. The current decision state is `excluded`, so no downloader may run unless a later approved state is recorded and validated.
Parliament video media acquisition is not approved.

## Decision

- Decision scope: media acquisition
- Decision state: excluded
- Media download: disabled
- Public media release: disabled
- Private preservation: not approved

## Media Rights Split

| Media type | Status |
| --- | --- |
| `metadata` | allowed |
| `captions` | excluded |
| `transcripts` | excluded |
| `thumbnails` | excluded |
| `audio` | excluded |
| `video` | excluded |
| `page_snapshots` | excluded |

## Rights Evidence

| Source | Title | Access status |
| --- | --- | --- |
| `parliament-copyright-and-video-terms` | Copyright - New Zealand Parliament | official-terms-review-complete |
| `parliament-tv-explained` | The Parliament TV and Radio page explained | official-help-review-complete |
| `standing-orders-appendix-d` | Appendix D: Coverage of proceedings | official-terms-review-complete |
| `parliament-practice-official-coverage` | Chapter 12 - Communicating and Engaging with Parliament | official-practice-review-complete |
| `youtube-terms-of-service` | Terms of Service - YouTube | platform-terms-review-complete |
| `vimeo-terms-of-service` | Vimeo Terms of Service | platform-terms-review-complete |
| `tvnz-footage-licensing` | TVNZ Licensing footage request | licensing-review-complete |
| `ngataonga-collection-home` | Ngā Taonga Sound & Vision | archive-access-review-complete |
| `archives-nz-audiovisual-reuse` | Audiovisual collections - Archives New Zealand | reuse-review-complete |
| `internet-archive-terms-of-use` | Internet Archive's Terms of Use | web-archive-terms-review-complete |

## Fallback Resources

Fallback resources are evidence-only in this track. They cannot be used for acquisition unless a later rights decision explicitly approves them.

| Resource | Title | Classification |
| --- | --- | --- |
| `parliament-website-video` | Parliament website video and Parliament Video help pages | evidence-only |
| `youtube-parliament-channel` | Official NZ Parliament YouTube channel | evidence-only |
| `vimeo-era-links` | Vimeo-era Parliament video links | evidence-only |
| `tvnz-licensing` | TVNZ Licensing | evidence-only |
| `nga-taonga` | Ngā Taonga Sound & Vision | evidence-only |
| `internet-archive` | Internet Archive | evidence-only |

## Review Notes

- RNZ reuse guidance remains a follow-up item because official retrieval was not reliable in this run.
- The guard remains metadata-first and blocks media acquisition until a later approved state exists.

## Guard

The repo gate is implemented by `scripts/check_parliament_video_media_acquisition_decision.py`. It blocks any media acquisition path until the manifest records `private preservation only` or `public release`.
