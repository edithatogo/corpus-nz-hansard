# Spec: Repository SOTA Hardening

## Goal

Harden the published `corpus-nz-hansard` GitHub repository and `edithatogo/nz-hansard-corpus` Hugging Face dataset so they are easier to discover, cite, audit, reproduce, and reuse without weakening provenance or licensing caveats.

## Current Verified State

- GitHub repository is public: `https://github.com/edithatogo/corpus-nz-hansard`.
- GitHub release is public as prerelease: `v0.1.0-review.20260603`.
- Hugging Face dataset is public: `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`.
- Zenodo DOI resolves: `https://doi.org/10.5281/zenodo.20591997`.
- Hugging Face remote `CITATION.cff`, README, and `manifests/public_dataset_release_manifest.json` include the DOI and `published: true`.

## Problems To Address

- GitHub repository metadata is thin:
  - Description still says `Review-stage`.
  - No homepage URL is configured.
  - No repository topics are configured.
  - No license is detected by GitHub.
  - Wiki and Projects are enabled even though they are not part of the documented release workflow.
- Hugging Face metadata is thin:
  - `cardData` is null.
  - Tags are not useful for dataset discovery.
  - README needs Hugging Face dataset-card YAML front matter.
- License/provenance metadata was weak before this track:
  - `CITATION.cff` used `NOASSERTION`.
  - Zenodo used `other-open`.
  - The repo lacked a machine-readable license/notice pattern that explained source Hansard status while avoiding overclaiming ownership over parliamentary material.
- Release posture needed an explicit decision:
  - Published DOI exists, but the GitHub release remains a prerelease and the project still uses a `0.1.0-review...` version string.
  - This track records the decision to keep review-stage language until a separate canonical `v0.1.0` promotion decision.

## Required Outputs

- GitHub repository metadata updated or explicitly documented:
  - Description.
  - Homepage URL.
  - Topics.
  - Wiki/Projects decision.
  - License visibility decision.
- Hugging Face dataset card front matter added and remotely verified:
  - Dataset tags.
  - Language.
  - License/provenance fields where safe.
  - Dataset format and task/category metadata.
  - DOI/citation links.
- License/provenance hardening:
  - Keep source ZIP redistribution excluded.
  - Keep no-official-endorsement caveat.
  - Add a clear `NOTICE`, `LICENSE`, or `LICENSES/` structure if it can be done honestly.
  - Update `CITATION.cff` only if license metadata can be improved without overclaiming.
- Release posture decision:
  - Either keep review-stage and document why, or create/promote a formal `v0.1.0` release.
  - If promoting, update version, release notes, GitHub release posture, Hugging Face metadata, and Zenodo/version references consistently.
- Verification evidence:
  - GitHub metadata readback.
  - Hugging Face dataset-info readback showing non-null/meaningful card metadata.
  - DOI resolution check.
  - CI/test results.

## Acceptance Criteria

- GitHub repository has useful description, homepage, and topics.
- GitHub repository settings only expose surfaces intentionally used by this project.
- Hugging Face `dataset_info(...).cardData` is non-null and includes the agreed metadata.
- Hugging Face dataset page presents the DOI and public locations clearly.
- License/provenance is more discoverable but still honest about parliamentary source material and source ZIP non-redistribution.
- No stale statements say publication is blocked, credential-gated, or DOI-less.
- `python -m unittest discover tests` passes.
- Latest GitHub Actions test workflow passes after changes.
- If a new GitHub/Hugging Face/Zenodo release is created or promoted, all public surfaces cross-link consistently.

## Non-Goals

- Do not redistribute the source ZIP.
- Do not claim official endorsement by New Zealand Parliament.
- Do not claim party attribution, resolved member identity, or authoritative speech-turn segmentation.
- Do not change normalized data semantics unless a separate data-quality track is opened.
- Do not add heavyweight services or external indexing unless explicitly approved.
