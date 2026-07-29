"""Report external-link availability without acting as a release gate."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

URL_RE = re.compile(r"https?://[^)\]>\s]+")
NON_FATAL_HTTP = {401, 403, 405, 406, 429, 500, 502, 503, 504}
CURL = shutil.which("curl")


def check(url: str) -> tuple[str, str]:
    if CURL is None:
        return url, "network-error:curl-unavailable"
    command = [
        CURL,
        "--head",
        "--location",
        "--max-time",
        "15",
        "--silent",
        "--show-error",
        "--output",
        "/dev/null",
        "--write-out",
        "%{http_code}",
        "--user-agent",
        "rsi-model-link-audit/1.0",
        url,
    ]
    result = subprocess.run(  # noqa: S603 -- fixed curl flags; URL is one non-shell argument.
        command,
        capture_output=True,
        check=False,
        text=True,
    )
    try:
        status = int(result.stdout[-3:])
    except ValueError:
        status = 0
    if 200 <= status < 400:
        return url, f"ok:{status}"
    if status in NON_FATAL_HTTP:
        return url, f"reachable-restricted:{status}"
    if status:
        return url, f"http-error:{status}"
    return url, f"network-error:curl-{result.returncode}"


def main(argv: Sequence[str] | None = None) -> int:
    """Report external-link availability for one explicit manuscript."""
    parser = argparse.ArgumentParser(prog="rsi-check-external-links")
    parser.add_argument(
        "--manuscript",
        type=Path,
        default=Path.cwd() / "docs" / "Recursive_Industrial_Intelligence_r4.0.md",
    )
    args = parser.parse_args(argv)
    manuscript = args.manuscript.resolve()
    if not manuscript.is_file():
        print(f"manuscript not found: {manuscript}", file=sys.stderr)
        return 2
    urls = sorted(set(URL_RE.findall(manuscript.read_text(encoding="utf-8"))))
    with ThreadPoolExecutor(max_workers=10) as executor:
        pending = {executor.submit(check, url): url for url in urls}
        results = [future.result() for future in as_completed(pending)]
    failures = sorted(
        (url, status)
        for url, status in results
        if status.startswith(("http-error", "network-error"))
    )
    restricted = sum(status.startswith("reachable-restricted") for _, status in results)
    for url, status in failures:
        print(f"WARN {status} {url}")
    print(
        f"External links: {len(urls)} checked, "
        f"{len(failures)} unavailable, {restricted} restricted/transient"
    )
    if failures:
        print(
            "External availability is reported separately and is not the "
            "publication-integrity gate."
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
