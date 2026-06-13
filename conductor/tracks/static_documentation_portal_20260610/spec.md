# Spec: Static Documentation Portal

## Goal

Publish a static documentation surface for researchers, maintainers, and release reviewers.

## MoSCoW Requirements

### Must

- Show release ladder status, endpoint readiness, validation manifests, citation guidance, and data dictionaries.
- Distinguish public releases, sample outputs, local review packages, and blocked tracks.
- Build reproducibly from repository docs and manifests.

### Should

- Include generated status tables and links to schemas/manifests.
- Support GitHub Pages or equivalent static hosting.

### Could

- Add examples, notebooks, and visual coverage summaries.

### Won't

- Replace source-of-truth manifests with hand-maintained status prose.

## Acceptance Criteria

- Static site build exists and reflects current release/track status.
- Public docs avoid claiming readiness for sample-only endpoints.
