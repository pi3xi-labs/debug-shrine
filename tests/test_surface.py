import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from debugshrine.model import surface_band


def test_surface_edges():
    assert surface_band(0.3499) == "Stable"
    assert surface_band(0.3500) == "Emerging"
    assert surface_band(0.5999) == "Emerging"
    assert surface_band(0.6000) == "Locked"
