from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import auto
from enum import Enum
from typing import List
from typing import Set

from src.utils import load_data
from src.utils import print_result


class Orientation(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()
    DIAGONAL = auto()


def abs_range(a: int, b: int) -> List[int]:
    increment = 1 if a < b else -1
    return list(range(a, b + increment, increment))


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class Line:
    start: Point
    end: Point
    orientation: Orientation

    def get_points(self) -> List[Point]:
        if self.orientation == Orientation.HORIZONTAL:
            return [Point(x=x, y=self.start.y) for x in abs_range(self.start.x, self.end.x)]
        elif self.orientation == Orientation.VERTICAL:
            return [Point(x=self.start.x, y=y) for y in abs_range(self.start.y, self.end.y)]
        else:
            return [
                Point(x=x, y=y)
                for x, y in zip(
                    abs_range(self.start.x, self.end.x), abs_range(self.start.y, self.end.y)
                )
            ]

    @staticmethod
    def parse(line: str) -> Line:
        split_line = line.split(" -> ")
        start = Point(*map(int, split_line[0].split(",")))
        end = Point(*map(int, split_line[1].split(",")))
        if start.x == end.x:
            orientation = Orientation.VERTICAL
        elif start.y == end.y:
            orientation = Orientation.HORIZONTAL
        else:
            orientation = Orientation.DIAGONAL
        return Line(start, end, orientation)


def part(lines: List[Line], orientations: Set[Orientation]) -> int:
    lines = [line for line in lines if line.orientation in orientations]
    points = [point for line in lines for point in line.get_points()]
    return len([k for k, v in Counter(points).items() if v > 1])


if __name__ == "__main__":
    example_data = [Line.parse(val) for val in load_data(True)]
    data = [Line.parse(val) for val in load_data(False)]

    task1_orientations = {Orientation.HORIZONTAL, Orientation.VERTICAL}
    task2_orientations = {Orientation.HORIZONTAL, Orientation.VERTICAL, Orientation.DIAGONAL}

    assert part(example_data, task1_orientations) == 5
    print_result(1, part(data, task1_orientations))

    assert part(example_data, task2_orientations) == 12
    print_result(2, part(data, task2_orientations))
