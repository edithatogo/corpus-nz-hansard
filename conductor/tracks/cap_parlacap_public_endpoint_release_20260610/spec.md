# Spec: CAP/ParlaCAP Public Endpoint Release

## Goal

Move CAP/ParlaCAP topic outputs from sample readiness to a validated public endpoint release.

## MoSCoW Requirements

### Must

- Define topic units, source selectors, codebook version, annotator/model provenance, and confidence/status fields.
- Generate validated CAP/ParlaCAP-compatible output for the declared scope.
- Preserve links to speech/proceeding/document components.
- Emit validation manifest, codebook provenance, and docs.

### Should

- Confirm expectations with relevant CAP/ParlaCAP maintainers before external submission.
- Include quality metrics and confusion/error analysis for coded samples.

### Could

- Publish human-coded gold samples before model-coded full output.

### Won't

- Present model-only topic labels as validated human-coded CAP data.

## Acceptance Criteria

- Topic package has declared scope, codebook provenance, validation evidence, and non-overclaiming docs.
