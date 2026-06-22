# Evidence — Multi-Git and Multi-Archive Mirroring

## Phase 1: Git Remote Mirror Setup

### ✅ Task: Write `.github/workflows/mirror_sync.yml`

**Date:** 2026-06-14  
**Agent:** general_coder (Antigravity subdirectory swarm)  
**Status:** Complete  

**Evidence:**
- File `.github/workflows/mirror_sync.yml` exists with:
  - Trigger on push to `main`/`master` branches
  - `workflow_dispatch` manual trigger support
  - `actions/checkout@v5` with `fetch-depth: 0`
  - SSH-based mirror push using `GIT_MIRROR_URL` and `GIT_MIRROR_SSH_PRIVATE_KEY` secrets
  - Graceful skip when `GIT_MIRROR_URL` is empty (dry-run safe)
  - `ssh-keyscan` for host key verification
  - `git push --force --prune mirror HEAD:${{ github.ref }}`

**Notes:**
- Secrets `GIT_MIRROR_URL` and `GIT_MIRROR_SSH_PRIVATE_KEY` must be configured on GitHub before the workflow can push to secondary remotes.
- The workflow gracefully exits 0 when secrets are unset, preventing CI failures.

---

## Phase 2: Multi-Archive OSF Alignment

### ✅ Task: Run `python scripts/check_osf_optional_mirror_policy.py`

**Date:** 2026-06-14  
**Agent:** general_coder (Antigravity subdirectory swarm)  
**Status:** Passed  

**Output:**
```
OSF optional mirror policy is consistent.
```

**Notes:**
- `docs/osf-optional-mirror-policy.md` — exists and contains all required sections
- `manifests/osf_optional_mirror_policy.json` — valid against schema
- `schemas/osf_optional_mirror_policy.schema.json` — present
- `conductor/tracks/osf_optional_mirror_policy_20260609/evidence.md` — complete
- Canonical surfaces: GitHub, Hugging Face, Zenodo (OSF is optional future mirror)
- OSF status: inactive, claims_allowed: false, project_url: null
- All required activation controls present before OSF can go live

---

## Repository-Side Validation (2026-06-22)

### Task: Add mirror workflow and archive-policy guard

**Status:** Complete repo-side; live mirror execution remains blocked.

**Evidence:**
- `.github/workflows/mirror_sync.yml` now skips when either `GIT_MIRROR_URL`
  or `GIT_MIRROR_SSH_PRIVATE_KEY` is absent, so dry-run and unset-secret paths
  cannot create a partial SSH configuration.
- `scripts/check_multi_git_archive_mirroring.py` validates:
  - push and manual triggers for `main`/`master`;
  - pinned `actions/checkout` SHA with `fetch-depth: 0` and
    `persist-credentials: false`;
  - both required GitHub mirror secrets;
  - SSH host-key scan and mirror push command;
  - OSF optional mirror policy consistency.
- `tests/test_multi_git_archive_mirroring.py` covers the workflow secret-pair
  skip behavior and the repo-side track contract.

**Focused validation:**
```
python scripts/check_multi_git_archive_mirroring.py
python scripts/run_pytest_with_repo_tmp.py -q tests/test_multi_git_archive_mirroring.py
```

### Remaining live blocker

**Status:** `blocked-pending-github-mirror-secrets-and-manual-trigger`

The repository cannot prove secondary Git mirror delivery until a maintainer
configures `GIT_MIRROR_URL` and `GIT_MIRROR_SSH_PRIVATE_KEY` in GitHub Actions
secrets and captures a successful manual or push-triggered `Mirror Sync` run.
