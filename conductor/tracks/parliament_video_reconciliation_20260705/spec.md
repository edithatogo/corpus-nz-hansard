# Parliament Video Reconciliation

## Overview

Validate the Parliament video metadata archive against multiple independent sources before any completeness claim.

The implementation is metadata-first/no-download. Reconciliation may use URLs, catalogue records, broadcast metadata, page snapshots, hashes, sitting dates, and external identifiers, but must not download video or audio media files.

## Requirements

- Reconcile video records against Parliament sitting calendars, Hansard sitting dates, committee meeting records, sitting programmes, Parliament site search, official Parliament Video, NZ Parliament YouTube, Parliament On Demand, Vimeo, TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive URL evidence, and web archives.
- Classify gaps as expected no video, video found, metadata only, fallback-only, missing everywhere, access blocked, rights blocked, or duplicate/migrated.
- Produce machine-readable exception ledgers.
- Separate historical broadcast existence evidence from currently retrievable Parliament-hosted video evidence.

## Delivery Discipline

- Commit after each task and attach a git notes summary to the task commit.
- Commit each Conductor plan update separately.
- At the end of each phase, create a phase checkpoint commit, attach a git notes verification report, push to the remote after the phase checkpoint, inspect GitHub Actions, and address any failing checks before beginning the next phase.
- Keep the Quality workflow aware of this track through `scripts/check_parliament_video_track_plan.py`.

## Acceptance Criteria

- Metadata completeness is backed by multi-source reconciliation.
- Unresolved gaps are explicit and stable.
- No media completeness claim is possible from metadata alone.
- Fallback-only findings remain labelled as fallback-only until official or rights-approved evidence resolves them.
