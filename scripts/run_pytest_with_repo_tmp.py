"""Run pytest with repository-local temporary directories."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_tmp = Path(".test-tmp")
    repo_tmp.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["TMP"] = str(repo_tmp)
    env["TEMP"] = str(repo_tmp)
    return subprocess.call([sys.executable, "-m", "pytest", *sys.argv[1:]], env=env)


if __name__ == "__main__":
    raise SystemExit(main())
