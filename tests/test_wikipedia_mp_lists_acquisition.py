from __future__ import annotations

from scripts.check_wikipedia_mp_lists_acquisition import _failures


def test_wikipedia_mp_lists_acquisition_evidence_is_consistent() -> None:
    assert _failures() == []
