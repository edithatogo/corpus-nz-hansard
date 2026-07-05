# Parliament Video Ongoing Archive Plan

## Implementation Protocol

- For every task: mark the task `[~]`, add dry-run or fixture tests first where feasible, implement the operating increment, run focused validation, commit after each task, attach git notes to the task commit, then commit the plan update with the short SHA.
- For every phase: create a phase checkpoint commit, attach git notes containing validation evidence, push to the remote after each phase, inspect GitHub Actions for the pushed commit, and address any failing checks before starting the next phase.
- This track must remain metadata-first/no-download unless a later approved media decision explicitly changes that state. No media download is allowed by default.
- GitHub Actions visibility is required through the Quality workflow step that runs `scripts/check_parliament_video_track_plan.py`.

## Phase 1: Refresh Design
- [ ] Task: Define refresh cadence, snapshot retention, alert thresholds, and CI workflow boundaries.
- [ ] Task: Define stale-source, link-rot, and count-regression policies.
- [ ] Task: Define ongoing fallback monitoring for TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive, and web archives.
- [ ] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs.
- [ ] Task: Conductor - User Manual Verification 'Refresh Design' (Protocol in workflow.md)

## Phase 2: Scheduled Archive
- [ ] Task: Add scheduled metadata refresh workflow and local runner.
- [ ] Task: Add new/deleted/changed record reports and gap-ledger updates.
- [ ] Task: Add tests and dry-run fixtures.
- [ ] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs.
- [ ] Task: Conductor - User Manual Verification 'Scheduled Archive' (Protocol in workflow.md)

## Phase 3: Operational Gates
- [ ] Task: Add quality-gate integration and no-media-download guard.
- [ ] Task: Run full validation, including `pixi run parliament-video-track-plan`, and document operating procedure.
- [ ] Task: Create phase checkpoint, push to the remote after each phase, inspect GitHub Actions, and address any failing checks before handoff.
- [ ] Task: Conductor - User Manual Verification 'Operational Gates' (Protocol in workflow.md)
