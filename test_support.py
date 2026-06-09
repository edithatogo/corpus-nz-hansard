import os
import tempfile
import uuid
from pathlib import Path


def test_tmp_dir() -> Path:
    """Return a writable root for local test artifacts."""
    configured = os.environ.get("CORPUS_NZ_HANSARD_TEST_TMP")
    candidate = (Path(configured) if configured else Path(tempfile.gettempdir())) / "corpus-nz-hansard-tests"
    try:
        candidate.mkdir(parents=True, exist_ok=True)
        probe = candidate / f".probe-{uuid.uuid4().hex}"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError:
        if configured:
            raise
        candidate = Path(tempfile.gettempdir()) / f"corpus-nz-hansard-tests-{uuid.uuid4().hex}"
        candidate.mkdir(parents=True, exist_ok=True)
    return candidate
