from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from functools import partial

from joblib import Parallel
from joblib import delayed
from tqdm import tqdm

from utils import load_data
from utils import print_result


@dataclass(frozen=True, slots=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other: Coordinate) -> Coordinate:
        return Coordinate(self.x + other.x, self.y + other.y)


@dataclass
class MazeData:
    position: Coordinate
    direction: Direction
    size: tuple[int, int]
    blocks: set[Coordinate]
    history: list[Coordinate] = field(init=False)
    history_with_direction: list[tuple[Coordinate, Direction]] = field(init=False)

    def __post_init__(self) -> None:
        self.history = []
        self.history_with_direction = []


class Direction(Enum):
    UP = Coordinate(0, -1)
    DOWN = Coordinate(0, 1)
    LEFT = Coordinate(-1, 0)
    RIGHT = Coordinate(1, 0)

    def rotate(self) -> Direction:
        if self == Direction.UP:
            return Direction.RIGHT
        elif self == Direction.RIGHT:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.LEFT
        elif self == Direction.LEFT:
            return Direction.UP
        else:
            raise ValueError(f"Unknown direction: {self}")


def parse(data: list[str]) -> MazeData:
    position = None
    blocks = set()
    size = len(data[0]), len(data)
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char == "^":
                position = Coordinate(j, i)
            elif char == "#":
                blocks.add(Coordinate(j, i))
    if position is None:
        raise ValueError("No starting position found")

    return MazeData(position, Direction.UP, size, blocks)


def in_area(data: MazeData) -> bool:
    return 0 <= data.position.x < data.size[0] and 0 <= data.position.y < data.size[1]


def is_blocked(data: MazeData) -> bool:
    return data.position + data.direction.value in data.blocks


def move(data: MazeData) -> None:
    while is_blocked(data):
        data.direction = data.direction.rotate()
    data.position += data.direction.value


def walk_path(data: MazeData) -> MazeData:
    data = dataclasses.replace(data)
    while in_area(data):
        data.history.append(data.position)
        move(data)
    return data


def task01(data: MazeData) -> int:
    data = walk_path(data)
    print(data)
    return len(set(data.history))


def copy(data: MazeData) -> MazeData:
    return MazeData(
        position=data.position,
        direction=data.direction,
        size=data.size,
        blocks=data.blocks.copy(),
    )


def determine_loop(data: MazeData, block: Coordinate) -> int:
    data = copy(data)
    data.blocks.add(block)
    while in_area(data):
        current = (data.position, data.direction)
        if current in data.history_with_direction:
            return 1
        data.history_with_direction.append((data.position, data.direction))
        move(data)
    return 0


def task02(data: MazeData) -> int:
    walked_path = walk_path(copy(data)).history
    partial_method = partial(determine_loop, copy(data))
    result = Parallel(n_jobs=-1)(
        delayed(partial_method)(loc) for loc in tqdm(set(walked_path) - {data.position})
    )
    return sum(result)


if __name__ == "__main__":
    example_data = parse(load_data(True))
    data = parse(load_data())

    assert task01(example_data) == 41
    print_result(1, task01(data))

    assert task02(example_data) == 6
    print_result(2, task02(data))
