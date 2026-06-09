"""Generate Popolo/Open Civic Data sample artifacts from neutral fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _first(fixtures: dict[str, Any], family: str) -> dict[str, Any]:
    return fixtures["components"][family][0]


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def build_sample(fixtures: dict[str, Any]) -> dict[str, Any]:
    member = _first(fixtures, "members")
    party = _first(fixtures, "parties")
    motion = _first(fixtures, "motions")
    vote_event = _first(fixtures, "votes")
    speech_turn = _first(fixtures, "speech_turns")
    proceeding = _first(fixtures, "proceeding_items")

    person = {
        "id": member["member_id"],
        "name": member["display_name"],
        "other_names": [{"name": alias} for alias in member["aliases"]],
        "identifiers": [{"scheme": "nzhc-component", "identifier": member["member_id"]}],
        "sources": [{"id": source_id} for source_id in member["authority_source_ids"]],
        "provenance": member["provenance"],
        "validation_status": member["validation_status"],
    }
    organization = {
        "id": party["party_id"],
        "name": party["party_name"],
        "classification": "party",
        "other_names": [{"name": alias} for alias in party["party_aliases"]],
        "identifiers": [{"scheme": "nzhc-component", "identifier": party["party_id"]}],
        "sources": [{"id": source_id} for source_id in party["authority_source_ids"]],
        "provenance": party["provenance"],
        "validation_status": party["validation_status"],
    }
    membership = {
        "id": "nzhc-component-membership-0001",
        "person_id": member["member_id"],
        "organization_id": party["party_id"],
        "role": "member",
        "start_date": member["service_periods"][0]["start_date"],
        "end_date": member["service_periods"][0]["end_date"],
        "sources": [{"id": source_id} for source_id in member["authority_source_ids"]],
        "provenance": {"derived_from": "fixtures/neutral_components.json"},
        "validation_status": "candidate",
    }
    motion_object = {
        "id": motion["motion_id"],
        "text": motion["motion_text"],
        "classification": "procedural-question",
        "source_stable_id": motion["source_stable_id"],
        "proceeding_item_id": motion["proceeding_item_id"],
        "sources": [{"id": source_id} for source_id in motion["authority_source_ids"]],
        "provenance": motion["provenance"],
        "validation_status": motion["validation_status"],
    }
    vote_event_object = {
        "id": vote_event["vote_event_id"],
        "motion_id": vote_event["motion_id"],
        "classification": vote_event["vote_type"],
        "result": vote_event["result"],
        "counts": {
            "ayes": vote_event["ayes_count"],
            "noes": vote_event["noes_count"],
            "abstentions": vote_event["abstentions_count"],
        },
        "source_stable_id": vote_event["source_stable_id"],
        "sources": [{"id": source_id} for source_id in vote_event["authority_source_ids"]],
        "provenance": vote_event["provenance"],
        "validation_status": vote_event["validation_status"],
    }
    vote_rows = [
        {
            "id": f"{vote_event['vote_event_id']}-party-{party_vote['party_id']}",
            "vote_event_id": vote_event["vote_event_id"],
            "motion_id": vote_event["motion_id"],
            "voter_id": party_vote["party_id"],
            "voter_type": "organization",
            "option": party_vote["vote_position"],
            "count": party_vote["count"],
            "resolution_status": party_vote["resolution_status"],
            "provenance": vote_event["provenance"],
        }
        for party_vote in vote_event["party_votes"]
    ]
    speech_rows = [
        {
            "id": speech_turn["speech_turn_id"],
            "speaker_id": speech_turn["speaker_member_id"],
            "proceeding_item_id": speech_turn["proceeding_item_id"],
            "source_stable_id": speech_turn["source_stable_id"],
            "text": speech_turn["speech_text"],
            "references": [{"id": proceeding["proceeding_item_id"], "type": "proceeding_item"}],
            "provenance": speech_turn["provenance"],
            "validation_status": speech_turn["validation_status"],
        }
    ]

    return {
        "people": [person],
        "organizations": [organization],
        "memberships": [membership],
        "motions": [motion_object],
        "vote_events": [vote_event_object],
        "votes": vote_rows,
        "speeches": speech_rows,
    }


def generate_sample(output_dir: Path) -> dict[str, Any]:
    fixtures = _load_json(ROOT / "fixtures/neutral_components.json")
    sample = build_sample(fixtures)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_outputs = {
        "people": output_dir / "people.json",
        "organizations": output_dir / "organizations.json",
        "memberships": output_dir / "memberships.json",
        "motions": output_dir / "motions.json",
        "vote_events": output_dir / "vote-events.json",
    }
    for key, path in json_outputs.items():
        _write_json(path, sample[key])

    _write_jsonl(output_dir / "votes.jsonl", sample["votes"])
    _write_jsonl(output_dir / "speeches.jsonl", sample["speeches"])
    (output_dir / "README.md").write_text(
        "\n".join(
            [
                "# Popolo / Open Civic Data Sample Package",
                "",
                "Maintainer-review civic-data sample generated from `fixtures/neutral_components.json`.",
                "This package is sample-not-release and remains blocked-pending-validated-components.",
                "",
                "- `people.json`",
                "- `organizations.json`",
                "- `memberships.json`",
                "- `motions.json`",
                "- `vote-events.json`",
                "- `votes.jsonl`",
                "- `speeches.jsonl`",
                "",
                "Vote records distinguish `party_vote` organization rows from future individual member votes.",
                "No full voting record is inferred from text patterns alone.",
                "Validation manifest: `manifests/popolo_opencivicdata_validation_manifest.json`.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    return {
        "output_dir": output_dir.as_posix(),
        "outputs": [
            path.as_posix()
            for path in [
                *json_outputs.values(),
                output_dir / "votes.jsonl",
                output_dir / "speeches.jsonl",
            ]
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Popolo/Open Civic Data sample package."
    )
    parser.add_argument("--output-dir", default="samples/popolo-opencivicdata")
    args = parser.parse_args()
    print(json.dumps(generate_sample(ROOT / args.output_dir), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
