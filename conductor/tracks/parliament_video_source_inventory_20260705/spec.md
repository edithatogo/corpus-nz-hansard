# Parliament Video Source Inventory

## Overview

Inventory every known public NZ Parliament video surface before any capture work. This track turns the current coverage finding into a source-by-source map that can drive metadata fetchers and later reconciliation.

## Requirements

- Cover official YouTube, `videos.parliament.nz`, previous Parliament On Demand, select committee archive pages, Vimeo-era links, embedded Parliament website media, and discoverable feeds/APIs/sitemaps.
- Record source URL, platform, expected date range, access method, rights notes, media types, metadata availability, and known blockers.
- Reconcile against adjacent repo evidence, especially `sm-govt-nz`, without treating it as a complete Parliament video archive.
- Preserve metadata-first/no-download policy.

## Acceptance Criteria

- A source inventory manifest and docs exist.
- Every known video surface has a stable source id.
- Rights/access/completeness status is explicit.
- Validation prevents any complete-archive claim.
