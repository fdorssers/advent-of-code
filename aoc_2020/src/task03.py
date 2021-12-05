import math
from typing import Tuple

import numpy as np

from utils import load_data
from utils import print_result


def tree_counter(array: np.array, slope: Tuple[int, int]) -> int:
    x, y, num_trees = 0, 0, 0
    while y < array.shape[0] - 1:
        x = (x + slope[0]) % array.shape[1]
        y += slope[1]
        num_trees += array[y, x]
    return num_trees


def parse_input(lines: list[str]) -> np.array:
    return np.array([[1 if char == "#" else 0 for char in line] for line in lines])


if __name__ == "__main__":
    example_data = parse_input(load_data(True))
    data = parse_input(load_data(False))

    part1_slope = (3, 1)
    part2_slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    assert tree_counter(example_data, part1_slope) == 7
    print_result(1, tree_counter(data, part1_slope))

    assert math.prod([tree_counter(example_data, slope) for slope in part2_slopes]) == 336
    print_result(2, math.prod([tree_counter(data, slope) for slope in part2_slopes]))
