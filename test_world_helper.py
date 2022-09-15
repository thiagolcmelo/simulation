import pytest

from world import World
from world_helper import next_id


def test_next_id():
    world = World(initial_individuals=10)
    assert next_id(world=world) == 10
