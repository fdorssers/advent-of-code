from itertools import groupby

import numpy as np

from utils import load_data
from utils import print_result

PointType = tuple[int, int]
FoldType = tuple[str, int]


def parse_data(lines: list[str]) -> tuple[list[PointType], list[FoldType]]:
    coords_group, folds_group = [
        list(group) for key, group in groupby(lines, lambda x: bool(x)) if key
    ]
    coords = [(int(coord[1]), int(coord[0])) for coord in [c.split(",") for c in coords_group]]
    folds = [(fold[0], int(fold[1])) for fold in [f.split()[-1].split("=") for f in folds_group]]
    return coords, folds


def create_array(points: list[PointType]) -> np.array:
    width = max(p[1] for p in points) + 1
    height = max(p[0] for p in points) + 1
    array = np.full((height, width), 0)
    for point in points:
        array[point] = 1
    return array


def fold_paper(array: np.array, folds: list[FoldType]) -> np.array:
    for direction, line in folds:
        if direction == "y":
            array = array[:line, :] | np.flipud(array[line + 1 :, :])
        if direction == "x":
            array = array[:, :line] | np.fliplr(array[:, line + 1 :])
    return array


def part1(points: list[PointType], folds: list[FoldType]) -> int:
    return int(np.sum(fold_paper(create_array(points), folds)))


def part2(points: list[PointType], folds: list[FoldType]) -> str:
    array = fold_paper(create_array(points), folds).astype(str)
    array[array == "0"] = " "
    array[array == "1"] = "#"
    return "\n".join(["".join(line) for line in array.tolist()])


if __name__ == "__main__":
    example_coords, example_folds = parse_data(load_data(True))
    coords, folds = parse_data(load_data(False))

    assert part1(example_coords, example_folds[:1]) == 17
    print_result(1, part1(coords, folds[:1]))

    print("The result for task 13 part 2 is:")
    print(part2(coords, folds))
