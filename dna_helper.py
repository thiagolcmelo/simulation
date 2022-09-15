from random import choices
from typing import List

from constants import *


DNA = List[str]


# Creates a new random DNA from bases with size
def new_dna(bases: str = DNA_BASES, size: int = DNA_SIZE) -> DNA:
    return choices(bases, k=size)


# Creates a new DNA by sampling elements from the two other DNA sequences
def combine_dna(dna1: DNA, dna2: DNA, size: int = DNA_SIZE) -> DNA:
    return new_dna(dna1 + dna2, size)
