# Plan - Multi-Git and Multi-Archive Mirroring

## Closed Current Scope (2026-06-23)

- [x] Task: Write `.github/workflows/mirror_sync.yml` to support automated SSH mirroring to secondary Git remotes.
- [x] Task: Add repo-side validation for mirror workflow and archive policy evidence.
- [x] Task: Review and verify OSF optional mirror policy configurations.
- [x] Task: Run `python scripts/check_osf_optional_mirror_policy.py` to verify consistency.
- [x] Task: Record machine-readable repo-side readiness and live activation blockers in `manifests/multi_git_archive_mirroring_status.json`.
- [x] Task: Move live GitLab/GitHub mirror activation out of the current plan and into the future roadmap.

## Future Roadmap Scope

Live mirror activation is deferred. A future roadmap item must create or gain access to the GitLab namespace `edithatogo`, create `edithatogo/corpus-nz-hansard`, configure GitHub Actions secrets `GIT_MIRROR_URL` and `GIT_MIRROR_SSH_PRIVATE_KEY`, and capture a successful manual or push-triggered `Mirror Sync` run.
