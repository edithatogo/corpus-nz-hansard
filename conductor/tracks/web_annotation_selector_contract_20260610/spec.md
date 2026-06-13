# Spec: W3C Web Annotation Selector Contract

## Goal

Standardize selector payloads for source spans across derived components, endpoints, search chunks, RDF links, and NLP outputs.

## MoSCoW Requirements

### Must

- Define a reusable selector schema covering document ID, character offsets, text quote, text position, source hash, and normalization policy.
- Support W3C Web Annotation-style selectors without requiring every endpoint to emit full annotation graphs.
- Validate selector bounds, quote matching, and source-document linkage.

### Should

- Support line/page selectors where source archives expose stable page or line positions.
- Feed speech turns, topic units, UD tokens, search chunks, and RDF annotations.

### Could

- Add JSON-LD context for full annotation graph exports.

### Won't

- Use selectors that depend only on unstable generated row numbers.

## Acceptance Criteria

- Shared selector schema, docs, tests, and migration notes exist.
- Existing and future endpoint specs reference the same selector contract.
