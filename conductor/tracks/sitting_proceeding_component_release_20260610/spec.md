# Spec: Sitting And Proceeding Component Release

## Goal

Create validated corpus-wide sitting and proceeding components that can anchor downstream parliamentary endpoints.

## MoSCoW Requirements

### Must

- Represent sittings, proceeding sections, order-of-business units, dates, chamber/session metadata, and source links.
- Reconcile generated structures against official sitting/proceeding evidence where available.
- Emit schemas, validation manifests, and coverage metrics.

### Should

- Support stable IDs for proceedings and nested units.
- Preserve links to raw document boundaries and selectors.
- Feed Akoma Ntoso, ParlaMint, RDF, CAP/ParlaCAP, and search/RAG layers.

### Could

- Add a manual correction queue for difficult historical structures.

### Won't

- Claim full historical completeness until official reconciliation passes.

## Acceptance Criteria

- Component output is reproducible and validates against schema.
- Coverage reports identify missing, inferred, and reconciled sittings/proceedings.
- Downstream endpoint dependencies are explicitly updated.
