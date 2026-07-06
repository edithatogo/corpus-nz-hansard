# Parliament Video Media Acquisition Decision

## Overview

Record the rights, storage, and publication decision before any Parliament video/audio files are downloaded or archived.

This track is the only place that can change the metadata-first/no-download posture. Until it records an approved decision state, all other tracks must treat media files as externally hosted and must not download video or audio.

## Requirements

- Review Parliament copyright, official Parliament Video access terms, Parliament TV restrictions, NZ Parliament YouTube/YouTube terms, Vimeo terms, Parliament On Demand terms, TVNZ Archive access terms, Ngā Taonga access terms, RNZ reuse terms, Parliament Today/AM Network evidence, Archives New Zealand access terms, Internet Archive/web archives policy, and any platform-specific access limits.
- Decide whether media files are excluded, private preservation only, or approved for public release.
- If approved, define checksums, storage layout, sidecar metadata, captions/transcripts handling, and publication boundaries.
- If not approved, keep the metadata archive as the release artifact and mark media as externally hosted.
- Separate rights decisions for metadata, captions, transcripts, thumbnails, audio, video, and page snapshots.

## Delivery Discipline

- Commit after each task and attach a git notes summary to the task commit.
- Commit each Conductor plan update separately.
- At the end of each phase, create a phase checkpoint commit, attach a git notes verification report, push to the remote after the phase checkpoint, inspect GitHub Actions, and address any failing checks before beginning the next phase.
- Keep the Quality workflow aware of this track through `scripts/check_parliament_video_track_plan.py`.

## Acceptance Criteria

- A rights decision manifest exists.
- No downloader can run without the approved decision state.
- Metadata, captions, transcripts, audio, and video file rights are separated.
- Fallback resources cannot be used for media acquisition unless their rights evidence and access method are explicitly approved.
