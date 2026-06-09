# Spec: Corpus Family Naming And Publication Alignment

## Goal

Keep `corpus-nz-hansard` as the systematic Hansard label and align all public environments with the preferred legislation sibling label `corpus-nz-legislation`.

## Context

Sibling legislation project path: `C:\Users\60217257\OneDrive - Flinders\repos\corpus-law-nz`.

Preferred corpus-family labels:

- `corpus-nz-hansard`
- `corpus-nz-legislation`

## Acceptance Criteria

- Conductor product/setup docs record the naming preference.
- Requirements and design docs include cross-corpus publication-surface gates and Mermaid diagrams.
- GitHub, Hugging Face, Zenodo, OSF, and future metadata environments have explicit tasks.
- Existing published URLs and DOI records remain stable unless migration is separately approved.
- Hugging Face viewer/access health is included as a release-readiness requirement.

## Environment Requirements

- GitHub: keep `corpus-nz-hansard`; align topics, homepage, release posture, CI, license, and sibling links.
- Hugging Face: keep `edithatogo/nz-hansard-corpus`; verify viewer health, file layout, `private=false`, and `gated=false`; fix any confirmed split/cast or file-layout issue; add sibling links.
- Zenodo: keep `10.5281/zenodo.20595194` as canonical; treat `10.5281/zenodo.20591997` as superseded review record; align related identifiers and license/provenance.
- OSF: optional review/mirror only; document file-size, checksum, citation, and update rules before use.
- Other: generate Croissant, RO-Crate, Frictionless, DCAT/PROV-O metadata after core release metadata stabilises.

## Out of Scope

- Renaming published DOI records.
- Breaking existing GitHub/HF URLs.
- Publishing OSF mirrors before policy exists.
