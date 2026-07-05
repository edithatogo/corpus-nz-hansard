# Parliament Video Reconciliation

## Overview

Validate the Parliament video metadata archive against multiple independent sources before any completeness claim.

## Requirements

- Reconcile video records against Parliament sitting calendars, Hansard sitting dates, committee meeting records, sitting programmes, Parliament site search, YouTube, On Demand, Vimeo, and Internet Archive URL evidence.
- Classify gaps as expected no video, video found, metadata only, fallback-only, missing everywhere, access blocked, rights blocked, or duplicate/migrated.
- Produce machine-readable exception ledgers.

## Acceptance Criteria

- Metadata completeness is backed by multi-source reconciliation.
- Unresolved gaps are explicit and stable.
- No media completeness claim is possible from metadata alone.
