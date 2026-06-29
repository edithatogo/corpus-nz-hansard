# Evidence: Monthly Dynamic Archive Publication

## GitHub Actions Dry Run, 2026-06-29

- Workflow: Monthly Dynamic Archive Publication
- Run: https://github.com/edithatogo/corpus-nz-hansard/actions/runs/28365543839
- Run ID: 28365543839
- Commit: 4d553499669cead8d143ddddc1cec0a7ab4975e4
- Mode: dry-run
- Result: success
- Duration: 3m30s
- Source archive URL configured: true
- Record schema validation: ok
- Validated record count: 193922
- Archive manifest file count: 855

Artifacts downloaded locally to `%TEMP%/monthly-run-28365543839` for hash verification:

| Artifact | Size bytes | SHA-256 |
|---|---:|---|
| monthly-dynamic-archive-28365543839/nz-hansard-corpus-0.1.0.tar.gz | 327553932 | a80775eb2b505a060eb21f9badb10925ada1201064e06951a4765c2e1fdea085 |
| monthly-dynamic-archive-28365543839/nz-hansard-corpus-0.1.0.manifest.json | 183958 | f6eff145f86d8eb0cb5671ba12afc5722bd5567a14b90c1ef98dc3f0ec19cb07 |
| monthly-publication-results-28365543839/monthly_dynamic_archive_publication_evidence.json | 2751 | 44ec8679563d53fed40da6d9958721deff322965c6edca48f49738b2099c3b13 |

Dry-run publication boundary:

- Hugging Face upload step skipped by `publication_mode=dry-run`.
- Zenodo draft upload step skipped by `publication_mode=dry-run`.
- Protected Zenodo publish handoff skipped by `publication_mode=dry-run`.
