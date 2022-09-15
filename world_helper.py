from random import randint
from typing import List, Tuple


Point = Tuple[int, int]


def distribute_populations(size: Tuple[int, int], populations: int) -> List[Point]:
    points = []
    for i in range(populations):
        point = (randint(0, size[0] - 1), randint(0, size[1] - 1))
        while point in points:
            point = (randint(0, size[0] - 1), randint(0, size[1] - 1))
        points.append(point)
    return points
