# Upstream Submission Execution

## Purpose

Record upstream handoff attempts for maintainer-review packages after endpoint validation gates pass.

## Current Targets

- ParlaMint-NZ / TEI
- Popolo / Open Civic Data
- Akoma Ntoso
- CAP / ParlaCAP
- Universal Dependencies / CoNLL-U
- RDF / Linked Data

## Submission Rule

- Do not mark a target submitted without external evidence.
- Keep local blockers explicit.
- Record the upstream mechanism, template, gate, URL, date, response, and follow-up for each target.

## Current State

- All tracked targets remain blocked locally.
- No submission URLs are recorded yet.
- This is a local-review-only execution log.

## Validation

- `python scripts/check_upstream_submission_execution.py`
- `python -m unittest tests.test_upstream_submission_execution`
