# Parliament Video Media Acquisition Decision Plan

## Implementation Protocol

- For every task: mark the task `[~]`, add decision-schema tests first where feasible, implement the decision increment, run focused validation, commit after each task, attach git notes to the task commit, then commit the plan update with the short SHA.
- For every phase: create a phase checkpoint commit, attach git notes containing validation evidence, push to the remote after each phase, inspect GitHub Actions for the pushed commit, and address any failing checks before starting the next phase.
- This track must preserve no media download until the approved decision state exists and has passed CI.
- GitHub Actions visibility is required through the Quality workflow step that runs `scripts/check_parliament_video_track_plan.py`.

## Phase 1: Rights Review
- [ ] Task: Record Parliament, YouTube, Vimeo, and archive-site rights/terms evidence.
- [ ] Task: Record TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive, and web archives rights/access evidence.
- [ ] Task: Define decision states for excluded, private preservation, and public release.
- [ ] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs.
- [ ] Task: Conductor - User Manual Verification 'Rights Review' (Protocol in workflow.md)

## Phase 2: Acquisition Gate
- [ ] Task: Add decision manifest, schema, and checker.
- [ ] Task: Add hard guards preventing media download without an approved decision.
- [ ] Task: Add tests for blocked and approved states.
- [ ] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs.
- [ ] Task: Conductor - User Manual Verification 'Acquisition Gate' (Protocol in workflow.md)

## Phase 3: Handoff
- [ ] Task: If approved, produce private media archive implementation plan; otherwise document metadata-only final state.
- [ ] Task: Run validation, including `pixi run parliament-video-track-plan`, and record final decision evidence.
- [ ] Task: Create phase checkpoint, push to the remote after each phase, inspect GitHub Actions, and address any failing checks before handoff.
- [ ] Task: Conductor - User Manual Verification 'Handoff' (Protocol in workflow.md)
