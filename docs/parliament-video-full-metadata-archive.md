# Parliament Video Full Metadata Archive

Release posture: metadata-first archive with normalized JSONL, hashes, monthly refresh, and cache policy.

This track captures approved NZ Parliament video metadata surfaces without downloading video or audio media files. It archives normalized JSONL, source snapshots, request logs, hashes, and blocked records. It is not a complete media archive.

The cache policy keeps normalized IDs, retry behavior, and pagination stable across refreshes.

## Refresh Policy

- Cadence: monthly
- Snapshot retention: 12
- Comparison basis: latest_snapshot

## Cache Policy

- Cache root: `derived/parliament_video_full_metadata_archive/cache`
- Normalized ID prefix: `parliament-video-full-metadata-archive`
- Retry attempts: 3
- Backoff strategy: exponential
- Pagination page size: 50

## Policy

- Metadata-first only.
- No media download.
- No public media release.
- No completeness claim.
- Rights review required before media acquisition.
- Fallbacks are validation only.

## Summary

| Field | Value |
| --- | --- |
| Records | 16 |
| Approved sources | 16 |
| Captured sources | 15 |
| Blocked sources | 1 |
| Fetched sources | 6 |
| Index-only sources | 9 |
| Official sources | 9 |
| Fallback sources | 7 |
| Rights-gated sources | 2 |
| Adjacent repo findings | 3 |

Metadata completeness claim: False
Media completeness claim: False
Retrospective archive complete: False
Ongoing archive complete: False
Complete video archive: False

## Normalized JSONL

The archive writes normalized JSONL records and a snapshot history so refreshes remain resumable and hash-backed.

## Gap Report

The gap report separates fetched, index-only, blocked, and rights-gated metadata records.

## Next Actions

- Keep monthly refreshes resumable and hash-backed.
- Preserve the separation between metadata completeness and media completeness.
- Keep fallback resources validation-only unless the rights decision changes.
