"""Build a sample OntoLex-Lemon terminology layer."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "samples" / "ontolex-lemon-terminology-layer"
MANIFEST_PATH = ROOT / "manifests" / "ontolex_lemon_terminology_layer.json"

RELEASE_STATUS = "release-ready-sample-ontolex-lemon-layer"

TERMS = [
    {
        "id": "sitting",
        "pref_label": "sitting",
        "definition": "A parliamentary meeting date represented as a sample terminology concept.",
        "variants": ["sitting day"],
        "source": "corpus-neutral-component-model",
        "review_status": "agent-reviewed-sample",
    },
    {
        "id": "proceeding",
        "pref_label": "proceeding",
        "definition": "A structured item of parliamentary business represented in sample endpoint layers.",
        "variants": ["business item"],
        "source": "corpus-neutral-component-model",
        "review_status": "agent-reviewed-sample",
    },
    {
        "id": "speech-turn",
        "pref_label": "speech turn",
        "definition": "A contribution attributed to a speaker in the validated sample speech-turn component.",
        "variants": ["turn", "contribution"],
        "source": "validated-speech-turn-component",
        "review_status": "agent-reviewed-sample",
    },
    {
        "id": "bill",
        "pref_label": "bill",
        "definition": "A legislative proposal referenced by the corpus interoperability samples.",
        "variants": ["legislative bill"],
        "source": "bills-api-integration",
        "review_status": "agent-reviewed-sample",
    },
    {
        "id": "motion",
        "pref_label": "motion",
        "definition": "A parliamentary motion represented in the sample extraction vocabulary.",
        "variants": ["house motion"],
        "source": "vote-motion-bill-question-extraction",
        "review_status": "agent-reviewed-sample",
    },
    {
        "id": "party-vote",
        "pref_label": "party vote",
        "definition": "A vote attribution concept used in sample party-attribution evidence.",
        "variants": ["party division"],
        "source": "corpus-wide-party-attribution",
        "review_status": "agent-reviewed-sample",
    },
]


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def term_uri(term_id: str) -> str:
    return f"https://w3id.org/nz-hansard/term/{term_id}"


def turtle_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def build_turtle() -> str:
    lines = [
        "@prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> .",
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "@prefix prov: <http://www.w3.org/ns/prov#> .",
        "@prefix nzh: <https://w3id.org/nz-hansard/> .",
        "",
        "nzh:terminology-scheme a skos:ConceptScheme ;",
        '    skos:prefLabel "NZ Hansard sample terminology scheme"@en ;',
        '    dcterms:description "Sample-only OntoLex-Lemon terminology layer; not an authoritative legal vocabulary."@en .',
        "",
    ]
    for term in TERMS:
        uri = f"nzh:term/{term['id']}"
        lex = f"nzh:lexical-entry/{term['id']}"
        sense = f"nzh:lexical-sense/{term['id']}"
        lines.extend(
            [
                f"{uri} a skos:Concept ;",
                "    skos:inScheme nzh:terminology-scheme ;",
                f'    skos:prefLabel "{turtle_escape(term["pref_label"])}"@en ;',
                f'    skos:definition "{turtle_escape(term["definition"])}"@en ;',
                f'    prov:wasDerivedFrom "{turtle_escape(term["source"])}" ;',
                f'    dcterms:conformsTo "{term["review_status"]}" .',
                "",
                f"{lex} a ontolex:LexicalEntry ;",
                f'    ontolex:canonicalForm [ ontolex:writtenRep "{turtle_escape(term["pref_label"])}"@en ] ;',
                f"    ontolex:sense {sense} .",
                "",
                f"{sense} a ontolex:LexicalSense ;",
                f"    ontolex:isLexicalizedSenseOf {uri} .",
                "",
            ],
        )
        for index, variant in enumerate(term["variants"], start=1):
            lines.extend(
                [
                    f"nzh:lexical-entry/{term['id']}-variant-{index} a ontolex:LexicalEntry ;",
                    f'    ontolex:canonicalForm [ ontolex:writtenRep "{turtle_escape(variant)}"@en ] ;',
                    f"    ontolex:sense {sense} .",
                    "",
                ],
            )
    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    payload = {
        "release_status": RELEASE_STATUS,
        "generated_at": now,
        "scheme_uri": "https://w3id.org/nz-hansard/terminology-scheme",
        "terms": [
            {
                **term,
                "concept_uri": term_uri(term["id"]),
                "lexical_entry_uri": f"https://w3id.org/nz-hansard/lexical-entry/{term['id']}",
            }
            for term in TERMS
        ],
        "public_claims": {
            "sample_terminology_layer": True,
            "full_corpus_vocabulary": False,
            "authoritative_legal_definitions": False,
            "official_parliamentary_glossary": False,
            "external_ontology_acceptance": False,
            "stable_uri_review_complete": False,
        },
    }
    write_json(OUT_DIR / "terminology.json", payload)
    (OUT_DIR / "terminology.ttl").write_text(build_turtle(), encoding="utf-8")
    (OUT_DIR / "README.md").write_text(
        f"""# OntoLex-Lemon Terminology Layer

Release status: {RELEASE_STATUS}.

This is a sample-only optional terminology layer for parliamentary corpus vocabulary. It does not claim a full corpus vocabulary, authoritative legal definitions, an official parliamentary glossary, external ontology acceptance, or completed stable URI review.
""",
        encoding="utf-8",
    )
    write_json(
        MANIFEST_PATH,
        {
            "track": "ontolex_lemon_terminology_layer_20260610",
            "title": "OntoLex-Lemon Terminology Layer",
            "release_status": RELEASE_STATUS,
            "generated_at": now,
            "term_count": len(TERMS),
            "artifacts": [
                "samples/ontolex-lemon-terminology-layer/terminology.json",
                "samples/ontolex-lemon-terminology-layer/terminology.ttl",
                "samples/ontolex-lemon-terminology-layer/README.md",
                "docs/ontolex-lemon-terminology-layer.md",
            ],
            "public_claims": payload["public_claims"],
        },
    )


if __name__ == "__main__":
    main()
