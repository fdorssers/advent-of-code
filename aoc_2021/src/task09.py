import math
from collections import deque
from itertools import product
from typing import Iterator

import numpy as np

from utils import load_data
from utils import print_result


def find_minima(array: np.array) -> Iterator[tuple[int, int]]:
    height, width = array.shape
    for row, col in product(range(height), range(width)):
        if array[max(row - 1, 0) : row + 2, max(col - 1, 0) : col + 2].min() == array[row, col]:
            yield row, col


def part1(array: np.array) -> int:
    return sum(array[point] + 1 for point in find_minima(array))


def find_neighbours(point: tuple[int, int], array: np.array) -> Iterator[tuple[int, int]]:
    height, width = array.shape
    for col, row in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        new_point = (point[0] + row, point[1] + col)
        if (0 <= new_point[1] < width) and (0 <= new_point[0] < height):
            yield new_point


def is_part_of_basin(
    current: tuple[int, int], neighbour: tuple[int, int], array: np.array
) -> bool:
    return bool((array[current] < array[neighbour]) and (array[neighbour] < 9))


def find_basin(point: tuple[int, int], array: np.array) -> set[tuple[int, int]]:
    basin = {point}
    queue = deque([point])
    while queue:
        current_point = queue.popleft()
        for neighbour in find_neighbours(current_point, array):
            if is_part_of_basin(current_point, neighbour, array):
                basin.add(neighbour)
                queue.append(neighbour)
    return basin


def part2(array: np.array) -> int:
    basins = [find_basin(minimum, array) for minimum in find_minima(array)]
    return math.prod(sorted([len(basin) for basin in basins])[-3:])


if __name__ == "__main__":
    example_data = np.array([list(map(int, list(line))) for line in load_data(True)])
    data = np.array([list(map(int, list(line))) for line in load_data(False)])

    assert part1(example_data) == 15
    print_result(1, part1(data))

    assert part2(example_data) == 1134
    print_result(2, part2(data))
