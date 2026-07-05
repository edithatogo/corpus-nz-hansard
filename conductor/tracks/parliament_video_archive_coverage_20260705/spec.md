# Parliament Video Archive Coverage

## Overview

Create a metadata-first coverage ledger for New Zealand Parliament video surfaces. The goal is to make the current gap explicit: Parliament video is not completely archived in this repo or adjacent repos, and any future media acquisition requires separate rights and access review.

## Functional Requirements

1. Inventory the known public Parliament video surfaces:
   - official NZ Parliament YouTube channel
   - `videos.parliament.nz` for the 54th Parliament onward
   - previous Parliament On Demand site for 53rd Parliament and earlier
   - select committee archive and Vimeo-era live-stream links
2. Record whether each surface has local evidence, adjacent-repo evidence, metadata-only coverage, video-file coverage, and known gaps.
3. Record adjacent repo findings, especially `sm-govt-nz` YouTube metadata coverage and the absence of a complete NZ Parliament video archive.
4. Preserve a metadata-first policy with no video-file download, no public-release claim, and no completeness claim.
5. Add validation and tests that prevent accidental claims that Parliament videos are fully archived.

## Non-Functional Requirements

- Keep outputs deterministic and reproducible.
- Do not add credentials, API keys, or bulk media downloads.
- Keep rights boundaries explicit for Parliament TV footage and third-party hosted material.
- Keep the implementation compatible with existing quality gates.

## Acceptance Criteria

- `manifests/parliament_video_archive_coverage.json` validates against its schema.
- The docs state that retrospective and ongoing video archiving are not complete.
- The checker validates source surfaces, adjacent repo findings, rights boundaries, and no-completeness policy.
- Tests exercise the builder and checker.

## Out of Scope

- Downloading video files.
- Claiming full YouTube, Parliament website, On Demand, or Vimeo completeness.
- Publishing media files or media-derived transcripts.
- Changing `sm-govt-nz` source registries in this track.
