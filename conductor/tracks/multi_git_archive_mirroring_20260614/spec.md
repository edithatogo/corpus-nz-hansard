# Specification - Multi-Git and Multi-Archive Mirroring

## Overview
This track implements multi-git repository mirroring and backup publishing strategies for the `corpus-nz-hansard` pipeline to improve durability and avoid single-point-of-failure repository/dataset hosting.

## Requirements
1. **Multi-Git Mirroring**: Automatically push codebase updates to secondary Git remotes on pushes to canonical branches once maintainer-owned GitHub Actions secrets are configured.
2. **Safe Secret Boundary**: The workflow must skip before SSH setup or push when either `GIT_MIRROR_URL` or `GIT_MIRROR_SSH_PRIVATE_KEY` is missing.
3. **Multi-Archive Dataset Boundary**: Maintain Hugging Face as the canonical live dataset repository, Zenodo as the immutable citation/snapshot repository, and OSF as an inactive optional review mirror until the OSF activation policy is satisfied.
4. **Machine-Readable Status**: Record repo-side readiness and live blockers in `manifests/multi_git_archive_mirroring_status.json`.

## Acceptance Criteria
- `.github/workflows/mirror_sync.yml` exists and triggers on pushes to main/master branches and manual `workflow_dispatch`.
- Workflow uses a pinned `actions/checkout` SHA, full history, and `persist-credentials: false`.
- Workflow successfully bypasses when credentials are empty or incomplete.
- Multi-archive setup covers Hugging Face, Zenodo, and the inactive OSF optional mirror policy.
- Repo-side checker validates the workflow, status manifest, quality-gate wiring, and OSF policy linkage.
- Live mirror delivery remains blocked until GitHub secrets exist and a successful manual or push-triggered Mirror Sync run is captured.
