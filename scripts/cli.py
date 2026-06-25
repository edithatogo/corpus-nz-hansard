"""Legacy shim for the package CLI."""

from __future__ import annotations

from collections.abc import Sequence

from nz_hansard_corpus.cli import main as package_main


def main(argv: Sequence[str] | None = None) -> int:
    """Run the package CLI from the legacy scripts namespace."""
    return package_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
