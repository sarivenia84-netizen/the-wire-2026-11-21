#!/usr/bin/env python3
"""Render index.html to a PNG using headless Chrome for Testing."""

import subprocess
import sys
from pathlib import Path

DEFAULT_CHROME = Path.home() / ".cache" / "ms-playwright" / "chromium-1208" / "chrome-linux64" / "chrome"
DEFAULT_OUTPUT = "news-20261121.png"

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"

FLAGS = [
    "--headless",
    "--no-sandbox",
    "--disable-gpu",
    "--hide-scrollbars",
    "--screenshot={output}",
    "--window-size=1600,2000",
    "--force-device-scale-factor=2",
]


def main(argv):
    chrome = Path(argv[1]) if len(argv) > 1 else DEFAULT_CHROME
    output = argv[2] if len(argv) > 2 else DEFAULT_OUTPUT

    if not INDEX.exists():
        print(f"error: {INDEX} not found", file=sys.stderr)
        return 1
    if not chrome.exists():
        print(f"error: chrome not found at {chrome}", file=sys.stderr)
        return 1

    out = ROOT / output
    cmd = [str(chrome)]
    for flag in FLAGS:
        cmd.append(flag.format(output=out))
    cmd.append(str(INDEX.resolve()))

    subprocess.run(cmd, check=True)

    size = out.stat().st_size
    print(f"wrote {out} ({size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
