import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from notice_validator import OWNER, validate_notice_file, validate_notice_text


def test_notice_file_ok():
    assert validate_notice_file(ROOT / "NOTICE")


def test_notice_ok_inline():
    assert validate_notice_text(
        """
        DebugShrine METHOD CONTRACT
        Copyright (c) 2026 pi3xi-labs / wizyig
        Mozilla Public License
        """
    )


def test_notice_e001():
    with pytest.raises(ValueError, match="NOTICE_E001"):
        validate_notice_text(
            """
            DebugShrine METHOD CONTRACT
            Copyright (c) 2026 AnotherOwner
            Mozilla Public License
            """
        )


def test_notice_e002():
    with pytest.raises(ValueError, match="NOTICE_E002"):
        validate_notice_text(
            """
            DebugShrine METHOD CONTRACT
            Copyright (c) 2026 pi3xi-labs / wizyig
            """
        )


def test_notice_e003():
    with pytest.raises(ValueError, match="NOTICE_E003"):
        validate_notice_text(
            """
            Copyright (c) 2026 pi3xi-labs / wizyig
            Mozilla Public License
            """
        )


def test_owner_constant():
    assert OWNER == "Copyright (c) 2026 pi3xi-labs / wizyig"
