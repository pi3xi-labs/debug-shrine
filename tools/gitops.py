#!/usr/bin/env python3
"""
Git helper for DebugShrine PUBLIC artifacts.

Does not store tokens. Does not force-push.
Default remote operations are dry unless --push is set AND origin exists.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from debugshrine.excel import build_workbook  # noqa: E402
from debugshrine.model import AuditRecord, aggregate  # noqa: E402


def run(cmd: list[str], cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)


def git_root() -> Path | None:
    r = run(["git", "rev-parse", "--show-toplevel"], check=False)
    if r.returncode != 0:
        return None
    return Path(r.stdout.strip())


def cmd_status() -> int:
    print("repo:", git_root() or "(not a git repo)")
    r = run(["git", "status", "--short"], check=False)
    print(r.stdout or r.stderr)
    return r.returncode


def cmd_init() -> int:
    if git_root():
        print("already a git repo:", git_root())
        return 0
    run(["git", "init"], cwd=ROOT)
    print("initialized", ROOT)
    return 0


SAMPLE = [
    AuditRecord("REC_001", "2026-09-30T00:00:00Z", "T1", "review", "A", "A", False),
    AuditRecord("REC_002", "2026-09-30T00:01:00Z", "T2", "review", "A", "B", False),
    AuditRecord("REC_003", "2026-09-30T00:02:00Z", "T3", "freeze", "A", "B", True),
    AuditRecord("REC_004", "2026-09-30T00:03:00Z", "T4", "review", "A", "B", False),
    AuditRecord("REC_005", "2026-09-30T00:04:00Z", "T5", "review", "C", "C", False),
]


def cmd_snapshot(commit: bool, push: bool) -> int:
    out = ROOT / "out"
    out.mkdir(exist_ok=True)
    xlsx = build_workbook(out / "DebugShrine_PUBLIC_v1.0.1_hogan.xlsx")
    records = [r.to_public_dict() for r in SAMPLE]
    (out / "records.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in records) + "\n",
        encoding="utf-8",
    )
    (out / "aggregate.json").write_text(
        json.dumps(aggregate(SAMPLE), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("wrote", xlsx)
    print("wrote", out / "records.jsonl")
    print("wrote", out / "aggregate.json")

    if not git_root() and not commit:
        print("no git repo; skip commit (run init, or pass --commit after git init)")
        return 0

    if commit:
        run(["git", "add", str(out), str(ROOT / "SPEC.md"), str(ROOT / "DATA_STRUCTURE.md")], check=False)
        msg = "chore(debugshrine): refresh public snapshot"
        r = run(["git", "commit", "-m", msg], check=False)
        print(r.stdout or r.stderr)
        if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
            return r.returncode

    if push:
        rem = run(["git", "remote"], check=False)
        if "origin" not in rem.stdout:
            print("no origin; skip push")
            return 0
        r = run(["git", "push", "origin", "HEAD"], check=False)
        print(r.stdout or r.stderr)
        return r.returncode
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("init")
    s = sub.add_parser("snapshot")
    s.add_argument("--commit", action="store_true")
    s.add_argument("--push", action="store_true", help="push HEAD to origin; never force")
    args = p.parse_args()
    if args.cmd == "status":
        return cmd_status()
    if args.cmd == "init":
        return cmd_init()
    if args.cmd == "snapshot":
        return cmd_snapshot(commit=args.commit, push=args.push)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
