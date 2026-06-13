# Spec: Akoma Ntoso Public Endpoint Release

## Goal

Move Akoma Ntoso output from sample package to a validated public endpoint release.

## MoSCoW Requirements

### Must

- Select and document the Akoma Ntoso profile and conformance boundaries.
- Generate validated document/proceeding structure with stable IDs and source selectors.
- Preserve source document linkage, dates, chamber/session metadata, and provenance.
- Emit schema/profile validation evidence, manifest, and docs.

### Should

- Align proceedings, questions, motions, speeches, and votes with released neutral components.
- Include examples showing profile-specific choices.

### Could

- Release only well-validated document types first.

### Won't

- Treat sample XML as a public release without profile validation.

## Acceptance Criteria

- Public endpoint output validates under the declared profile or records exact deviations.
- Release docs distinguish profile conformance, limitations, and excluded structures.
