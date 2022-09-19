from __future__ import annotations
from collections import Counter
from dataclasses import dataclass, field
from random import random, sample, shuffle
from typing import Dict, List

from asset import Asset, AssetType, ASSET_NUM, ASSET_TYPES
from asset_site import AssetSite
from constants import *
from dna_helper import combine_dna, DNA, new_dna


@dataclass
class Individual:
    dna: DNA
    influence: int
    preferences: Dict[AssetType, float]
    age: int = 0
    assets: List[Asset] = field(default_factory=lambda: [])
    starving_days: int = 0

    @property
    def preferred_asset_type(self) -> AssetType:
        return sorted(self.preferences.items(), key=lambda p: p[1], reverse=True)[0][0]

    @property
    def happiness(self) -> float:
        return (
            sum([self.preferences[a.asset_type] for a in self.assets])
            * INDIVIDUAL_HAPPINESS_UNIT
        )

    @classmethod
    def make_from_parents(cls, parent1: Individual, parent2: Individual) -> Individual:
        return cls(
            dna=combine_dna(parent1.dna, parent2.dna),
            influence=0,
            preferences=Individual._preferences_from_parents(parent1, parent2),
        )

    @classmethod
    def make_from_atoms(cls) -> Individual:
        return cls(
            dna=new_dna(),
            influence=0,
            preferences=Individual._preferences_from_atoms(),
        )

    @classmethod
    def get_individuals(cls, size: int) -> List[Individual]:
        return [cls.make_from_atoms() for _ in range(size)]

    @staticmethod
    def avg_dna_counts(population: List[Individual]) -> Counter:
        all_bases = Counter()
        total_individuals = len(population)
        for individual in population:
            all_bases.update(individual.dna)
        for b in all_bases:
            all_bases[b] /= total_individuals
        return all_bases

    @staticmethod
    def _preferences_from_parents(
        parent1: Individual, parent2: Individual
    ) -> Dict[AssetType, float]:
        randomness = (random() * 2 - 1) * PREFERENCE_RANDOMNESS_DELTA
        preferences = {
            at: (parent1.preferences[at] + parent2.preferences[at]) / 2.0
            for at in ASSET_TYPES
        }
        for at in ASSET_TYPES:
            preferences[at] = min(
                PREFERENCE_MAX_VALUE,
                max(PREFERENCE_MIN_VALUE, preferences[at] + randomness),
            )
        return preferences

    @staticmethod
    def _preferences_from_atoms() -> Dict[AssetType, float]:
        step = (PREFERENCE_MAX_VALUE - PREFERENCE_MIN_VALUE) / (ASSET_NUM - 1)
        preferences = [PREFERENCE_MIN_VALUE + i * step for i in range(ASSET_NUM)]
        random_types = sample(ASSET_TYPES, k=ASSET_NUM)
        return dict(zip(random_types, preferences))

    def get_preference_for_asset_type(self, asset_type: AssetType) -> float:
        return self.preferences[asset_type]

    def has_asset_type(self, asset_type: AssetType) -> bool:
        return any([a.asset_type == asset_type for a in self.assets])

    def grant_asset(self, asset: Asset) -> None:
        self.assets.append(asset)

    def grant_many_assets(self, assets: List[Asset]) -> None:
        self.assets.extend(assets)

    def revoke(self, asset_type: AssetType) -> Asset:
        for i in range(len(self.assets)):
            if self.assets[i].asset_type == asset_type:
                return self.assets.pop(i)
        raise RuntimeError(f"Individual does not have asset of type {asset_type}")

    def inherit(self, parent: Individual) -> None:
        self.grant_many_assets(parent.leave_heritage())

    def leave_heritage(self) -> List[Asset]:
        shuffle(self.assets)
        l = len(self.assets)
        hl = int(l / 2)
        heritage, self.assets = self.assets[:hl], self.assets[hl:]
        return heritage

    def collect_assets(self, assets: AssetSite) -> AssetSite:
        left_behind = AssetSite()
        for asset in assets:
            preference = self.get_preference_for_asset_type(asset.asset_type)
            if random() < preference:
                self.grant_asset(asset)
            else:
                left_behind.append(asset)
        return left_behind

    def get_old(self, units: int) -> bool:
        self.age += units

        for i in range(len(self.assets)):
            if self.assets[i].is_edible:
                self.assets.pop(i)
                self.starving_days = 0
                break
        else:
            self.starving_days += 1

        starve_probability = (
            1 + INDIVIDUAL_DAILY_STARVATION_PROBABILITY
        ) ** self.starving_days - 1
        if (
            random() < (INDIVIDUAL_DEATH_PROBABILITY + starve_probability)
            or self.age > INDIVIDUAL_MAX_AGE
        ):
            return False
        return True

    def dna_distance(self, avg_dna: Counter) -> float:
        dna = Counter(self.dna)
        return sum([(avg - dna[base]) ** 2 for base, avg in avg_dna.items()])

    def fight(self, other: Individual) -> List[Individual]:
        if self.influence < other.influence:
            other.grant_many_assets(self.assets)
            return [other]
        elif self.influence > other.influence:
            self.grant_many_assets(other.assets)
            return [self]
        else:
            return [self, other]

    def reproduce_with(self, other: Individual) -> List[Individual]:
        child = Individual.make_from_parents(self, other)
        child.inherit(self)
        child.inherit(other)
        return [self, child, other]

    def __hash__(self) -> int:
        dna = "-".join(self.dna)
        influence = str(self.influence)
        preferences = "-".join(map(str, self.preferences.items()))
        age = str(self.age)
        assets = tuple(self.assets)
        return hash((dna, influence, preferences, age, assets))
