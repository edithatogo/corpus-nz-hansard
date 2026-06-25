from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(script: str) -> None:
    subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)


def test_ontolex_lemon_terminology_layer_builds_and_validates() -> None:
    run_script("scripts/build_ontolex_lemon_terminology_layer.py")
    run_script("scripts/check_ontolex_lemon_terminology_layer.py")

    sample = json.loads(
        (ROOT / "samples" / "ontolex-lemon-terminology-layer" / "terminology.json").read_text(
            encoding="utf-8"
        ),
    )
    assert sample["public_claims"]["sample_terminology_layer"] is True
    assert sample["public_claims"]["full_corpus_vocabulary"] is False
    assert sample["public_claims"]["authoritative_legal_definitions"] is False
