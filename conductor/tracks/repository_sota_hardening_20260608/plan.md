# Plan: Repository SOTA Hardening

## Phase 1: Live Metadata Audit

- [x] Task: Capture current GitHub metadata.
    - [x] Read repository description, homepage, topics, visibility, license detection, wiki, projects, issues, and release posture.
    - [x] Record whether the current prerelease state is intentional.
- [x] Task: Capture current Hugging Face metadata.
    - [x] Read dataset info, tags, `cardData`, file list, README, citation file, and public release manifest.
    - [x] Identify missing YAML front matter fields.
- [x] Task: Capture current citation and DOI state.
    - [x] Verify Zenodo record status, DOI, concept DOI, files, and access rights.
    - [x] Verify GitHub release and Hugging Face page cross-link to DOI.

## Phase 2: Decide Release Posture and License Pattern

- [x] Task: Decide review-stage vs canonical release.
    - [x] If keeping review-stage, document the rationale and what blocks promotion.
    - [x] If promoting, define version, tag/release updates, and downstream metadata updates.
- [x] Task: Decide license/provenance representation.
    - [x] Review existing `docs/licensing-and-provenance.md`.
    - [x] Choose safe machine-readable metadata for GitHub, Hugging Face, CITATION, and Zenodo notes.
    - [x] Add `NOTICE`, `LICENSE`, or `LICENSES/` only if it improves clarity without overclaiming.

## Phase 3: GitHub Hardening

- [x] Task: Update GitHub repository metadata.
    - [x] Set description to match published DOI-backed dataset state.
    - [x] Set homepage to the preferred public dataset or DOI surface.
    - [x] Add useful topics such as `new-zealand`, `hansard`, `parliament`, `corpus`, `parquet`, `dataset`, `open-data`.
    - [x] Disable unused Wiki/Projects or document why they remain enabled.
- [x] Task: Refresh GitHub release posture.
    - [x] Keep or change prerelease status based on Phase 2 decision.
    - [x] Ensure release notes and assets point to Hugging Face and Zenodo DOI.

## Phase 4: Hugging Face Hardening

- [x] Task: Add dataset-card YAML front matter.
    - [x] Include safe metadata for language, tags, dataset format, license/provenance, DOI, and source caveats.
    - [x] Preserve current dataset-card content below the front matter.
- [x] Task: Republish Hugging Face dataset.
    - [x] Stage from current repo state in a clean environment.
    - [x] Run the existing Hugging Face publish workflow.
    - [x] Verify `cardData` is non-null and the DOI appears in remote README/CITATION/manifest.

## Phase 5: Documentation and Verification

- [x] Task: Update repo documentation.
    - [x] Update README, publication status, hosting decision matrix, release checklist, and setup docs as needed.
    - [x] Remove stale review-only wording if release posture changes.
- [x] Task: Verify all surfaces.
    - [x] Run `python -m unittest discover tests`.
    - [x] Confirm GitHub Actions tests pass.
    - [x] Confirm GitHub metadata readback.
    - [x] Confirm Hugging Face dataset-info readback.
    - [x] Confirm DOI resolution.
    - [x] Record evidence in `evidence.md`.
