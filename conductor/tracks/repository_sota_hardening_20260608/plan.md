# Plan: Repository SOTA Hardening

## Phase 1: Live Metadata Audit

- [ ] Task: Capture current GitHub metadata.
    - [ ] Read repository description, homepage, topics, visibility, license detection, wiki, projects, issues, and release posture.
    - [ ] Record whether the current prerelease state is intentional.
- [ ] Task: Capture current Hugging Face metadata.
    - [ ] Read dataset info, tags, `cardData`, file list, README, citation file, and public release manifest.
    - [ ] Identify missing YAML front matter fields.
- [ ] Task: Capture current citation and DOI state.
    - [ ] Verify Zenodo record status, DOI, concept DOI, files, and access rights.
    - [ ] Verify GitHub release and Hugging Face page cross-link to DOI.

## Phase 2: Decide Release Posture and License Pattern

- [ ] Task: Decide review-stage vs canonical release.
    - [ ] If keeping review-stage, document the rationale and what blocks promotion.
    - [ ] If promoting, define version, tag/release updates, and downstream metadata updates.
- [ ] Task: Decide license/provenance representation.
    - [ ] Review existing `docs/licensing-and-provenance.md`.
    - [ ] Choose safe machine-readable metadata for GitHub, Hugging Face, CITATION, and Zenodo notes.
    - [ ] Add `NOTICE`, `LICENSE`, or `LICENSES/` only if it improves clarity without overclaiming.

## Phase 3: GitHub Hardening

- [ ] Task: Update GitHub repository metadata.
    - [ ] Set description to match published DOI-backed dataset state.
    - [ ] Set homepage to the preferred public dataset or DOI surface.
    - [ ] Add useful topics such as `new-zealand`, `hansard`, `parliament`, `corpus`, `parquet`, `dataset`, `open-data`.
    - [ ] Disable unused Wiki/Projects or document why they remain enabled.
- [ ] Task: Refresh GitHub release posture.
    - [ ] Keep or change prerelease status based on Phase 2 decision.
    - [ ] Ensure release notes and assets point to Hugging Face and Zenodo DOI.

## Phase 4: Hugging Face Hardening

- [ ] Task: Add dataset-card YAML front matter.
    - [ ] Include safe metadata for language, tags, dataset format, license/provenance, DOI, and source caveats.
    - [ ] Preserve current dataset-card content below the front matter.
- [ ] Task: Republish Hugging Face dataset.
    - [ ] Stage from current repo state in a clean environment.
    - [ ] Run the existing Hugging Face publish workflow.
    - [ ] Verify `cardData` is non-null and the DOI appears in remote README/CITATION/manifest.

## Phase 5: Documentation and Verification

- [ ] Task: Update repo documentation.
    - [ ] Update README, publication status, hosting decision matrix, release checklist, and setup docs as needed.
    - [ ] Remove stale review-only wording if release posture changes.
- [ ] Task: Verify all surfaces.
    - [ ] Run `python -m unittest discover tests`.
    - [ ] Confirm GitHub Actions tests pass.
    - [ ] Confirm GitHub metadata readback.
    - [ ] Confirm Hugging Face dataset-info readback.
    - [ ] Confirm DOI resolution.
    - [ ] Record evidence in `evidence.md`.
