#!/usr/bin/env python3
"""Public release gate. Does not claim RFC 9110 clause coverage."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from notice_validator import validate_notice_file  # noqa: E402

CONTRACT_FILES = [
    ROOT / "classification.schema.json",
    ROOT / "debugshrine" / "model.py",
]
FORBIDDEN_IN_CONTRACT = ["RFC006", "RFC007", "RFC008"]


def check_schema() -> None:
    json.loads((ROOT / "classification.schema.json").read_text(encoding="utf-8"))


def check_boundary_files() -> None:
    for p in CONTRACT_FILES:
        text = p.read_text(encoding="utf-8")
        for tok in FORBIDDEN_IN_CONTRACT:
            if tok in text:
                raise RuntimeError(f"{p.name} contains forbidden token: {tok}")


def main() -> int:
    try:
        check_schema()
        validate_notice_file()
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "check_license.py")], cwd=ROOT)
        if r.returncode != 0:
            return r.returncode
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "check_license_hash.py")], cwd=ROOT)
        if r.returncode != 0:
            return r.returncode
        check_boundary_files()
        print("PUBLIC RELEASE CHECK: PASS")
        return 0
    except Exception as e:
        print(f"PUBLIC RELEASE CHECK: FAIL\n{e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
