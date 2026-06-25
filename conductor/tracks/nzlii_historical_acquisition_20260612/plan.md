# Plan: NZLII Historical Acquisition

Status: complete-deferred.

Release status: closed-deferred-external-access-required.

- [x] Task: Attempt access to nzlii.org/nz/legis/hist_bill/ - blocked (Cloudflare 403)
- [x] Task: Try alternative NZLII access patterns - https/http historical bills and nzparl paths remain Cloudflare 403
- [x] Task: Recheck robots.txt - current 2026-06-24 recheck also returns Cloudflare 403
- [x] Task: Check if NZLII has an API or bulk data access - no repo-verified API/bulk path
- [x] Task: Document repo-side resolution as complete-deferred in manifests/nzlii_historical_acquisition_status.json

Future unblock criteria:

- NZLII permission or documented bulk/API access path.
- Verified browser-backed access route approved for collection-scale acquisition.
- Alternate official or archive source covering the same historical bills without bypassing access controls.

Operational boundary: do not keep retrying direct HTTP acquisition while Cloudflare challenge responses persist. Use HathiTrust and official parliamentary sources as preferred historical acquisition paths.
