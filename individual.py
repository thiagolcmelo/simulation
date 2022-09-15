from __future__ import annotations
from dataclasses import dataclass, field
from random import random, sample
from typing import Dict, List

from asset import Asset, AssetType, ASSET_NUM, ASSET_TYPES
from constants import *
from dna_helper import combine_dna, DNA, new_dna


@dataclass
class Individual:
    id: int
    dna: DNA
    influence: int
    happiness: int
    preferences: Dict[AssetType, float]
    age: int = 0
    assets: List[Asset] = field(default_factory=lambda: [])

    @classmethod
    def make_from_parents(
        cls, id: int, parent1: Individual, parent2: Individual
    ) -> Individual:
        return cls(
            id=id,
            dna=combine_dna(parent1.dna, parent2.dna),
            influence=0,
            happiness=0,
            preferences=Individual._preferences_from_parents(parent1, parent2),
        )

    @classmethod
    def make_from_atoms(cls, id: int) -> Individual:
        return cls(
            id=id,
            dna=new_dna(),
            influence=0,
            happiness=0,
            preferences=Individual._preferences_from_atoms(),
        )

    @classmethod
    def get_individuals(cls, size: int) -> List[Individual]:
        return [cls.make_from_atoms(id=i) for i in range(size)]

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

    def grant_asset(self, asset: Asset) -> None:
        self.assets.append(asset)
        self.happiness += self.preferences[asset.asset_type] * INDIVIDUAL_HAPPINESS_UNIT
