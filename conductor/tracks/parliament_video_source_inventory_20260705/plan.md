# Parliament Video Source Inventory Plan

## Implementation Protocol

- For every task: mark the task `[~]`, implement the smallest coherent change, run focused validation, commit after each task, attach git notes to the task commit, then commit the plan update with the short SHA.
- For every phase: create a phase checkpoint commit, attach git notes containing validation evidence, push to the remote after each phase, inspect GitHub Actions for the pushed commit, and address any failing checks before starting the next phase.
- This track must remain metadata-first/no-download. No media download is allowed, including video or audio media files.
- GitHub Actions visibility is required through the Quality workflow step that runs `scripts/check_parliament_video_track_plan.py`.

## Phase 1: Source Taxonomy
- [x] Task: Define source families, platform classes, fallback classes, rights classes, and archive-status values. `d476db3`
- [~] Task: List official Parliament Video, NZ Parliament YouTube, previous Parliament On Demand, select committee archive, Vimeo-era, embedded Parliament website, feed/API, sitemap, and search surfaces.
- [ ] Task: Add fallback-resource taxonomy for TVNZ Archive, Ngā Taonga, RNZ, Parliament Today, Archives New Zealand, Internet Archive, and web archives.
- [ ] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs.
- [ ] Task: Conductor - User Manual Verification 'Source Taxonomy' (Protocol in workflow.md)

## Phase 2: Manifest And Docs
- [ ] Task: Add source inventory schema, builder, manifest, and documentation.
- [ ] Task: Record adjacent repo evidence from `sm-govt-nz`, `hathi-nz`, and `corpus-law-nz`.
- [ ] Task: Add no-download/no-completeness policy checks.
- [ ] Task: Commit and annotate task outputs with git notes, then update this plan with task SHAs.
- [ ] Task: Conductor - User Manual Verification 'Manifest And Docs' (Protocol in workflow.md)

## Phase 3: Validation
- [ ] Task: Add tests and checker for inventory completeness, rights status, and source ids.
- [ ] Task: Run focused and repo-level validation, including `pixi run parliament-video-track-plan`.
- [ ] Task: Create phase checkpoint, push to the remote after each phase, inspect GitHub Actions, and address any failing checks before handoff.
- [ ] Task: Conductor - User Manual Verification 'Validation' (Protocol in workflow.md)
