from pathlib import Path

import pytest
from jsonschema import ValidationError, validate

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = __import__("json").loads((ROOT / "classification.schema.json").read_text(encoding="utf-8"))


def test_normal():
    validate(
        {"GovernanceFlag": False, "RouteError": False, "Classification": "NORMAL"},
        SCHEMA,
    )


def test_boundary():
    validate(
        {"GovernanceFlag": False, "RouteError": True, "Classification": "BOUNDARY"},
        SCHEMA,
    )


def test_governance():
    validate(
        {"GovernanceFlag": True, "RouteError": False, "Classification": "GOVERNANCE"},
        SCHEMA,
    )


def test_governance_priority_over_boundary():
    validate(
        {"GovernanceFlag": True, "RouteError": True, "Classification": "GOVERNANCE"},
        SCHEMA,
    )


def test_boundary_rejected_when_governance():
    with pytest.raises(ValidationError):
        validate(
            {"GovernanceFlag": True, "RouteError": True, "Classification": "BOUNDARY"},
            SCHEMA,
        )


def test_boundary_requires_route_error():
    with pytest.raises(ValidationError):
        validate(
            {"GovernanceFlag": False, "RouteError": False, "Classification": "BOUNDARY"},
            SCHEMA,
        )


def test_normal_requires_false_false():
    with pytest.raises(ValidationError):
        validate(
            {"GovernanceFlag": False, "RouteError": True, "Classification": "NORMAL"},
            SCHEMA,
        )


def test_http_404_does_not_imply_boundary():
    validate(
        {
            "GovernanceFlag": False,
            "RouteError": False,
            "Classification": "NORMAL",
            "HttpStatus": 404,
        },
        SCHEMA,
    )


def test_http_500_does_not_imply_governance():
    validate(
        {
            "GovernanceFlag": False,
            "RouteError": True,
            "Classification": "BOUNDARY",
            "HttpStatus": 500,
        },
        SCHEMA,
    )
