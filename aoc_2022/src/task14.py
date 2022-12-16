import re

import numpy as np
from more_itertools import sliding_window

from utils import load_data
from utils import print_result


def generate_points(start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    if start[0] == end[0]:
        return [(start[0], i) for i in range(min(start[1], end[1]), max(start[1], end[1]) + 1)]
    elif start[1] == end[1]:
        return [(i, start[1]) for i in range(min(start[0], end[0]), max(start[0], end[0]) + 1)]
    else:
        raise ValueError(f"Diagonal points")


def parse_data(lines: list[str]) -> list[tuple[set[int], set[int]]]:
    line_coords: list[list[tuple[int, int]]] = [
        [tuple(map(int, part.split(","))) for part in line.split("->")] for line in lines
    ]
    print(line_coords)

    rock_coords = []
    for line_coord in line_coords:
        for start, end in sliding_window(line_coord, 2):
            rock_coords.extend(generate_points(start, end))

    min_x = min(p[0] for p in rock_coords)
    max_x = max(p[0] for p in rock_coords)
    min_y = min(p[1] for p in rock_coords)
    min_y = max(p[1] for p in rock_coords)

    np.zeros(())

    # pairs = []
    # for line in lines:
    #     a, b, c, d = [int(val) for val in re.findall(r"\d+", line)]
    #     pairs.append((set(range(a, b + 1)), set(range(c, d + 1))))
    return


def part1(pairs: list[tuple[set[int], set[int]]]) -> int:
    return sum([1 for pair in pairs if not (pair[0] - pair[1]) or not (pair[1] - pair[0])])


def part2(pairs: list[tuple[set[int], set[int]]]) -> int:
    return sum([1 for pair in pairs if pair[0] & pair[1]])


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    # data = parse_data(load_data(False))
    #
    # assert part1(example_data) == 2
    # print_result(1, part1(data))
    #
    # assert part2(example_data) == 4
    # print_result(2, part2(data))
