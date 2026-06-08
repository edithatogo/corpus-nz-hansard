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
- `SOURCE_ARCHIVE_URL`: private/downloadable URL for `2024-09-06 Hansard Extract from DocumentsDB.zip`

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
hf repo create $env:HF_REPO_ID --type dataset --yes
hf upload-large-folder $env:HF_REPO_ID generated\huggingface --repo-type dataset
```

Do not claim publication until the remote dataset page and uploaded files are verified.
