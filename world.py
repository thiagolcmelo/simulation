from collections import Counter, defaultdict
from dataclasses import dataclass, field
from random import sample, shuffle, randint
from typing import List, Tuple

from asset import Asset
from individual import Individual
from world_helper import get_points_distributed, Point


@dataclass
class Conflict:
    place: Point
    individuals: List[Individual] = field(default_factory=lambda: [])
    assets: List[Asset] = field(default_factory=lambda: [])


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

        self.individuals_positions = defaultdict(list)
        self._distribute_individuals()

        self.assets_positions = defaultdict(list)
        self._distribute_assets()
        self.time_is_passing = False

    def solve_conflicts(self, solutions: List[Conflict] = None) -> List[Conflict]:
        if self.time_is_passing:
            self._set_solutions(solutions=solutions)
        else:
            self._collect_assets()
            self.time_is_passing = True
        self._move_time()
        return self._get_conflicts()

    def _move_time(self) -> None:
        self._collect_assets()
        self._age_individuals()
        self._move_individuals()

    def _collect_assets(self) -> None:
        pass

    def _age_individuals(self) -> None:
        pass

    def _move_individuals(self) -> None:
        pass

    def _set_solutions(self, solutions: List[Conflict]) -> None:
        for solution in solutions:
            self.individuals_positions[solution.place] = solution.individuals
            self.assets_positions[solution.place] = solution.assets

    def _get_conflicts(self) -> List[Conflict]:
        conflicts = []
        for point, individuals in self.individuals_positions.items():
            if len(individuals) > 1:
                conflicts.append(
                    Conflict(point, individuals, self.assets_positions[point])
                )
        return conflicts

    def _distribute_individuals(self) -> None:
        points = get_points_distributed(
            grid_size=self.size, num_points=self.initial_populations
        )
        individuals = Individual.get_individuals(size=self.initial_individuals)
        for individual in individuals:
            position = sample(points, k=1)[0]
            position = Point(position.x, position.y)
            position = self._randomize_point(position)
            self.individuals_positions[position].append(individual)

    def _randomize_point(self, point: Point, units: int = 1) -> Point:
        dx = randint(-units, units)
        dy = randint(-units, units)
        point.x = min(max(0, point.x + dx), self.size[0] - 1)
        point.y = min(max(0, point.y + dy), self.size[1] - 1)
        return point

    def _distribute_assets(self) -> None:
        points = get_points_distributed(
            grid_size=self.size, num_points=self.initial_assets, unique=False
        )
        points_counter = Counter(points)
        for point, num_assets in points_counter.items():
            assets = Asset.get_assets(size=num_assets)
            self.assets_positions[point].extend(assets)
