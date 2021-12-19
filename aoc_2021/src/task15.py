from heapq import heappop
from heapq import heappush
from typing import Iterator
from typing import NamedTuple

import numpy as np

from utils import load_data
from utils import print_result


class Point(NamedTuple):
    row: int
    col: int


def at_target(point: Point, array: np.array, times: int) -> bool:
    return bool(
        point.row == times * array.shape[0] - 1 and point.col == times * array.shape[1] - 1
    )


def find_neighbours(point: Point, array: np.array, times: int) -> Iterator[Point]:
    height, width = [v * times for v in array.shape]
    for col, row in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        neighbour = Point(point.row + row, point.col + col)
        if (0 <= neighbour[0] < width) and (0 <= neighbour[1] < height):
            yield neighbour


def lowest_risk(array: np.array, times: int) -> int:
    visited = {Point(0, 0)}
    heap = [(0, Point(0, 0))]
    while heap:
        risk_so_far, current_point = heappop(heap)
        if at_target(current_point, array, times):
            return risk_so_far
        for neighbour in find_neighbours(current_point, array, times):
            row_multiple = neighbour.row // array.shape[0]
            col_multiple = neighbour.col // array.shape[1]
            row = neighbour.row % array.shape[0]
            col = neighbour.col % array.shape[1]
            calculated_risk_level = ((array[row, col] + row_multiple + col_multiple) - 1) % 9 + 1
            if neighbour not in visited:
                visited.add(neighbour)
                heappush(heap, (risk_so_far + calculated_risk_level, neighbour))
    raise ValueError("Did not reach target")


if __name__ == "__main__":
    example_data = np.array([[int(char) for char in line] for line in load_data(True)])
    data = np.array([[int(char) for char in line] for line in load_data(False)])

    assert lowest_risk(example_data, 1) == 40
    print_result(1, lowest_risk(data, 1))

    assert lowest_risk(example_data, 5) == 315
    print_result(1, lowest_risk(data, 5))
