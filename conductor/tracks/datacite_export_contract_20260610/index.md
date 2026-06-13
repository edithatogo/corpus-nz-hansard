# Track datacite_export_contract_20260610 Context

Add a DataCite export contract to the release metadata flow so DOI-hosted publication workflows have a generated machine-readable payload.

This track extends the metadata-package generator with a DataCite JSON payload derived from the public dataset release manifest, `.zenodo.json`, and the existing metadata-package policy. The contract is local and generated; DOI minting and deposit remain human-gated.

Current implementation surface:

- `docs/datacite-export-contract.md`
- `generated/metadata/datacite.json`
- `manifests/metadata_packages_manifest.json`
- `scripts/build_metadata_packages.py`
- `scripts/check_metadata_packages.py`
