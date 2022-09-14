from typing import List, Tuple

from minion import Minion


class World:
    def __init__(
        self,
        size: Tuple[int, int] = (1000, 1000),
        initial_individuals: int = 100,
        initial_populations: int = 10,
    ) -> None:
        self.size = size
        self.individuals = [
            Minion.make_from_atoms(id=i) for i in range(initial_individuals)
        ]
        self.initial_populations = initial_populations
