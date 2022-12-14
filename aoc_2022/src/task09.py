from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from utils import load_data
from utils import print_result


@dataclass
class Command:
    direction: str
    steps: int


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)


DIRECTIONS = {"U": Point(0, 1), "D": Point(0, -1), "L": Point(-1, 0), "R": Point(1, 0)}


class State:
    head: Point = Point(0, 0)
    tail: Point = Point(0, 0)
    visited: set[Point] = {Point(0, 0)}

    @staticmethod
    def _is_connected(diff: Point) -> bool:
        return (abs(diff.x) <= 1) and (abs(diff.y) <= 1)

    def process_command(self, command: Command) -> None:
        print(f"Processing command: {command}")
        for _ in range(command.steps):
            self.head += DIRECTIONS[command.direction]
            # print(f"Head: {self.head}")
            # print(f"Tail before: {self.tail}")
            diff = self.head - self.tail
            if not self._is_connected(diff):
                if (abs(diff.x) == 2) and (-1 <= diff.y <= 1):
                    self.tail += Point(np.sign(diff.x), diff.y)
                # if (diff.x == 2) and (-1 <= diff.y <= 1):
                # print(f"Moving right")
                # self.tail += Point(1, diff.y)
                # elif (diff.x == -2) and (-1 <= diff.y <= 1):
                # print(f"Moving left")
                # self.tail += Point(-1, diff.y)

                elif (-1 <= diff.x <= 1) and (abs(diff.y) == 2):
                    self.tail += Point(diff.x, np.sign(diff.y))
                # elif (-1 <= diff.x <= 1) and (diff.y == 2):
                # print(f"Moving up")
                # self.tail += Point(diff.x, 1)
                # elif (-1 <= diff.x <= 1) and (diff.y == -2):
                # print(f"Moving down")
                # self.tail += Point(diff.x, -1)
                else:
                    raise ValueError(f"Unsupported diff: {diff}")
                # if self.head.x == self.tail.x:
                #     self.tail = self.tail + Point(0, -np.sign())
                # print(f"Tail after: {self.tail}")
            self.visited.add(self.tail)
            # print()


def parse_data(lines: list[str]) -> list[Command]:
    return [Command(line.split()[0], int(line.split()[1])) for line in lines]


def part1(commands: list[Command]) -> int:
    board = State()
    for command in commands:
        board.process_command(command)
    # print(board.visited)
    return len(board.visited)


def part2(pairs: list[tuple[set[int], set[int]]]) -> int:
    # return sum([1 for pair in pairs if pair[0] & pair[1]])
    return 0


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    data = parse_data(load_data(False))

    # Output: 6193
    # Required: 6181

    assert part1(example_data) == 13
    print_result(1, part1(data))
    #
    # assert part2(example_data) == 4
    # print_result(2, part2(data))
