"""Generate a Universal Dependencies / CoNLL-U maintainer-review sample."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SPEECH_COMPONENT_ID = "nzhc-component-0000000000000005"
PROCEEDING_COMPONENT_ID = "nzhc-component-0000000000000002"
SITTING_COMPONENT_ID = "nzhc-component-0000000000000001"
SOURCE_STABLE_ID = "HansS_20240625_067140000"
SOURCE_TEXT = "This bill is set down for committee stage immediately."
SAMPLE_ID = "ud-conllu-sample-20260610"

TOKENS: list[dict[str, Any]] = [
    {
        "id": 1,
        "form": "This",
        "lemma": "this",
        "upos": "DET",
        "xpos": "_",
        "feats": "PronType=Dem",
        "head": 2,
        "deprel": "det",
        "deps": "_",
        "misc": "StartChar=0|EndChar=4",
        "start_offset": 0,
        "end_offset": 4,
    },
    {
        "id": 2,
        "form": "bill",
        "lemma": "bill",
        "upos": "NOUN",
        "xpos": "_",
        "feats": "_",
        "head": 4,
        "deprel": "nsubj",
        "deps": "_",
        "misc": "StartChar=5|EndChar=9",
        "start_offset": 5,
        "end_offset": 9,
    },
    {
        "id": 3,
        "form": "is",
        "lemma": "be",
        "upos": "AUX",
        "xpos": "_",
        "feats": "Mood=Ind|Tense=Pres|VerbForm=Fin",
        "head": 4,
        "deprel": "cop",
        "deps": "_",
        "misc": "StartChar=10|EndChar=12",
        "start_offset": 10,
        "end_offset": 12,
    },
    {
        "id": 4,
        "form": "set",
        "lemma": "set",
        "upos": "VERB",
        "xpos": "_",
        "feats": "VerbForm=Part",
        "head": 0,
        "deprel": "root",
        "deps": "_",
        "misc": "StartChar=13|EndChar=16",
        "start_offset": 13,
        "end_offset": 16,
    },
    {
        "id": 5,
        "form": "down",
        "lemma": "down",
        "upos": "PART",
        "xpos": "_",
        "feats": "_",
        "head": 4,
        "deprel": "compound:prt",
        "deps": "_",
        "misc": "StartChar=17|EndChar=21",
        "start_offset": 17,
        "end_offset": 21,
    },
    {
        "id": 6,
        "form": "for",
        "lemma": "for",
        "upos": "ADP",
        "xpos": "_",
        "feats": "_",
        "head": 8,
        "deprel": "case",
        "deps": "_",
        "misc": "StartChar=22|EndChar=25",
        "start_offset": 22,
        "end_offset": 25,
    },
    {
        "id": 7,
        "form": "committee",
        "lemma": "committee",
        "upos": "NOUN",
        "xpos": "_",
        "feats": "_",
        "head": 8,
        "deprel": "compound",
        "deps": "_",
        "misc": "StartChar=26|EndChar=35",
        "start_offset": 26,
        "end_offset": 35,
    },
    {
        "id": 8,
        "form": "stage",
        "lemma": "stage",
        "upos": "NOUN",
        "xpos": "_",
        "feats": "_",
        "head": 4,
        "deprel": "obl",
        "deps": "_",
        "misc": "StartChar=36|EndChar=41",
        "start_offset": 36,
        "end_offset": 41,
    },
    {
        "id": 9,
        "form": "immediately",
        "lemma": "immediately",
        "upos": "ADV",
        "xpos": "_",
        "feats": "_",
        "head": 4,
        "deprel": "advmod",
        "deps": "_",
        "misc": "StartChar=42|EndChar=53",
        "start_offset": 42,
        "end_offset": 53,
    },
    {
        "id": 10,
        "form": ".",
        "lemma": ".",
        "upos": "PUNCT",
        "xpos": "_",
        "feats": "_",
        "head": 4,
        "deprel": "punct",
        "deps": "_",
        "misc": "StartChar=53|EndChar=54",
        "start_offset": 53,
        "end_offset": 54,
    },
]


def _conllu_line(token: dict[str, Any]) -> str:
    return "\t".join(
        [
            str(token["id"]),
            token["form"],
            token["lemma"],
            token["upos"],
            token["xpos"],
            token["feats"],
            str(token["head"]),
            token["deprel"],
            token["deps"],
            token["misc"],
        ]
    )


def build_conllu_text() -> str:
    return "\n".join(
        [
            f"# sent_id = {SAMPLE_ID}-1",
            f"# text = {SOURCE_TEXT}",
            f"# source_stable_id = {SOURCE_STABLE_ID}",
            f"# source_component_id = {SPEECH_COMPONENT_ID}",
            f"# source_proceeding_item_id = {PROCEEDING_COMPONENT_ID}",
            f"# source_sitting_id = {SITTING_COMPONENT_ID}",
            "# target_text_unit = speech_turn",
            "",
            *(_conllu_line(token) for token in TOKENS),
            "",
        ]
    )


def build_alignment_manifest() -> dict[str, Any]:
    return {
        "sample_id": SAMPLE_ID,
        "track_id": "ud_conllu_endpoint_20260609",
        "source_stable_id": SOURCE_STABLE_ID,
        "source_component_id": SPEECH_COMPONENT_ID,
        "source_proceeding_item_id": PROCEEDING_COMPONENT_ID,
        "source_sitting_id": SITTING_COMPONENT_ID,
        "target_text_unit": "speech_turn",
        "source_text": SOURCE_TEXT,
        "tokenizer": {
            "name": "manual-fixture-whitespace",
            "version": "ud-fixture-20260610",
            "policy": "Preserve source offsets and keep punctuation as a separate token.",
        },
        "tokens": [
            {
                "id": token["id"],
                "form": token["form"],
                "start_offset": token["start_offset"],
                "end_offset": token["end_offset"],
            }
            for token in TOKENS
        ],
        "validation": {
            "status": "sample-not-release",
            "readiness_status": "blocked-pending-validated-components",
            "offset_alignment": "preserved",
        },
    }


def build_model_metadata() -> dict[str, Any]:
    return {
        "track_id": "ud_conllu_endpoint_20260609",
        "annotation_family": "Universal Dependencies / CoNLL-U",
        "annotation_version": "2.x",
        "language": "en",
        "target_text_unit": "speech_turn",
        "source_component_ids": [
            SPEECH_COMPONENT_ID,
            PROCEEDING_COMPONENT_ID,
            SITTING_COMPONENT_ID,
        ],
        "tokenizer": {
            "name": "manual-fixture-whitespace",
            "version": "ud-fixture-20260610",
        },
        "parser": {
            "name": "manual-ud-tree",
            "version": "ud-fixture-20260610",
        },
        "prototype_tools": {
            "stanza": {
                "status": "planned",
                "comparison_note": "Candidate comparison target for a later fixture benchmark.",
            },
            "spacy": {
                "status": "planned",
                "comparison_note": "Candidate comparison target for a later fixture benchmark.",
            },
        },
        "default_pipeline": "manual-fixture",
        "selection_note": "Manual fixture output preserves source offsets and parseability while the Stanza/spaCy comparison is still pending.",
    }


def generate_sample(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    conllu_path = output_dir / "parliament_sample.conllu"
    alignments_path = output_dir / "parliament_sample.alignments.json"
    readme_path = output_dir / "README.md"
    metadata_path = ROOT / "manifests/ud_conllu_model_metadata.json"

    conllu_path.write_text(build_conllu_text(), encoding="utf-8", newline="\n")
    alignments_path.write_text(
        json.dumps(build_alignment_manifest(), indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    metadata_path.write_text(
        json.dumps(build_model_metadata(), indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    readme_path.write_text(
        "\n".join(
            [
                "# Universal Dependencies / CoNLL-U Sample Package",
                "",
                "Maintainer-review sample generated from a validated speech turn.",
                "This package is sample-not-release and records blocked-pending-validated-components.",
                "See manifests/ud_conllu_validation_manifest.json and manifests/ud_conllu_model_metadata.json for the sample contract.",
                "",
                "- `parliament_sample.conllu`",
                "- `parliament_sample.alignments.json`",
                "",
                "The sample preserves source offsets from the speech-turn fixture and keeps punctuation as a separate token.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "output_dir": output_dir.as_posix(),
        "conllu": conllu_path.as_posix(),
        "alignments": alignments_path.as_posix(),
        "readme": readme_path.as_posix(),
        "model_metadata": metadata_path.as_posix(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a UD/CoNLL-U sample package.")
    parser.add_argument("--output-dir", default="samples/ud-conllu")
    args = parser.parse_args()
    result = generate_sample(ROOT / args.output_dir)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
