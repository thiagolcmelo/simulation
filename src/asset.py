from __future__ import annotations
from enum import Enum
from random import choices
from typing import List


class AssetType(Enum):
    TYPE0 = "TYPE0"
    TYPE1 = "TYPE1"
    TYPE2 = "TYPE2"
    TYPE3 = "TYPE3"
    TYPE4 = "TYPE4"
    TYPE5 = "TYPE5"
    TYPE6 = "TYPE6"
    TYPE7 = "TYPE7"
    TYPE8 = "TYPE8"
    TYPE9 = "TYPE9"


class AssetNature(Enum):
    GROWABLE = "GROWABLE"
    NON_GROWABLE = "NON_GROWABLE"


ASSET_TYPES = [
    AssetType.TYPE0,
    AssetType.TYPE1,
    AssetType.TYPE2,
    AssetType.TYPE3,
    AssetType.TYPE4,
    AssetType.TYPE5,
    AssetType.TYPE6,
    AssetType.TYPE7,
    AssetType.TYPE8,
    AssetType.TYPE9,
]
ASSET_NUM = len(ASSET_TYPES)


def asset_type_nature(asset_type: AssetType) -> AssetNature:
    if asset_type in (
        AssetType.TYPE0,
        AssetType.TYPE1,
        AssetType.TYPE2,
        AssetType.TYPE3,
    ):
        return AssetNature.GROWABLE
    return AssetNature.NON_GROWABLE


def is_asset_edible(asset_type: AssetType) -> bool:
    return asset_type in (AssetType.TYPE0, AssetType.TYPE1)


class Asset:
    def __init__(self, asset_type: AssetType) -> None:
        self.asset_type = asset_type
        self.asset_nature = asset_type_nature(asset_type)

    @classmethod
    def get_assets(cls, size: int) -> List[Asset]:
        types = choices(ASSET_TYPES, k=size)
        return [cls(t) for t in types]

    @property
    def is_edible(self) -> bool:
        return is_asset_edible(self.asset_type)

    @property
    def is_growable(self) -> bool:
        return self.asset_nature == AssetNature.GROWABLE

    def __str__(self) -> str:
        return f"<Asset: {self.asset_type.name}>"

    def __repr__(self) -> str:
        return f"<Asset: {self.asset_type.name}, {self.asset_nature.name}>"

    def __hash__(self) -> int:
        return hash((str(self.asset_type.name), str(self.asset_nature.name)))
