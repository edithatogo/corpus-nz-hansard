# Entity Linking Exploratory Outputs

## Scope

This track publishes non-authoritative, machine-assisted entity-linking outputs for
people, organisations, places, legislation, ministries, portfolios, and committees.
The outputs are exploratory only and must not be treated as validated parliamentary or
legal metadata.

## Outputs

- `samples/entity-linking-exploratory/entity_linking_exploratory.jsonl`
- `samples/entity-linking-exploratory/entity_linking_exploratory_review.csv`

## Review Sample

The review sample records positive, ambiguous, unresolved, negative, and excluded
examples. It preserves mention text, selectors, candidate IDs, candidate scores,
authority-source references, and provenance.

## False-Positive Analysis

Known false-positive patterns include:

- office titles mistaken for people or portfolios
- electorate labels mistaken for places
- generic procedural phrases mistaken for committees
- ministry names that need dated authority snapshots
- bill titles that should only be linked when the title match is exact

These patterns are explicitly retained so downstream evaluation can measure where a
rule or model would over-link text.

## Downstream Use

Exploratory outputs may feed search or RAG enrichment and RDF exploratory graphs, but
they remain non-authoritative until independently validated.

## Validation

- `python scripts/build_entity_linking_exploratory_outputs.py`
- `python scripts/check_entity_linking_exploratory_outputs.py`
- `python -m unittest tests.test_entity_linking_exploratory_outputs`
