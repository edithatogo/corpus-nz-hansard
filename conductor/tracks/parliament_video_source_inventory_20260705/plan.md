# Parliament Video Source Inventory Plan

## Implementation Protocol

- For every task: mark the task `[~]`, implement the smallest coherent change, run focused validation, commit after each task, attach git notes to the task commit, then commit the plan update with the short SHA.
- For every phase: create a phase checkpoint commit, attach git notes containing validation evidence, push to the remote after each phase, inspect GitHub Actions for the pushed commit, and address any failing checks before starting the next phase.
- This track must remain metadata-first/no-download. No media download is allowed, including video or audio media files.
- GitHub Actions visibility is required through the Quality workflow step that runs `scripts/check_parliament_video_track_plan.py`.

## Phase 1: Source Taxonomy [checkpoint: 4531eca]
- [x] Task: Define source families, platform classes, fallback classes, rights classes, and archive-status values. `d476db3`
- [x] Task: List official Parliament Video, NZ Parliament YouTube, previous Parliament On Demand, select committee archive, Vimeo-era, embedded Parliament website, feed/API, sitemap, and search surfaces. `63c301d`
- [x] Task: Add fallback-resource taxonomy for TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive, and web archives. `4b76af1`
- [x] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs. `d476db3`, `63c301d`, `4b76af1`
- [x] Task: Conductor - User Manual Verification 'Source Taxonomy' (Protocol in workflow.md)

## Phase 2: Manifest And Docs [checkpoint: 87dbabb]
- [x] Task: Add source inventory schema, builder, manifest, and documentation. `06d332f`
- [x] Task: Record adjacent repo evidence from `sm-govt-nz`, `hathi-nz`, and `corpus-law-nz`. `06d332f`
- [x] Task: Add no-download/no-completeness policy checks. `06d332f`
- [x] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs. `06d332f`
- [x] Task: Conductor - User Manual Verification 'Manifest And Docs' (Protocol in workflow.md) `06d332f`

## Phase 3: Validation [checkpoint: 44f1aac]
- [x] Task: Add tests and checker for inventory completeness, rights status, and source ids. `06d332f`
- [x] Task: Run focused and repo-level validation, including `pixi run parliament-video-track-plan`. `f02b360`
- [x] Task: Create phase checkpoint, push to the remote after each phase, inspect GitHub Actions, and address any failing checks before handoff. `f02b360`
- [x] Task: Conductor - User Manual Verification 'Validation' (Protocol in workflow.md) `f02b360`
