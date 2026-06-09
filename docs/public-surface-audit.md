# Public Surface Audit

This document is the human-readable companion to `manifests/public_surface_audit.json`.

## Scope

The audit records the public-surface claims that are currently allowed for `corpus-nz-hansard` and the surfaces that remain inactive or planned. It preserves the corpus-family labels `corpus-nz-hansard` and `corpus-nz-legislation`.

## Current public surfaces

| Surface | Status | Role |
| --- | --- | --- |
| GitHub | Active | Code, documentation, Actions, issues, and lightweight release assets. |
| Hugging Face | Active | Canonical normalized document-level Parquet dataset host. |
| Zenodo | Active | Immutable citable archive and DOI-bearing snapshot. |
| OSF | Inactive | Optional future mirror or review-bundle host only after a dedicated policy. |
| Future metadata | Planned | Croissant, RO-Crate, Frictionless, DCAT, PROV-O, and related metadata exports. |

## Claim boundaries

- GitHub, Hugging Face, and Zenodo may be described as active public release surfaces when the audit ledger and public release manifest agree.
- OSF must not be described as published or complete until `osf_optional_mirror_policy_20260609` defines scope, checksums, citation wording, version mapping, and maintenance responsibility.
- Future metadata environments, including future metadata package hosts, must not be described as published until validated metadata packages exist.
- Existing GitHub, Hugging Face, and Zenodo URLs must not be changed without a migration plan that protects citations, DOI metadata, manifests, and downstream links.

## Validation

Regenerate the audit ledger with:

```powershell
python scripts/build_public_surface_audit.py
```

Validate it with:

```powershell
python scripts/check_public_surface_audit.py
```

The validator checks the ledger schema, required surfaces, claim boundaries, URL agreement with `manifests/public_dataset_release_manifest.json`, and documentation/evidence coverage.

## Zenodo and zenodraft

This audit track does not change Zenodo draft/archive mechanics. Any future Zenodo draft/archive workflow work must use or formally evaluate `zenodraft`, map `ZENODO_TOKEN` or sandbox credentials explicitly, validate metadata before upload, separate file upload/update from publish, and keep production publish behind protected approval.
