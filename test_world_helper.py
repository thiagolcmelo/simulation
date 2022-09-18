import pytest

from asset import Asset, AssetType
from individual import Individual
from world_helper import get_points_distributed, solve_duel, take


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
