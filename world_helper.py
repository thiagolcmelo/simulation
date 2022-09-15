from dataclasses import dataclass
from random import randint
from typing import List, Tuple


@dataclass
class Point:
    x: int
    y: int


def get_points_distributed(grid_size: Tuple[int, int], num_points: int) -> List[Point]:
    points = []
    for i in range(num_points):
        point = Point(randint(0, grid_size[0] - 1), randint(0, grid_size[1] - 1))
        while point in points:
            point = Point(randint(0, grid_size[0] - 1), randint(0, grid_size[1] - 1))
        points.append(point)
    return points
