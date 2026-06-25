#!/usr/bin/env python3
"""Move batch1 tracks from Active to Archived in tracks.md"""
import re

md_path = "conductor/tracks.md"
with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

# The 10 tracks to archive from batch 1
track_ids = [
    "corpus_wide_member_identity_release_20260610",
    "corpus_wide_party_attribution_release_20260610",
    "validated_speech_turn_component_release_20260610",
    "sitting_proceeding_component_release_20260610",
    "vote_motion_bill_question_extraction_release_20260610",
    "parlamint_nz_public_endpoint_release_20260610",
    "popolo_opencivicdata_public_endpoint_release_20260610",
    "akoma_ntoso_public_endpoint_release_20260610",
    "cap_parlacap_public_endpoint_release_20260610",
    "ud_conllu_public_endpoint_release_20260610",
]

entries = {}
for tid in track_ids:
    pattern = re.compile(
        r"### \[x\] Track: .*?\n\n"
        rf"Track ID: `{re.escape(tid)}`\n\n"
        r"Goal: .*?\n\n"
        rf"Link: \[conductor/tracks/{re.escape(tid)}/\].*?\)",
        re.DOTALL,
    )
    m = pattern.search(content)
    if m:
        entries[tid] = m.group(0)

# Remove from current location (in reverse to preserve indices)
for tid in reversed(track_ids):
    if tid in entries:
        content = content.replace(entries[tid], "")

# Add to Archived Tracks section (after the last archived entry)
archived_marker = "## Archived Tracks"
lines = content.split("\n")
insert_pos = None
for i, line in enumerate(lines):
    if line.strip() == archived_marker:
        insert_pos = i + 1
        # Find the last archived entry
        for j in range(i + 1, len(lines)):
            if lines[j].startswith("## ") and lines[j] != archived_marker:
                insert_pos = j
                break
            insert_pos = j + 1
        break

if insert_pos is not None:
    # Build the entries to insert
    insert_text = ""
    for tid in track_ids:
        if tid in entries:
            insert_text += "\n" + entries[tid]
    lines.insert(insert_pos, insert_text)

content = "\n".join(lines)

# Clean up multiple blank lines
content = re.sub(r"\n{4,}", "\n\n\n", content)

with open(md_path, "w", encoding="utf-8") as f:
    f.write(content)

print("tracks.md updated: batch 1 tracks moved to Archived Tracks section")
print(f"Tracks processed: {len([t for t in track_ids if t in entries])}")