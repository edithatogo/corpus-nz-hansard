# Parliament Video Source Inventory

## Overview

Inventory every known public NZ Parliament video surface before any capture work. This track turns the current coverage finding into a source-by-source map that can drive metadata fetchers and later reconciliation.

The implementation is metadata-first/no-download. It must not download video or audio media files, and it must not claim retrospective or ongoing completeness until later reconciliation tracks prove that claim.

## Source Scope

Primary official sources:

- Official Parliament Video at `https://videos.parliament.nz/`.
- Current Parliament website "Watch" and "Parliament in action" pages.
- NZ Parliament YouTube channel and playlist/video surfaces.
- Parliament On Demand at `https://ondemand.parliament.nz/`, including 52nd-53rd Parliament select committee archive pages.
- Select committee live-stream pages and committee-specific archive links.
- Vimeo-hosted New Zealand Parliament and secondary-account videos linked from Parliament pages.

Fallback and validation resources:

- TVNZ Archive / Ministry for Culture and Heritage title-list evidence for historically broadcast Parliament-related footage.
- Ngā Taonga Sound & Vision audiovisual holdings and access pathways for historical broadcast material.
- RNZ Parliament pages and audio/reporting surfaces where Parliament video may be absent but sitting evidence exists.
- Parliament Today and AM Network/Parliament TV reporting references as historical broadcast metadata evidence.
- Archives New Zealand audiovisual holdings and catalogue records.
- Internet Archive, web archives, Memento/CDX evidence, and archived page snapshots as link-rot and prior-existence evidence only.
- Adjacent repos including `sm-govt-nz`, `hathi-nz`, and `corpus-law-nz`, with explicit notes that they do not provide a complete Parliament video archive.

## Requirements

- Cover official YouTube, official Parliament Video, previous Parliament On Demand, select committee archive pages, Vimeo-era links, embedded Parliament website media, and discoverable feeds/APIs/sitemaps.
- Record source URL, platform, expected date range, access method, rights notes, media types, metadata availability, adjacent-repo evidence, fallback-source role, and known blockers.
- Classify each source as official, platform mirror, fallback evidence, catalogue-only, web-archive evidence, blocked, rights-gated, or out-of-scope.
- Preserve metadata-first/no-download policy across all source discovery.
- Record when a fallback resource is useful for validation but not an acquisition source.
- Reconcile against adjacent repo evidence, especially `sm-govt-nz`, without treating it as a complete Parliament video archive.

## Delivery Discipline

- Commit after each task and attach a git notes summary to the task commit.
- Commit each Conductor plan update separately.
- At the end of each phase, create a phase checkpoint commit, attach a git notes verification report, push to the remote after the phase checkpoint, inspect GitHub Actions, and address any failing checks before beginning the next phase.
- Keep the Quality workflow aware of this track through `scripts/check_parliament_video_track_plan.py`.

## Acceptance Criteria

- A source inventory manifest and docs exist.
- Every known video surface has a stable source id.
- Rights/access/completeness status is explicit.
- Fallback resources are ranked and separated from acquisition sources.
- Validation prevents any complete-archive claim.
