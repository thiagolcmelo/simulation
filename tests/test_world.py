from unittest import mock
from unittest.mock import PropertyMock, patch
import pytest

from asset import Asset, AssetNature, AssetType
from asset_site import AssetSite
from conflict import Conflict
from constants import ASSET_MAX_FOR_TYPE_IN_POINT, INDIVIDUAL_MAX_AGE
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


def test_get_conflicts():
    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )

    point = Point(0, 0)
    site = AssetSite()
    site.extend(Asset.get_assets(10))
    world.site_positions[point] = site

    individuals = Individual.get_individuals(size=3)
    world.individuals_positions[point] = individuals

    conclicts = world.get_conflicts()
    assert len(conclicts) == 1
    conclict = conclicts[0]
    for asset in site:
        assert asset in conclict.assets


def test_solve_conflicts():
    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )

    individuals = Individual.get_individuals(4)
    for individual in individuals:
        individual.grant_many_assets(Asset.get_assets(5))

    point1 = Point(0, 0)
    point2 = Point(1, 1)

    site1 = AssetSite()
    site1.extend(Asset.get_assets(10))

    site2 = AssetSite()
    site2.extend(Asset.get_assets(10))

    conclict1 = Conflict(point1, individuals[:2], site1)
    conclict2 = Conflict(point2, individuals[2:], site2)

    world.solve_conflicts([conclict1, conclict2])

    assert len(world.individuals_positions[point1]) == 2
    assert len(world.individuals_positions[point2]) == 2
    assert len(world.site_positions[point1]) == 10
    assert len(world.site_positions[point2]) == 10


@patch("individual.random")
def test_collect_assets(random_mock):
    random_mock.return_value = 0.0

    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )

    individual = Individual.make_from_atoms()
    individual.grant_many_assets(Asset.get_assets(5))

    point = Point(0, 0)
    site = AssetSite()
    site.extend(Asset.get_assets(10))

    world.individuals_positions[point].append(individual)
    world.site_positions[point] = site

    world._collect_assets()
    assert len(individual.assets) == 15


@patch("world.random")
@patch.object(World, "get_random_neighboor")
def test_regenerate_assets_success(mock_random_neighboor, random_mock):
    point1 = Point(0, 0)
    point2 = Point(1, 1)

    mock_random_neighboor.return_value = point2
    random_mock.return_value = 0.0

    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )
    site = AssetSite()
    site.append(Asset(AssetType.TYPE0))
    world.site_positions[point1] = site
    world._regenerate_assets()
    assert len(world.site_positions[point2]) == 1


@patch("world.random")
@patch.object(World, "get_random_neighboor")
def test_regenerate_assets_fail(mock_random_neighboor, random_mock):
    point1 = Point(0, 0)
    point2 = Point(1, 1)

    mock_random_neighboor.return_value = point2
    random_mock.return_value = 1.0

    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )
    site = AssetSite()
    site.append(Asset(AssetType.TYPE0))
    world.site_positions[point1] = site
    world._regenerate_assets()
    assert len(world.site_positions[point2]) == 0


@patch("world.random")
@patch.object(World, "get_random_neighboor")
def test_regenerate_assets_fail_because_crowded(mock_random_neighboor, random_mock):
    point1 = Point(0, 0)
    point2 = Point(1, 1)

    mock_random_neighboor.return_value = point2
    random_mock.return_value = 0.0

    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )
    world.site_positions[point1].append(Asset(AssetType.TYPE0))

    for _ in range(ASSET_MAX_FOR_TYPE_IN_POINT):
        world.site_positions[point2].append(Asset(AssetType.TYPE0))

    world._regenerate_assets()

    assert len(world.site_positions[point2]) == ASSET_MAX_FOR_TYPE_IN_POINT


@pytest.mark.parametrize(
    "assets_num, survive",
    [
        (10, True),
        (10, False),
    ],
)
@patch.object(Individual, "get_old")
def test_age_individuals(get_old_mock, assets_num, survive):
    get_old_mock.return_value = survive
    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )
    individual = Individual.make_from_atoms()
    individual.grant_many_assets(Asset.get_assets(assets_num))
    point = Point(0, 0)
    world.individuals_positions[point].append(individual)

    world._age_individuals()

    if survive:
        assert len(world.individuals_positions[point]) == 1
        assert len(world.site_positions[point]) == 0
    else:
        assert len(world.individuals_positions[point]) == 0
        assert len(world.site_positions[point]) == assets_num

    get_old_mock.assert_called_with(1)


@patch.object(World, "get_all_individuals")
@patch.object(Individual, "dna_distance")
def test_update_influences(dna_distance_mock, get_all_individuals_mock):
    dna_distance_mock.side_effect = [10.0, 20.0, 30.0, 40.0]

    world = World(
        size=(10, 10), initial_assets=50, initial_individuals=0, initial_populations=0
    )

    point = Point(0, 0)
    individuals = Individual.get_individuals(4)
    get_all_individuals_mock.return_value = individuals

    for i in range(4):
        individuals[i].age = i + 1
        individuals[i].grant_many_assets(Asset.get_assets(10 * (i + 1)))

    world.individuals_positions[point].extend(individuals)

    world_wealth = float(50 + 10 + 20 + 30 + 40)

    influences = [
        (1.0 / 10.0) * (1.0 / INDIVIDUAL_MAX_AGE) * (10.0 / world_wealth),
        (1.0 / 20.0) * (2.0 / INDIVIDUAL_MAX_AGE) * (20.0 / world_wealth),
        (1.0 / 30.0) * (3.0 / INDIVIDUAL_MAX_AGE) * (30.0 / world_wealth),
        (1.0 / 40.0) * (4.0 / INDIVIDUAL_MAX_AGE) * (40.0 / world_wealth),
    ]

    world._update_influences()

    individuals = sorted(individuals, key=lambda i: i.influence)
    for individual, influence in zip(individuals, influences):
        assert individual.influence == pytest.approx(influence)


def test_update_influences_no_distance():
    world = World(
        size=(10, 10), initial_assets=10, initial_individuals=0, initial_populations=0
    )

    point = Point(0, 0)
    individual = Individual.make_from_atoms()
    world.individuals_positions[point].append(individual)
    world._update_influences()
    assert individual.influence == 1.0


def test_update_influences_no_wealth():
    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )
    point = Point(0, 0)
    individual1 = Individual.make_from_atoms()
    individual2 = Individual.make_from_atoms()
    world.individuals_positions[point].append(individual1)
    world.individuals_positions[point].append(individual2)
    world._update_influences()
    assert individual1.influence == 1.0
    assert individual2.influence == 1.0


def test_total_assets():
    world = World(
        size=(10, 10), initial_assets=50, initial_individuals=0, initial_populations=0
    )
    point = Point(0, 0)
    world.site_positions[point].extend(Asset.get_assets(10))
    individuals = Individual.get_individuals(1)
    individuals[0].grant_many_assets(Asset.get_assets(10))
    world.individuals_positions[point].extend(individuals)
    assert world.total_assets == 70


@patch.object(World, "get_random_neighboor")
def test_move_individuals(get_random_neighboor_mock):
    point1 = Point(0, 0)
    point2 = Point(1, 1)
    get_random_neighboor_mock.return_value = point2

    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )
    individual = Individual.make_from_atoms()
    world.individuals_positions[point1].append(individual)

    world._move_individuals()

    assert len(world.individuals_positions[point1]) == 0
    assert len(world.individuals_positions[point2]) == 1
    assert world.individuals_positions[point2][0] == individual


@patch.object(World, "_collect_assets")
@patch.object(World, "_regenerate_assets")
@patch.object(World, "_age_individuals")
@patch.object(World, "_update_influences")
@patch.object(World, "_move_individuals")
def test_move_time(
    collect_assets_mock,
    regenerate_assets_mock,
    age_individuals_mock,
    update_influences_mock,
    move_individuals_mock,
):
    world = World(
        size=(10, 10), initial_assets=0, initial_individuals=0, initial_populations=0
    )
    world.move_time()
    collect_assets_mock.assert_called_once()
    regenerate_assets_mock.assert_called_once()
    age_individuals_mock.assert_called_once()
    update_influences_mock.assert_called_once()
    move_individuals_mock.assert_called_once()


@patch("world.Individual.happiness", new_callable=PropertyMock)
def test_indicators(happiness_mock):
    avg_happiness = 5.0
    happiness_mock.return_value = 5.0

    world = World(
        size=(10, 10),
        initial_assets=0,
        initial_individuals=9,
        initial_populations=3,
    )

    indicators = world.indicators

    assert indicators.get("total_population") == 9
    assert indicators.get("avg_happines") == pytest.approx(avg_happiness)


@patch("world.Individual.happiness", new_callable=PropertyMock)
def test_indicators_zero_population(happiness_mock):
    avg_happiness = 0.0
    happiness_mock.return_value = 0.0

    world = World(
        size=(10, 10),
        initial_assets=0,
        initial_individuals=0,
        initial_populations=0,
    )

    indicators = world.indicators

    assert indicators.get("total_population") == 0
    assert indicators.get("avg_happines") == pytest.approx(avg_happiness)
