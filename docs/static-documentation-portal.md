# Static Documentation Portal

This portal is a static status surface generated from repository docs and manifests.
It is designed for researchers, maintainers, and release reviewers.
It shows validation status alongside citation patterns and endpoint readiness.

## Build

```powershell
python scripts\build_static_documentation_portal.py
python scripts\check_static_documentation_portal.py
python -m unittest tests.test_static_documentation_portal
```

## Scope

- Release ladder status
- Endpoint readiness
- Citation guidance
- Data dictionary entry points
- Public release surfaces

## Hosting

Serve the generated `docs/static-documentation-portal/` directory as a static site on
GitHub Pages or any equivalent static host.

The portal is read-only. Hosting it does not change any release claim, and it does not
promote sample-only endpoints or blocked tracks into public release status.

## Claim Boundary

The portal mirrors repository state. It does not replace source-of-truth manifests.
Sample-only endpoints and blocked tracks remain outside the public release claim.
