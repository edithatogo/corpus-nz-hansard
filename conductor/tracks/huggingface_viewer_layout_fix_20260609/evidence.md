# Evidence: Hugging Face Viewer Layout Fix

## Initial Evidence

Status: opened on 2026-06-09.

Evidence should capture current and target public-surface behaviour across GitHub, Hugging Face, Zenodo, OSF, and future metadata environments.

## Live Hugging Face Viewer Probe - 2026-06-09

Read-only live checks confirmed that the dataset repository is public but the Hugging Face viewer layout is unhealthy:

- `https://huggingface.co/api/datasets/edithatogo/nz-hansard-corpus` reports `private: false` and `gated: false`.
- The live file list includes `data/hansard.parquet` plus downloadable `docs/`, `manifests/`, and `schemas/` assets.
- The rendered dataset page selects `validation` and shows a `CastError`.
- `https://datasets-server.huggingface.co/splits?dataset=edithatogo/nz-hansard-corpus` returns only `validation`.
- `https://datasets-server.huggingface.co/first-rows?dataset=edithatogo/nz-hansard-corpus&config=default&split=validation` returns HTTP 500.
- `https://datasets-server.huggingface.co/parquet?dataset=edithatogo/nz-hansard-corpus` returns no discovered Parquet files for the default config.
- The failed schema fields include `generated_at`, `rows_by_file`, and `summary`, matching `manifests/public_dataset_release_manifest.json` rather than the canonical Parquet dataset.

Interpretation: this is a Hugging Face file-layout or data-files configuration problem. The viewer appears to auto-detect the release manifest JSON as a dataset split instead of treating `data/hansard.parquet` as the canonical dataset source.

Required follow-up: constrain the Hub data-files/config metadata or staged layout so only `data/hansard.parquet` is used for the viewer dataset, while manifests, schemas, docs, CITATION, and NOTICE remain downloadable. Republish and recheck `splits`, `first-rows`, and `parquet` datasets-server endpoints.

## Staging Contract Fix - 2026-06-09

Repo-side fix:

- `DATASET_CARD.md` now declares an explicit Hugging Face `configs` block.
- The only viewer data file is `data/hansard.parquet`.
- The declared split is `train`.
- `docs/`, `manifests/`, and `schemas/` remain downloadable assets but are excluded from dataset viewer auto-detection.
- `tests/test_stage_huggingface_dataset.py` verifies that the staged `README.md` retains the `configs` block and that manifests/schemas remain present as assets.

Required live follow-up after the next Hugging Face publish:

- `https://datasets-server.huggingface.co/splits?dataset=edithatogo/nz-hansard-corpus` should report the configured Parquet-backed split.
- `https://datasets-server.huggingface.co/first-rows?dataset=edithatogo/nz-hansard-corpus&config=default&split=train` should return rows.
- `https://datasets-server.huggingface.co/parquet?dataset=edithatogo/nz-hansard-corpus` should discover `data/hansard.parquet`.

## Publish Attempt - 2026-06-09

GitHub Actions run `27199782809` rebuilt the corpus and completed successfully, but the upload step reported:

```json
{
  "uploaded": false,
  "reason": "remote_manifest_matches_local"
}
```

Live readback after that run showed the remote `README.md` still lacked the `configs` block, and datasets-server still reported only the bad `validation` split. The workflow now passes `--force` to `scripts/upload_huggingface_dataset.py` so metadata/card-only public-surface changes are uploaded even when the release manifest content is unchanged.
