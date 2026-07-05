# Parliament Video Full Metadata Archive Plan

## Implementation Protocol

- For every task: mark the task `[~]`, add tests or fixtures first where feasible, implement the acquisition increment, run focused validation, commit after each task, attach git notes to the task commit, then commit the plan update with the short SHA.
- For every phase: create a phase checkpoint commit, attach git notes containing validation evidence, push to the remote after each phase, inspect GitHub Actions for the pushed commit, and address any failing checks before starting the next phase.
- This track must remain metadata-first/no-download. No media download is allowed, including video or audio media files.
- GitHub Actions visibility is required through the Quality workflow step that runs `scripts/check_parliament_video_track_plan.py`.

## Phase 1: Acquisition Design
- [ ] Task: Define cache layout, normalized IDs, retry policy, and refresh cadence.
- [ ] Task: Define source-specific pagination/enumeration rules.
- [ ] Task: Define fallback-source acquisition boundaries for TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive, and web archives.
- [ ] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs.
- [ ] Task: Conductor - User Manual Verification 'Acquisition Design' (Protocol in workflow.md)

## Phase 2: Full Metadata Capture
- [ ] Task: Implement resumable metadata acquisition for approved video surfaces.
- [ ] Task: Write normalized JSONL, manifests, source snapshots, hashes, and blocked records.
- [ ] Task: Add tests with mocked pages/API responses.
- [ ] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs.
- [ ] Task: Conductor - User Manual Verification 'Full Metadata Capture' (Protocol in workflow.md)

## Phase 3: Reporting And Gates
- [ ] Task: Generate metadata archive manifest and gap report.
- [ ] Task: Add quality-gate checks and run full validation, including `pixi run parliament-video-track-plan`.
- [ ] Task: Create phase checkpoint, push to the remote after each phase, inspect GitHub Actions, and address any failing checks before handoff.
- [ ] Task: Conductor - User Manual Verification 'Reporting And Gates' (Protocol in workflow.md)
