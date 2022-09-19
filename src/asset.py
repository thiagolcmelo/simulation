from __future__ import annotations
from enum import Enum
from random import choices
from typing import List


class AssetType(Enum):
    EDIBLE = "EDIBLE"
    GROWABLE = "GROWABLE"
    NON_GROWABLE = "NON_GROWABLE"


ASSET_TYPES = [
    AssetType.EDIBLE,
    AssetType.GROWABLE,
    AssetType.NON_GROWABLE,
]
ASSET_NUM = len(ASSET_TYPES)


class Asset:
    def __init__(self, asset_type: AssetType) -> None:
        self.asset_type = asset_type

    @classmethod
    def get_assets(cls, size: int) -> List[Asset]:
        types = choices(ASSET_TYPES, k=size)
        return [cls(t) for t in types]

    @classmethod
    def get_edible(cls, size: int) -> List[Asset]:
        return [cls(AssetType.EDIBLE) for _ in range(size)]

    @classmethod
    def get_growable(cls, size: int, with_edible: bool = False) -> List[Asset]:
        if with_edible:
            types = choices([AssetType.EDIBLE, AssetType.GROWABLE], k=size)
            return [cls(t) for t in types]
        return [cls(AssetType.GROWABLE) for _ in range(size)]

    @classmethod
    def get_non_growable(cls, size: int) -> List[Asset]:
        return [cls(AssetType.NON_GROWABLE) for _ in range(size)]

    @property
    def is_edible(self) -> bool:
        return self.asset_type == AssetType.EDIBLE

    @property
    def is_growable(self) -> bool:
        return self.asset_type in (AssetType.EDIBLE, AssetType.GROWABLE)

    def __str__(self) -> str:
        return f"<Asset: {self.asset_type.name}>"

    def __repr__(self) -> str:
        return f"<Asset: {self.asset_type.name}>"

    def __hash__(self) -> int:
        return hash(str(self.asset_type.name))
