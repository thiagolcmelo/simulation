from dataclasses import dataclass, field
from typing import List

from asset_site import AssetSite
from individual import Individual
from point import Point


@dataclass
class Conflict:
    place: Point
    individuals: List[Individual] = field(default_factory=lambda: [])
    assets: AssetSite = field(default_factory=lambda: AssetSite())
