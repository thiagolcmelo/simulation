from collections import defaultdict
from itertools import chain
from typing import List

from asset import Asset, AssetType


class AssetSite:
    def __init__(self) -> None:
        self._assets = defaultdict(list)
        self._total_of_type = defaultdict(int)
        self._total_assets = 0

    def get_growable_assets(self) -> List[Asset]:
        return self._assets[AssetType.EDIBLE] + self._assets[AssetType.GROWABLE]

    def append(self, asset: Asset) -> None:
        self._assets[asset.asset_type].append(asset)
        self._total_of_type[asset.asset_type] += 1
        self._total_assets += 1

    def extend(self, assets: Asset) -> None:
        for asset in assets:
            self.append(asset)

    def total_of_type(self, asset_type: AssetType) -> int:
        return self._total_of_type[asset_type]

    def __contains__(self, asset: Asset) -> bool:
        return self._total_of_type[asset.asset_type] > 0

    def __len__(self) -> int:
        return self._total_assets

    def __iter__(self):
        self._n = 0
        self._total_assets_ref = chain(*self._assets.values())
        return self

    def __next__(self):
        if self._n < self._total_assets:
            result = next(self._total_assets_ref)
            self._n += 1
            return result
        else:
            raise StopIteration
