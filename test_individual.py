import pytest

from asset import Asset, ASSET_NUM, ASSET_TYPES
from individual import (
    HAPPINESS_UNIT,
    MAX_AGE,
    MAX_PREFERENCE,
    MIN_PREFERENCE,
    Individual,
    RANDOMNESS_DELTA,
)


def assert_valid_individual(individual: Individual) -> None:
    assert len(individual.dna) > 0
    assert individual.influence >= 0
    assert individual.happiness >= 0
    assert len(individual.preferences) == ASSET_NUM
    assert 0 <= individual.age <= MAX_AGE

    for at, p in individual.preferences.items():
        assert at in ASSET_TYPES
        assert MIN_PREFERENCE <= p <= MAX_PREFERENCE


def test_make_from_atoms():
    individual = Individual.make_from_atoms(id=1)
    assert individual.id == 1
    assert_valid_individual(individual)


def test_make_from_parents():
    parent1 = Individual.make_from_atoms(1)
    parent2 = Individual.make_from_atoms(2)
    individual = Individual.make_from_parents(id=3, parent1=parent1, parent2=parent2)

    assert individual.id == 3
    assert_valid_individual(individual)

    preferences1 = parent1.preferences
    preferences2 = parent2.preferences
    preferences3 = individual.preferences

    for p in preferences1.keys():
        p1 = preferences1[p]
        p2 = preferences2[p]
        p3 = preferences3[p]
        assert p3 == pytest.approx((p1 + p2) / 2, abs=RANDOMNESS_DELTA)


def test_get_individuals():
    individuals = Individual.get_individuals(size=20)
    assert len(individuals) == 20
    for m in individuals:
        assert_valid_individual(m)


def test_grant_asset():
    individual = Individual.make_from_atoms(id=1)
    assets = Asset.get_assets(size=1)
    asset_ = assets[0]
    individual.grant_asset(asset_)
    assert len(individual.assets) == 1
    assert individual.happiness == pytest.approx(
        individual.preferences[asset_.asset_type] * HAPPINESS_UNIT
    )
