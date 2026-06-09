# Evidence: OSF Optional Mirror Policy

## Initial Evidence

Status: opened on 2026-06-09.

Evidence should capture current and target public-surface behaviour across GitHub, Hugging Face, Zenodo, OSF, and future metadata environments.

## Current OSF Status - 2026-06-09

No OSF publication surface is currently claimed for `corpus-nz-hansard`.

Active publication surfaces are GitHub, Hugging Face, and Zenodo. OSF remains a policy decision, not a completed mirror. Before any OSF use, this track must decide whether OSF is:

- unused;
- a review-bundle host only; or
- an optional public mirror with checksums, citation policy, version mapping, and maintenance ownership.

## Policy Decision - 2026-06-10

Decision: OSF is an optional future mirror, not a canonical publication surface for the current release.

This is recorded in:

- `docs/osf-optional-mirror-policy.md`
- `manifests/osf_optional_mirror_policy.json`
- `schemas/osf_optional_mirror_policy.schema.json`
- `scripts/check_osf_optional_mirror_policy.py`
- `tests/test_osf_optional_mirror_policy.py`

## Canonical Surfaces

Current canonical surfaces remain:

- GitHub: `https://github.com/edithatogo/corpus-nz-hansard`
- Hugging Face: `https://huggingface.co/datasets/edithatogo/nz-hansard-corpus`
- Zenodo DOI: `https://doi.org/10.5281/zenodo.20595194`

The policy preserves the corpus-family labels `corpus-nz-hansard` and `corpus-nz-legislation`.

## OSF Activation Controls

OSF public claims remain disabled until all activation controls are recorded:

- OSF project URL
- release version
- source commit
- mirrored artifacts
- SHA-256 checksums
- canonical artifact URLs
- citation wording
- maintenance owner

Checksum mismatch is a publication blocker. OSF must remain a convenience mirror or review-bundle host, not a replacement for GitHub, Hugging Face, or Zenodo.

## Citation Boundary

Formal citation remains the Zenodo DOI:

`NZ Hansard Corpus. Version 0.1.0. https://doi.org/10.5281/zenodo.20595194`

Any future OSF project copy must say that OSF is a convenience mirror and that the Zenodo DOI is the authoritative citation target.

## Future Metadata Implications

Future Croissant, RO-Crate, Frictionless, DCAT, PROV-O, RDF, and related metadata packages may include OSF only as an optional mirror. They must keep GitHub, Hugging Face, and Zenodo as the canonical public surfaces unless a later migration plan changes that deliberately.

## Zenodo Requirement Applicability

This track does not change Zenodo draft/archive workflow mechanics. The zenodraft requirement is therefore not applicable to the repo-side OSF policy implementation; Zenodo remains the authoritative DOI-bearing surface and protected publishing remains covered by `zenodo_rights_metadata_and_zenodraft_workflow_20260609`.

## Focused Validation

Commands run:

```powershell
python scripts/check_osf_optional_mirror_policy.py
python -m unittest tests.test_osf_optional_mirror_policy
```
