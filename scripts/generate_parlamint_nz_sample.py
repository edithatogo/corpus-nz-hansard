"""Generate a ParlaMint-NZ maintainer-review sample from neutral fixtures."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("", TEI_NS)


def _tei(tag: str) -> str:
    return f"{{{TEI_NS}}}{tag}"


def _xml_attr(name: str) -> str:
    return f"{{{XML_NS}}}{name}"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _first(fixtures: dict[str, Any], family: str) -> dict[str, Any]:
    return fixtures["components"][family][0]


def build_sample_tree(fixtures: dict[str, Any]) -> ET.ElementTree:
    sitting = _first(fixtures, "sittings")
    proceeding = _first(fixtures, "proceeding_items")
    speech_turn = _first(fixtures, "speech_turns")
    member = _first(fixtures, "members")
    party = _first(fixtures, "parties")
    bill = _first(fixtures, "bills")
    vote = _first(fixtures, "votes")

    root = ET.Element(_tei("TEI"), {_xml_attr("id"): "ParlaMint-NZ.sample"})
    header = ET.SubElement(root, _tei("teiHeader"))
    file_desc = ET.SubElement(header, _tei("fileDesc"))
    title_stmt = ET.SubElement(file_desc, _tei("titleStmt"))
    ET.SubElement(title_stmt, _tei("title")).text = "ParlaMint-NZ sample from neutral fixtures"
    publication_stmt = ET.SubElement(file_desc, _tei("publicationStmt"))
    ET.SubElement(
        publication_stmt, _tei("p")
    ).text = "Maintainer-review sample; not a public endpoint release."
    source_desc = ET.SubElement(file_desc, _tei("sourceDesc"))
    source_p = ET.SubElement(source_desc, _tei("p"))
    source_p.text = f"Derived from neutral fixture source {proceeding['source_stable_id']}."

    profile_desc = ET.SubElement(header, _tei("profileDesc"))
    partic_desc = ET.SubElement(profile_desc, _tei("particDesc"))
    list_person = ET.SubElement(partic_desc, _tei("listPerson"))
    person = ET.SubElement(
        list_person,
        _tei("person"),
        {_xml_attr("id"): member["member_id"]},
    )
    ET.SubElement(person, _tei("persName")).text = member["display_name"]
    affiliation = ET.SubElement(person, _tei("affiliation"), {"ref": f"#{party['party_id']}"})
    affiliation.text = "Candidate fixture affiliation for reference-resolution testing."
    list_org = ET.SubElement(partic_desc, _tei("listOrg"))
    org = ET.SubElement(list_org, _tei("org"), {_xml_attr("id"): party["party_id"]})
    ET.SubElement(org, _tei("orgName")).text = party["party_name"]

    encoding_desc = ET.SubElement(header, _tei("encodingDesc"))
    project_desc = ET.SubElement(encoding_desc, _tei("projectDesc"))
    ET.SubElement(project_desc, _tei("p")).text = (
        "NZ-specific procedure, vote, and stage mappings are recorded in "
        "docs/parlamint-nz-mapping.md."
    )

    text = ET.SubElement(root, _tei("text"))
    body = ET.SubElement(text, _tei("body"))
    div = ET.SubElement(
        body,
        _tei("div"),
        {
            "type": "sitting",
            "corresp": f"#{sitting['sitting_id']}",
            "ana": "sample-not-release",
        },
    )
    head = ET.SubElement(div, _tei("head"))
    head.text = proceeding["title"]
    u = ET.SubElement(
        div,
        _tei("u"),
        {
            _xml_attr("id"): speech_turn["speech_turn_id"],
            "who": f"#{member['member_id']}",
            "corresp": f"#{proceeding['proceeding_item_id']}",
        },
    )
    u.text = speech_turn["speech_text"]
    note = ET.SubElement(div, _tei("note"), {"type": "vote"})
    note.text = f"{vote['vote_type']} on {bill['bill_title']}: {vote['result']}"

    stand_off = ET.SubElement(root, _tei("standOff"))
    list_event = ET.SubElement(stand_off, _tei("listEvent"))
    event = ET.SubElement(
        list_event,
        _tei("event"),
        {
            _xml_attr("id"): vote["vote_event_id"],
            "corresp": f"#{vote['motion_id']}",
            "type": vote["vote_type"],
        },
    )
    ET.SubElement(event, _tei("label")).text = vote["result"]

    return ET.ElementTree(root)


def generate_sample(output_dir: Path) -> dict[str, Any]:
    fixtures_path = ROOT / "fixtures/neutral_components.json"
    fixtures = _load_json(fixtures_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    sample_path = output_dir / "ParlaMint-NZ.sample.xml"
    metadata_path = output_dir / "ParlaMint-NZ.metadata.xml"
    readme_path = output_dir / "README.md"

    tree = build_sample_tree(fixtures)
    tree.write(sample_path, encoding="utf-8", xml_declaration=True)

    metadata_root = ET.Element(_tei("teiCorpus"), {_xml_attr("id"): "ParlaMint-NZ.metadata"})
    header = ET.SubElement(metadata_root, _tei("teiHeader"))
    file_desc = ET.SubElement(header, _tei("fileDesc"))
    title_stmt = ET.SubElement(file_desc, _tei("titleStmt"))
    ET.SubElement(title_stmt, _tei("title")).text = "ParlaMint-NZ sample metadata"
    publication_stmt = ET.SubElement(file_desc, _tei("publicationStmt"))
    ET.SubElement(publication_stmt, _tei("p")).text = "Metadata sample for maintainer review only."
    source_desc = ET.SubElement(file_desc, _tei("sourceDesc"))
    ET.SubElement(source_desc, _tei("p")).text = "Generated from fixtures/neutral_components.json."
    ET.ElementTree(metadata_root).write(metadata_path, encoding="utf-8", xml_declaration=True)

    readme_path.write_text(
        "\n".join(
            [
                "# ParlaMint-NZ Sample Package",
                "",
                "Maintainer-review sample generated from neutral fixtures.",
                "This package is sample-not-release and is not ParlaMint-NZ readiness evidence.",
                "",
                "- `ParlaMint-NZ.sample.xml`",
                "- `ParlaMint-NZ.metadata.xml`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    return {
        "output_dir": output_dir.as_posix(),
        "sample_xml": sample_path.as_posix(),
        "metadata_xml": metadata_path.as_posix(),
        "readme": readme_path.as_posix(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a ParlaMint-NZ sample package.")
    parser.add_argument("--output-dir", default="samples/parlamint-nz")
    args = parser.parse_args()
    result = generate_sample(ROOT / args.output_dir)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
