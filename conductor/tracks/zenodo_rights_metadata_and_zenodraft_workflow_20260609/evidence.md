# Evidence: Zenodo Rights Metadata And Zenodraft Workflow

## Initial Evidence

Status: opened on 2026-06-09.

Evidence should capture current and target public-surface behaviour across GitHub, Hugging Face, Zenodo, OSF, and future metadata environments.

## Protected Publication Boundary - 2026-06-09

Repo-side workflow hardening separates Zenodo draft/update operations from final publication:

- `.github/workflows/zenodo_archive.yml` can build and upload archive files to a draft, but no longer exposes a `publish` input or passes `--publish`.
- `.github/workflows/zenodo_metadata.yml` updates metadata without exposing a publish input.
- `scripts/upload_zenodo_archive.py` creates/updates draft files and metadata without publishing.
- `scripts/update_zenodo_metadata.py` updates metadata without publishing.
- `scripts/publish_zenodo_deposition.py` is the only script that calls the Zenodo publish action.
- `.github/workflows/zenodo_publish.yml` runs that publish script through the `zenodo-production-publish` environment.

Remaining operator requirement: configure `zenodo-production-publish` in GitHub repository settings with required reviewers before using it as a production release approval gate.
