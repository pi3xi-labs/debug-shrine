#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = json.loads((ROOT / "release_manifest.json").read_text(encoding="utf-8"))
    expected = manifest["license_sha256"]
    actual = hashlib.sha256((ROOT / "LICENSE").read_bytes()).hexdigest()
    if actual != expected:
        print(f"[FAIL] LICENSE SHA256 mismatch\nexpected={expected}\nactual={actual}")
        return 1
    print("[PASS] LICENSE HASH")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
