from collections import Counter, defaultdict
from itertools import repeat
from random import sample, randint, random
from secrets import choice
from typing import Dict, List, Tuple

from asset import Asset
from asset_site import AssetSite
from conflict import Conflict
from constants import (
    ASSET_REPRODUCTION_PROBABILITY,
    ASSET_MAX_FOR_TYPE_IN_POINT,
    INDIVIDUAL_MAX_AGE,
)
from individual import Individual
from point import Point
from world_helper import get_points_distributed


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

        self.site_positions = defaultdict(AssetSite)
        self._distribute_assets()
        self.time_is_passing = False

    @property
    def indicators(self) -> Dict[str, float]:
        all_individuals = self.get_all_individuals()
        total_population = len(all_individuals)
        if total_population == 0:
            avg_happines = 0
        else:
            avg_happines = (
                sum([i.happiness for i in all_individuals]) / total_population
            )
        return {
            "total_population": total_population,
            "avg_happines": avg_happines,
        }

    @property
    def total_assets(self) -> int:
        total = 0
        for site in self.site_positions.values():
            total += len(site)
        for individual in self.get_all_individuals():
            total += len(individual.assets)
        return total

    def get_conflicts(self) -> List[Conflict]:
        conflicts = []
        for point, individuals in self.individuals_positions.items():
            if len(individuals) > 1:
                conflicts.append(
                    Conflict(point, individuals, self.site_positions[point])
                )
        return conflicts

    def solve_conflicts(self, solutions: List[Conflict] = None) -> None:
        for solution in solutions:
            self.individuals_positions[solution.place] = solution.individuals
            self.site_positions[solution.place] = solution.assets

    def move_time(self) -> None:
        self._collect_assets()
        self._regenerate_assets()
        self._age_individuals()
        self._update_influences()
        self._move_individuals()

    def get_individuals_not_competing(self) -> List[Tuple[Point, Individual]]:
        free_individuals = []
        for point, individuals in self.individuals_positions.items():
            if len(individuals) == 1:
                free_individuals.append((point, individuals[0]))
        return free_individuals

    def get_all_individuals(self) -> List[Individual]:
        all_individuals = []
        for point in self.individuals_positions:
            all_individuals.extend(self.individuals_positions[point])
        return all_individuals

    def get_assets_free_and_growable(self) -> List[Tuple[Point, Asset]]:
        eligible_assets = []
        for point, assets in self.site_positions.items():
            if len(self.individuals_positions[point]) == 0:
                eligible_assets.extend(zip(repeat(point), assets.get_growable_assets()))
        return eligible_assets

    def is_valid_point(self, point: Point) -> bool:
        return 0 <= point.x < self.size[0] and 0 <= point.y < self.size[1]

    def get_random_neighboor(self, point: Point) -> Point:
        options = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        while True:
            dx, dy = choice(options)
            neighboor = Point(point.x + dx, point.y + dy)
            if self.is_valid_point(neighboor):
                return neighboor

    def _collect_assets(self) -> None:
        not_competing = self.get_individuals_not_competing()
        for point, individual in not_competing:
            self.site_positions[point] = individual.collect_assets(
                self.site_positions[point]
            )

    def _regenerate_assets(self) -> None:
        assets = self.get_assets_free_and_growable()
        for point, asset in assets:
            neighbor = self.get_random_neighboor(point)
            total_of_kind_in_point = self.site_positions[neighbor].total_of_type(
                asset.asset_type
            )
            if (
                total_of_kind_in_point < ASSET_MAX_FOR_TYPE_IN_POINT
                and random() < ASSET_REPRODUCTION_PROBABILITY
            ):
                self.site_positions[neighbor].append(Asset(asset.asset_type))

    def _age_individuals(self) -> None:
        for point in self.individuals_positions:
            individuals = self.individuals_positions[point]
            alive = []
            for individual in individuals:
                is_alive = individual.get_old(1)
                if is_alive:
                    alive.append(individual)
                else:
                    self.site_positions[point].extend(individual.assets)
            self.individuals_positions[point] = alive

    def _update_influences(self) -> None:
        all_individuals = self.get_all_individuals()
        all_bases = Individual.avg_dna_counts(all_individuals)
        world_wealth = float(self.total_assets)
        for individual in all_individuals:
            distance = individual.dna_distance(all_bases)
            if distance > 0 and world_wealth > 0:
                individual.influence = (
                    (1.0 / distance)
                    * float(individual.age)
                    / float(INDIVIDUAL_MAX_AGE)
                    * float(len(individual.assets))
                    / world_wealth
                )
            else:
                individual.influence = 1.0

    def _move_individuals(self) -> None:
        new_positions = defaultdict(list)
        for point in self.individuals_positions:
            individuals = self.individuals_positions[point]
            for individual in individuals:
                neighboor = self.get_random_neighboor(point)
                new_positions[neighboor].append(individual)
        self.individuals_positions = new_positions

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
            self.site_positions[point].extend(assets)
