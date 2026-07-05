# Evidence

Release posture: metadata-first coverage ledger.

Evidence added:

- `scripts/build_parliament_video_archive_coverage.py` generates the video coverage manifest and docs.
- `scripts/check_parliament_video_archive_coverage.py` validates schema, source surfaces, adjacent-repo findings, and rights/no-completeness guardrails.
- `tests/test_parliament_video_archive_coverage.py` exercises the builder and checker.
- `manifests/parliament_video_archive_coverage.json` records that Parliament videos are not completely archived.

Final finding:

- Retrospective Parliament video coverage is not complete.
- Ongoing Parliament video archiving is not complete.
- Adjacent repos do not provide a complete NZ Parliament video archive.
- Future work should be a metadata seed-fetcher track before any media-file acquisition decision.
