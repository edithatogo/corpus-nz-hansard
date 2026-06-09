# Spec: Release Ladder

## MoSCoW Requirements

### Must

- Define document-level, authority-source, neutral-component, endpoint, and upstream-contribution release levels.
- Map each current and future artifact to a release level.
- Define validation and publication gates for each level.
- Preserve `v0.1.0` as immutable document-level data except metadata/cross-reference corrections.

### Should

- Add release-series fields to component and endpoint manifests.
- Document how Hugging Face, GitHub, Zenodo, and upstream contribution packages relate.

### Could

- Add automation for release-readiness manifests by ladder level.

### Won't

- Publish endpoint artifacts as part of document-level releases.

## Acceptance Criteria

- Release ladder policy and manifest fields are documented and testable.
