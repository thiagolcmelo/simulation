from unittest.mock import patch
import pytest

from asset import Asset, AssetType
from asset_site import AssetSite
from conflict import Conflict
from individual import Individual
from point import Point
from world_helper import (
    get_points_distributed,
    harvest_by_influence,
    natural_solver,
    solve_duel,
    solve_interaction_naturally,
    solve_naturally,
    take,
)


def test_distribute_populations():
    points = get_points_distributed(grid_size=(100, 100), num_points=10)
    assert len(points) == 10
    for p in points:
        assert 0 <= p.x < 100
        assert 0 <= p.y < 100
    assert len(set(map(lambda p: f"{p.x}-{p.y}", points))) == 10


def test_distribute_populations_unique():
    points = get_points_distributed(grid_size=(100, 100), num_points=10, unique=True)
    assert len(set(map(lambda p: f"{p.x}-{p.y}", points))) == 10


def test_distribute_populations_unique_full():
    for _ in range(5):
        points = get_points_distributed(grid_size=(2, 2), num_points=4, unique=True)
        assert len(set(map(lambda p: f"{p.x}-{p.y}", points))) == 4


def test_distribute_populations_not_unique():
    points = get_points_distributed(grid_size=(3, 3), num_points=10, unique=False)
    assert len(set(map(lambda p: f"{p.x}-{p.y}", points))) < 10


def test_distribute_populations_impossible_raises():
    with pytest.raises(RuntimeError):
        get_points_distributed(grid_size=(3, 3), num_points=10, unique=True)


def test_take():
    individual1, individual2 = Individual.get_individuals(2)
    asset = Asset(individual2.preferred_asset_type)
    individual1.grant_asset(asset)

    assert asset in individual1.assets
    assert len(individual1.assets) == 1
    assert len(individual2.assets) == 0

    take(individual1, individual2)

    assert asset in individual2.assets
    assert len(individual1.assets) == 0
    assert len(individual2.assets) == 1


def test_solve_duel():
    individual1, individual2, individual3 = Individual.get_individuals(3)
    individual1.influence = 10.0
    individual2.influence = 20.0
    individual3.influence = 30.0

    individual1.preferences[AssetType.TYPE0] = 0.9
    individual2.preferences[AssetType.TYPE0] = 0.9
    individual3.preferences[AssetType.TYPE0] = 0.9

    individual1.grant_asset(Asset(AssetType.TYPE0))
    individual2.grant_asset(Asset(AssetType.TYPE0))
    individual3.grant_asset(Asset(AssetType.TYPE0))

    # 2 takes from 1
    solve_duel(individual1, individual2)
    assert len(individual1.assets) == 0
    assert len(individual2.assets) == 2

    # 3 takes from 2
    solve_duel(individual2, individual3)
    assert len(individual2.assets) == 1
    assert len(individual3.assets) == 2

    # 3 tries to take from 1 but it is empty
    solve_duel(individual1, individual3)
    assert len(individual1.assets) == 0
    assert len(individual3.assets) == 2

    # 3 takes from 2 again
    solve_duel(individual3, individual2)
    assert len(individual2.assets) == 0
    assert len(individual3.assets) == 3


@patch("individual.random")
def test_harvest_by_influence(random_mock):
    random_mock.return_value = 0.0
    individual1, individual2, individual3 = Individual.get_individuals(3)
    individual1.preferences[AssetType.TYPE0] = 0.9
    individual2.preferences[AssetType.TYPE0] = 0.9
    individual3.preferences[AssetType.TYPE0] = 0.9

    individuals = [individual1, individual2, individual3]

    individual1.influence = 10.0
    individual2.influence = 20.0
    individual3.influence = 30.0

    assets = [Asset(AssetType.TYPE0), Asset(AssetType.TYPE0)]
    site = AssetSite()
    site.extend(assets)

    harvest_by_influence(individuals, site)
    assert len(individual1.assets) == 0
    assert len(individual2.assets) == 0
    assert len(individual3.assets) == 2


@patch("world_helper.solve_naturally")
def test_natural_solver(solve_naturally_mock):
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

    natural_solver([conclict1, conclict2])
    solve_naturally_mock.assert_called()


@patch("world_helper.solve_interaction_naturally")
def test_solve_naturally(solve_interaction_naturally_mock):
    individuals = Individual.get_individuals(4)
    for individual in individuals:
        individual.grant_many_assets(Asset.get_assets(5))
    point = Point(0, 0)
    site = AssetSite()
    site.extend(Asset.get_assets(10))
    conclict = Conflict(point, individuals, site)
    conclict = solve_naturally(conclict)
    solve_interaction_naturally_mock.assert_called()


@patch("world_helper.random")
def test_solve_interaction_naturally_reproduction(random_mock):
    random_mock.side_effect = [
        0.0,
    ]
    individual1, individual2 = Individual.get_individuals(2)
    individual1.grant_many_assets(Asset.get_assets(5))
    individual2.grant_many_assets(Asset.get_assets(5))
    individuals = solve_interaction_naturally(individual1, individual2)
    assert len(individuals) == 3
    assert (
        len(individuals[0].assets)
        + len(individuals[1].assets)
        + len(individuals[2].assets)
        == 10
    )


@patch("world_helper.random")
def test_solve_interaction_naturally_assassination(random_mock):
    random_mock.side_effect = [
        1.0,
        0.0,
    ]
    individual1, individual2 = Individual.get_individuals(2)
    individual1.grant_many_assets(Asset.get_assets(5))
    individual2.grant_many_assets(Asset.get_assets(5))
    individual1.influence = 10.0
    individual2.influence = 20.0
    individuals = solve_interaction_naturally(individual1, individual2)
    assert len(individuals) == 1
    assert len(individuals[0].assets) == 10


@patch("world_helper.random")
def test_solve_interaction_naturally_duel(random_mock):
    random_mock.side_effect = [
        1.0,
        1.0,
    ]
    individual1, individual2 = Individual.get_individuals(2)
    individual1.grant_many_assets(Asset.get_assets(5))
    individual2.grant_many_assets(Asset.get_assets(5))
    individual1.influence = 10.0
    individual2.influence = 20.0
    individuals = solve_interaction_naturally(individual1, individual2)
    assert len(individuals) == 2
    assert len(individuals[0].assets) + len(individuals[1].assets) == 10
