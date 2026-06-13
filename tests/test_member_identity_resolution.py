from __future__ import annotations

import unittest

import scripts.check_member_identity_resolution as member_check
from scripts.build_member_identity_review import resolve_member_field


class MemberIdentityResolutionTests(unittest.TestCase):
    def test_authority_manifest_is_consistent(self) -> None:
        authority = member_check._json(member_check.AUTHORITY_PATH)
        self.assertEqual(len(authority["authority_sources"]), 2)
        self.assertEqual(len(authority["member_records"]), 2)

    def test_resolver_handles_multiple_members(self) -> None:
        matches = resolve_member_field("CLAYTON COSGROVE; Hon Roger Sowry")
        self.assertEqual(len(matches), 2)
        self.assertEqual(
            [match["member_display_name"] for match in matches],
            ["Clayton Cosgrove", "Roger Morrison Sowry"],
        )

    def test_checker_passes(self) -> None:
        self.assertEqual(member_check._failures(), [])


if __name__ == "__main__":
    unittest.main()
