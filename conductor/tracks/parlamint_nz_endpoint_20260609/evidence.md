# Evidence: ParlaMint-NZ Endpoint

## TEI Mapping

- Added `docs/parlamint-nz-mapping.md`.
- The mapping records neutral fixture fields to TEI locations and keeps NZ-specific sittings, questions, votes, stages, rulings, interjections, and procedural text controlled by the neutral component and procedure models.

## Sample Package

- Added `scripts/generate_parlamint_nz_sample.py`.
- Generated `samples/parlamint-nz/ParlaMint-NZ.sample.xml`.
- Generated `samples/parlamint-nz/ParlaMint-NZ.metadata.xml`.
- Generated `samples/parlamint-nz/README.md`.
- The sample traces derived values to `fixtures/neutral_components.json` and is explicitly `sample-not-release`.

## Validation Manifest

- Added `manifests/parlamint_nz_validation_manifest.json`.
- Added `scripts/check_parlamint_nz_endpoint.py`.
- Added `tests/test_parlamint_nz_endpoint.py`.
- The checker validates XML well-formedness, TEI namespaces, neutral reference resolution, dependency groups, release-ladder mapping, traceability, and readiness caveats.

## Readiness Boundary

- Full ParlaMint-NZ readiness remains `blocked-pending-validated-components`.
- Member identity, party attribution, and speech-turn validation are still required before public endpoint publication.
- Full ParlaMint schema validation remains deferred until validated neutral component releases exist and endpoint dependencies are pinned.
