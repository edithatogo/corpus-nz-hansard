# Track web_annotation_selector_contract_20260610 Context

Define a shared W3C Web Annotation selector contract for source-linked derived outputs.

This contract standardizes selector payloads across speech turns, topic units, UD tokens, RDF annotations, and search chunks without requiring every endpoint to emit a full annotation graph.

Current implementation surface:

- `schemas/web_annotation_selector.schema.json`
- `manifests/web_annotation_selector_contract.json`
- `docs/web-annotation-selector-contract.md`
- `docs/web-annotation-selector-migration.md`
- `docs/endpoint-contracts.md`

## Shared Selector Schema

The shared selector schema preserves `source_document_id`, `source_document_uri`, `source_hash`, `source_stable_id`, `source_component_id`, and a selector-specific payload.

## Normalization Policy

The contract preserves source text by default, keeps UTF-8 code-point offsets, and uses source-preserving casing unless a downstream consumer requires a narrower normalization rule.

## Migration Notes

Existing `sourceStableId`, offset, quote, and fragment fields migrate onto the shared selector schema without forcing endpoint-specific annotation graphs.

## Endpoint References

`docs/endpoint-contracts.md` is the shared endpoint reference that points consumers at the selector contract.
