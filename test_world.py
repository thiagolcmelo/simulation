import pytest

from world import World


def test_world_initialize_assets():
    world = World(
        size=(10, 10), initial_assets=20, initial_individuals=10, initial_populations=3
    )
    assert sum(map(len, world.assets_positions.values())) == 20


def test_world_initialize_individuals():
    world = World(
        size=(10, 10), initial_assets=20, initial_individuals=10, initial_populations=3
    )
    assert len(world.individuals) == 10
