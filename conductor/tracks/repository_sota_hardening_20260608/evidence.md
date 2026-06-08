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
- Metadata includes `pretty_name`, `language`, `license`, `license_name`, `license_link`, `size_categories`, `task_categories`, and discovery tags.

### Live Publication Surfaces

To be recorded after push and remote workflow readbacks:

- GitHub metadata readback.
- GitHub Actions test run.
- Hugging Face publish workflow.
- Hugging Face `dataset_info(...).cardData` readback.
- Zenodo DOI resolution readback.
