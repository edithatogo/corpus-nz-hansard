# Spec: Dependency Extras Policy

## MoSCoW Requirements

### Must

- Keep `requirements.txt` as the base runtime.
- Govern optional dependency groups for data, schema, XML, RDF, authority, NLP, ML, and metadata work.
- Require endpoint tracks to record tool, library, and model versions in validation manifests.

### Should

- Add installation checks for optional groups when endpoint implementation begins.
- Pin dependencies that affect generated release artifacts.

### Could

- Migrate to package extras in `pyproject.toml` if the repository becomes an installable package.

### Won't

- Add heavy NLP/ML/RDF/XML stacks to the default install without a direct production import.

## Acceptance Criteria

- Dependency groups are documented and endpoint tracks cite the relevant group.
