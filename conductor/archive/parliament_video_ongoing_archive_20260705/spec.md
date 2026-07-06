# Parliament Video Ongoing Archive

## Overview

Set up ongoing Parliament video metadata refresh, gap monitoring, and alerting after full metadata capture and reconciliation are in place.

The ongoing archive is metadata-first/no-download unless the media acquisition decision track later approves media acquisition. Scheduled jobs must never download video or audio media files by default.

## Requirements

- Add scheduled metadata refresh for approved sources.
- Preserve prior snapshots, detect new/deleted/changed records, and update gap ledgers without losing history.
- Add source-count regression, stale-source, link-rot, and blocked-source checks.
- Monitor official Parliament Video, NZ Parliament YouTube, Parliament On Demand, Vimeo/select committee surfaces, TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive, and web archives according to their approved metadata/evidence roles.
- Keep media publication disabled unless the media acquisition decision track approves it.
- Ensure GitHub Actions reports track-specific refresh status and preserves failure artifacts.

## Delivery Discipline

- Commit after each task and attach a git notes summary to the task commit.
- Commit each Conductor plan update separately.
- At the end of each phase, create a phase checkpoint commit, attach a git notes verification report, push to the remote after the phase checkpoint, inspect GitHub Actions, and address any failing checks before beginning the next phase.
- Keep the Quality workflow aware of this track through `scripts/check_parliament_video_track_plan.py`.

## Acceptance Criteria

- Ongoing metadata refresh is repeatable and CI-visible.
- New Parliament videos are detected and reported.
- Reconciliation gaps remain auditable over time.
- No scheduled job downloads media unless explicitly approved.
- Fallback-source drift is tracked without overclaiming archive completeness.
