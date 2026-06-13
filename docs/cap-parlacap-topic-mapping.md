# CAP / ParlaCAP Topic Mapping

This repository exposes a repository-declared review map for maintainer review and sample validation.
It is intentionally narrower than an upstream CAP contribution and keeps model-coded labels out of validated publication.

Current surface:

- `manifests/cap_parlacap_topic_codebook.json`
- `manifests/cap_parlacap_topic_validation_manifest.json`
- `samples/cap-parlacap/cap_parlacap_topics.csv`
- `samples/cap-parlacap/README.md`

Rules:

- Every topic row must reference a source component or reviewed fixture row.
- human-coded and rule-coded labels are treated as reviewed output.
- Model-coded labels stay exploratory-only until independent evaluation evidence exists.
- Topic codes must validate against the declared repository review map.
- ParlaCAP-compatible speech/topic output stays blocked until validated speech-turn components are available.
- Readiness remains `blocked-pending-validated-components`.

Known limitations:

- The codebook mapping is repository-declared and pending maintainer confirmation.
- This sample package does not claim a public CAP / ParlaCAP release.
- The endpoint still depends on validated neutral component releases before publication.
