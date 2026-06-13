# Spec: DataCite Export Contract

## Goal

Add the missing DataCite export contract and generated payload for DOI-hosting workflows.

## MoSCoW Requirements

### Must

- Map project metadata to DataCite-required and recommended fields.
- Generate a machine-readable DataCite payload for each release package.
- Validate identifiers, creators/contributors, titles, publisher, publication year, resource type, rights, related identifiers, and funding fields.
- Integrate DataCite validation into release-package checks.

### Should

- Reuse SOTA metadata package values where possible.
- Document fields that must remain human-reviewed before DOI deposit.

### Could

- Add examples for Zenodo, Dataverse, and OSF metadata translation.

### Won't

- Mint or deposit DOIs automatically without a human publication gate.

## Acceptance Criteria

- DataCite export, checker, docs, and manifest integration exist.
- Release docs state which metadata is generated and which is depositor-reviewed.
