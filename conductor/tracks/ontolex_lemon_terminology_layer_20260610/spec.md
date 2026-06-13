# Spec: OntoLex-Lemon Terminology Layer

## Goal

Add an optional terminology/lexicon layer for NZ parliamentary and legal vocabulary if downstream RDF/NLP use cases require it.

## MoSCoW Requirements

### Must

- Keep the layer optional and separate from canonical corpus facts.
- Define terms, variants, concepts, sources, provenance, and review status.
- Avoid implying official definitions without source authority.

### Should

- Integrate with SKOS concept schemes and RDF linked-data outputs.
- Support multilingual/variant labels if evidence exists.

### Could

- Add examples for glossary and search expansion use cases.

### Won't

- Treat generated term lists as authoritative legal definitions.

## Acceptance Criteria

- Terminology layer has explicit source, status, and optional-publication boundaries.
