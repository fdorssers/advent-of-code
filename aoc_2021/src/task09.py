from itertools import product

import numpy as np

from utils import load_data
from utils import print_result


def part1(array: np.array) -> int:
    mask = np.full_like(array, False, dtype=bool)
    height, width = array.shape
    for i, j in product(range(height), range(width)):
        mask[i, j] = array[max(i - 1, 0) : i + 2, max(j - 1, 0) : j + 2].min() == array[i, j]
    return int((array[mask] + 1).sum())


if __name__ == "__main__":
    example_data = np.array([list(map(int, list(line))) for line in load_data(True)])
    data = np.array([list(map(int, list(line))) for line in load_data(False)])

    assert part1(example_data) == 15
    print_result(1, part1(data))

    # assert part2(example_data) == 61229
    # print_result(2, part2(data))
