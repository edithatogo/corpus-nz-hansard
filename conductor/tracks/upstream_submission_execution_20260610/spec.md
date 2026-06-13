# Spec: Upstream Submission Execution

## Goal

Convert maintainer-review drafts into real upstream submission handoffs, issues, or pull requests only after endpoint validation gates pass.

## MoSCoW Requirements

### Must

- Identify eligible upstream targets and required package formats.
- Require endpoint validation evidence before submission.
- Record submission dates, URLs, contacts, response status, and follow-up actions.
- Keep external feedback separate from local implementation completion.

### Should

- Use prepared maintainer-review package templates.
- Track requested changes as new Conductor tracks when substantive.

### Could

- Submit staged previews for maintainer feedback before public release.

### Won't

- Treat locally prepared packages as submitted without external evidence.

## Acceptance Criteria

- Submission log and evidence artifacts exist for each upstream handoff.
- Registry distinguishes local readiness, submitted, accepted, rejected, and waiting states.
