# Parliament Dataset Full Acquisition

`manifests/parliament_dataset_full_acquisition.json` records the bounded, resumable full-acquisition layer for Parliament-hosted dataset families approved by the inventory and seed tracks.

This track is repeatable, resumable, hash-backed, rights-safe. It stays `not-public-release-ready` and does not authorize bulk acquisition or public release.

## Scope

The acquisition layer covers the same Parliament-hosted dataset families as the inventory and seed tracks:

- Hansard / debates
- Daily progress
- Journals
- Papers presented, current papers, and AJHR
- Order Papers, oral questions, written questions, business statements, and sitting programme
- Select committees
- Petitions
- MPs, former MPs, parties, seating, and contact/office downloads
- Parliamentary rules and procedure
- Parliament video, audio, and calendar metadata

NZ legislation and Gazette remain out of scope. HathiTrust and Internet Archive are not acquisition dependencies.

## Cache Policy

Each target writes a bounded cache directory under `derived/parliament_dataset_full_acquisition/<family>/<source_id>/`.

The cache policy is conservative: reuse a cached `target.json` record when it is present, and only refetch when a caller disables resume.

The cache stores:

- the index response
- up to two detail proofs when discoverable
- a per-target `target.json` record

The target record captures URL provenance, content hashes, record counts, rights boundaries, refresh cadence, and resumability flags.

## Refresh Cadence

The manifest records a family-level refresh cadence so later tracks can schedule repeat acquisition without assuming completeness:

- Daily for Hansard, daily progress, current-business, members, petitions, and media metadata surfaces
- Weekly for journals, papers, and select-committee surfaces
- Weekly for parliamentary rules and procedure surfaces

## Operator Commands

```powershell
pixi run python scripts\fetch_parliament_dataset_full_acquisition.py --manifest manifests\parliament_dataset_full_acquisition.json --output-dir derived\parliament_dataset_full_acquisition
pixi run python scripts\check_parliament_dataset_full_acquisition.py
```

The checker validates:

- the manifest schema
- bounded request URLs
- hash-backed proofs
- the `not-public-release-ready` publication boundary
- official Parliament sources are preferred
- no bulk acquisition
- rights-safe exclusion of HathiTrust, Internet Archive, NZ legislation, and the Gazette

## Current Status

This is an implementation and validation layer, not a publication surface. It exists so later release tracks can promote approved outputs without reworking acquisition provenance.
