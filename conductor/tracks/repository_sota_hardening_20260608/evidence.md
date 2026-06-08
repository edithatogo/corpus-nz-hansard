# Evidence: Repository SOTA Hardening

## Initial Audit

Status: opened.

This track was created after publication of the Zenodo DOI to capture the remaining SOTA hardening work for GitHub and Hugging Face.

Observed current state before implementation:

- GitHub repository is public.
- GitHub release `v0.1.0-review.20260603` is public and remains a prerelease.
- Hugging Face dataset is public.
- Zenodo DOI resolves.
- Publication issues are closed.

Known gaps to verify and address:

- GitHub metadata lacks topics, homepage, and detected license.
- Hugging Face dataset metadata lacks structured card data.
- Release posture still uses review-stage naming.
- License/provenance metadata needs a clearer machine-readable pattern.

## Implementation

Status: complete.

Implemented:

- Added `LICENSE` with MIT terms for original repository materials.
- Added `NOTICE.md` to document scope boundaries for Hansard source material, no official endorsement, and source ZIP non-redistribution.
- Added Hugging Face YAML metadata front matter to `DATASET_CARD.md`.
- Fixed `scripts/stage_huggingface_dataset.py` so `DATASET_CARD.md` remains the staged Hugging Face `README.md` instead of being overwritten by the repo README.
- Updated `scripts/upload_huggingface_dataset.py` so every publish run resets the Hugging Face dataset repository to `private=false` and `gated=false`, including manifest-matching no-op uploads.
- Added `LICENSE` and `NOTICE.md` to Hugging Face, GitHub release package, and Zenodo archive staging scripts.
- Updated `CITATION.cff` from `NOASSERTION` to MIT for repository materials.
- Updated release notes and publication docs to keep review-stage posture explicit while reflecting DOI-backed publication.
- Kept `0.1.0-review.20260603` as a prerelease because member identity, party attribution, and speech-turn segmentation remain explicit review-stage limitations.

## Verification Log

### Local Tests

Command:

```powershell
python -m unittest discover tests
```

Result:

- Passed.
- Test count: 37.

### Hugging Face Metadata Parse

Command:

```powershell
python -c "from huggingface_hub import DatasetCard; card=DatasetCard.load('DATASET_CARD.md'); print(card.data.to_dict())"
```

Result:

- Parsed successfully.
- Metadata includes `pretty_name`, `language`, `license`, `license_link`, `size_categories`, `task_categories`, and discovery tags.

### Failed Remote Publish Attempt

Run:

- `https://github.com/edithatogo/corpus-nz-hansard/actions/runs/27138350198`

Result:

- Failed in the Hugging Face upload step.
- Cause: Hugging Face server-side YAML validation rejected free-text `license_name`; the field must match a lowercase identifier pattern.
- Resolution: remove `license_name` from YAML metadata and keep the repository/source-material nuance in `NOTICE.md` and the dataset-card body.

### Hugging Face Access Regression

Observation after successful publish:

- `HfApi().dataset_info("edithatogo/nz-hansard-corpus", repo_type="dataset").gated` returned `auto`.
- The dataset page and README resolved publicly, but Parquet download returned `401 Unauthorized` with `X-Error-Code: GatedRepo`.

Resolution:

- The uploader now calls `update_repo_settings(repo_type="dataset", private=False, gated=False)` immediately after repo creation/update and before any manifest-match upload short-circuit.
- `tests.test_upload_huggingface_dataset` asserts that the access settings update runs before `upload_folder`.

### Live Publication Surfaces

Recorded after push and remote workflow readbacks:

- GitHub repository metadata readback:
  - Repository: `https://github.com/edithatogo/corpus-nz-hansard`
  - Description: `DOI-backed NZ Hansard document-level corpus pipeline and Parquet dataset`
  - Homepage: `https://doi.org/10.5281/zenodo.20591997`
  - License detection: MIT.
  - Topics: `corpus`, `dataset`, `hansard`, `legal-corpus`, `legislative-data`, `new-zealand`, `open-data`, `parliament`, `parquet`.
  - Wiki and Projects disabled; Issues enabled.
- GitHub release readback:
  - Release: `https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0-review.20260603`
  - Draft: false.
  - Prerelease: true.
  - ZIP digest: `sha256:8ca3ced7024b16f276052f720b27baed581c9b34547990829d97ad582afa1370`.
  - Manifest digest: `sha256:012a0e77a52a8b8fa5e6eaf68fbf9bb4021d4e44eb3e4898d9fb33be404e57fb`.
- GitHub Actions:
  - Tests run `27139174647`: success on commit `030956d90794bd6dfd81458405db7ff5bebb66bd`.
  - Hugging Face publish run `27139214442`: success on commit `030956d90794bd6dfd81458405db7ff5bebb66bd`.
- Hugging Face dataset readback:
  - Dataset: `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`
  - Commit SHA: `f682f8e42a01071f2ebcc2fcfea79b9eb5be5271`.
  - `private=False`.
  - `gated=False`.
  - `cardData` populated.
  - `license=mit`.
  - Unauthenticated Parquet `HEAD` request returned `200 OK` with `Content-Length: 331036080`.
  - Remote README contains `license: mit`, `NOTICE.md`, and `https://doi.org/10.5281/zenodo.20591997`.
  - Remote `CITATION.cff` contains `doi: "10.5281/zenodo.20591997"` and `license: "MIT"`.
  - Remote public manifest contains `publication.doi=10.5281/zenodo.20591997`, `license.repository_materials=MIT`, and `artifacts.notice=NOTICE.md`.
- Zenodo DOI resolution readback:
  - `https://doi.org/10.5281/zenodo.20591997` redirects to `https://zenodo.org/records/20591997` and returned `200 OK`.
