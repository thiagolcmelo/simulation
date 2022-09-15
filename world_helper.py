from dataclasses import dataclass
from random import randint
from typing import List, Tuple


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f'(x={self.x}, y={self.y})'


def get_points_distributed(
    grid_size: Tuple[int, int], num_points: int, unique: bool = True
) -> List[Point]:
    if unique and num_points > grid_size[0] * grid_size[1]:
        raise RuntimeError(
            f"cannot uniquely place {num_points} in grid {grid_size[0]}x{grid_size[1]}"
        )
    points = []
    for i in range(num_points):
        point = Point(randint(0, grid_size[0] - 1), randint(0, grid_size[1] - 1))
        if unique:
            while point in points:
                point = Point(
                    randint(0, grid_size[0] - 1), randint(0, grid_size[1] - 1)
                )
        points.append(point)
    return points
