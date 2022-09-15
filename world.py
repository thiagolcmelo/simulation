from random import sample, shuffle, randint
from typing import List, Tuple

from asset import Asset
from minion import Minion
from world_helper import get_points_distributed, Point


class World:
    def __init__(
        self,
        size: Tuple[int, int] = (100, 100),
        initial_individuals: int = 100,
        initial_populations: int = 10,
        initial_assets: int = 1_000,
    ) -> None:
        self.size = size
        self.initial_individuals = initial_individuals
        self.initial_populations = initial_populations
        self.initial_assets = initial_assets
        self.assets = Asset.get_assets(size=initial_assets)
        self.individuals = Minion.get_minions(size=initial_individuals)
        self._distribute_individuals()

    def _distribute_individuals(self) -> None:
        individuals_per_population = self.initial_individuals / self.initial_populations
        points = get_points_distributed(
            grid_size=self.size, num_points=self.initial_populations
        )
        ids = [i.id for i in self.individuals]
        shuffle(ids)
        self.individuals_positions = {}
        for id_ in ids:
            position = self._randomize_point(sample(points, l=1)[0])
            self.individuals_positions[id_] = position

    def _randomize_point(self, point: Point, units: int = 1) -> Point:
        dx = randint(-units, units)
        dy = randint(-units, units)
        point.x = min(max(0, point.x + dx), self.size[0] - 1)
        point.y = min(max(0, point.y + dy), self.size[1] - 1)
        return point

    def _distribute_assets(self) -> None:
        self.assets_positions = {}
