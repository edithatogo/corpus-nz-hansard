# SOTA Metadata Packages

This document defines the generated metadata packages for `corpus-nz-hansard`.
The repository exports Croissant, RO-Crate, Frictionless Data Package, DCAT,
DataCite, and PROV-O metadata from canonical release inputs, not as hand-maintained
release descriptions.

## Current State

The public dataset release is already anchored by:

- `manifests/public_dataset_release_manifest.json`
- `manifests/public_surface_audit.json`
- `.zenodo.json`
- `CITATION.cff`
- `DATASET_CARD.md`
- `schemas/hansard_record.schema.json`

GitHub, Hugging Face, and Zenodo are active public surfaces for the `0.1.0`
release. OSF remains optional and inactive. Future metadata environments must
not be described as published until generated metadata-package outputs are
uploaded to that surface and read back.

The DataCite export contract is documented separately in
`docs/datacite-export-contract.md` and is generated alongside the other
metadata-package outputs.

## Target Packages

The package contract is recorded in
`manifests/metadata_packages_manifest.json` and validated by
`scripts/check_metadata_packages.py`.

| Package | Format | Generated Output | Validation Command |
| --- | --- | --- | --- |
| Croissant | JSON-LD | `generated/metadata/croissant.jsonld` | `python scripts/check_metadata_packages.py` |
| RO-Crate | JSON-LD | `generated/metadata/ro-crate-metadata.json` | `python scripts/check_metadata_packages.py` |
| Frictionless | JSON | `generated/metadata/datapackage.json` | `python scripts/check_metadata_packages.py` |
| DCAT | Turtle | `generated/metadata/dcat.ttl` | `python scripts/check_metadata_packages.py` |
| DataCite | JSON | `generated/metadata/datacite.json` | `python scripts/check_metadata_packages.py` |
| PROV-O | Turtle | `generated/metadata/prov-o.ttl` | `python scripts/check_metadata_packages.py` |

Each package entry must name its source manifests, validation command, checksum
algorithm, checksum field, output path, and publication-surface links. The
generated files live under `generated/metadata/`, and
`manifests/metadata_packages_manifest.json` records their SHA-256 checksums.

Regenerate package files and manifest checksums with:

```powershell
python scripts\build_metadata_packages.py
```

## Migration Constraints

- Preserve the corpus-family labels `corpus-nz-hansard` and
  `corpus-nz-legislation`.
- Preserve existing GitHub, Hugging Face, and Zenodo URLs and DOI records unless
  a migration plan is recorded first.
- Do not claim OSF or future metadata publication until generated package files
  are uploaded to that surface and the active public surface manifests are
  updated.
- Keep Zenodo draft and publication workflows separate. Any Zenodo-related
  package upload workflow must use the existing sandbox-first and protected
  production-publication policy.

## Validation

Run the focused metadata package checks with:

```powershell
python -m unittest tests.test_metadata_packages
python scripts\check_metadata_packages.py
```
