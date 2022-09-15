import pytest

from asset import ASSET_NUM, ASSET_TYPES
from minion import MAX_PREFERENCE, MIN_PREFERENCE, Minion, RANDOMNESS_DELTA


def test_make_from_atoms():
    minion = Minion.make_from_atoms(id=1)
    assert minion.id == 1
    assert len(minion.dna) > 0
    assert minion.influence == 0
    assert minion.happiness == 0
    assert len(minion.preferences) == ASSET_NUM
    assert minion.age == 0

    for at, p in minion.preferences.items():
        assert at in ASSET_TYPES
        assert MIN_PREFERENCE <= p <= MAX_PREFERENCE


def test_make_from_parents():
    parent1 = Minion.make_from_atoms(1)
    parent2 = Minion.make_from_atoms(2)
    minion = Minion.make_from_parents(id=3, parent1=parent1, parent2=parent2)

    assert minion.id == 3
    assert len(minion.dna) == len(parent1.dna) and len(minion.dna) == len(parent2.dna)
    assert minion.influence == 0
    assert minion.happiness == 0
    assert len(minion.preferences) == ASSET_NUM
    assert minion.age == 0

    preferences1 = parent1.preferences
    preferences2 = parent2.preferences
    preferences3 = minion.preferences

    for p in preferences1.keys():
        p1 = preferences1[p]
        p2 = preferences2[p]
        p3 = preferences3[p]
        assert p3 == pytest.approx((p1 + p2) / 2, abs=RANDOMNESS_DELTA)
