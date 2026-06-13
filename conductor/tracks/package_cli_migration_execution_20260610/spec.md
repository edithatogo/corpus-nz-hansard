# Spec: Package And CLI Migration Execution

## Goal

Execute the package/CLI migration plan from corpus-family engineering alignment.

## MoSCoW Requirements

### Must

- Preserve existing script behaviour, manifests, tests, and release outputs.
- Introduce package modules and CLI entry points incrementally.
- Keep backwards-compatible script shims or migration notes.
- Validate with current unit, ruff, manifest, and release checks.

### Should

- Align CLI naming with corpus-family conventions.
- Improve developer docs and task discovery.

### Could

- Publish internal package docs or API reference after migration.

### Won't

- Rewrite pipeline logic without regression evidence.

## Acceptance Criteria

- Package/CLI entry points exist, legacy workflows still pass, and docs describe migration paths.
