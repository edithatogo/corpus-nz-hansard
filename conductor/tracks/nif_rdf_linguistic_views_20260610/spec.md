# Spec: NIF/RDF Linguistic Annotation Views

## Goal

Add NIF/RDF linguistic annotation views linking token and sentence annotations to stable source selectors.

## MoSCoW Requirements

### Must

- Depend on RDF linked-data and UD/CoNLL-U endpoint maturity.
- Link token/sentence annotations to stable document selectors and source hashes.
- Validate RDF parsing, URI stability, selector consistency, and vocabulary use.

### Should

- Reuse canonical URI, W3C Web Annotation, and model provenance contracts.
- Include SPARQL examples for linguistic annotations.

### Could

- Publish NIF views for a sample before full corpus generation.

### Won't

- Duplicate NLP payloads without stable links to source text.

## Acceptance Criteria

- NIF/RDF output validates and has clear dependency and machine-generated status.
