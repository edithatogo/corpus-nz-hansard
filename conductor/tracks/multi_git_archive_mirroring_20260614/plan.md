# Plan - Multi-Git and Multi-Archive Mirroring

## Phase 1: Git Remote Mirror Setup
- [x] Task: Write `.github/workflows/mirror_sync.yml` to support automated SSH mirroring to secondary Git remotes (GitLab/Codeberg).
- [ ] Task: Configure repository secrets `GIT_MIRROR_URL` and `GIT_MIRROR_SSH_PRIVATE_KEY` on GitHub.
- [ ] Task: Verify successful manual and push triggers for mirror sync.

## Phase 2: Multi-Archive OSF Alignment
- [ ] Task: Review and verify OSF optional mirror policy configurations.
- [ ] Task: Run `python scripts/check_osf_optional_mirror_policy.py` to verify consistency.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Multi-Archive OSF Alignment' (Protocol in workflow.md)
