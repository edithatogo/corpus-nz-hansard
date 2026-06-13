# Evidence: DataCite Export Contract

Status: complete.

Implemented artifacts:

- `docs/datacite-export-contract.md`
- `generated/metadata/datacite.json`
- `manifests/metadata_packages_manifest.json`
- `schemas/metadata_packages_manifest.schema.json`
- `scripts/build_metadata_packages.py`
- `scripts/check_metadata_packages.py`
- `tests/test_metadata_packages.py`

Validation evidence:

- `python scripts/build_metadata_packages.py`
- `python scripts/check_metadata_packages.py`
- `python -m unittest tests.test_metadata_packages`

Release boundary:

- The DataCite payload is generated from release metadata and is checksum-tracked with the other metadata packages.
- DOI minting and deposit remain outside this track and require the normal human publication gate.
- The generated payload is a local release artifact, not a published deposit record.
