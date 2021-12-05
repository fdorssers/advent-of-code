from itertools import combinations
from math import prod

from utils import load_data
from utils import print_result


def part(values: list[int], n: int) -> int:
    return next(prod(vals) for vals in combinations(values, n) if sum(vals) == 2020)


if __name__ == "__main__":
    example_data = [int(line) for line in load_data(True)]
    data = [int(line) for line in load_data(False)]

    assert part(example_data, 2) == 514579
    print_result(1, part(data, 2))

    assert part(example_data, 3) == 241861950
    print_result(2, part(data, 3))
