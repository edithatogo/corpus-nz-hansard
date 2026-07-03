from __future__ import annotations

import unittest

from scripts.record_learning_candidate import append_candidate, build_entry_lines
from test_support import repo_tmp_dir


class RecordLearningCandidateTests(unittest.TestCase):
    def test_build_entry_lines_preserves_evidence(self) -> None:
        self.assertEqual(
            build_entry_lines("Learning candidate", ["workflow=Quality", "run_id=123"]),
            [
                "- [ ] Learning candidate",
                "  - workflow=Quality",
                "  - run_id=123",
            ],
        )

    def test_append_candidate_adds_to_active_candidates_without_duplicates(self) -> None:
        backlog = repo_tmp_dir() / "learning-candidate-backlog.md"
        backlog.write_text(
            "# Conductor Improvement Backlog\n\n"
            "## Active candidates\n"
            "- [ ] Existing item\n\n"
            "## Other section\n"
            "- Keep this section separate.\n",
            encoding="utf-8",
        )

        inserted, candidate_lines = append_candidate(
            backlog,
            "Learning candidate (review) for Upstream Submission",
            ["event_type=review", "run_id=123"],
        )
        duplicate_inserted, duplicate_lines = append_candidate(
            backlog,
            "Learning candidate (review) for Upstream Submission",
            ["event_type=review", "run_id=123"],
        )

        text = backlog.read_text(encoding="utf-8")
        self.assertTrue(inserted)
        self.assertFalse(duplicate_inserted)
        self.assertEqual(candidate_lines, duplicate_lines)
        self.assertEqual(text.count("Learning candidate (review)"), 1)
        self.assertIn("  - event_type=review", text)
        self.assertLess(text.index("Learning candidate (review)"), text.index("## Other section"))


if __name__ == "__main__":
    unittest.main()
