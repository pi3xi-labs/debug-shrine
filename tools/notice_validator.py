#!/usr/bin/env python3
"""Shared NOTICE validator. Exit 0 PASS, 1 NOTICE violation, 2 runtime error."""

from __future__ import annotations

from pathlib import Path

OWNER = "Copyright (c) 2026 pi3xi-labs / wizyig"
LICENSE_NAME = "Mozilla Public License"
CONTRACT_NAME = "DebugShrine METHOD CONTRACT"

ROOT = Path(__file__).resolve().parents[1]


def validate_notice_text(text: str) -> bool:
    if OWNER not in text:
        raise ValueError("NOTICE_E001: copyright mismatch")
    if LICENSE_NAME not in text:
        raise ValueError("NOTICE_E002: license reference missing")
    if CONTRACT_NAME not in text:
        raise ValueError("NOTICE_E003: contract name missing")
    return True


def validate_notice_file(path: str | Path | None = None) -> bool:
    p = Path(path) if path else ROOT / "NOTICE"
    return validate_notice_text(p.read_text(encoding="utf-8"))


def main() -> int:
    try:
        validate_notice_file()
        print("[PASS] NOTICE validation")
        return 0
    except ValueError as e:
        print(f"[FAIL] {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
