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

## Hugging Face Publication, 2026-06-29

- Workflow: Monthly Dynamic Archive Publication
- Run: https://github.com/edithatogo/corpus-nz-hansard/actions/runs/28365942236
- Run ID: 28365942236
- Commit: 664ed035bba2e072d18f5ef9658885316c04a71e
- Mode: huggingface
- Result: success
- Duration: 3m41s
- Dataset: https://huggingface.co/datasets/edithatogo/nz-hansard-corpus
- Dataset private: false
- Dataset gated: false
- Dataset revision: main
- Dataset revision SHA: d1e834bb363ef2ce2b35793980385998706d8838
- Dataset last modified: 2026-06-29T10:39:40Z
- Viewer splits: default/train
- Viewer first rows: accessible through Hugging Face Dataset Viewer API
- Validated record count in run evidence: 193922
- Record schema validation in run evidence: ok

GitHub Actions publication artifacts downloaded locally to `%TEMP%/monthly-run-28365942236` for hash verification:

| Artifact | Size bytes | SHA-256 |
|---|---:|---|
| monthly-dynamic-archive-28365942236/nz-hansard-corpus-0.1.0.tar.gz | 327554169 | da347782d26928c52e2334f96b72d0aa721a4c436428003b1727851ea98c363f |
| monthly-dynamic-archive-28365942236/nz-hansard-corpus-0.1.0.manifest.json | 184195 | e3ac38caffb81dc72691844f669899d205d0c12c094b0a8171cfd01da56374d1 |
| monthly-publication-results-28365942236/huggingface-upload.json | 282 | b5c399164891bd2d7bf65a82372b0ed20e21ed72989fcd18b5b3d3b5838af107 |
| monthly-publication-results-28365942236/monthly_dynamic_archive_publication_evidence.json | 2855 | 938224a7ecc6ab631062a9ced9d174d29185d4ebf0e9fe7a64279211c349b6cb |

Hugging Face supporting files verified through the Hub API:

- `data/hansard.parquet`
- `docs/`
- `manifests/`
- `schemas/`
- `README.md`
- `CITATION.cff`
- `LICENSE`
- `NOTICE.md`
- `VERSION`

Publication boundary:

- Zenodo draft upload step skipped by `publication_mode=huggingface`.
- Protected Zenodo publish handoff skipped by `publication_mode=huggingface`.
