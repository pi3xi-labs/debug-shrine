#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = "Copyright (c) 2026 pi3xi-labs / wizyig"


def main() -> int:
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    if OWNER not in notice:
        print("[FAIL] NOTICE mismatch")
        return 1
    if "Mozilla Public License" not in license_text:
        print("[FAIL] LICENSE mismatch")
        return 1
    if "Version 2.0" not in license_text:
        print("[FAIL] LICENSE mismatch")
        return 1
    print("[PASS] LICENSE CHECK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
