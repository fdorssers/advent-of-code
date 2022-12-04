import re

from utils import load_data
from utils import print_result


def parse_data(lines: list[str]) -> list[tuple[set[int], set[int]]]:
    pairs = []
    for line in lines:
        a, b, c, d = [int(val) for val in re.findall(r"\d+", line)]
        pairs.append((set(range(a, b + 1)), set(range(c, d + 1))))
    return pairs


def part1(pairs: list[tuple[set[int], set[int]]]) -> int:
    return sum([1 for pair in pairs if not (pair[0] - pair[1]) or not (pair[1] - pair[0])])


def part2(pairs: list[tuple[set[int], set[int]]]) -> int:
    return sum([1 for pair in pairs if pair[0] & pair[1]])


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    data = parse_data(load_data(False))

    assert part1(example_data) == 2
    print_result(1, part1(data))

    assert part2(example_data) == 4
    print_result(2, part2(data))
