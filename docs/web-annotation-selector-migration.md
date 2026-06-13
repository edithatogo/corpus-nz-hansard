# Web Annotation Selector Migration Notes

## Goal

Migrate source-span fields onto the shared selector contract without changing the underlying release semantics.

## Current Patterns

- `sourceStableId` in RDF and related linked-data outputs becomes the `source_stable_id` field in selector payloads.
- `StartChar` / `EndChar` pairs in CoNLL-U alignments become `text_position.start_offset` and `text_position.end_offset`.
- `href`, `refersTo`, and `by` references in annotation-like outputs stay as source-linked identifiers but should be paired with selector payloads where spans are material.
- Search chunks can use the same source document identifiers and hashes even when only text quotes are available.

## Migration Rules

- Preserve the original source document identifier and source hash.
- Prefer `TextQuoteSelector` when the exact source text is available.
- Prefer `TextPositionSelector` when offsets are stable and exact text quoting is not enough.
- Use `FragmentSelector` for stable URI fragments and resource-internal references.
- Use `LinePositionSelector` or `PagePositionSelector` only when the archive exposes stable line or page positions.

## Non-Goals

- Do not infer selectors from transient row ordering.
- Do not replace the existing endpoint-specific provenance model.
- Do not emit full annotation graphs unless a downstream consumer explicitly needs them.
