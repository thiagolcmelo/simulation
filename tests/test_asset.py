from lib2to3.pgen2.token import GREATER
from unittest.mock import patch
from asset import Asset, ASSET_TYPES, AssetType


def test_get_assets():
    assets = Asset.get_assets(5)
    assert len(assets) == 5
    for a in assets:
        assert a.asset_type in ASSET_TYPES


def test_get_edible():
    assets = Asset.get_edible(5)
    assert len(assets) == 5
    for a in assets:
        assert a.asset_type == AssetType.EDIBLE


def test_get_growable():
    assets1 = Asset.get_growable(5)

    assert len(assets1) == 5
    for a in assets1:
        assert a.asset_type == AssetType.GROWABLE

    with patch("asset.choices") as choices_mock:
        choices_mock.return_value = [AssetType.EDIBLE, AssetType.GROWABLE]
        assets2 = Asset.get_growable(2, with_edible=True)
        assert len(assets2) == 2
        assert assets2[0].asset_type == AssetType.EDIBLE
        assert assets2[1].asset_type == AssetType.GROWABLE


def test_get_non_growable():
    assets = Asset.get_non_growable(5)
    assert len(assets) == 5
    for a in assets:
        assert a.asset_type == AssetType.NON_GROWABLE


def test_is_edible():
    asset0 = Asset(AssetType.EDIBLE)
    asset1 = Asset(AssetType.GROWABLE)
    asset2 = Asset(AssetType.NON_GROWABLE)
    assert asset0.is_edible
    assert not asset1.is_edible
    assert not asset2.is_edible


def test_is_growable():
    asset0 = Asset(AssetType.EDIBLE)
    asset1 = Asset(AssetType.GROWABLE)
    asset2 = Asset(AssetType.NON_GROWABLE)
    assert asset0.is_growable
    assert asset1.is_growable
    assert not asset2.is_growable


def test_asset_to_string():
    asset = Asset(AssetType.GROWABLE)
    assert str(asset) == "<Asset: GROWABLE>"


def test_asset_repr():
    asset = Asset(AssetType.GROWABLE)
    assert repr(asset) == "<Asset: GROWABLE>"


def test_asset_hash():
    asset = Asset(AssetType.EDIBLE)
    assert hash(asset) == hash(str(AssetType.EDIBLE.name))
