import pytest

from world_helper import distribute_populations


def test_distribute_populations():
    points = distribute_populations(size=(100, 100), populations=10)
    assert len(points) == 10
    for p in points:
        assert 0 <= p.x < 100
        assert 0 <= p.y < 100
    assert len(set(map(lambda p: f"{p.x}-{p.y}", points))) == 10
