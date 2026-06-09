PYTHON ?= python

.PHONY: quality quality-config provenance-policy lint format-check typecheck spell workflow-audit toml-check workflow-syntax test

quality: lint format-check typecheck spell workflow-audit toml-check workflow-syntax quality-config provenance-policy test

quality-config:
	$(PYTHON) scripts/check_quality_gate.py

provenance-policy:
	$(PYTHON) scripts/check_release_provenance_policy.py

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
