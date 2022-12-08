from itertools import product
from typing import Iterable

import numpy as np

from utils import load_data
from utils import print_result


def parse_data(lines: list[str]) -> np.array:
    return np.array([list(map(int, line)) for line in lines])


def determine_visibility(grid: np.array, row: int, col: int) -> bool:
    val = grid[row, col]
    from_top = (val > grid[:row, col]).all()
    from_bottom = (val > grid[row + 1 :, col]).all()
    from_left = (val > grid[row, :col]).all()
    from_right = (val > grid[row, col + 1 :]).all()
    return bool(from_top or from_bottom or from_left or from_right)


def part1(grid: np.array) -> int:
    return sum(
        determine_visibility(grid, row, col)
        for row, col in product(range(grid.shape[0]), range(grid.shape[1]))
    )


def check_direction(current_tree: int, trees: Iterable[int]) -> int:
    count = 0
    for tree in trees:
        count += 1
        if tree >= current_tree:
            break
    return count


def determine_score(grid: np.array, row: int, col: int) -> int:
    current_tree = grid[row, col]
    up_count = check_direction(current_tree, reversed(grid[:row, col]))
    down_count = check_direction(current_tree, grid[row + 1 :, col])
    left_count = check_direction(current_tree, reversed(grid[row, :col]))
    right_count = check_direction(current_tree, grid[row, col + 1 :])
    return up_count * down_count * right_count * left_count


def part2(grid: np.array) -> int:
    return max(
        [
            determine_score(grid, row, col)
            for row, col in product(range(grid.shape[0]), range(grid.shape[1]))
        ]
    )


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    data = parse_data(load_data(False))

    assert part1(example_data) == 21
    print_result(1, part1(data))

    assert part2(example_data) == 8
    print_result(2, part2(data))
