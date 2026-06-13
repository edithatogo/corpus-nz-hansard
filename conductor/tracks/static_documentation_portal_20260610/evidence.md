# Evidence: Static Documentation Portal

Status: complete.

Implemented artifacts:

- `docs/static-documentation-portal.md`
- `docs/static-documentation-portal/index.html`
- `manifests/static_documentation_portal_manifest.json`
- `schemas/static_documentation_portal.schema.json`
- `scripts/build_static_documentation_portal.py`
- `scripts/check_static_documentation_portal.py`
- `tests/test_static_documentation_portal.py`

Validation evidence:

- `python scripts/build_static_documentation_portal.py`
- `python scripts/check_static_documentation_portal.py`
- `python -m unittest tests.test_static_documentation_portal`

Boundary:

- The portal is static and read-only.
- It mirrors repository docs/manifests and does not replace them.
- Sample-only endpoints and blocked tracks remain outside the public release claim.
