# Parliament Video Media Acquisition Decision

## Overview

Record the rights, storage, and publication decision before any Parliament video/audio files are downloaded or archived.

## Requirements

- Review Parliament copyright, Parliament TV restrictions, YouTube/Vimeo terms, and any platform-specific access limits.
- Decide whether media files are excluded, private preservation only, or approved for public release.
- If approved, define checksums, storage layout, sidecar metadata, captions/transcripts handling, and publication boundaries.
- If not approved, keep the metadata archive as the release artifact and mark media as externally hosted.

## Acceptance Criteria

- A rights decision manifest exists.
- No downloader can run without the approved decision state.
- Metadata, captions, transcripts, audio, and video file rights are separated.
