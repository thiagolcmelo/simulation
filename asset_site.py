from collections import defaultdict

from asset import Asset, AssetType


class AssetSite:
    def __init__(self) -> None:
        self.growable = []
        self.non_growable = []
        self.edible = []
        self._total_of_type = defaultdict(int)
        self.total_assets = 0

    def append(self, asset: Asset) -> None:
        if asset.is_edible:
            self.edible.append(asset)
        elif asset.is_growable:
            self.growable.append(asset)
        else:
            self.non_growable.append(asset)
        self._total_of_type[asset.asset_type] += 1
        self.total_assets += 1

    def extend(self, assets: Asset) -> None:
        for asset in assets:
            self.append(asset)

    def total_of_type(self, asset_type: AssetType) -> int:
        return self._total_of_type[asset_type]

    def __len__(self) -> int:
        return self.total_assets

    def __iter__(self):
        self._n = 0
        self._total_assets_ref = self.edible + self.growable + self.non_growable
        return self

    def __next__(self):
        if self._n < self.total_assets:
            result = self._total_assets_ref[self._n]
            self._n += 1
            return result
        else:
            raise StopIteration
