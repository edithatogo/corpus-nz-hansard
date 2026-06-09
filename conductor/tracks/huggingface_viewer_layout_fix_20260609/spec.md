# Spec: Hugging Face Viewer Layout Fix

## Goal

Verify and fix any confirmed Hugging Face viewer split/cast or file-layout issue, then add layout regression checks.

## Acceptance Criteria

- The work preserves the preferred corpus-family labels corpus-nz-hansard and corpus-nz-legislation.
- GitHub, Hugging Face, Zenodo, OSF, and future metadata environments are considered where relevant.
- Evidence is recorded in the track and linked documentation.
- Existing published URLs and DOI records are not broken without a migration plan.

## Zenodo Requirement

Any Zenodo draft/archive workflow work in this track must use or formally evaluate zenodraft from https://github.com/zenodraft/zenodraft. Publication commands must remain separate from draft upload/update commands and require protected approval.
