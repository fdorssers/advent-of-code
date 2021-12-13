from collections import deque
from itertools import count
from itertools import product
from typing import Iterator

import numpy as np

from utils import load_data
from utils import print_result


def find_flash_locations(grid: np.array) -> list[tuple[int, int]]:
    return list(zip(*np.where(grid == 10)))


def find_neighbours_incl_self(point: tuple[int, int], array: np.array) -> list[tuple[int, int]]:
    neighbours = []
    height, width = array.shape
    for col, row in product([-1, 0, 1], [-1, 0, 1]):
        new_point = (point[0] + row, point[1] + col)
        if (0 <= new_point[1] < width) and (0 <= new_point[0] < height):
            neighbours.append(new_point)
    return neighbours


def create_mask(points: list[tuple[int, int]], shape: tuple[int, int]) -> np.array:
    mask = np.full(shape, False, bool)
    for row, col in points:
        mask[row, col] = True
    return mask


def find_new_10s(points: list[tuple[int, int]], grid: np.array) -> Iterator[tuple[int, int]]:
    for neighbour in points:
        if grid[neighbour] == 10:
            yield neighbour


def flash(grid: np.array) -> np.array:
    flash_locations = deque(find_flash_locations(grid))
    while flash_locations:
        flash_location = flash_locations.popleft()
        neighbours = find_neighbours_incl_self(flash_location, grid)
        neighbour_mask = create_mask(neighbours, grid.shape)
        grid[neighbour_mask] += 1
        flash_locations.extend(find_new_10s(neighbours, grid))
    return grid


def part1(grid: np.array) -> int:
    flash_count = 0
    for i in range(100):
        grid += 1
        grid = flash(grid)
        flash_count += (grid >= 10).sum()
        grid[grid >= 10] = 0
    return flash_count


def part2(grid: np.array) -> int:
    for i in count(start=0):
        grid += 1
        grid = flash(grid)
        if (grid >= 10).sum() == 100:
            return i + 1
        grid[grid >= 10] = 0
    raise ValueError("No synchronized flash found")


if __name__ == "__main__":
    example_data = np.array([list(map(int, list(line))) for line in load_data(True)])
    data = np.array([list(map(int, list(line))) for line in load_data(False)])

    assert part1(example_data.copy()) == 1656
    print_result(1, part1(data.copy()))

    assert part2(example_data.copy()) == 195
    print_result(2, part2(data.copy()))
