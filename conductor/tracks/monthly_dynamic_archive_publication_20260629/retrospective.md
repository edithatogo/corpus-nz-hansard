# Retrospective: Monthly Dynamic Archive Publication

Track ID: `monthly_dynamic_archive_publication_20260629`

## Phase 1: Publication Contract

- Outcome: completed
- Evidence: `conductor/tracks/monthly_dynamic_archive_publication_20260629/evidence.md`
- What worked: the contract separated generated artifacts, public surfaces, rights boundaries, and protected Zenodo publication.
- Follow-up: keep evidence manifests machine-readable and aligned with the strongest verified publication run.
- Reviewer sign-off: recorded by repository maintainer review in the completed track evidence.

## Phase 2: Scheduled GitHub Actions

- Outcome: completed
- Evidence: `.github/workflows/monthly_dynamic_archive_publication.yml`
- What worked: dry-run, Hugging Face, Zenodo draft, and full modes gave a staged release path without direct unprotected Zenodo publication.
- Follow-up: keep publication workflows manual or scheduled only, with dependency-update paths excluded from publication.
- Reviewer sign-off: recorded by repository maintainer review in the completed track evidence.

## Phase 3: Evidence And Validation

- Outcome: completed
- Evidence: `scripts/check_monthly_dynamic_archive_publication.py`
- What worked: the checker protects required evidence fields, rights boundaries, protected handoff behavior, and cross-surface consistency.
- Follow-up: extend checks when future publication surfaces become active.
- Reviewer sign-off: recorded by repository maintainer review in the completed track evidence.

## Phase 4: First Monthly Release Proof

- Outcome: completed
- Evidence: `conductor/tracks/monthly_dynamic_archive_publication_20260629/evidence.md`
- What worked: dry-run, Hugging Face publication, Zenodo draft upload, protected publish, public record verification, and artifact hash checks were all captured.
- Follow-up: keep monthly scheduled runs reviewed against public Hugging Face and Zenodo surfaces after each material release.
- Reviewer sign-off: recorded by repository maintainer review in the completed track evidence.
