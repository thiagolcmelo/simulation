import pytest

from asset import Asset, ASSET_NUM, ASSET_TYPES
from asset_site import AssetSite
from constants import *
from individual import Individual


def assert_valid_individual(individual: Individual) -> None:
    assert len(individual.dna) > 0
    assert individual.influence >= 0
    assert individual.happiness >= 0
    assert len(individual.preferences) == ASSET_NUM
    assert 0 <= individual.age <= INDIVIDUAL_MAX_AGE

    for at, p in individual.preferences.items():
        assert at in ASSET_TYPES
        assert PREFERENCE_MIN_VALUE <= p <= PREFERENCE_MAX_VALUE


def test_make_from_atoms():
    individual = Individual.make_from_atoms()
    assert_valid_individual(individual)


def test_make_from_parents():
    parent1 = Individual.make_from_atoms()
    parent2 = Individual.make_from_atoms()
    individual = Individual.make_from_parents(parent1=parent1, parent2=parent2)

    assert_valid_individual(individual)

    preferences1 = parent1.preferences
    preferences2 = parent2.preferences
    preferences3 = individual.preferences

    for p in preferences1.keys():
        p1 = preferences1[p]
        p2 = preferences2[p]
        p3 = preferences3[p]
        assert p3 == pytest.approx((p1 + p2) / 2, abs=PREFERENCE_RANDOMNESS_DELTA)


def test_get_individuals():
    individuals = Individual.get_individuals(size=20)
    assert len(individuals) == 20
    for m in individuals:
        assert_valid_individual(m)


def test_grant_asset():
    individual = Individual.make_from_atoms()
    assets = Asset.get_assets(size=1)
    asset_ = assets[0]
    individual.grant_asset(asset_)
    assert len(individual.assets) == 1
    assert individual.happiness == pytest.approx(
        individual.preferences[asset_.asset_type] * INDIVIDUAL_HAPPINESS_UNIT
    )


def test_collect_assets():
    individual = Individual.make_from_atoms()
    assets = Asset.get_assets(size=100)
    site = AssetSite()
    site.extend(assets)

    site = individual.collect_assets(site)
    assert type(site) is AssetSite
    assert len(site) + len(individual.assets) == 100

    for at in individual.preferences:
        individual.preferences[at] = 1.0
    site = individual.collect_assets(site)
    assert type(site) is AssetSite
    assert len(individual.assets) == 100
    assert len(site) == 0
