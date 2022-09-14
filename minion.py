from __future__ import annotations
from dataclasses import dataclass
from random import sample
from typing import Dict

from asset import AssetType, ASSET_NUM, ASSET_TYPES
from dna_helper import combine_dna, DNA, new_dna


@dataclass
class Minion:
    id: int
    dna: DNA
    influence: int
    happiness: int
    preferences: Dict[AssetType, float]
    age: int = 0

    def make_from_parents(
        cls,
        id: int,
        parent1: Minion,
        parent2: Minion
    ) -> Minion:
        return cls(
            id=id,
            dna=combine_dna(parent1.dna, parent2.dna),
            influence=0,
            happiness=0,
            preferences=Minion._preferences_from_parents(parent1, parent2),
        )

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
        parent1: Minion,
        parent2: Minion
    ) -> Dict[AssetType, float]:
        return {
            at: (parent1[at] + parent2[at]) / 2.0
            for at in ASSET_TYPES
        }

    @staticmethod
    def _preferences_from_atoms() -> Dict[AssetType, float]:
        max_preference = 0.9
        min_preference = 0.1
        step = (max_preference - min_preference) / (ASSET_NUM - 1)
        preferences = [min_preference + i * step for i in range(ASSET_NUM)]
        random_types = sample(ASSET_TYPES, k=ASSET_NUM)
        return dict(zip(random_types, preferences))
