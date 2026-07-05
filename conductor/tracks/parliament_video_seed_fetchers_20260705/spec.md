# Parliament Video Seed Fetchers

## Overview

Implement bounded, metadata-only seed fetchers for each approved Parliament video source family. This proves access and normalization without bulk media acquisition.

The implementation is metadata-first/no-download. Fetchers may request HTML, JSON, feeds, API responses, and page metadata, but must not download video or audio media files.

## Requirements

- Add seed fetchers for official Parliament Video, NZ Parliament YouTube, previous Parliament On Demand, select committee video archive, and Vimeo-era/live-stream links.
- Add fallback proof probes for TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive, and web archives where they expose metadata or catalogue records without requiring media downloads.
- Capture only metadata, source URLs, request evidence, counts, hashes, timestamps, and blocked reasons.
- Explicitly classify sources as official, mirror, fallback-validation, catalogue-only, evidence-only, blocked, or rights-gated.
- Mock external network access in tests.
- Do not download video/audio files.

## Delivery Discipline

- Commit after each task and attach a git notes summary to the task commit.
- Commit each Conductor plan update separately.
- At the end of each phase, create a phase checkpoint commit, attach a git notes verification report, push to the remote after the phase checkpoint, inspect GitHub Actions, and address any failing checks before beginning the next phase.
- Keep the Quality workflow aware of this track through `scripts/check_parliament_video_track_plan.py`.

## Acceptance Criteria

- Seed manifests are generated with bounded examples per source family.
- Fetchers are resumable and rights-safe.
- Tests verify dedupe keys, hashes, blocked states, and no media downloads.
- Fallback probes are evidence-only and cannot be promoted to acquisition sources without a later rights decision.
