import re
from dataclasses import dataclass
from itertools import product
from typing import Optional

from utils import load_data
from utils import print_result


@dataclass
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


def add_tuple(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return t1[0] + t2[0], t1[1] + t2[1]


def apply_drag(velocity: tuple[int, int]) -> tuple[int, int]:
    new_y_val = velocity[1] - 1
    if velocity[0] == 0:
        return velocity[0], new_y_val
    elif velocity[0] > 0:
        return velocity[0] - 1, new_y_val
    else:
        return velocity[0] + 1, new_y_val


def determine_trajectory(initial_velocity: tuple[int, int], target: Target) -> Optional[int]:
    current_position = (0, 0)
    current_velocity = initial_velocity
    highest = 0
    while (current_velocity[0] > 0) or (current_position[1] >= target.end[1]):
        current_position = add_tuple(current_position, current_velocity)
        highest = current_position[1] if current_position[1] > highest else highest
        if target.in_bounds(current_position):
            return highest
        if target.impossible(current_position):
            return None
        current_velocity = apply_drag(current_velocity)
    return None


def part1(target: Target) -> int:
    x_velocities = range(0, target.end[0])
    y_velocities = range(target.end[1], 1000)
    results = [
        max_height
        for velocity in product(x_velocities, y_velocities)
        if (max_height := determine_trajectory(velocity, target))
    ]
    return max(results)


if __name__ == "__main__":
    example_data = parse_target(load_data(True)[0])
    data = parse_target(load_data(False)[0])

    assert part1(example_data) == 45
    print_result(1, part1(data))

    # assert cheapest_fuel(example_data, p2_calc) == 168
    # print_result(1, cheapest_fuel(data, p2_calc))
