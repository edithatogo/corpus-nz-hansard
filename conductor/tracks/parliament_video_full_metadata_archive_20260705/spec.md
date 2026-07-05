# Parliament Video Full Metadata Archive

## Overview

Scale from seed proofs to complete metadata capture for all approved NZ Parliament video surfaces, while keeping media files out of scope.

The implementation is metadata-first/no-download. It may archive metadata, source snapshots, request logs, captions/transcript metadata where rights permit, and hashes of retrieved metadata documents, but it must not download video or audio media files.

## Requirements

- Implement resumable metadata acquisition across all inventory-approved surfaces.
- Store normalized JSONL, source snapshots where allowed, request logs, hashes, counts, and blocked records.
- Add cache policy, retry/backoff, rate limiting, and deterministic IDs.
- Preserve source-specific boundaries for official Parliament Video, NZ Parliament YouTube, Parliament On Demand, Vimeo, select committee archive pages, TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive, and web archives.
- Treat fallback resources as validation/corroboration unless a later rights decision explicitly approves acquisition.
- Generate coverage and gap reports without claiming media archive completeness.

## Delivery Discipline

- Commit after each task and attach a git notes summary to the task commit.
- Commit each Conductor plan update separately.
- At the end of each phase, create a phase checkpoint commit, attach a git notes verification report, push to the remote after the phase checkpoint, inspect GitHub Actions, and address any failing checks before beginning the next phase.
- Keep the Quality workflow aware of this track through `scripts/check_parliament_video_track_plan.py`.

## Acceptance Criteria

- Full metadata archive manifest is repeatable and hash-backed.
- All approved surfaces are captured or explicitly blocked.
- Monthly refresh can update metadata without rewriting unresolved gaps.
- Metadata archive completeness and media archive completeness remain separate states.
