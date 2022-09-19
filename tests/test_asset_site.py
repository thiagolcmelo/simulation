from collections import defaultdict

from asset import Asset
from asset_site import AssetSite


def test_site_apend():
    asset = Asset.get_assets(1)[0]
    site = AssetSite()
    site.append(asset)
    assert asset in site


def test_site_extend():
    assets = Asset.get_assets(2)
    site = AssetSite()
    site.extend(assets)
    for asset in assets:
        assert asset in site


def test_site_total_of_type():
    assets = Asset.get_assets(100)
    per_type = defaultdict(int)
    for asset in assets:
        per_type[asset.asset_type] += 1
    site = AssetSite()
    site.extend(assets)

    for asset_type, count in per_type.items():
        assert site.total_of_type(asset_type) == count


def test_site_len():
    assets = Asset.get_assets(100)
    site = AssetSite()
    site.extend(assets)
    assert len(site) == 100


def test_site_iteration():
    assets = Asset.get_assets(100)
    site = AssetSite()
    site.extend(assets)
    for asset in site:
        assert asset in assets
        assets.pop(assets.index(asset))
    assert len(assets) == 0


def test_get_growable_assets():
    edible = Asset.get_edible(3)
    growable = Asset.get_growable(3)
    non_growable = Asset.get_non_growable(3)

    site = AssetSite()
    site.extend(edible)
    site.extend(growable)
    site.extend(non_growable)

    assert len(site.get_growable_assets()) == 6
