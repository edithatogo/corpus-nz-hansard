# Canonical ID And URI Policy

## Purpose

Stable identifiers are required before neutral components, RDF, Popolo/Open Civic Data, ParlaMint, Akoma Ntoso, CAP/ParlaCAP, CoNLL-U, or linked metadata outputs are published.

The machine-readable policy is `manifests/id_uri_policy.json`. Deterministic helper functions live in `scripts/canonical_ids.py`.

## Document Identity

The published document-level identity field is `stable_id`. Reuse `stable_id` whenever document-level identity is sufficient, and do not rewrite `v0.1.0` `stable_id` values.

The existing fallback to source file plus source row is a published document-level legacy fallback only. New neutral components and endpoint artifacts must not depend on transient file paths or row positions alone.

## Canonical ID Pattern

New IDs use canonical JSON payloads and a SHA-256 digest prefix:

```text
nzhc-{artifact-class-or-component-type}-{sha256(canonical-json-payload)[0:16]}
```

The payload must include stable release, source, component, validation, or authority fields. It must not use generated file paths, array indexes, or source row positions as the only identity input.

Required examples:

- Document view: `nzhc-document-8e93abc58c9b722f`
- Speech-turn component: `nzhc-component-0dc17fbde51c939f`
- Endpoint artifact: `nzhc-endpoint-artifact-1198084efe0e38e7`
- Authority source snapshot: `nzhc-authority-source-d89cb3c98830032d`

## URI Namespace

Planned namespace:

```text
https://w3id.org/nz-hansard/
```

URI patterns:

- `https://w3id.org/nz-hansard/document/{id}`
- `https://w3id.org/nz-hansard/component/{id}`
- `https://w3id.org/nz-hansard/endpoint/{id}`
- `https://w3id.org/nz-hansard/authority/{id}`
- `https://w3id.org/nz-hansard/sample/{id}`

SPARQL-friendly prefixes:

```sparql
PREFIX nzh: <https://w3id.org/nz-hansard/>
PREFIX nzhc: <https://w3id.org/nz-hansard/component/>
```

Do not mint RDF URIs outside this namespace without adding a compatibility note and validation evidence.

## Deprecation And Redirects

If a published identifier changes, add a mapping manifest at `manifests/id_uri_deprecations.json` before publishing the replacement.

Minimum mapping fields:

- `old_id`
- `new_id`
- `old_uri`
- `new_uri`
- `reason`
- `effective_date`
- `replacement_status`

Old URIs should remain resolvable through redirects or explicit tombstone documentation. DOI, release-note, and endpoint manifests that referenced old IDs must remain auditable.

## Endpoint Gate

Endpoint tracks must reference `manifests/id_uri_policy.json` before publication. RDF and civic-data endpoints must validate generated IDs and URIs against this policy before release.

