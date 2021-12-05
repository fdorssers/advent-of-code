from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from itertools import groupby
from typing import List
from typing import Tuple

import numpy as np

from utils import load_data
from utils import print_result


@dataclass
class Board:
    numbers: np.array
    mask: np.array
    _bingo_marks: int = field(init=False)

    def __post_init__(self) -> None:
        self._bingo_marks = self.numbers.shape[0]

    def mark_number(self, number: int) -> None:
        self.mask = self.mask | (self.numbers == number)

    def has_bingo(self) -> bool:
        return bool(
            (self.mask.sum(axis=0) == self._bingo_marks).any()
            or (self.mask.sum(axis=1) == self._bingo_marks).any()
        )

    def get_unmarked_value(self) -> int:
        return int(self.numbers[~self.mask].sum())

    def reset(self) -> None:
        self.mask = np.full_like(self.numbers, False, dtype=bool)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Board):
            return False
        return bool((self.numbers == o.numbers).all() & (self.mask == o.mask).all())

    @staticmethod
    def parse_strings(lines: List[str]) -> Board:
        array = np.array([[int(val) for val in line.split()] for line in lines])
        return Board(numbers=array, mask=np.full_like(array, False, dtype=bool))


def parse_data(lines: List[str]) -> Tuple[List[int], List[Board]]:
    numbers = [int(val) for val in lines[0].split(",")]
    boards = [
        Board.parse_strings(list(group))
        for key, group in groupby(lines[2:], lambda x: bool(x))
        if key
    ]
    return numbers, boards


def part1(numbers: List[int], boards: List[Board]) -> int:
    for number in numbers:
        for board in boards:
            board.mark_number(number)
            if board.has_bingo():
                return board.get_unmarked_value() * number
    raise ValueError("No solution found")


def part2(numbers: List[int], boards: List[Board]) -> int:
    for number in numbers:
        to_be_removed = []
        for board in boards:
            board.mark_number(number)
            if board.has_bingo():
                if len(boards) == 1:
                    return board.get_unmarked_value() * number
                to_be_removed.append(board)
        for board in to_be_removed:
            boards.remove(board)
    raise ValueError("No solution found")


if __name__ == "__main__":
    example_numbers, example_boards = parse_data(load_data(True))
    numbers, boards = parse_data(load_data(False))

    assert part1(example_numbers, example_boards) == 4512
    print_result(1, part1(numbers, boards))

    for board in example_boards:
        board.reset()
    for board in boards:
        board.reset()

    assert part2(example_numbers, example_boards) == 1924
    print_result(2, part2(numbers, boards))
