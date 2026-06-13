"""Generate an RDF / linked-data maintainer-review sample."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR_DEFAULT = ROOT / "samples/rdf-linked-data"
SOURCE_STABLE_ID = "HansS_20240625_067140000"
SAMPLE_ID = "rdf-linked-data-sample-20260610"

TTL_CONTENT = """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix nzh: <https://w3id.org/nz-hansard/> .
@prefix nzhc: <https://w3id.org/nz-hansard/component/> .
@prefix nzhs: <https://w3id.org/nz-hansard/sample/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix schema: <https://schema.org/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix time: <http://www.w3.org/2006/time#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

nzhs:rdf-linked-data-sample a dcat:Dataset, prov:Entity ;
  dcterms:title "RDF linked-data sample package" ;
  dcterms:description "Maintainer-review linked-data sample generated from the neutral component fixture set." ;
  dcterms:issued "2026-06-10"^^xsd:date ;
  dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
  dcterms:source <https://github.com/edithatogo/corpus-nz-hansard> ;
  dcat:distribution nzhs:distribution-ttl, nzhs:distribution-jsonld ;
  prov:wasDerivedFrom nzhc:nzhc-component-0000000000000001,
    nzhc:nzhc-component-0000000000000002,
    nzhc:nzhc-component-0000000000000003,
    nzhc:nzhc-component-0000000000000004,
    nzhc:nzhc-component-0000000000000005,
    nzhc:nzhc-component-0000000000000006,
    nzhc:nzhc-component-0000000000000007,
    nzhc:nzhc-component-0000000000000008,
    nzhc:nzhc-component-0000000000000009 .

nzhs:distribution-ttl a dcat:Distribution ;
  dcterms:title "RDF Turtle sample" ;
  dcterms:format "text/turtle" ;
  dcat:downloadURL <https://w3id.org/nz-hansard/sample/rdf-linked-data-sample/linked-data.ttl> .

nzhs:distribution-jsonld a dcat:Distribution ;
  dcterms:title "RDF JSON-LD sample" ;
  dcterms:format "application/ld+json" ;
  dcat:downloadURL <https://w3id.org/nz-hansard/sample/rdf-linked-data-sample/linked-data.jsonld> .

nzhs:party-scheme a skos:ConceptScheme ;
  dcterms:title "Party concept scheme" .

nzhs:role-scheme a skos:ConceptScheme ;
  dcterms:title "Role concept scheme" .

nzhs:proceeding-type-scheme a skos:ConceptScheme ;
  dcterms:title "Proceeding type concept scheme" .

nzhs:vote-type-scheme a skos:ConceptScheme ;
  dcterms:title "Vote type concept scheme" .

nzhs:topic-scheme a skos:ConceptScheme ;
  dcterms:title "Topic code concept scheme" .

nzhs:party-example-party a skos:Concept, nzh:Party ;
  skos:inScheme nzhs:party-scheme ;
  skos:prefLabel "Example Party"@en ;
  dcterms:identifier "nzhc-component-0000000000000004" ;
  prov:wasDerivedFrom nzhc:nzhc-component-0000000000000004 .

nzhs:role-member a skos:Concept ;
  skos:inScheme nzhs:role-scheme ;
  skos:prefLabel "Member"@en .

nzhs:proceeding-type-vote a skos:Concept ;
  skos:inScheme nzhs:proceeding-type-scheme ;
  skos:prefLabel "Vote"@en .

nzhs:vote-type-party-vote a skos:Concept ;
  skos:inScheme nzhs:vote-type-scheme ;
  skos:prefLabel "Party vote"@en .

nzhs:topic-transport a skos:Concept ;
  skos:inScheme nzhs:topic-scheme ;
  skos:prefLabel "Transport"@en ;
  skos:notation "transport" .

nzhc:nzhc-component-0000000000000001 a nzh:Session, prov:Entity ;
  dcterms:identifier "nzhc-component-0000000000000001" ;
  time:hasTime nzhs:sitting-time-2024-06-25 ;
  prov:wasDerivedFrom <https://w3id.org/nz-hansard/document/47HansS_20240625_067140000> .

nzhs:sitting-time-2024-06-25 a time:Instant ;
  time:inXSDDate "2024-06-25"^^xsd:date .

nzhc:nzhc-component-0000000000000002 a nzh:ProceedingItem, prov:Entity ;
  dcterms:identifier "nzhc-component-0000000000000002" ;
  dcterms:title "Land Transport (Clean Vehicle Standard) Amendment Bill - second reading" ;
  dcterms:isPartOf nzhc:nzhc-component-0000000000000001 ;
  dcterms:type nzhs:proceeding-type-vote ;
  prov:wasDerivedFrom <https://w3id.org/nz-hansard/document/47HansS_20240625_067140000> .

nzhc:nzhc-component-0000000000000003 a foaf:Person, prov:Entity ;
  dcterms:identifier "nzhc-component-0000000000000003" ;
  foaf:name "Example Member" ;
  nzh:role nzhs:role-member ;
  prov:wasDerivedFrom <https://w3id.org/nz-hansard/authority/nzhc-authority-source-d89cb3c98830032d> .

nzhc:nzhc-component-0000000000000004 a nzh:Party, skos:Concept, prov:Entity ;
  dcterms:identifier "nzhc-component-0000000000000004" ;
  skos:inScheme nzhs:party-scheme ;
  skos:prefLabel "Example Party"@en ;
  prov:wasDerivedFrom <https://w3id.org/nz-hansard/authority/nzhc-authority-source-d89cb3c98830032d> .

nzhc:nzhc-component-0000000000000005 a nzh:SpeechTurn, prov:Entity ;
  dcterms:identifier "nzhc-component-0000000000000005" ;
  dcterms:subject nzhs:topic-transport ;
  nzh:sourceStableId "HansS_20240625_067140000" ;
  nzh:proceedingItem nzhc:nzhc-component-0000000000000002 ;
  nzh:speaker nzhc:nzhc-component-0000000000000003 ;
  prov:wasDerivedFrom <https://w3id.org/nz-hansard/component/nzhc-component-0000000000000005> .

nzhc:nzhc-component-0000000000000006 a nzh:Motion, prov:Entity ;
  dcterms:identifier "nzhc-component-0000000000000006" ;
  dcterms:title "That the Land Transport (Clean Vehicle Standard) Amendment Bill be now read a second time." ;
  dcterms:isPartOf nzhc:nzhc-component-0000000000000002 ;
  prov:wasDerivedFrom <https://w3id.org/nz-hansard/component/nzhc-component-0000000000000006> .

nzhc:nzhc-component-0000000000000007 a nzh:VoteEvent, prov:Entity ;
  dcterms:identifier "nzhc-component-0000000000000007" ;
  nzh:motion nzhc:nzhc-component-0000000000000006 ;
  nzh:voteType nzhs:vote-type-party-vote ;
  prov:wasDerivedFrom <https://w3id.org/nz-hansard/component/nzhc-component-0000000000000007> .

nzhc:nzhc-component-0000000000000008 a nzh:Bill, prov:Entity ;
  dcterms:identifier "nzhc-component-0000000000000008" ;
  dcterms:title "Land Transport (Clean Vehicle Standard) Amendment Bill" ;
  dcterms:isPartOf nzhc:nzhc-component-0000000000000002 ;
  prov:wasDerivedFrom <https://w3id.org/nz-hansard/component/nzhc-component-0000000000000008> .

nzhc:nzhc-component-0000000000000009 a nzh:TopicAssignment, prov:Entity ;
  dcterms:identifier "nzhc-component-0000000000000009" ;
  dcterms:subject nzhs:topic-transport ;
  nzh:targetComponent nzhc:nzhc-component-0000000000000002 ;
  prov:wasDerivedFrom <https://w3id.org/nz-hansard/component/nzhc-component-0000000000000009> .
"""

JSONLD_CONTENT = {
    "@context": {
        "@vocab": "https://w3id.org/nz-hansard/",
        "nzh": "https://w3id.org/nz-hansard/",
        "nzhc": "https://w3id.org/nz-hansard/component/",
        "nzhs": "https://w3id.org/nz-hansard/sample/",
        "dcat": "http://www.w3.org/ns/dcat#",
        "dcterms": "http://purl.org/dc/terms/",
        "foaf": "http://xmlns.com/foaf/0.1/",
        "prov": "http://www.w3.org/ns/prov#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "schema": "https://schema.org/",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "time": "http://www.w3.org/2006/time#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "identifier": "dcterms:identifier",
        "title": "dcterms:title",
        "description": "dcterms:description",
        "issued": {"@id": "dcterms:issued", "@type": "xsd:date"},
        "license": {"@id": "dcterms:license", "@type": "@id"},
        "source": {"@id": "dcterms:source", "@type": "@id"},
        "format": "dcterms:format",
        "distribution": {"@id": "dcat:distribution", "@type": "@id"},
        "downloadURL": {"@id": "dcat:downloadURL", "@type": "@id"},
        "name": "foaf:name",
        "prefLabel": "skos:prefLabel",
        "notation": "skos:notation",
        "inScheme": {"@id": "skos:inScheme", "@type": "@id"},
        "wasDerivedFrom": {"@id": "prov:wasDerivedFrom", "@type": "@id"},
        "hasTime": {"@id": "time:hasTime", "@type": "@id"},
        "inXSDDate": {"@id": "time:inXSDDate", "@type": "xsd:date"},
        "isPartOf": {"@id": "dcterms:isPartOf", "@type": "@id"},
        "type": {"@id": "dcterms:type", "@type": "@id"},
        "subject": {"@id": "dcterms:subject", "@type": "@id"},
        "proceedingItem": {"@id": "nzh:proceedingItem", "@type": "@id"},
        "speaker": {"@id": "nzh:speaker", "@type": "@id"},
        "motion": {"@id": "nzh:motion", "@type": "@id"},
        "voteType": {"@id": "nzh:voteType", "@type": "@id"},
        "targetComponent": {"@id": "nzh:targetComponent", "@type": "@id"},
        "role": {"@id": "nzh:role", "@type": "@id"},
        "sourceStableId": "nzh:sourceStableId",
    },
    "@graph": [
        {
            "@id": "nzhs:rdf-linked-data-sample",
            "@type": ["dcat:Dataset", "prov:Entity"],
            "title": "RDF linked-data sample package",
            "description": "Maintainer-review linked-data sample generated from the neutral component fixture set.",
            "issued": "2026-06-10",
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "source": "https://github.com/edithatogo/corpus-nz-hansard",
            "distribution": ["nzhs:distribution-ttl", "nzhs:distribution-jsonld"],
            "wasDerivedFrom": [
                "nzhc:nzhc-component-0000000000000001",
                "nzhc:nzhc-component-0000000000000002",
                "nzhc:nzhc-component-0000000000000003",
                "nzhc:nzhc-component-0000000000000004",
                "nzhc:nzhc-component-0000000000000005",
                "nzhc:nzhc-component-0000000000000006",
                "nzhc:nzhc-component-0000000000000007",
                "nzhc:nzhc-component-0000000000000008",
                "nzhc:nzhc-component-0000000000000009",
            ],
        },
        {
            "@id": "nzhs:distribution-ttl",
            "@type": "dcat:Distribution",
            "title": "RDF Turtle sample",
            "format": "text/turtle",
            "downloadURL": "https://w3id.org/nz-hansard/sample/rdf-linked-data-sample/linked-data.ttl",
        },
        {
            "@id": "nzhs:distribution-jsonld",
            "@type": "dcat:Distribution",
            "title": "RDF JSON-LD sample",
            "format": "application/ld+json",
            "downloadURL": "https://w3id.org/nz-hansard/sample/rdf-linked-data-sample/linked-data.jsonld",
        },
        {
            "@id": "nzhs:party-scheme",
            "@type": "skos:ConceptScheme",
            "title": "Party concept scheme",
        },
        {"@id": "nzhs:role-scheme", "@type": "skos:ConceptScheme", "title": "Role concept scheme"},
        {
            "@id": "nzhs:proceeding-type-scheme",
            "@type": "skos:ConceptScheme",
            "title": "Proceeding type concept scheme",
        },
        {
            "@id": "nzhs:vote-type-scheme",
            "@type": "skos:ConceptScheme",
            "title": "Vote type concept scheme",
        },
        {
            "@id": "nzhs:topic-scheme",
            "@type": "skos:ConceptScheme",
            "title": "Topic code concept scheme",
        },
        {
            "@id": "nzhs:party-example-party",
            "@type": ["skos:Concept", "nzh:Party"],
            "identifier": "nzhc-component-0000000000000004",
            "prefLabel": {"@value": "Example Party", "@language": "en"},
            "inScheme": "nzhs:party-scheme",
            "wasDerivedFrom": "nzhc:nzhc-component-0000000000000004",
        },
        {
            "@id": "nzhs:role-member",
            "@type": "skos:Concept",
            "prefLabel": {"@value": "Member", "@language": "en"},
            "inScheme": "nzhs:role-scheme",
        },
        {
            "@id": "nzhs:proceeding-type-vote",
            "@type": "skos:Concept",
            "prefLabel": {"@value": "Vote", "@language": "en"},
            "inScheme": "nzhs:proceeding-type-scheme",
        },
        {
            "@id": "nzhs:vote-type-party-vote",
            "@type": "skos:Concept",
            "prefLabel": {"@value": "Party vote", "@language": "en"},
            "inScheme": "nzhs:vote-type-scheme",
        },
        {
            "@id": "nzhs:topic-transport",
            "@type": "skos:Concept",
            "prefLabel": {"@value": "Transport", "@language": "en"},
            "notation": "transport",
            "inScheme": "nzhs:topic-scheme",
        },
        {
            "@id": "nzhs:sitting-time-2024-06-25",
            "@type": "time:Instant",
            "inXSDDate": "2024-06-25",
        },
        {
            "@id": "nzhc:nzhc-component-0000000000000001",
            "@type": ["nzh:Session", "prov:Entity"],
            "identifier": "nzhc-component-0000000000000001",
            "hasTime": "nzhs:sitting-time-2024-06-25",
            "wasDerivedFrom": "https://w3id.org/nz-hansard/document/47HansS_20240625_067140000",
        },
        {
            "@id": "nzhc:nzhc-component-0000000000000002",
            "@type": ["nzh:ProceedingItem", "prov:Entity"],
            "identifier": "nzhc-component-0000000000000002",
            "title": "Land Transport (Clean Vehicle Standard) Amendment Bill - second reading",
            "isPartOf": "nzhc:nzhc-component-0000000000000001",
            "type": "nzhs:proceeding-type-vote",
            "wasDerivedFrom": "https://w3id.org/nz-hansard/document/47HansS_20240625_067140000",
        },
        {
            "@id": "nzhc:nzhc-component-0000000000000003",
            "@type": ["foaf:Person", "prov:Entity"],
            "identifier": "nzhc-component-0000000000000003",
            "name": "Example Member",
            "role": "nzhs:role-member",
            "wasDerivedFrom": "https://w3id.org/nz-hansard/authority/nzhc-authority-source-d89cb3c98830032d",
        },
        {
            "@id": "nzhc:nzhc-component-0000000000000004",
            "@type": ["nzh:Party", "skos:Concept", "prov:Entity"],
            "identifier": "nzhc-component-0000000000000004",
            "prefLabel": {"@value": "Example Party", "@language": "en"},
            "inScheme": "nzhs:party-scheme",
            "wasDerivedFrom": "https://w3id.org/nz-hansard/authority/nzhc-authority-source-d89cb3c98830032d",
        },
        {
            "@id": "nzhc:nzhc-component-0000000000000005",
            "@type": ["nzh:SpeechTurn", "prov:Entity"],
            "identifier": "nzhc-component-0000000000000005",
            "subject": "nzhs:topic-transport",
            "sourceStableId": SOURCE_STABLE_ID,
            "proceedingItem": "nzhc:nzhc-component-0000000000000002",
            "speaker": "nzhc:nzhc-component-0000000000000003",
            "wasDerivedFrom": "https://w3id.org/nz-hansard/component/nzhc-component-0000000000000005",
        },
        {
            "@id": "nzhc:nzhc-component-0000000000000006",
            "@type": ["nzh:Motion", "prov:Entity"],
            "identifier": "nzhc-component-0000000000000006",
            "title": "That the Land Transport (Clean Vehicle Standard) Amendment Bill be now read a second time.",
            "isPartOf": "nzhc:nzhc-component-0000000000000002",
            "wasDerivedFrom": "https://w3id.org/nz-hansard/component/nzhc-component-0000000000000006",
        },
        {
            "@id": "nzhc:nzhc-component-0000000000000007",
            "@type": ["nzh:VoteEvent", "prov:Entity"],
            "identifier": "nzhc-component-0000000000000007",
            "motion": "nzhc:nzhc-component-0000000000000006",
            "voteType": "nzhs:vote-type-party-vote",
            "wasDerivedFrom": "https://w3id.org/nz-hansard/component/nzhc-component-0000000000000007",
        },
        {
            "@id": "nzhc:nzhc-component-0000000000000008",
            "@type": ["nzh:Bill", "prov:Entity"],
            "identifier": "nzhc-component-0000000000000008",
            "title": "Land Transport (Clean Vehicle Standard) Amendment Bill",
            "isPartOf": "nzhc:nzhc-component-0000000000000002",
            "wasDerivedFrom": "https://w3id.org/nz-hansard/component/nzhc-component-0000000000000008",
        },
        {
            "@id": "nzhc:nzhc-component-0000000000000009",
            "@type": ["nzh:TopicAssignment", "prov:Entity"],
            "identifier": "nzhc-component-0000000000000009",
            "subject": "nzhs:topic-transport",
            "targetComponent": "nzhc:nzhc-component-0000000000000002",
            "wasDerivedFrom": "https://w3id.org/nz-hansard/component/nzhc-component-0000000000000009",
        },
    ],
}

SHACL_CONTENT = """@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix nzh: <https://w3id.org/nz-hansard/> .
@prefix nzhc: <https://w3id.org/nz-hansard/component/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

nzh:DatasetShape a sh:NodeShape ;
  sh:targetClass dcat:Dataset ;
  sh:property [
    sh:path dcterms:title ;
    sh:minCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path dcterms:issued ;
    sh:minCount 1 ;
    sh:datatype xsd:date ;
  ] ;
  sh:property [
    sh:path dcat:distribution ;
    sh:minCount 1 ;
  ] .

nzh:SpeechTurnShape a sh:NodeShape ;
  sh:targetClass nzh:SpeechTurn ;
  sh:property [
    sh:path dcterms:identifier ;
    sh:minCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path nzh:sourceStableId ;
    sh:minCount 1 ;
    sh:datatype xsd:string ;
  ] ;
  sh:property [
    sh:path nzh:proceedingItem ;
    sh:minCount 1 ;
  ] ;
  sh:property [
    sh:path nzh:speaker ;
    sh:minCount 1 ;
  ] ;
  sh:property [
    sh:path dcterms:subject ;
    sh:minCount 1 ;
  ] .

nzh:ProvenanceShape a sh:NodeShape ;
  sh:targetClass prov:Entity ;
  sh:property [
    sh:path prov:wasDerivedFrom ;
    sh:minCount 1 ;
  ] .
"""

README_TEXT = """# RDF Linked Data Sample Package

Maintainer-review sample generated from the neutral component fixture set.
This package is sample-not-release and records blocked-pending-validated-components.

References:

- `manifests/rdf_linked_data_validation_manifest.json`
- `manifests/rdf_linked_data_model_metadata.json`
- `docs/rdf-linked-data-mapping.md`
- `samples/rdf-linked-data/linked-data.ttl`
- `samples/rdf-linked-data/linked-data.jsonld`
- `samples/rdf-linked-data/shapes.ttl`
- `samples/rdf-linked-data/sparql-queries.rq`

The sample stays within `https://w3id.org/nz-hansard/`, uses PROV-O and DCAT, and records SKOS concept schemes for parties, roles, proceeding types, vote types, and topic codes. W3C Time records the sitting date, and `stanza` and `spacy` remain prototype comparison candidates rather than committed export dependencies.
"""

SPARQL_TEXT = """PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX nzh: <https://w3id.org/nz-hansard/>
PREFIX nzhc: <https://w3id.org/nz-hansard/component/>
PREFIX nzhs: <https://w3id.org/nz-hansard/sample/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?speechTurn ?topicLabel ?speakerName WHERE {
  ?speechTurn a nzh:SpeechTurn ;
    dcterms:subject ?topic ;
    nzh:speaker ?speaker .
  ?topic skos:prefLabel ?topicLabel .
  ?speaker <http://xmlns.com/foaf/0.1/name> ?speakerName .
}

SELECT ?dataset ?distribution WHERE {
  ?dataset a <http://www.w3.org/ns/dcat#Dataset> ;
    <http://www.w3.org/ns/dcat#distribution> ?distribution .
}
"""


def generate_sample(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ttl_path = output_dir / "linked-data.ttl"
    jsonld_path = output_dir / "linked-data.jsonld"
    shapes_path = output_dir / "shapes.ttl"
    sparql_path = output_dir / "sparql-queries.rq"
    readme_path = output_dir / "README.md"

    ttl_path.write_text(TTL_CONTENT, encoding="utf-8", newline="\n")
    jsonld_path.write_text(
        json.dumps(JSONLD_CONTENT, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    shapes_path.write_text(SHACL_CONTENT, encoding="utf-8", newline="\n")
    sparql_path.write_text(SPARQL_TEXT, encoding="utf-8", newline="\n")
    readme_path.write_text(README_TEXT, encoding="utf-8", newline="\n")

    return {
        "output_dir": output_dir.as_posix(),
        "turtle": ttl_path.as_posix(),
        "jsonld": jsonld_path.as_posix(),
        "shapes": shapes_path.as_posix(),
        "sparql": sparql_path.as_posix(),
        "readme": readme_path.as_posix(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an RDF linked-data sample package.")
    parser.add_argument("--output-dir", default="samples/rdf-linked-data")
    args = parser.parse_args()
    result = generate_sample(ROOT / args.output_dir)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
