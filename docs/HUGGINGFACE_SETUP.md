# Hugging Face Setup

This project should use Hugging Face Datasets for the live browsable corpus if public release is approved.

Recommended target:

```text
edithatogo/nz-hansard-corpus
```

## Required Environment

```powershell
$env:HF_TOKEN = "hf_..."
$env:HF_REPO_ID = "edithatogo/nz-hansard-corpus"
```

For GitHub Actions, configure repository secrets:

- `HF_TOKEN`
- `SOURCE_ARCHIVE_URL`: private Hugging Face `resolve/main/...` URL for `2024-09-06 Hansard Extract from DocumentsDB.zip`

Recommended source archive URL pattern:

```text
https://huggingface.co/datasets/edithatogo/nz-hansard-source-archive/resolve/main/source/2024-09-06%20Hansard%20Extract%20from%20DocumentsDB.zip
```

`SOURCE_ARCHIVE_URL` downloads use `HF_TOKEN` when present and are verified against SHA-256 `2ac02c0042a4fb291fd8e401db5f469de2539e42c9e07c4c72eca16be9a17299` before any publication build continues.

Check GitHub Actions readiness before publishing:

```powershell
gh workflow run publication_readiness.yml --repo edithatogo/corpus-nz-hansard -f target=huggingface
```

## Staging

Build the local Hugging Face upload folder:

```powershell
python scripts\stage_huggingface_dataset.py --output-dir generated\huggingface
```

The staged layout is:

```text
README.md
data/hansard.parquet
manifests/
schemas/
docs/
```

The source ZIP is not staged.

## Upload

After `hf auth login` or `HF_TOKEN` is configured:

```powershell
python scripts\upload_huggingface_dataset.py --repo-id $env:HF_REPO_ID --folder generated\huggingface
```

Do not claim publication until the remote dataset page and uploaded files are verified.
