"""Generate an Akoma Ntoso maintainer-review sample from neutral fixtures."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AKN_NS = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"
ET.register_namespace("", AKN_NS)


def _akn(tag: str) -> str:
    return f"{{{AKN_NS}}}{tag}"


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
    motion = _first(fixtures, "motions")
    vote = _first(fixtures, "votes")
    bill = _first(fixtures, "bills")

    root = ET.Element(_akn("akomaNtoso"))
    doc = ET.SubElement(root, _akn("doc"), {"name": "debate", "contains": "debate"})
    meta = ET.SubElement(doc, _akn("meta"))
    identification = ET.SubElement(meta, _akn("identification"))
    frbr_work = ET.SubElement(identification, _akn("FRBRWork"))
    ET.SubElement(frbr_work, _akn("FRBRthis"), {"value": "/akn/nz/hansard/sample/2026-06-10"})
    ET.SubElement(frbr_work, _akn("FRBRuri"), {"value": "/akn/nz/hansard/sample"})
    ET.SubElement(
        frbr_work, _akn("FRBRdate"), {"date": sitting["sitting_date"], "name": "generated"}
    )
    ET.SubElement(frbr_work, _akn("FRBRauthor"), {"href": "#neutral-fixture-generator"})
    ET.SubElement(frbr_work, _akn("FRBRcountry"), {"value": "nz"})

    frbr_expression = ET.SubElement(identification, _akn("FRBRExpression"))
    ET.SubElement(
        frbr_expression, _akn("FRBRthis"), {"value": "/akn/nz/hansard/sample/2026-06-10/eng"}
    )
    ET.SubElement(frbr_expression, _akn("FRBRlanguage"), {"language": "en"})

    frbr_manifestation = ET.SubElement(identification, _akn("FRBRManifestation"))
    ET.SubElement(
        frbr_manifestation, _akn("FRBRthis"), {"value": "/akn/nz/hansard/sample/2026-06-10/eng/xml"}
    )

    lifecycle = ET.SubElement(meta, _akn("lifecycle"))
    ET.SubElement(
        lifecycle,
        _akn("eventRef"),
        {
            "id": "event-sitting",
            "date": sitting["sitting_date"],
            "source": f"#{sitting['sitting_id']}",
            "href": f"#{proceeding['proceeding_item_id']}",
        },
    )

    references = ET.SubElement(meta, _akn("references"))
    tlc_org = ET.SubElement(references, _akn("TLCOrganization"))
    ET.SubElement(
        tlc_org, _akn("organization"), {"id": party["party_id"], "showAs": party["party_name"]}
    )
    ET.SubElement(
        references, _akn("TLCPerson"), {"id": member["member_id"], "showAs": member["display_name"]}
    )

    body = ET.SubElement(doc, _akn("body"))
    debate = ET.SubElement(
        body,
        _akn("debate"),
        {
            "eId": "debate-1",
            "source": proceeding["source_stable_id"],
            "refersTo": f"#{motion['motion_id']}",
        },
    )
    heading = ET.SubElement(debate, _akn("heading"))
    heading.text = proceeding["title"]

    speech = ET.SubElement(
        debate,
        _akn("speech"),
        {
            "eId": speech_turn["speech_turn_id"],
            "by": f"#{member['member_id']}",
            "as": "speaker",
            "refersTo": f"#{party['party_id']}",
        },
    )
    ET.SubElement(speech, _akn("from")).text = member["display_name"]
    ET.SubElement(speech, _akn("p")).text = speech_turn["speech_text"]
    ET.SubElement(
        speech, _akn("note"), {"type": "source"}
    ).text = f"Source order preserved from {proceeding['source_stable_id']}."

    vote_block = ET.SubElement(
        debate, _akn("vote"), {"eId": vote["vote_event_id"], "type": vote["vote_type"]}
    )
    ET.SubElement(vote_block, _akn("heading")).text = motion["motion_text"]
    outcome = ET.SubElement(vote_block, _akn("outcome"), {"result": vote["result"]})
    ET.SubElement(outcome, _akn("p")).text = (
        f"{bill['bill_title']} stage: {bill['stage']}. "
        f"Ayes {vote['ayes_count']}, noes {vote['noes_count']}."
    )
    ET.SubElement(
        vote_block, _akn("note"), {"type": "provenance"}
    ).text = f"Source provenance preserved from {vote['source_stable_id']} and {proceeding['source_stable_id']}."

    return ET.ElementTree(root)


def generate_sample(output_dir: Path) -> dict[str, Any]:
    fixtures_path = ROOT / "fixtures/neutral_components.json"
    fixtures = _load_json(fixtures_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    sample_path = output_dir / "Akoma-Ntoso.sample.xml"
    metadata_path = output_dir / "Akoma-Ntoso.metadata.xml"
    readme_path = output_dir / "README.md"

    tree = build_sample_tree(fixtures)
    tree.write(sample_path, encoding="utf-8", xml_declaration=True)

    metadata_root = ET.Element(_akn("akomaNtoso"))
    doc = ET.SubElement(metadata_root, _akn("doc"), {"name": "metadata"})
    meta = ET.SubElement(doc, _akn("meta"))
    ET.SubElement(meta, _akn("identification"))
    body = ET.SubElement(doc, _akn("body"))
    ET.SubElement(
        body, _akn("p")
    ).text = "Maintainer-review metadata for Akoma Ntoso sample packaging."
    ET.ElementTree(metadata_root).write(metadata_path, encoding="utf-8", xml_declaration=True)

    readme_path.write_text(
        "\n".join(
            [
                "# Akoma Ntoso Sample Package",
                "",
                "Maintainer-review sample generated from neutral fixtures.",
                "This package is sample-not-release and records blocked-pending-validated-components.",
                "See manifests/akoma_ntoso_validation_manifest.json and fixtures/neutral_components.json for the narrow sample contract.",
                "The generated XML lives at samples/akoma-ntoso/Akoma-Ntoso.sample.xml.",
                "",
                "- `Akoma-Ntoso.sample.xml`",
                "- `Akoma-Ntoso.metadata.xml`",
                "",
                "The package preserves source order and source provenance for a narrow NZ parliamentary sample.",
                "These notes are mapping notes only and are not schema validation evidence.",
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
    parser = argparse.ArgumentParser(description="Generate an Akoma Ntoso sample package.")
    parser.add_argument("--output-dir", default="samples/akoma-ntoso")
    args = parser.parse_args()
    result = generate_sample(ROOT / args.output_dir)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
