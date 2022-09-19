import pytest

from asset import Asset, ASSET_TYPES, AssetNature, AssetType


def test_get_assets():
    assets = Asset.get_assets(5)
    assert len(assets) == 5
    for a in assets:
        assert a.asset_type in ASSET_TYPES


def test_is_edible():
    asset0 = Asset(AssetType.TYPE0)
    asset1 = Asset(AssetType.TYPE1)
    asset2 = Asset(AssetType.TYPE2)
    asset3 = Asset(AssetType.TYPE3)
    asset4 = Asset(AssetType.TYPE4)
    assert asset0.is_edible
    assert asset1.is_edible
    assert not asset2.is_edible
    assert not asset3.is_edible
    assert not asset4.is_edible


def test_is_growable():
    asset0 = Asset(AssetType.TYPE0)
    asset1 = Asset(AssetType.TYPE1)
    asset2 = Asset(AssetType.TYPE2)
    asset3 = Asset(AssetType.TYPE3)
    asset4 = Asset(AssetType.TYPE4)
    assert asset0.is_growable
    assert asset1.is_growable
    assert asset2.is_growable
    assert asset3.is_growable
    assert not asset4.is_growable


def test_asset_to_string():
    asset = Asset(AssetType.TYPE0)
    assert str(asset) == "<Asset: TYPE0>"


def test_asset_repr():
    asset = Asset(AssetType.TYPE0)
    assert repr(asset) == "<Asset: TYPE0, GROWABLE>"


def test_asset_hash():
    asset = Asset(AssetType.TYPE0)
    assert hash(asset) == hash((AssetType.TYPE0, AssetNature.GROWABLE))
