# Parliament Video Ongoing Archive

## Overview

Set up ongoing Parliament video metadata refresh, gap monitoring, and alerting after full metadata capture and reconciliation are in place.

## Requirements

- Add scheduled metadata refresh for approved sources.
- Preserve prior snapshots, detect new/deleted/changed records, and update gap ledgers without losing history.
- Add source-count regression, stale-source, link-rot, and blocked-source checks.
- Keep media publication disabled unless the media acquisition decision track approves it.

## Acceptance Criteria

- Ongoing metadata refresh is repeatable and CI-visible.
- New Parliament videos are detected and reported.
- Reconciliation gaps remain auditable over time.
- No scheduled job downloads media unless explicitly approved.
