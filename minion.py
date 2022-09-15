from __future__ import annotations
from dataclasses import dataclass
from random import random, sample
from typing import Dict

from asset import AssetType, ASSET_NUM, ASSET_TYPES
from dna_helper import combine_dna, DNA, new_dna


MAX_PREFERENCE = 0.9
MIN_PREFERENCE = 0.1
RANDOMNESS_DELTA = 0.05


@dataclass
class Minion:
    id: int
    dna: DNA
    influence: int
    happiness: int
    preferences: Dict[AssetType, float]
    age: int = 0

    @classmethod
    def make_from_parents(cls, id: int, parent1: Minion, parent2: Minion) -> Minion:
        return cls(
            id=id,
            dna=combine_dna(parent1.dna, parent2.dna),
            influence=0,
            happiness=0,
            preferences=Minion._preferences_from_parents(parent1, parent2),
        )

    @classmethod
    def make_from_atoms(cls, id: int) -> Minion:
        return cls(
            id=id,
            dna=new_dna(),
            influence=0,
            happiness=0,
            preferences=Minion._preferences_from_atoms(),
        )

    @staticmethod
    def _preferences_from_parents(
        parent1: Minion, parent2: Minion
    ) -> Dict[AssetType, float]:
        randomness = (random() * 2 - 1) * RANDOMNESS_DELTA
        return {
            at: (parent1.preferences[at] + parent2.preferences[at]) / 2.0 + randomness
            for at in ASSET_TYPES
        }

    @staticmethod
    def _preferences_from_atoms() -> Dict[AssetType, float]:
        step = (MAX_PREFERENCE - MIN_PREFERENCE) / (ASSET_NUM - 1)
        preferences = [MIN_PREFERENCE + i * step for i in range(ASSET_NUM)]
        random_types = sample(ASSET_TYPES, k=ASSET_NUM)
        return dict(zip(random_types, preferences))
