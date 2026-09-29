#!/usr/bin/env python3
"""Generate DebugShrine Excel 方眼紙."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from debugshrine.excel import build_workbook  # noqa: E402

DEFAULT_OUT = ROOT / "DebugShrine_PUBLIC_v1.0.1_hogan.xlsx"


def main() -> int:
    p = argparse.ArgumentParser(description="Build DebugShrine PUBLIC 方眼紙")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = p.parse_args()
    path = build_workbook(args.out)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
