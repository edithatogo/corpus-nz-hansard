# Track Entity Linking Exploratory Outputs

## Purpose

Publish explicitly non-authoritative, machine-assisted entity-linking outputs for
people, organisations, places, legislation, ministries, portfolios, and committees.

## Outputs

- `samples/entity-linking-exploratory/entity_linking_exploratory.jsonl`
- `samples/entity-linking-exploratory/entity_linking_exploratory_review.csv`

## Review Sample

The review sample preserves mentions, selectors, candidate IDs, candidate scores,
authority-source references, and provenance for positive, ambiguous, unresolved,
negative, and excluded examples.

## False-Positive Analysis

The bundle keeps office titles, electorate labels, generic procedural phrases, and
similar near-matches explicit so downstream evaluation can measure over-linking.

## Validation

- Manifest validates against schema.
- JSONL rows validate against the record schema.
- Review CSV covers the seven required entity types and the full class mix.
