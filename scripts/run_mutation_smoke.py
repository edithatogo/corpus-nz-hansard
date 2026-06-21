"""Run a narrow mutation smoke test when the platform supports mutmut."""

from __future__ import annotations

import platform
import subprocess
import sys


def main() -> int:
    if platform.system() == "Windows":
        print("mutation-smoke skipped: mutmut requires WSL on Windows.")
        return 0
    return subprocess.call(
        [
            "mutmut",
            "run",
            "--paths-to-mutate",
            "scripts/select_committee_reports/cache.py",
            "--tests-dir",
            "tests",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
