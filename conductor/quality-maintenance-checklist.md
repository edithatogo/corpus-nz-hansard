# Quality & Maintenance Tooling Baseline — corpus-nz-hansard

| Tool            | Status     | Notes                                                                 |
|-----------------|------------|-----------------------------------------------------------------------|
| Vale            | ✅ Present | `.vale.ini` exists, extends root styles, `MinAlertLevel = suggestion` |
| Markdownlint    | ✅ Present | `.markdownlint.json` created from root template                       |
| Renovate        | ✅ Present | `renovate.json` created, modelled on `cli-legislation-nz`             |
| Codecov         | ⏳ Conditional | `pytest-cov` in dev deps, `tool.coverage` configured. No `codecov.yml` — add when CI uploads XML |
| Scalene         | ✅ Present | Configured in `pyproject.toml` under `[tool.scalene]`                 |
