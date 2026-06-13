"""Generate interoperable metadata package files for the public release."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/metadata_packages_manifest.json"
RELEASE_MANIFEST_PATH = ROOT / "manifests/public_dataset_release_manifest.json"
ZENODO_PATH = ROOT / ".zenodo.json"
SCHEMA_PATH = ROOT / "schemas/hansard_record.schema.json"
OUTPUT_DIR = ROOT / "generated/metadata"


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")
    return _sha256(path)


def _write_text(path: Path, payload: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8", newline="\n")
    return _sha256(path)


def _record_fields(schema: dict[str, Any]) -> list[dict[str, str]]:
    fields: list[dict[str, str]] = []
    for name, definition in schema.get("properties", {}).items():
        field_type = definition.get("type", "string")
        if isinstance(field_type, list):
            field_type = next((item for item in field_type if item != "null"), "string")
        fields.append({"name": name, "dataType": str(field_type)})
    return fields


def _distribution(release: dict[str, Any]) -> list[dict[str, str]]:
    artifacts = release["artifacts"]
    publication = release["publication"]
    return [
        {
            "name": "Normalized Hansard Parquet",
            "encodingFormat": "application/vnd.apache.parquet",
            "contentUrl": f"{publication['github_release']}/{artifacts['parquet']}",
        },
        {
            "name": "Hansard DuckDB database",
            "encodingFormat": "application/vnd.duckdb",
            "contentUrl": f"{publication['github_release']}/{artifacts['duckdb']}",
        },
        {
            "name": "Hugging Face dataset viewer",
            "encodingFormat": "text/html",
            "contentUrl": publication["huggingface_dataset"],
        },
    ]


def _croissant(
    release: dict[str, Any], zenodo: dict[str, Any], schema: dict[str, Any]
) -> dict[str, Any]:
    publication = release["publication"]
    return {
        "@context": {
            "@language": "en",
            "@vocab": "https://schema.org/",
            "cr": "http://mlcommons.org/croissant/",
            "sc": "https://schema.org/",
        },
        "@type": "sc:Dataset",
        "name": zenodo["title"],
        "description": zenodo["description"],
        "url": publication["huggingface_dataset"],
        "identifier": publication["doi"],
        "license": zenodo["license"],
        "version": zenodo["version"],
        "datePublished": publication["publication_date"],
        "creator": zenodo["creators"],
        "keywords": zenodo["keywords"],
        "distribution": _distribution(release),
        "recordSet": [
            {
                "@type": "cr:RecordSet",
                "name": "hansard_records",
                "field": _record_fields(schema),
            }
        ],
    }


def _ro_crate(release: dict[str, Any], zenodo: dict[str, Any]) -> dict[str, Any]:
    publication = release["publication"]
    return {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": [
            {
                "@id": "ro-crate-metadata.json",
                "@type": "CreativeWork",
                "about": {"@id": "./"},
                "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
            },
            {
                "@id": "./",
                "@type": "Dataset",
                "name": zenodo["title"],
                "description": zenodo["description"],
                "datePublished": publication["publication_date"],
                "identifier": publication["doi"],
                "license": zenodo["license"],
                "version": zenodo["version"],
                "url": publication["zenodo_record"],
                "hasPart": [
                    {"@id": release["artifacts"]["parquet"]},
                    {"@id": release["artifacts"]["duckdb"]},
                    {"@id": release["artifacts"]["record_schema"]},
                ],
            },
            {
                "@id": release["artifacts"]["parquet"],
                "@type": "File",
                "encodingFormat": "application/vnd.apache.parquet",
            },
            {
                "@id": release["artifacts"]["duckdb"],
                "@type": "File",
                "encodingFormat": "application/vnd.duckdb",
            },
            {
                "@id": release["artifacts"]["record_schema"],
                "@type": "File",
                "encodingFormat": "application/schema+json",
            },
        ],
    }


def _frictionless(
    release: dict[str, Any], zenodo: dict[str, Any], schema: dict[str, Any]
) -> dict[str, Any]:
    fields = []
    for field in _record_fields(schema):
        fields.append(
            {
                "name": field["name"],
                "type": "integer" if field["dataType"] in {"integer", "number"} else "string",
            }
        )
    return {
        "profile": "data-package",
        "name": "corpus-nz-hansard",
        "title": zenodo["title"],
        "description": zenodo["description"],
        "homepage": release["publication"]["github_repository"],
        "version": zenodo["version"],
        "licenses": [{"name": zenodo["license"], "path": release["publication"]["zenodo_record"]}],
        "resources": [
            {
                "name": "hansard",
                "path": release["artifacts"]["parquet"],
                "format": "parquet",
                "mediatype": "application/vnd.apache.parquet",
                "schema": {"fields": fields},
            }
        ],
    }


def _ttl_literal(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _dcat(release: dict[str, Any], zenodo: dict[str, Any]) -> str:
    publication = release["publication"]
    return f"""@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://github.com/edithatogo/corpus-nz-hansard#dataset>
  a dcat:Dataset ;
  dcterms:title {_ttl_literal(zenodo["title"])} ;
  dcterms:description {_ttl_literal(zenodo["description"])} ;
  dcterms:identifier {_ttl_literal(publication["doi"])} ;
  dcterms:issued {_ttl_literal(publication["publication_date"])}^^xsd:date ;
  dcterms:license {_ttl_literal(zenodo["license"])} ;
  dcat:landingPage <{publication["huggingface_dataset"]}> ;
  dcat:distribution <https://github.com/edithatogo/corpus-nz-hansard#parquet> .

<https://github.com/edithatogo/corpus-nz-hansard#parquet>
  a dcat:Distribution ;
  dcterms:title "Normalized Hansard Parquet" ;
  dcat:mediaType "application/vnd.apache.parquet" ;
  dcat:downloadURL <{publication["github_release"]}/{release["artifacts"]["parquet"]}> .
"""


def _prov(release: dict[str, Any]) -> str:
    publication = release["publication"]
    source_sha = release["source"]["sha256"]
    return f"""@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<https://github.com/edithatogo/corpus-nz-hansard#release-v0.1.0>
  a prov:Entity ;
  dcterms:identifier "{publication["doi"]}" ;
  prov:wasGeneratedBy <https://github.com/edithatogo/corpus-nz-hansard#pipeline-run> ;
  prov:wasDerivedFrom <https://github.com/edithatogo/corpus-nz-hansard#source-archive> .

<https://github.com/edithatogo/corpus-nz-hansard#source-archive>
  a prov:Entity ;
  dcterms:title "{release["source"]["archive_name"]}" ;
  dcterms:identifier "sha256:{source_sha}" .

<https://github.com/edithatogo/corpus-nz-hansard#pipeline-run>
  a prov:Activity ;
  prov:used <https://github.com/edithatogo/corpus-nz-hansard#source-archive> ;
  prov:generated <https://github.com/edithatogo/corpus-nz-hansard#release-v0.1.0> .
"""


def _datacite(release: dict[str, Any], zenodo: dict[str, Any]) -> dict[str, Any]:
    publication = release["publication"]
    publication_date = publication["publication_date"]
    publication_year = int(publication_date.split("-", 1)[0])
    return {
        "schemaVersion": "http://datacite.org/schema/kernel-4",
        "identifier": {
            "identifier": publication["doi"],
            "identifierType": "DOI",
        },
        "creators": [
            {
                "name": creator["name"],
                "nameType": "Personal" if " " in creator["name"] else "Organizational",
            }
            for creator in zenodo.get("creators", [])
        ],
        "titles": [
            {
                "title": zenodo["title"],
            }
        ],
        "publisher": "Zenodo",
        "publicationYear": publication_year,
        "types": {
            "resourceTypeGeneral": "Dataset",
            "resourceType": zenodo["title"],
        },
        "version": zenodo["version"],
        "descriptions": [
            {
                "description": zenodo["description"],
                "descriptionType": "Abstract",
            }
        ],
        "contributors": [
            {
                "name": "NZ Hansard release automation",
                "contributorType": "DataCurator",
            }
        ],
        "dates": [
            {
                "date": publication_date,
                "dateType": "Issued",
            }
        ],
        "subjects": [{"subject": keyword} for keyword in zenodo.get("keywords", [])],
        "language": "en",
        "rightsList": [
            {
                "rights": zenodo["license"],
                "rightsUri": "https://github.com/edithatogo/corpus-nz-hansard/blob/main/NOTICE.md",
            }
        ],
        "relatedIdentifiers": [
            {
                "relatedIdentifier": publication["conceptdoi"],
                "relatedIdentifierType": "DOI",
                "relationType": "IsVersionOf",
            },
            {
                "relatedIdentifier": publication["github_repository"],
                "relatedIdentifierType": "URL",
                "relationType": "IsSupplementedBy",
            },
            {
                "relatedIdentifier": publication["github_release"],
                "relatedIdentifierType": "URL",
                "relationType": "IsSupplementedBy",
            },
            {
                "relatedIdentifier": publication["huggingface_dataset"],
                "relatedIdentifierType": "URL",
                "relationType": "IsIdenticalTo",
            },
        ],
        "fundingReferences": [],
    }


def main() -> int:
    manifest = _json(MANIFEST_PATH)
    release = _json(RELEASE_MANIFEST_PATH)
    zenodo = _json(ZENODO_PATH)
    schema = _json(SCHEMA_PATH)

    package_by_id = {package["id"]: package for package in manifest["packages"]}
    if "datacite" not in package_by_id:
        manifest["packages"].append(
            {
                "id": "datacite",
                "label": "DataCite",
                "standard": "DataCite Metadata Schema",
                "format": "json",
                "status": "planned",
                "output_path": "generated/metadata/datacite.json",
                "generator": "python scripts/build_metadata_packages.py",
                "source_manifests": [
                    "manifests/public_dataset_release_manifest.json",
                    ".zenodo.json",
                    "CITATION.cff",
                    "docs/datacite-export-contract.md",
                ],
                "validation_command": "python scripts/check_metadata_packages.py",
                "checksum_algorithm": "sha256",
                "checksum": None,
                "publication_surfaces": ["github", "zenodo"],
            }
        )
    if "docs/datacite-export-contract.md" not in manifest["source_manifests"]:
        manifest["source_manifests"].append("docs/datacite-export-contract.md")

    output_by_id = {
        "croissant": lambda path: _write_json(path, _croissant(release, zenodo, schema)),
        "ro-crate": lambda path: _write_json(path, _ro_crate(release, zenodo)),
        "frictionless": lambda path: _write_json(path, _frictionless(release, zenodo, schema)),
        "dcat": lambda path: _write_text(path, _dcat(release, zenodo)),
        "prov-o": lambda path: _write_text(path, _prov(release)),
        "datacite": lambda path: _write_json(path, _datacite(release, zenodo)),
    }

    for package in manifest["packages"]:
        package_id = package["id"]
        output_path = ROOT / package["output_path"]
        package["checksum"] = output_by_id[package_id](output_path)
        package["status"] = "generated"
        package["generator"] = "python scripts/build_metadata_packages.py"
        package["validation_command"] = "python scripts/check_metadata_packages.py"

    manifest["publication_claims_allowed"] = True
    manifest["publication_claims_note"] = (
        "Metadata packages are generated local release artifacts with SHA-256 checksums. "
        "Public-surface publication still follows the normal release upload and Zenodo "
        "sandbox-first policies."
    )
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Generated metadata packages in {OUTPUT_DIR.relative_to(ROOT).as_posix()}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
