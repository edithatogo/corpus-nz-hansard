# W3C Web Annotation Selector Contract

## Purpose

Standardize source-linked selector payloads across derived outputs without requiring every endpoint to emit a full Web Annotation graph.

## Contract

- Use a shared selector schema at `schemas/web_annotation_selector.schema.json`.
- Keep selector payloads source-linked by `source_document_id`, `source_document_uri`, `source_hash`, `source_stable_id`, and `source_component_id`.
- Support `TextQuoteSelector`, `TextPositionSelector`, `FragmentSelector`, `LinePositionSelector`, and `PagePositionSelector`.
- Preserve source-bound offsets and quote text as emitted from the source-linked derivative.

## Normalization Policy

- `unicode_normalization`: preserve source text unless a downstream consumer requires normalization.
- `whitespace_policy`: preserve source whitespace in the contract payload.
- `offset_basis`: use UTF-8 code points for character offsets unless a source archive exposes stable line or page positions.
- `case_sensitivity`: preserve source casing.

## Current Consumers

- speech turns
- topic units
- UD / CoNLL-U tokens
- RDF annotations
- search chunks

## Limits

- Selectors must not depend on row numbers or file paths alone.
- The contract does not require a full W3C Web Annotation graph for every output.
- Selector payloads describe source-linked spans, not gold annotation truth.

## Validation

- `python scripts/check_web_annotation_selector_contract.py`
- `python -m unittest tests.test_web_annotation_selector_contract`
