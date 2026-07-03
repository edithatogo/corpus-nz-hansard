from __future__ import annotations

import unittest

from scripts.check_conductor_learning_log import _failures, _parse_entries


class CheckConductorLearningLogTests(unittest.TestCase):
    def test_parse_entries_extracts_structured_learning_entry(self) -> None:
        text = """# Conductor Learning Log

## 2026-06-23 - Track 18 rollout
- `entry_id`: `track-18-root-legal-nz`
- `observed_on`: 2026-06-23
- `repo`: `legal-nz`
- `scope`: `track`
- `trigger`: `example`
- `severity`: `low`
- `status`: `resolved`
- `lessons_learned`:
  - Lesson one.
- `next_check_to_add`:
  - Check one.
"""
        entries = _parse_entries(text)

        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["entry_id"], "track-18-root-legal-nz")
        self.assertEqual(entries[0]["lessons_learned"], ["Lesson one."])

    def test_repository_learning_log_is_schema_valid(self) -> None:
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
