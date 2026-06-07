# Specification: Source Inventory Verification and Manifest Generation

## Scope

Analyze the raw ZIP archive containing the New Zealand Hansard transcripts and generate a comprehensive, inspectable manifest.

## Acceptance Criteria

- Source ZIP archive exists and hash matches.
- Extracted list of files is recorded with compressed and uncompressed sizes.
- A machine-readable `manifests/source_inventory.json` is generated.
- A human-readable verification report is compiled in markdown.
