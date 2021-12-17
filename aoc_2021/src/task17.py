import re
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from typing import Optional

import numpy as np

from utils import load_data
from utils import print_result


@dataclass(frozen=True)
class Target:
    start: tuple[int, int]
    end: tuple[int, int]

    def in_bounds(self, point: tuple[int, int]) -> bool:
        return (self.start[0] <= point[0] <= self.end[0]) and (
            self.end[1] <= point[1] <= self.start[1]
        )

    def impossible(self, point: tuple[int, int]) -> bool:
        return (point[0] > self.end[0]) or (point[1] < self.end[1])


def parse_target(line: str) -> Target:
    line.split(": ")
    start_x, end_x = map(int, re.findall(r"-?\d+", line.split(", ")[0]))
    start_y, end_y = map(int, re.findall(r"-?\d+", line.split(", ")[1]))
    return Target((start_x, end_y), (end_x, start_y))


def determine_trajectory(init_vel: tuple[int, int], target: Target) -> Optional[int]:
    cur_pos = (0, 0)
    cur_vel = init_vel
    highest = 0
    while cur_pos[1] >= target.end[1]:
        cur_pos = (cur_pos[0] + cur_vel[0], cur_pos[1] + cur_vel[1])
        highest = cur_pos[1] if cur_pos[1] > highest else highest
        if target.in_bounds(cur_pos):
            return highest
        if target.impossible(cur_pos):
            return None
        cur_vel = max(0, cur_vel[0] - 1), cur_vel[1] - 1
    return None


@lru_cache()
def find_heights_for_all_trajectories(target: Target) -> list[int]:
    x_velocities = range(0, target.end[0] + 1)
    y_velocities = range(target.end[1], np.abs(target.end[1]))
    return [
        max_height
        for velocity in product(x_velocities, y_velocities)
        if (max_height := determine_trajectory(velocity, target)) is not None
    ]


def part1(target: Target) -> int:
    return max(find_heights_for_all_trajectories(target))


def part2(target: Target) -> int:
    return len(find_heights_for_all_trajectories(target))


if __name__ == "__main__":
    example_data = parse_target(load_data(True)[0])
    data = parse_target(load_data(False)[0])

    assert part1(example_data) == 45
    print_result(1, part1(data))

    assert part2(example_data) == 112
    print_result(1, part2(data))
