# DataCite Export Contract

## Purpose

Generate a machine-readable DataCite metadata payload for DOI-hosted publication workflows from the canonical public release metadata.

## Source Inputs

- `manifests/public_dataset_release_manifest.json`
- `.zenodo.json`
- `CITATION.cff`
- `docs/sota-metadata-packages.md`

## Generated Fields

- `identifier`: DOI from the public release manifest.
- `creators`: repository citation authors from the release metadata.
- `titles`: dataset title from the Zenodo metadata.
- `publisher`: Zenodo.
- `publicationYear`: derived from the release publication date.
- `types`: `Dataset` resource type with the release title as the local resource label.
- `version`: release version from the Zenodo metadata.
- `descriptions`: dataset description from the Zenodo metadata.
- `contributors`: release automation metadata used for local deposit preparation.
- `dates`: issued date from the public release manifest.
- `subjects`: release keywords.
- `language`: `en`.
- `rightsList`: repository-level rights statement.
- `relatedIdentifiers`: DOI, GitHub, and Hugging Face links from the public release metadata.
- `fundingReferences`: empty until a depositor review adds actual funding data.

## Depositor-Reviewed Fields

- `rightsList`
- `contributors`
- `fundingReferences`
- Any manual edits to `identifier`, `publisher`, or `relatedIdentifiers` before deposit

## Limits

- The contract does not mint or deposit DOIs automatically.
- Zenodo publication still follows the sandbox-first and protected-production workflow.
- The generated payload is a local release artifact, not a published deposition record.

## Validation

- `python scripts/build_metadata_packages.py`
- `python scripts/check_metadata_packages.py`
- `python -m unittest tests.test_metadata_packages`
