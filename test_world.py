import pytest

from asset import Asset, AssetNature, AssetType
from individual import Individual
from world import World
from point import Point


def test_world_initialize_assets():
    world = World(
        size=(10, 10), initial_assets=20, initial_individuals=10, initial_populations=3
    )
    assert sum(map(len, world.site_positions.values())) == 20


def test_world_initialize_individuals():
    world = World(
        size=(10, 10), initial_assets=20, initial_individuals=10, initial_populations=3
    )
    assert sum(map(len, world.individuals_positions.values())) == 10


def test_get_individuals_not_competing():
    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )
    individuals = Individual.get_individuals(size=3)
    point1 = Point(3, 3)
    point2 = Point(4, 6)
    world.individuals_positions[point1].extend(individuals[:2])
    world.individuals_positions[point2].append(individuals[2])
    not_competing = world.get_individuals_not_competing()
    assert len(not_competing) == 1
    point, individual = not_competing[0]
    assert point == point2
    assert id(individual) == id(individuals[2])


def test_get_assets_free_and_growable():
    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )
    individuals = Individual.get_individuals(size=3)

    # 0 free, 0 growable
    point1 = Point(3, 3)
    world.individuals_positions[point1].append(individuals[0])
    # 1 free, 0 growable
    point2 = Point(4, 4)
    world.site_positions[point2].append(Asset(AssetType.TYPE4))
    # 0 free, 1 growable
    point3 = Point(5, 6)
    world.individuals_positions[point3].append(individuals[1])
    world.site_positions[point3].append(Asset(AssetType.TYPE0))
    # 1 free, 1 growable
    point4 = Point(6, 6)
    world.site_positions[point4].append(Asset(AssetType.TYPE1))

    free_and_growable = world.get_assets_free_and_growable()
    assert len(free_and_growable) == 1
    point, asset = free_and_growable[0]
    assert point == point4
    assert asset.asset_type == AssetType.TYPE1
    assert asset.asset_nature == AssetNature.GROWABLE


@pytest.mark.parametrize(
    "size, point, is_valid",
    [
        ((10, 10), Point(0, 0), True),
        ((10, 10), Point(0, 9), True),
        ((10, 10), Point(9, 0), True),
        ((10, 10), Point(9, 9), True),
        ((10, 10), Point(-1, 0), False),
        ((10, 10), Point(0, -1), False),
        ((10, 10), Point(-1, -1), False),
        ((10, 10), Point(-1, 9), False),
        ((10, 10), Point(-1, 10), False),
        ((10, 10), Point(9, 10), False),
        ((10, 10), Point(10, 9), False),
    ],
)
def test_is_valid_point(size, point, is_valid):
    world = World(
        size=size, initial_assets=0, initial_individuals=0, initial_populations=0
    )
    assert world.is_valid_point(point) == is_valid


@pytest.mark.parametrize(
    "point, options",
    [
        (Point(0, 0), (Point(0, 1), Point(1, 0), Point(1, 1))),
        (
            Point(0, 5),
            (Point(0, 4), Point(0, 6), Point(1, 4), Point(1, 5), Point(1, 6)),
        ),
        (Point(0, 9), (Point(1, 9), Point(1, 8), Point(0, 8))),
        (Point(9, 0), (Point(9, 1), Point(8, 1), Point(8, 0))),
        (Point(9, 9), (Point(9, 8), Point(8, 9), Point(8, 8))),
        (
            Point(5, 5),
            (
                Point(4, 4),
                Point(4, 5),
                Point(4, 6),
                Point(5, 4),
                Point(5, 6),
                Point(6, 4),
                Point(6, 5),
                Point(6, 6),
            ),
        ),
    ],
)
def test_get_random_neighboor(point, options):
    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )
    assert world.get_random_neighboor(point) in options


def test_get_all_individuals():
    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )
    individuals = Individual.get_individuals(size=3)
    point1 = Point(3, 3)
    world.individuals_positions[point1].append(individuals[0])
    world.individuals_positions[point1].append(individuals[1])
    point2 = Point(4, 4)
    world.individuals_positions[point2].append(individuals[2])

    all_individuals = world.get_all_individuals()
    assert len(all_individuals) == 3
    assert all_individuals[0] in individuals
    assert all_individuals[1] in individuals
    assert all_individuals[2] in individuals
