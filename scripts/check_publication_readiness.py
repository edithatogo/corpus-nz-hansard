"""Check credential and source inputs for public dataset publication."""

from __future__ import annotations

import argparse
import json
import os
from collections.abc import Mapping
from dataclasses import dataclass

PUBLICATION_TARGETS = ("github", "huggingface", "zenodo")


@dataclass(frozen=True)
class CheckResult:
    target: str
    name: str
    ready: bool
    detail: str


def _has_value(env: Mapping[str, str], name: str) -> bool:
    return bool(env.get(name, "").strip())


def _check_required(
    env: Mapping[str, str], target: str, name: str, description: str
) -> CheckResult:
    if _has_value(env, name):
        return CheckResult(target, name, True, f"{description} is configured.")
    return CheckResult(target, name, False, f"{description} is missing.")


def _check_creators_json(env: Mapping[str, str]) -> CheckResult:
    raw_value = env.get("ARCHIVE_CREATORS_JSON", "").strip()
    if not raw_value:
        return CheckResult(
            "zenodo", "ARCHIVE_CREATORS_JSON", False, "Zenodo creator metadata is missing."
        )
    try:
        creators = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        return CheckResult(
            "zenodo",
            "ARCHIVE_CREATORS_JSON",
            False,
            f"Zenodo creator metadata is not valid JSON: {exc.msg}.",
        )
    if not isinstance(creators, list) or not creators:
        return CheckResult(
            "zenodo",
            "ARCHIVE_CREATORS_JSON",
            False,
            "Zenodo creator metadata must be a non-empty JSON array.",
        )
    for index, creator in enumerate(creators, start=1):
        if not isinstance(creator, dict) or not str(creator.get("name", "")).strip():
            return CheckResult(
                "zenodo",
                "ARCHIVE_CREATORS_JSON",
                False,
                f"Zenodo creator {index} must be an object with a non-empty name.",
            )
    return CheckResult(
        "zenodo", "ARCHIVE_CREATORS_JSON", True, "Zenodo creator metadata is configured."
    )


def check_publication_readiness(
    *,
    env: Mapping[str, str] | None = None,
    targets: tuple[str, ...] = PUBLICATION_TARGETS,
) -> list[CheckResult]:
    """Return readiness checks for selected publication targets."""
    env = os.environ if env is None else env
    selected = set(targets)
    results: list[CheckResult] = []

    if "github" in selected:
        results.append(CheckResult("github", "release", True, "GitHub release is already public."))

    if "huggingface" in selected:
        results.append(_check_required(env, "huggingface", "HF_TOKEN", "Hugging Face token"))
        results.append(
            _check_required(env, "huggingface", "SOURCE_ARCHIVE_URL", "Source archive URL")
        )

    if "zenodo" in selected:
        results.append(_check_required(env, "zenodo", "ZENODO_TOKEN", "Zenodo token"))
        results.append(_check_required(env, "zenodo", "SOURCE_ARCHIVE_URL", "Source archive URL"))
        results.append(
            _check_required(env, "zenodo", "HF_TOKEN", "Source archive Hugging Face token")
        )
        results.append(_check_creators_json(env))

    return results


def format_results(results: list[CheckResult]) -> str:
    lines = ["Publication readiness"]
    for result in results:
        marker = "READY" if result.ready else "MISSING"
        lines.append(f"- [{marker}] {result.target}: {result.name} - {result.detail}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check public publication readiness inputs.")
    parser.add_argument(
        "--target",
        choices=PUBLICATION_TARGETS,
        action="append",
        help="Target to check. Repeat to check multiple targets. Defaults to all targets.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    targets = tuple(args.target) if args.target else PUBLICATION_TARGETS
    results = check_publication_readiness(targets=targets)
    print(format_results(results))
    return 0 if all(result.ready for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
