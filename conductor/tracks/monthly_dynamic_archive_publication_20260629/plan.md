# Plan: Monthly Dynamic Archive Publication

## Phase 1: Publication Contract

- [x] Task: Audit current GitHub, Hugging Face, and Zenodo publication workflows and identify the exact artifact set that must be included in each monthly archive.
- [x] Task: Define the monthly archive publication contract, including source inputs, generated outputs, manifest fields, public URLs, and rights-safe exclusions.
- [ ] Task: Add or update docs describing monthly dynamic releases, verification steps, rollback/retry procedure, and the distinction between draft upload and protected Zenodo publication.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Publication Contract' (Protocol in workflow.md)

## Phase 2: Scheduled GitHub Actions

- [ ] Task: Add a monthly scheduled GitHub Actions workflow with manual dispatch inputs for dry run, Hugging Face publish, Zenodo draft upload, and protected Zenodo publish handoff.
- [ ] Task: Ensure workflow permissions are least-privilege and required secrets are checked before network publication steps run.
- [ ] Task: Rebuild the full archive from the governed source archive input, including Parquet, docs, manifests, schemas, metadata packages, Zenodo tarball, and manifest.
- [ ] Task: Wire Hugging Face upload to capture the resulting revision and Zenodo draft/new-version upload to capture draft or DOI metadata.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Scheduled GitHub Actions' (Protocol in workflow.md)

## Phase 3: Evidence And Validation

- [ ] Task: Add a machine-readable monthly release evidence manifest that records GitHub run ID, commit SHA, archive hashes, manifest hashes, row counts, Hugging Face revision, Zenodo draft or DOI, and publication boundary notes.
- [ ] Task: Add repo-side checker and tests for schedule configuration, protected publication gates, required evidence fields, and cross-surface consistency.
- [ ] Task: Integrate the monthly release checker into publication readiness or quality gates without allowing dependency-update PRs to publish.
- [ ] Task: Run focused validation for the monthly release workflow, evidence manifest, and affected publication checks.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Evidence And Validation' (Protocol in workflow.md)

## Phase 4: First Monthly Release Proof

- [ ] Task: Execute a dry run from GitHub Actions and record artifact hashes and validation output.
- [ ] Task: Execute Hugging Face publication and verify the public dataset revision, viewer health, and supporting archive files.
- [ ] Task: Create or update a Zenodo draft/new version, verify uploaded archive files and metadata, and route final publish through the protected environment.
- [ ] Task: Update release evidence and Conductor track evidence with public URLs, revisions, DOI or draft IDs, and verification timestamps.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: First Monthly Release Proof' (Protocol in workflow.md)
