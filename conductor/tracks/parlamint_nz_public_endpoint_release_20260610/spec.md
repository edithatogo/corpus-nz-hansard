# Spec: ParlaMint-NZ Public Endpoint Release

## Goal

Move ParlaMint-NZ from contract/sample readiness to a validated public endpoint package.

## MoSCoW Requirements

### Must

- Declare exact coverage, exclusions, component dependencies, and validation status.
- Generate TEI/ParlaMint-compatible output from validated neutral components.
- Validate schema/profile conformance and source-document linkage.
- Include metadata, manifest, release notes, and maintainer-facing review evidence.

### Should

- Align speaker, party, sitting, and proceeding identifiers with released derived components.
- Include examples and known divergence notes for ParlaMint maintainers.

### Could

- Stage a limited historical subset before full corpus coverage.

### Won't

- Submit or publish outputs that rely on unvalidated speech turns or identity data without explicit status labels.

## Acceptance Criteria

- Endpoint package validates and has reproducible generation instructions.
- Public docs identify sample-only versus release-ready status accurately.
