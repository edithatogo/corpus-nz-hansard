# Specification - Multi-Git and Multi-Archive Mirroring

## Overview
This track implements multi-git repository mirroring and backup publishing strategies for the `corpus-nz-hansard` pipeline to guarantee durability and prevent censorship or single-point-of-failure repository/dataset takedowns.

## Requirements
1. **Multi-Git Mirroring**: Automatically push codebase updates to secondary Git remotes (GitLab and Codeberg) on every push to the canonical branches.
2. **Multi-Archive Datasets**: Redundantly archive datasets. Maintain Hugging Face as the canonical live dataset repository, Zenodo as the immutable citation and snapshot repository, and OSF as a convenience mirror and review repository.

## Acceptance Criteria
- `.github/workflows/mirror_sync.yml` exists and triggers on pushes to main/master branches.
- Workflow successfully executes dry-run or bypasses when credentials are empty.
- Multi-archive setup covers Hugging Face, Zenodo, and the OSF optional mirror policy.
