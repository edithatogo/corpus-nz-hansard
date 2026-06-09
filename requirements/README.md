# Optional Requirement Groups

`../requirements.txt` is the base runtime for the existing corpus pipeline.

These files document endpoint-specific optional stacks. Install them only for the track that needs them.
`requirements.txt` in this directory is an aggregate manifest for GitHub Dependency Graph visibility; it is not the default runtime install target.

```powershell
python -m pip install -r requirements\xml.txt
python -m pip install -r requirements\rdf.txt
python -m pip install -r requirements\nlp.txt
```

The optional groups intentionally do not include large model downloads. Track implementations must record model names, versions, and download commands in their validation manifests.

Policy authority is `manifests/dependency_extras_policy.json`, validated by `scripts/check_dependency_extras_policy.py`. Endpoint validation manifests must record `tool_versions`, `library_versions`, `model_versions`, `dependency_groups`, `install_commands`, `lock_or_constraints`, `release_affecting_dependencies`, and `validation_command`. Optional group install checks remain `deferred-until-implementation` until endpoint implementation starts, and release-affecting stacks use `pin-before-release-artifact`.

All governed groups:

- `requirements/data.txt`
- `requirements/schema.txt`
- `requirements/xml.txt`
- `requirements/rdf.txt`
- `requirements/authority.txt`
- `requirements/nlp.txt`
- `requirements/ml.txt`
- `requirements/metadata.txt`
