PYTHON ?= python

.PHONY: quality uv-lock uv-sync quality-config provenance-policy version-consistency public-surface-audit zenodo-rights shared-core metadata-packages osf-policy corpus-family-alignment corpus-family-engineering authority-sources historical-coverage lint format-check typecheck spell workflow-audit toml-check workflow-syntax test

quality: uv-lock uv-sync lint format-check typecheck spell workflow-audit toml-check workflow-syntax quality-config provenance-policy version-consistency public-surface-audit zenodo-rights shared-core metadata-packages osf-policy corpus-family-alignment corpus-family-engineering authority-sources historical-coverage test

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

historical-coverage:
	$(PYTHON) scripts/check_historical_coverage_audit.py

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
