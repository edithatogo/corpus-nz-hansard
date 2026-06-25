# Evidence: NZLII Historical Acquisition

Status: complete-deferred.

Release status: closed-deferred-external-access-required.

Manifest: `manifests/nzlii_historical_acquisition_status.json`

Current 2026-06-24 direct HTTP recheck:

- `https://www.nzlii.org/nz/legis/hist_bill/` returned Cloudflare 403 with `Cf-Mitigated: challenge`.
- `https://www.nzlii.org/nz/other/nzparl/` returned Cloudflare 403 with `Cf-Mitigated: challenge`.
- `http://www.nzlii.org/nz/legis/hist_bill/` returned Cloudflare 403 with `Cf-Mitigated: challenge`.
- `https://www.nzlii.org/robots.txt` returned Cloudflare 403 with `Cf-Mitigated: challenge` on the current recheck.

Prior evidence recorded robots.txt content signals (`search=yes`, `ai-train=no`), but the current recheck cannot rely on reachable robots.txt because that URL is also challenged.

Resolution: repo-side work is complete-deferred. Direct HTTP acquisition remains blocked and should not be retried as a normal acquisition path while Cloudflare challenge responses persist. Reopen only after NZLII permission, a documented bulk/API route, or a verified browser-backed route is available. HathiTrust and official Parliament sources remain the preferred historical acquisition routes while this blocker stands.
