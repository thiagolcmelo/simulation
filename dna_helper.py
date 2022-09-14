from random import choices
from string import ascii_lowercase
from typing import List

DNA = List[str]
DNA_BASES = ascii_lowercase
DNA_SIZE = 26


# Creates a new random DNA from bases with size
def new_dna(bases: str = DNA_BASES, size: int = DNA_SIZE) -> DNA:
    return choices(DNA_BASES, k=size)


# Creates a new DNA by sampling elements from the two other DNA sequences
def combine_dna(dna1: DNA, dna2: DNA, size: int = DNA_SIZE) -> DNA:
    return new_dna(dna1 + dna2, size)
