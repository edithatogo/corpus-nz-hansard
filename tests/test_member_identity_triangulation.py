from __future__ import annotations

from scripts.check_member_identity_triangulation import _failures


def test_member_identity_triangulation_evidence_is_consistent() -> None:
    assert _failures() == []
