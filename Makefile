PYTHON ?= python

.PHONY: quality pixi-install pixi-quality quality-config learning-log provenance-policy version-consistency public-surface-audit zenodo-rights shared-core metadata-packages osf-policy multi-git-archive-mirroring hathitrust-acquisition parliament-stealth-access wikipedia-mp-lists-acquisition member-identity-triangulation corpus-family-alignment corpus-family-engineering authority-sources parliament-dataset-inventory parliament-dataset-seed-fetchers parliament-dataset-full-acquisition parliament-video-source-inventory parliament-video-seed-fetchers parliament-video-reconciliation parliament-video-media-acquisition-decision historical-sitting-inventory historical-sitting-official-exports historical-sitting-official-exports-coverage historical-sitting-reconciliation historical-coverage release-ladder gold-evaluation canonical-ids dependency-extras procedure-model neutral-components akoma-ntoso parlamint-nz popolo-ocd ud-conllu rdf-linked-data corpus-wide-member-identity corpus-wide-party-attribution validated-speech-turn derived-fields-validation lint format-check typecheck typecheck-basedpyright typecheck-pyrefly spell workflow-audit toml-check workflow-syntax test test-offline benchmark profile-search-index security-audit sbom dependency-check dead-code mutation-smoke

quality: pixi-install lint format-check typecheck spell workflow-audit toml-check workflow-syntax quality-config learning-log provenance-policy version-consistency public-surface-audit zenodo-rights shared-core metadata-packages osf-policy multi-git-archive-mirroring hathitrust-acquisition parliament-stealth-access wikipedia-mp-lists-acquisition member-identity-triangulation corpus-family-alignment corpus-family-engineering authority-sources parliament-dataset-inventory parliament-dataset-seed-fetchers parliament-dataset-full-acquisition parliament-video-source-inventory parliament-video-seed-fetchers parliament-video-reconciliation parliament-video-media-acquisition-decision historical-sitting-inventory historical-sitting-official-exports historical-sitting-official-exports-coverage historical-sitting-reconciliation historical-coverage release-ladder gold-evaluation canonical-ids dependency-extras procedure-model neutral-components akoma-ntoso parlamint-nz popolo-ocd ud-conllu rdf-linked-data corpus-wide-member-identity corpus-wide-party-attribution validated-speech-turn derived-fields-validation test

pixi-install:
	pixi install

pixi-quality:
	pixi run quality

quality-config:
	$(PYTHON) scripts/check_quality_gate.py

learning-log:
	$(PYTHON) scripts/check_conductor_learning_log.py

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

multi-git-archive-mirroring:
	$(PYTHON) scripts/check_multi_git_archive_mirroring.py

hathitrust-acquisition:
	$(PYTHON) scripts/check_hathitrust_acquisition.py

parliament-stealth-access:
	$(PYTHON) scripts/check_parliament_website_stealth_access.py

wikipedia-mp-lists-acquisition:
	$(PYTHON) scripts/check_wikipedia_mp_lists_acquisition.py

member-identity-triangulation:
	$(PYTHON) scripts/check_member_identity_triangulation.py

corpus-family-alignment:
	$(PYTHON) scripts/check_corpus_family_alignment.py

corpus-family-engineering:
	$(PYTHON) scripts/check_corpus_family_engineering_alignment.py

authority-sources:
	$(PYTHON) scripts/check_authority_sources.py

parliament-dataset-inventory:
	$(PYTHON) scripts/check_parliament_dataset_inventory.py

parliament-dataset-seed-fetchers:
	$(PYTHON) scripts/check_parliament_dataset_seed_fetchers.py

parliament-dataset-full-acquisition:
	$(PYTHON) scripts/check_parliament_dataset_full_acquisition.py

parliament-video-source-inventory:
	$(PYTHON) scripts/check_parliament_video_source_inventory.py

parliament-video-seed-fetchers:
	$(PYTHON) scripts/check_parliament_video_seed_fetchers.py

parliament-video-reconciliation:
	$(PYTHON) scripts/check_parliament_video_reconciliation.py

parliament-video-media-acquisition-decision:
	$(PYTHON) scripts/check_parliament_video_media_acquisition_decision.py

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

typecheck-basedpyright:
	basedpyright --level error scripts/check_quality_gate.py scripts/select_committee_reports/cache.py tests/test_select_committee_reports_cache.py test_support.py

typecheck-pyrefly:
	pyrefly check scripts/build_search_index.py scripts/check_corpus_family_engineering_alignment.py scripts/check_quality_gate.py scripts/select_committee_reports/cache.py tests/test_build_search_index.py tests/test_corpus_family_engineering_alignment.py tests/test_select_committee_reports_cache.py test_support.py

spell:
	typos --config typos.toml

workflow-audit:
	zizmor --min-severity medium .github/workflows

toml-check:
	taplo format --check pyproject.toml pixi.toml typos.toml

workflow-syntax:
	actionlint -color

test:
	$(PYTHON) -m pytest -q

test-offline:
	$(PYTHON) -m pytest -q --disable-socket

benchmark:
	$(PYTHON) -m pytest -q tests/test_performance_benchmarks.py

profile-search-index:
	$(PYTHON) -m pyinstrument --outfile .tmp/search-index-profile.html -m pytest -q tests/test_build_search_index.py

security-audit:
	$(PYTHON) -m pip_audit --strict --cache-dir .tmp/pip-audit-cache --progress-spinner off

sbom:
	cyclonedx-py environment --output-file reports/sbom.cdx.json

dependency-check:
	deptry tests --exclude venv --exclude \.venv --exclude \.git --ignore DEP001,DEP002 --known-first-party scripts --known-first-party test_support --package-module-name-map FlagEmbedding=flagembedding,torch=torch,transformers=transformers,pydantic-ai-slim=pydantic_ai,msgspec=msgspec,orjson=orjson,xsdata=xsdata,ibis-framework=ibis,tantivy=tantivy,sqlite-vec=sqlite_vec --no-ansi

dead-code:
	vulture scripts/build_search_index.py scripts/check_quality_gate.py scripts/select_committee_reports/cache.py tests/test_build_search_index.py tests/test_select_committee_reports_cache.py test_support.py --min-confidence 80

mutation-smoke:
	$(PYTHON) scripts/run_mutation_smoke.py
