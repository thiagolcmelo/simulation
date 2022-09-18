from dataclasses import dataclass, field
from random import randint, random, shuffle
from typing import List, Tuple
from asset_site import AssetSite

from conflict import Conflict
from constants import *
from individual import Individual
from point import Point


def get_points_distributed(
    grid_size: Tuple[int, int], num_points: int, unique: bool = True
) -> List[Point]:
    if unique and num_points > grid_size[0] * grid_size[1]:
        raise RuntimeError(
            f"cannot uniquely place {num_points} in grid {grid_size[0]}x{grid_size[1]}"
        )
    points = []
    for _ in range(num_points):
        point = Point(randint(0, grid_size[0] - 1), randint(0, grid_size[1] - 1))
        if unique:
            while point in points:
                point = Point(
                    randint(0, grid_size[0] - 1), randint(0, grid_size[1] - 1)
                )
        points.append(point)
    return points


def take(giver: Individual, receiver: Individual) -> None:
    preferred_receiver = receiver.preferred_asset_type
    if giver.has_asset_type(preferred_receiver):
        receiver.grant_asset(giver.revoke(preferred_receiver))


def solve_duel(left: Individual, right: Individual) -> None:
    if left.influence < right.influence:
        take(left, right)
    elif left.influence > right.influence:
        take(right, left)


def harvest_by_influence(individuals: List[Individual], assets: AssetSite) -> AssetSite:
    individuals = sorted(individuals, key=lambda i: i.influence, reverse=True)
    for individual in individuals:
        assets = individual.collect_assets(assets)
    shuffle(individuals)
    return assets


def solve_naturally(conflict: Conflict) -> Conflict:
    conflict.assets = harvest_by_influence(conflict.individuals, conflict.assets)
    final_individuals = []
    for left, right in zip(conflict.individuals[::2], conflict.individuals[1::2]):
        if random() < INDIVIDUAL_REPRODUCTION_PROBABILITY:
            final_individuals.extend(left.reproduce_with(right))
        elif random() < INDIVIDUAL_ASSASSINATION_PROBABILITY:
            final_individuals.extend(left.fight(right))
        else:
            solve_duel(left, right)
            final_individuals.extend([left, right])
    conflict.individuals = final_individuals
    return conflict


def natural_solver(conflicts: List[Conflict]) -> List[Conflict]:
    return [solve_naturally(c) for c in conflicts]
