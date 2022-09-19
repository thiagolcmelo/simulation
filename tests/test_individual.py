from math import ceil, log10
from collections import Counter
from unittest.mock import patch

import pytest

from asset import Asset, ASSET_NUM, ASSET_TYPES, AssetType
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


def test_grant_asset():
    individual = Individual.make_from_atoms()
    assets = Asset.get_assets(size=1)
    asset_ = assets[0]
    individual.grant_asset(asset_)
    assert len(individual.assets) == 1
    assert individual.happiness == pytest.approx(
        individual.preferences[asset_.asset_type] * INDIVIDUAL_HAPPINESS_UNIT
    )


def test_grant_many_assets():
    individual = Individual.make_from_atoms()
    assets = Asset.get_assets(5)
    individual.grant_many_assets(assets)
    for asset in assets:
        assert asset in individual.assets


def test_revoke_success():
    individual = Individual.make_from_atoms()
    asset_old = Asset.get_assets(1)[0]
    individual.grant_asset(asset_old)
    assert asset_old in individual.assets
    assert len(individual.assets) == 1

    asset_new = individual.revoke(asset_old.asset_type)
    assert asset_new == asset_old
    assert len(individual.assets) == 0


def test_revoke_fail():
    individual = Individual.make_from_atoms()
    asset_old = Asset(AssetType.EDIBLE)
    individual.grant_asset(asset_old)
    assert asset_old in individual.assets
    assert len(individual.assets) == 1

    with pytest.raises(RuntimeError):
        _ = individual.revoke(AssetType.NON_GROWABLE)

    assert asset_old in individual.assets
    assert len(individual.assets) == 1


def test_inherit():
    assets = Asset.get_assets(100)
    parent1 = Individual.make_from_atoms()
    parent1.grant_many_assets(assets[:50])
    parent2 = Individual.make_from_atoms()
    parent2.grant_many_assets(assets[50:])

    child = Individual.make_from_parents(parent1, parent2)

    assert len(parent1.assets) == 50
    assert len(child.assets) == 0
    child.inherit(parent1)
    assert len(parent1.assets) + len(child.assets) == 50

    assert len(parent2.assets) == 50
    child.inherit(parent2)
    assert len(parent1.assets) + len(parent2.assets) + len(child.assets) == 100


@pytest.mark.parametrize(
    "age, starving_days, has_food, estimate, units, is_alive",
    [
        (1, 5, True, 1.0, 1, True),  # all good
        (100, 5, True, 1.0, 1, False),  # die from age
        (1, 5, True, 0.0, 1, False),  # die anyway
        (
            1,
            ceil(
                log10(1.0 + 0.5) / log10(1.0 + INDIVIDUAL_DAILY_STARVATION_PROBABILITY)
            ),
            False,
            0.5,
            1,
            False,
        ),  # die from starvation (bad test)
    ],
)
@patch("individual.random")
def test_get_old(random_mock, age, starving_days, has_food, estimate, units, is_alive):
    random_mock.return_value = estimate
    individual = Individual.make_from_atoms()
    individual.age = age
    individual.starving_days = starving_days
    if has_food:
        individual.grant_asset(Asset(AssetType.EDIBLE))
    assert individual.get_old(units) == is_alive


def test_avg_dna_counts():
    individual1 = Individual.make_from_atoms()
    individual2 = Individual.make_from_atoms()
    dna1 = ["a", "a", "b", "b", "c", "c"]
    dna2 = ["a", "a", "b", "b", "d", "d"]
    avg_dna_expected = Counter(dna1 + dna2)
    for b in avg_dna_expected:
        avg_dna_expected[b] /= 2.0
    individual1.dna = dna1
    individual2.dna = dna2
    avg_dna_actual = Individual.avg_dna_counts([individual1, individual2])

    for b in avg_dna_actual:
        assert avg_dna_actual[b] == pytest.approx(avg_dna_expected[b])


def test_dna_distance():
    individual = Individual.make_from_atoms()
    dna1 = ["a", "a", "b", "b", "c", "c"]
    dna2 = ["a", "a", "b", "b", "d", "d"]
    avg_dna = Counter(dna1 + dna2)
    for b in avg_dna:
        avg_dna[b] /= 2.0
    individual.dna = dna1

    # avg_population    = {'a': 2.0, 'b': 2.0, 'c': 1.0, 'd': 1.0}
    # individual_counts = {'a': 2.0, 'b': 2.0, 'c': 2.0, 'd': 0.0}
    distance_expected = (
        (2.0 - 2.0) ** 2 + (2.0 - 2.0) ** 2 + (2.0 - 1.0) ** 2 + (0.0 - 1.0) ** 2
    )

    distance_actual = individual.dna_distance(avg_dna)
    assert distance_actual == pytest.approx(distance_expected)


@pytest.mark.parametrize(
    "influence1, influence2, draw, survivor_index",
    [
        (10.0, 5.0, False, 0),
        (5.0, 10.0, False, 1),
        (10.0, 10.0, True, None),
    ],
)
def test_fight(influence1, influence2, draw, survivor_index):
    individual1 = Individual.make_from_atoms()
    individual2 = Individual.make_from_atoms()
    assets = Asset.get_assets(100)
    individual1.grant_many_assets(assets[:50])
    individual2.grant_many_assets(assets[50:])
    individual1.influence = influence1
    individual2.influence = influence2

    individuals = [individual1, individual2]
    result = individual1.fight(individual2)

    if draw:
        assert len(result) == 2
        assert len(result[0].assets) == 50
        assert len(result[1].assets) == 50
    else:
        assert len(result) == 1
        assert result[0] == individuals[survivor_index]
        assert len(result[0].assets) == 100


def test_reproduce_with():
    assets = Asset.get_assets(100)
    parent1 = Individual.make_from_atoms()
    parent1.grant_many_assets(assets[:50])
    parent2 = Individual.make_from_atoms()
    parent2.grant_many_assets(assets[50:])

    family = parent1.reproduce_with(parent2)
    assert len(family) == 3
    assert parent1 in family
    assert parent2 in family
    assert len(family[0].assets + family[1].assets + family[2].assets) == 100


def test_hash():
    individual = Individual.make_from_atoms()
    assert hash(individual) is not None
