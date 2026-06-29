# Monthly Dynamic Archive Releases

## Release Model

Monthly dynamic archive releases rebuild the current governed corpus archive from the source archive input and publish matching surfaces to GitHub Actions artifacts, Hugging Face, and Zenodo.

The default mode is validation-first:

1. Rebuild source inventory, schema discovery, normalized Parquet, and validation manifests.
2. Stage Hugging Face files under `generated/huggingface/`.
3. Build the Zenodo tarball and archive manifest under `generated/zenodo/`.
4. Write `manifests/monthly_dynamic_archive_publication_evidence.json`.
5. Upload GitHub Actions artifacts for review.
6. Publish to Hugging Face only when enabled and validation passes.
7. Upload a Zenodo draft or new version only when enabled and validation passes.
8. Publish the Zenodo draft only through the protected `zenodo-production-publish` environment.

## What Is Published

Hugging Face receives:

- `data/hansard.parquet`
- dataset card content
- `docs/`
- `manifests/`
- `schemas/`
- citation, license, notice, and version files

Zenodo receives:

- `nz-hansard-corpus-<version>.tar.gz`
- `nz-hansard-corpus-<version>.manifest.json`

Zenodo draft tooling must use or formally evaluate `zenodraft` before replacing or extending the existing draft/upload path.

GitHub Actions stores review artifacts:

- Zenodo archive tarball
- Zenodo archive manifest
- monthly publication evidence manifest

## What Remains Excluded

- The source ZIP is not committed.
- The source ZIP is not included in public monthly artifacts.
- Full historical completeness is not claimed beyond validated source and authority evidence.
- Official New Zealand Parliament endorsement is not claimed.
- Zenodo publication is not automatic from ordinary draft/upload jobs.

## Manual Verification

After a dry run:

1. Open the GitHub Actions run for `Monthly Dynamic Archive Publication`.
2. Confirm the run completed successfully.
3. Download the workflow artifacts.
4. Confirm the archive manifest contains a SHA-256 hash for the tarball.
5. Confirm `manifests/monthly_dynamic_archive_publication_evidence.json` records `publication_mode`.

After a Hugging Face publication:

1. Open `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`.
2. Confirm the latest revision matches the evidence manifest.
3. Confirm `data/hansard.parquet` exists.
4. Confirm `docs/`, `manifests/`, and `schemas/` are present.
5. Check the dataset viewer or datasets-server status for failed or pending entries.

After a Zenodo draft upload:

1. Open the draft URL or deposition ID recorded in the evidence manifest.
2. Confirm the tarball and matching manifest are attached.
3. Confirm metadata version, title, creators, related identifiers, and rights statement.
4. Do not publish unless the reviewer approves the protected publication job.

After protected Zenodo publication:

1. Open the Zenodo record or DOI URL.
2. Confirm the record is published.
3. Confirm files match the uploaded archive and manifest.
4. Confirm the evidence manifest records the DOI or record URL.

## Rollback And Retry

Hugging Face:

- If an upload fails before commit, rerun the workflow after correcting the failure.
- If a bad revision is pushed, restore by rerunning the workflow from the last known-good commit or by manually uploading the last validated staged folder.
- Record the restoration revision in the next evidence manifest.

Zenodo:

- If draft upload fails, delete or replace draft files and rerun the draft upload step.
- If draft metadata is wrong, update the draft before protected publication.
- If a draft is published incorrectly, do not delete records silently; create a corrected new version and document the supersession.

GitHub Actions:

- Failed dry runs can be rerun after correcting secrets, source archive access, or validation failures.
- Publication failures must not be bypassed by disabling validation checks.

## Required Secrets

- `SOURCE_ARCHIVE_URL`
- `HF_TOKEN`
- `ZENODO_TOKEN`
- `ARCHIVE_CREATORS_JSON`

## Protected Publication Boundary

Zenodo draft upload and Zenodo publication are intentionally separate:

- Draft upload creates or updates a reviewable draft/new version.
- Production publication requires the `zenodo-production-publish` protected environment.
- Monthly scheduled runs must not bypass that environment.
- Any future Zenodo draft implementation change must preserve the `zenodraft` evaluation/adoption requirement.
