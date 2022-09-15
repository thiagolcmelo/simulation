import pytest

from asset import Asset, ASSET_NUM, ASSET_TYPES
from minion import (
    HAPPINESS_UNIT,
    MAX_AGE,
    MAX_PREFERENCE,
    MIN_PREFERENCE,
    Minion,
    RANDOMNESS_DELTA,
)


def assert_valid_minion(minion: Minion) -> None:
    assert len(minion.dna) > 0
    assert minion.influence >= 0
    assert minion.happiness >= 0
    assert len(minion.preferences) == ASSET_NUM
    assert 0 <= minion.age <= MAX_AGE

    for at, p in minion.preferences.items():
        assert at in ASSET_TYPES
        assert MIN_PREFERENCE <= p <= MAX_PREFERENCE


def test_make_from_atoms():
    minion = Minion.make_from_atoms(id=1)
    assert minion.id == 1
    assert_valid_minion(minion)


def test_make_from_parents():
    parent1 = Minion.make_from_atoms(1)
    parent2 = Minion.make_from_atoms(2)
    minion = Minion.make_from_parents(id=3, parent1=parent1, parent2=parent2)

    assert minion.id == 3
    assert_valid_minion(minion)

    preferences1 = parent1.preferences
    preferences2 = parent2.preferences
    preferences3 = minion.preferences

    for p in preferences1.keys():
        p1 = preferences1[p]
        p2 = preferences2[p]
        p3 = preferences3[p]
        assert p3 == pytest.approx((p1 + p2) / 2, abs=RANDOMNESS_DELTA)


def test_get_minions():
    minions = Minion.get_minions(size=20)
    assert len(minions) == 20
    for m in minions:
        assert_valid_minion(m)


def test_grant_asset():
    minion = Minion.make_from_atoms(id=1)
    assets = Asset.get_assets(size=1)
    asset_ = assets[0]
    minion.grant_asset(asset_)
    assert len(minion.assets) == 1
    assert minion.happiness == pytest.approx(
        minion.preferences[asset_.asset_type] * HAPPINESS_UNIT
    )
