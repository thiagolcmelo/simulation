from enum import Enum
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


class Asset:
    def __init__(self, asset_type: AssetType) -> None:
        self.asset_type = asset_type
        if self.asset_type in ASSET_TYPES[:4]:
            self.asset_nature = AssetNature.GROWABLE
        else:
            self.asset_nature = AssetNature.NON_GROWABLE
