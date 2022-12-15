from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from more_itertools import flatten

from utils import load_data
from utils import print_result


def distance(c1: Coord, c2: Coord) -> int:
    return abs(c1.x - c2.x) + abs(c1.y - c2.y)


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


@dataclass
class Sensor:
    coord: Coord
    beacon: Coord

    @property
    def distance_to_beacon(self) -> int:
        return distance(self.coord, self.beacon)

    # @property
    # def covered_points(self):
    #     beacon_distance = self.distance_to_beacon
    #     for x in range(self.coord.x - beacon_distance, self.coord.x + beacon_distance + 1):
    #         for y in range(self.coord.y - beacon_distance, self.coord.y + beacon_distance + 1):
    #             if distance(self.coord, Coord(x, y)) <= beacon_distance:
    #                 yield Coord(x, y)

    # def covered_points_on_line(self, line: int):
    #     beacon_distance = self.distance_to_beacon
    #     if (self.coord.x - beacon_distance) <= line <= (self.coord.x + beacon_distance + 1):
    #         for y in range(self.coord.y - beacon_distance, self.coord.y + beacon_distance + 1):
    #             if distance(self.coord, Coord(line, y)) <= beacon_distance:
    #                 yield Coord(line, y)

    def covered_range_on_line(self, line: int) -> Iterator[tuple[int, int]]:
        beacon_distance = self.distance_to_beacon
        if (self.coord.y - beacon_distance) <= line <= (self.coord.y + beacon_distance):
            x_diff = abs(beacon_distance - abs(self.coord.y - line))
            r = self.coord.x - x_diff, self.coord.x + x_diff
            yield r


def parse_data(lines: list[str]) -> list[Sensor]:
    sensors = []
    for line in lines:
        sensor_part, beacon_part = line.split(": closest beacon is at ")
        sensor_split = sensor_part.split(", ")
        beacon_split = beacon_part.split(", ")
        sensor = Sensor(
            coord=Coord(int(sensor_split[0].split("=")[1]), int(sensor_split[1].split("=")[1])),
            beacon=Coord(int(beacon_split[0].split("=")[1]), int(beacon_split[1].split("=")[1])),
        )
        sensors.append(sensor)
    return sensors


def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    new_lines = []
    slines = sorted(ranges, key=lambda p: p[0])
    new_start, new_end = slines[0]
    for start, end in slines[1:]:
        if start > new_end:
            new_lines.append((new_start, new_end))
            new_start = start
            new_end = end
        else:
            new_end = max(end, new_end)
    new_lines.append((new_start, new_end))
    return new_lines


def split_ranges_by_beacon(
    ranges: list[tuple[int, int]], beacons: list[Coord]
) -> list[tuple[int, int]]:
    beacons = sorted(list(set(beacons)), key=lambda p: p.y)
    new_ranges = []
    for start, end in ranges:
        for beacon in beacons:
            if not (start <= beacon.y <= end):
                continue
            if (beacon.y == start) and (beacon.y == end):
                break
            elif beacon.y == start:
                start += 1
            elif beacon.y == end:
                end -= 1
            else:
                new_ranges.append((start, beacon.y - 1))
                new_ranges.append((beacon.y + 1, end))
                break
    return new_ranges


def part1(sensors: list[Sensor], line: int) -> int:
    lines = flatten(sensor.covered_range_on_line(line) for sensor in sensors)
    merged_lines = merge_ranges(lines)
    split_lines = split_ranges_by_beacon(
        merged_lines,
        [s.beacon for s in sensors if s.beacon.y == line],
    )
    return sum(r[1] - r[0] + 1 for r in split_lines)


def part2(pairs: list[tuple[set[int], set[int]]]) -> int:
    return sum([1 for pair in pairs if pair[0] & pair[1]])


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    data = parse_data(load_data(False))

    assert part1(example_data, 10) == 26
    print_result(1, part1(data, 2000000))

    # assert part2(example_data) == 4
    # print_result(2, part2(data))
