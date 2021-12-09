from itertools import groupby

from utils import load_data
from utils import print_result


def parse_data(lines: list[str]) -> list[list[str]]:
    return [list(v) for k, v in groupby(lines, key=lambda x: bool(x)) if k]


def part1(groups: list[list[str]]) -> int:
    return sum([len({answer for person in group for answer in person}) for group in groups])


def part2(groups: list[list[str]]) -> int:
    return sum([len(set.intersection(*[set(person) for person in group])) for group in groups])


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    data = parse_data(load_data(False))

    assert part1(example_data) == 11
    print_result(1, part1(data))

    assert part2(example_data) == 6
    print_result(2, part2(data))
