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


@dataclass
class AlmanacMap:
    from_: str
    to: str
    source_destination_maps: list[SourceDestinationMap]

    @staticmethod
    def parse(lines: list[str]) -> AlmanacMap:
        from_, to = lines[0].split()[0].split("-to-")
        maps = [SourceDestinationMap.parse(line) for line in lines[1:]]
        return AlmanacMap(from_, to, maps)

    def convert_number(self, number: int) -> int:
        for sdm in self.source_destination_maps:
            if sdm.source_range_start <= number < sdm.source_range_start + sdm.range_length:
                return number - sdm.source_range_start + sdm.destination_range_start
        return number

    def convert_number_range(self, number_range: tuple[int, int]) -> list[tuple[int, int]]:
        # print(f"    Converting {number_range=}")
        queue = deque([number_range])
        result = []
        while queue:
            #             print(f"      Current queue: {queue}")
            current = queue.popleft()
            found_match = False
            for sdm in self.source_destination_maps:
                if not (
                    sdm.source_range_start
                    <= current[0]
                    < sdm.source_range_start + sdm.range_length
                ):
                    #                     print(
                    #                         f"        ❌ {current=} not in {sdm.source_range_start=}+{sdm.range_length=} (={sdm.source_range_start+sdm.range_length})"
                    #                     )
                    continue
                #                 print(
                #                     f"        ✅ {current=} in {sdm.source_range_start=}+{sdm.range_length=} (={sdm.source_range_start+sdm.range_length})"
                #                 )
                source_start = sdm.source_range_start
                source_length = sdm.range_length
                source_end = source_start + source_length

                destination_start = sdm.destination_range_start

                current_start = current[0]
                current_length = current[1]
                current_end = current[0] + current_length

                new_start = current_start - source_start + destination_start
                new_length = min(current_length, source_end - current_start)

                #                 print(f"          Adding {(new_start, new_length)} to result")
                result.append((new_start, new_length))
                remaining_length = current_length - new_length
                if remaining_length:
                    #                     print(
                    #                         f"          Has remaining length {remaining_length}, adding to queue: {(current_start + new_length, remaining_length)=}"
                    #                     )
                    queue.append((current_start + new_length, remaining_length))
                found_match = True
                break
            if not found_match:
                result.append(current)
        return result

    def convert_number_ranges(self, number_ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
        #         print(f"  Converting number ranges: {number_ranges}")
        new_ranges = []
        for number_range in number_ranges:
            number_range_result = self.convert_number_range(number_range)
            #             print(f"    {number_range=} ==> {number_range_result=}")
            new_ranges.extend(number_range_result)
        return new_ranges

    def convert_numbers(self, numbers: list[int]) -> list[int]:
        return [self.convert_number(number) for number in numbers]


def parse(data: list[str]) -> tuple[list[int], dict[str, AlmanacMap]]:
    seeds = list(map(int, data[0].split(": ")[1].split()))
    almanac_maps = [
        AlmanacMap.parse(list(g)) for key, g in groupby(data[1:], lambda line: not line) if not key
    ]
    return seeds, {almanac_map.from_: almanac_map for almanac_map in almanac_maps}


def task01(seeds: list[int], almanac: dict[str, AlmanacMap]) -> int:
    return min(reduce(lambda a, b: b.convert_numbers(list(a)), almanac.values(), seeds))


def task02(seeds: list[int], almanac: dict[str, AlmanacMap]) -> int:
    number_ranges = list(map(tuple, chunked(seeds, 2)))
    for am in almanac.values():
        #         print(f"📖 Processing {am.from_} ==> {am}")
        number_ranges = am.convert_number_ranges(number_ranges)
    #     print(min(nr[0] for nr in number_ranges))
    return int(min(nr[0] for nr in number_ranges))


if __name__ == "__main__":
    example_data = parse(load_data(True))
    data = parse(load_data())

    assert task01(*example_data) == 35
    print_result(1, task01(*data))

    assert task02(*example_data) == 46
    print_result(2, task02(*data))
