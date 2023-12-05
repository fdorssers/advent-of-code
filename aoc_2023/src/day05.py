from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import reduce
from itertools import groupby

from more_itertools import chunked

from utils import load_data
from utils import print_result


@dataclass
class SourceDestinationMap:
    destination_range_start: int
    source_range_start: int
    range_length: int

    @staticmethod
    def parse(line: str) -> SourceDestinationMap:
        return SourceDestinationMap(*map(int, line.strip().split()))


def parse_map_lines(lines: list[str]) -> list[SourceDestinationMap]:
    return [SourceDestinationMap.parse(line) for line in lines[1:]]


def parse(data: list[str]) -> tuple[list[int], list[list[SourceDestinationMap]]]:
    seeds = list(map(int, data[0].split(": ")[1].split()))
    almanac_maps = [
        parse_map_lines(list(g)) for key, g in groupby(data[1:], lambda line: not line) if not key
    ]
    return seeds, almanac_maps


##########
# Task 1 #
##########


def convert_number(number: int, sdms: list[SourceDestinationMap]) -> int:
    for sdm in sdms:
        if sdm.source_range_start <= number < sdm.source_range_start + sdm.range_length:
            return number - sdm.source_range_start + sdm.destination_range_start
    return number


def convert_numbers(numbers: list[int], sdms: list[SourceDestinationMap]) -> list[int]:
    return [convert_number(number, sdms) for number in numbers]


def task01(seeds: list[int], almanac: list[list[SourceDestinationMap]]) -> int:
    return min(reduce(lambda a, am: convert_numbers(list(a), am), almanac, seeds))


##########
# Task 2 #
##########


def convert_number_range(
    number_range: tuple[int, int], sdms: list[SourceDestinationMap]
) -> list[tuple[int, int]]:
    queue = deque([number_range])
    result = []
    while queue:
        current = queue.popleft()
        for sdm in sdms:
            if not (
                sdm.source_range_start <= current[0] < sdm.source_range_start + sdm.range_length
            ):
                continue

            new_length = min(current[1], sdm.source_range_start + sdm.range_length - current[0])

            result.append(
                (
                    current[0] - sdm.source_range_start + sdm.destination_range_start,
                    new_length,
                )
            )
            remaining_length = current[1] - new_length
            if remaining_length:
                queue.append((current[0] + new_length, remaining_length))
            break
        else:
            result.append(current)
    return result


def convert_number_ranges(
    number_ranges: list[tuple[int, int]], sdms: list[SourceDestinationMap]
) -> list[tuple[int, int]]:
    new_ranges = []
    for number_range in number_ranges:
        new_ranges.extend(convert_number_range(number_range, sdms))
    return new_ranges


def task02(seeds: list[int], almanac: list[list[SourceDestinationMap]]) -> int:
    number_ranges = list(map(tuple, chunked(seeds, 2)))
    for am in almanac:
        number_ranges = convert_number_ranges(number_ranges, am)
    return int(min(nr[0] for nr in number_ranges))


if __name__ == "__main__":
    example_data = parse(load_data(True))
    data = parse(load_data())

    assert task01(*example_data) == 35
    print_result(1, task01(*data))

    assert task02(*example_data) == 46
    print_result(2, task02(*data))
