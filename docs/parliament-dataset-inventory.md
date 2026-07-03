# Parliament Dataset Inventory

`manifests/parliament_dataset_inventory.json` is the source-of-truth inventory for Parliament-hosted datasets that can extend `corpus-nz-hansard` beyond the current DocumentsDB Hansard extract.

NZ legislation and Gazette remain out of scope. They are handled through the adjacent legislation/government-publication repositories and must not be added to this repo as acquisition targets.

## Scope

The inventory covers these dataset families:

| Family | Primary posture |
|---|---|
| Hansard/debates | Official Parliament first; historical fallbacks only after gap evidence |
| Order Paper, oral questions, written questions, business statements, sitting programme | Official Parliament current-business surfaces |
| Daily Progress | Official Parliament outcome/progress surface |
| Journals | Official weekly/session/index/historic journal surfaces before fallbacks |
| Papers presented, current papers, AJHR | Official Parliament papers surfaces before historical fallbacks |
| Select committees | Official reports, submissions/advice, meetings, submitters, and video metadata |
| Petitions | Official Parliament petitions pages |
| MPs, former MPs, parties, seating, contact/office downloads | Official Parliament identity and office surfaces |
| Parliamentary rules and procedure | Official rules, Standing Orders, Speakers' Rulings, and procedure material |
| Parliament video/audio/calendar metadata | Official media and calendar metadata surfaces |

This is an inventory, not an acquisition manifest. It does not claim historical completeness and it does not authorize bulk downloads.

## Source Posture

Official Parliament sources are always ranked before fallback or supporting sources in each family. Fallbacks are recorded only so later tracks can prove whether they help fill documented gaps.

Supported source postures:

| Posture | Meaning |
|---|---|
| `official` | New Zealand Parliament source and first acquisition candidate |
| `fallback` | Credible non-Parliament source for documented gaps |
| `supporting` | Context source that can inform interpretation but is not a primary acquisition source |
| `evidence_only` | Evidence of demand, request history, or access state |
| `excluded` | Explicitly out of scope for this track |

HathiTrust and Internet Archive are excluded acquisition dependencies for this inventory. They may be mentioned only as excluded or non-primary baselines, not as dependencies for the Parliament website expansion path.

Data.govt.nz requests are evidence only. A data.govt.nz record can show demand or past official discussion, but it is not a content source and must not be treated as a fetcher target.

## Credible Alternatives

When official Parliament coverage is incomplete, the inventory records these non-HathiTrust and non-Internet-Archive alternatives:

| Alternative | Use |
|---|---|
| Papers Past / National Library | Historical discovery and OCR cross-checks for debates, journals, and AJHR |
| Google Books | Item discovery and possible historical volume triangulation |
| University and library catalogues or physical holdings | Holding evidence and digitisation candidates |
| O Nehera / Waikato | British Parliamentary Papers context for colonial-era relationships |
| Data.govt.nz requests | Evidence only, never acquisition |

Each fallback source declares the official `fallback_for` source IDs it can support.

## Reconciliation

The inventory reconciles with existing repo artifacts:

| Artifact | Relationship |
|---|---|
| `manifests/authority_sources.json` | Keeps member, party, sitting, bill, vote, motion, and procedure authority-source IDs stable |
| `manifests/historical_sitting_inventory.json` | Keeps historical sitting boundaries separate from broad Parliament dataset discovery |
| `docs/cross-repo-dataset-architecture.md` | Keeps legislation/Gazette boundaries outside this repo |

The inventory deliberately broadens Parliament dataset discovery without changing the existing authority-source contract.

## Handoff

The next track is `parliament_dataset_seed_fetchers_20260703`.

Seed fetchers should produce one bounded proof per high-value family: one index proof, one sample/detail proof, and a downloadable-file or metadata proof where available. Proof artifacts should include URL, retrieval timestamp, content hash, source posture, access constraints, and item counts where they are cheap to obtain.

No seed fetcher should bulk enumerate archives, claim coverage completeness, or publish newly inventoried content.
