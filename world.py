from typing import List, Tuple

from asset import Asset
from minion import Minion


class World:
    def __init__(
        self,
        size: Tuple[int, int] = (100, 100),
        initial_individuals: int = 100,
        initial_populations: int = 10,
        initial_assets: int = 1_000,
    ) -> None:
        self.size = size
        self.initial_individuals
        self.initial_populations = initial_populations
        self.initial_assets = initial_assets
        self.individuals = [
            Minion.make_from_atoms(id=i) for i in range(initial_individuals)
        ]
        self.assets = Asset.get_assets(size=initial_assets)