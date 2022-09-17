from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"(x={self.x}, y={self.y})"
