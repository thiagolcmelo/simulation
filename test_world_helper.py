import pytest

from world_helper import get_points_distributed


def test_distribute_populations():
    points = get_points_distributed(grid_size=(100, 100), num_points=10)
    assert len(points) == 10
    for p in points:
        assert 0 <= p.x < 100
        assert 0 <= p.y < 100
    assert len(set(map(lambda p: f"{p.x}-{p.y}", points))) == 10
