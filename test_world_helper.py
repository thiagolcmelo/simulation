import pytest

from world_helper import get_points_distributed


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


def test_distribute_populations_not_unique():
    points = get_points_distributed(grid_size=(3, 3), num_points=10, unique=False)
    assert len(set(map(lambda p: f"{p.x}-{p.y}", points))) < 10


def test_distribute_populations_impossible_raises():
    try:
        points = get_points_distributed(grid_size=(3, 3), num_points=10, unique=True)
        assert False, "Expected RuntimeError"
    except RuntimeError:
        pass
    except Exception as err:
        assert False, "Expected RuntimeError"
