# OSF Optional Mirror Policy

This policy defines OSF's role for `corpus-nz-hansard`. It preserves the corpus-family labels `corpus-nz-hansard` and `corpus-nz-legislation`.

## Decision

OSF is an optional future mirror, not a canonical publication surface for the current release. OSF is inactive until explicit mirror evidence exists.

The canonical public surfaces remain:

| Surface | Role |
| --- | --- |
| GitHub | Code, documentation, Actions, issues, and lightweight release assets. |
| Hugging Face | Canonical normalized document-level Parquet dataset host. |
| Zenodo | Immutable DOI-bearing archive and citation target. |
| OSF | Optional checksum-verified mirror or review-bundle host after explicit setup evidence exists. |

No current publication claim may say the OSF mirror is live, complete, citable, or authoritative until an OSF project URL, file inventory, checksums, version mapping, and maintenance owner are recorded in `manifests/osf_optional_mirror_policy.json`.

## Allowed OSF Uses

OSF may be used for:

- a non-canonical mirror of the same release artifacts already published through GitHub, Hugging Face, or Zenodo;
- review bundles that need a stable project workspace before a final DOI-bearing release;
- supplementary provenance packets that point back to the canonical GitHub, Hugging Face, and Zenodo records.

OSF must not be used as:

- the primary release authority;
- a replacement for the Zenodo DOI record;
- a divergent dataset version with different normalized Parquet content;
- a host for source ZIP redistribution unless rights review approves that separately.

## Required Mirror Controls

Before OSF is described as active, the OSF entry in `manifests/osf_optional_mirror_policy.json` must record:

- the OSF project URL;
- the release version and source commit;
- every mirrored artifact path;
- SHA-256 checksums for every mirrored artifact;
- the matching canonical URL for each artifact;
- the citation wording shown on OSF;
- the maintenance owner;
- the refresh cadence and deprecation process.

Checksum mismatches must be treated as publication blockers. A mirror refresh must update OSF files and the local manifest together.

## Citation Policy

Citation guidance must continue to direct users to the Zenodo DOI for formal citation. Zenodo remains the DOI authority.

`NZ Hansard Corpus. Version 0.1.0. https://doi.org/10.5281/zenodo.20595194`

OSF copy must say that OSF is a convenience mirror and that the Zenodo DOI is the authoritative citation target. OSF metadata should link to:

- `https://github.com/edithatogo/corpus-nz-hansard`
- `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`
- `https://doi.org/10.5281/zenodo.20595194`

## Future metadata environments

Future Croissant, RO-Crate, Frictionless, DCAT, PROV-O, RDF, and related metadata packages must point to the same canonical public surfaces. If they include OSF, they must label it as `optionalMirror` or equivalent, not as the authoritative dataset identifier.

## Validation

Validate the local policy files with:

```powershell
python scripts/check_osf_optional_mirror_policy.py
```

The validator checks the JSON schema, canonical-surface boundaries, OSF claim restrictions, checksum policy, citation policy, and Conductor evidence coverage.
