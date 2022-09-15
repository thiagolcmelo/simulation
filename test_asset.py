import pytest

from asset import Asset, ASSET_TYPES


def test_get_assets():
    assets = Asset.get_assets(5)
    assert len(assets) == 5
    for a in assets:
        assert a.asset_type in ASSET_TYPES
