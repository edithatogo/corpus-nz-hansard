PYTHON ?= python

.PHONY: quality uv-lock uv-sync quality-config provenance-policy version-consistency public-surface-audit zenodo-rights shared-core metadata-packages osf-policy corpus-family-alignment corpus-family-engineering authority-sources historical-sitting-inventory historical-sitting-official-exports historical-sitting-official-exports-coverage historical-coverage release-ladder gold-evaluation canonical-ids dependency-extras procedure-model neutral-components akoma-ntoso parlamint-nz popolo-ocd corpus-wide-member-identity corpus-wide-party-attribution validated-speech-turn lint format-check typecheck spell workflow-audit toml-check workflow-syntax test derived-fields-validation

quality: uv-lock uv-sync lint format-check typecheck spell workflow-audit toml-check workflow-syntax quality-config provenance-policy version-consistency public-surface-audit zenodo-rights shared-core metadata-packages osf-policy corpus-family-alignment corpus-family-engineering authority-sources historical-sitting-inventory historical-sitting-official-exports historical-sitting-official-exports-coverage historical-coverage release-ladder gold-evaluation canonical-ids dependency-extras procedure-model neutral-components akoma-ntoso parlamint-nz popolo-ocd corpus-wide-member-identity corpus-wide-party-attribution validated-speech-turn derived-fields-validation test

uv-lock:
	uv lock --check

uv-sync:
	uv sync --frozen --all-groups

quality-config:
	$(PYTHON) scripts/check_quality_gate.py

provenance-policy:
	$(PYTHON) scripts/check_release_provenance_policy.py

version-consistency:
	$(PYTHON) scripts/check_release_version_consistency.py

public-surface-audit:
	$(PYTHON) scripts/check_public_surface_audit.py

zenodo-rights:
	$(PYTHON) scripts/check_zenodo_rights_metadata.py

shared-core:
	$(PYTHON) scripts/check_shared_core_schema.py

metadata-packages:
	$(PYTHON) scripts/check_metadata_packages.py

osf-policy:
	$(PYTHON) scripts/check_osf_optional_mirror_policy.py

corpus-family-alignment:
	$(PYTHON) scripts/check_corpus_family_alignment.py

corpus-family-engineering:
	$(PYTHON) scripts/check_corpus_family_engineering_alignment.py

authority-sources:
	$(PYTHON) scripts/check_authority_sources.py

historical-sitting-inventory:
	$(PYTHON) scripts/check_historical_sitting_inventory.py

historical-sitting-official-exports:
	$(PYTHON) scripts/check_historical_sitting_official_exports.py

historical-sitting-official-exports-coverage:
	$(PYTHON) scripts/build_historical_sitting_official_exports_coverage.py

historical-coverage:
	$(PYTHON) scripts/check_historical_coverage_audit.py

release-ladder:
	$(PYTHON) scripts/check_release_ladder.py

gold-evaluation:
	$(PYTHON) scripts/check_gold_evaluation_datasets.py

canonical-ids:
	$(PYTHON) scripts/check_canonical_id_uri_policy.py

dependency-extras:
	$(PYTHON) scripts/check_dependency_extras_policy.py

procedure-model:
	$(PYTHON) scripts/check_nz_parliamentary_procedure_model.py

neutral-components:
	$(PYTHON) scripts/check_neutral_component_model.py

akoma-ntoso:
	$(PYTHON) scripts/check_akoma_ntoso_endpoint.py

parlamint-nz:
	$(PYTHON) scripts/check_parlamint_nz_endpoint.py

popolo-ocd:
	$(PYTHON) scripts/check_popolo_opencivicdata_endpoint.py

corpus-wide-member-identity:
	$(PYTHON) scripts/check_corpus_wide_member_identity.py

corpus-wide-party-attribution:
	$(PYTHON) scripts/check_corpus_wide_party_attribution.py

validated-speech-turn:
	$(PYTHON) scripts/check_validated_speech_turn_component.py

ud-conllu:
	$(PYTHON) scripts/check_ud_conllu_endpoint.py

rdf-linked-data:
	$(PYTHON) scripts/check_rdf_linked_data_endpoint.py

derived-fields-validation:
	$(PYTHON) scripts/validate_derived_fields.py

lint:
	$(PYTHON) -m ruff check --no-cache .

format-check:
	$(PYTHON) -m ruff format --check --no-cache .

typecheck:
	ty check --error all .

spell:
	typos --config typos.toml

workflow-audit:
	zizmor --min-severity medium .github/workflows

toml-check:
	taplo format --check pyproject.toml typos.toml

workflow-syntax:
	actionlint -color

test:
	$(PYTHON) -m unittest discover tests
