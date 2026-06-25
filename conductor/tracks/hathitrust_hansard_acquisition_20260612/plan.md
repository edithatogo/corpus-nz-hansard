# Plan: HathiTrust Hansard Acquisition

Status: complete-deferred.

Release status: closed-deferred-external-access-required.

- [x] Task: Identify collection and verify 510 full-view items
- [x] Task: Investigate HathiTrust API endpoints (documented in evidence.md)
- [x] Task: Build deterministic inventory manifest from committed Wayback sample
- [x] Task: Document external unblock requirements for HathiTrust Data API key, local hathifile, or browser-backed enumeration
- [x] Task: Enumerate known sample volume IDs (39 sample IDs recovered; remaining 471 require OAuth/API, hathifile, or verified browser-backed access)
- [x] Task: Close repo-side work as complete-deferred until external access is available

## Current Reconciliation (2026-06-25)

Completed evidence-backed work is limited to source identification, archived collection review, API/access-path documentation, and a 39-ID sample inventory from Wayback page 1. This track has not acquired the complete HathiTrust corpus: the complete 510-volume identifier list, bibliographic metadata, OCR downloads, corpus conversion, and sitting-calendar reconciliation remain external-input requirements.

The track is closed as complete-deferred. Reopen only with one of the accepted evidence paths below:

1. Provide a local monthly `hathi_full_YYYYMMDD.txt.gz` hathifile and run `python scripts/fetch_hathitrust.py --from-hathifile <file> --validate-inventory`.
2. Obtain a HathiTrust Data API OAuth/access key and validate a METS/OCR probe.
3. Use a verified browser-backed collection enumeration path and document the resulting 510-ID evidence.

The acquisition remains non-claiming until `enumerated_count == 510` and approved OCR/API access is validated.
