# Parliament Video Seed Fetchers

## Overview

Implement bounded, metadata-only seed fetchers for each approved Parliament video source family. This proves access and normalization without bulk media acquisition.

## Requirements

- Add seed fetchers for official YouTube, `videos.parliament.nz`, previous On Demand, select committee video archive, and Vimeo-era/live-stream links.
- Capture only metadata, source URLs, request evidence, counts, hashes, timestamps, and blocked reasons.
- Mock external network access in tests.
- Do not download video/audio files.

## Acceptance Criteria

- Seed manifests are generated with bounded examples per source family.
- Fetchers are resumable and rights-safe.
- Tests verify dedupe keys, hashes, blocked states, and no media downloads.
