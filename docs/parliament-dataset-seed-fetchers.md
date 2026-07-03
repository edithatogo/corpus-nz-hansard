# Parliament Dataset Seed Fetchers

`manifests/parliament_dataset_seed_fetchers.json` records bounded proof runs for the highest-value Parliament dataset families selected from `parliament_dataset_inventory.json`.

This track is intentionally small and safe:

* it fetches only one index or list surface and one representative sample/detail surface per selected source;
* it stores only bounded derived artifacts under `derived/parliament_dataset_seed_fetchers/`;
* it records timestamps, content hashes, request URLs, access constraints, and proof status;
* it does not claim completeness, publication readiness, or bulk acquisition.

## Selected Families

The seed set covers the families required by the track:

* Journals
* Papers presented and AJHR/current papers
* Order Paper and questions
* Select committee reports, submissions/advice, and meetings
* Petitions
* Members, parties, and contact downloads

official Parliament sources are preferred. Fallback sources are sampled only when the inventory marks them credible.

## Output Layout

Seed artifacts are written beneath:

`derived/parliament_dataset_seed_fetchers/<dataset_family>/<source_id>/`

Each target writes bounded raw response artifacts plus the manifest entry describing the request URLs, hashes, sample counts, and proof status.

## Handoff To Full Acquisition

The full-acquisition track should reuse the same source IDs, request URLs, and access notes from the seed manifest.

The handoff requirements are:

1. keep request counts bounded in seed mode;
2. preserve hashes and timestamps;
3. promote only the approved sources with stable retrieval behavior;
4. keep blocked or deferred sources explicitly marked until the acquisition strategy changes.

No seed artifact in this track should be interpreted as a final corpus snapshot.

The checkpoint evidence here is bounded seed proofs only, not a full acquisition.
The next phase is the full acquisition handoff, which should preserve the no bulk acquisition rule.
