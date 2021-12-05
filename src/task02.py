from __future__ import annotations

from dataclasses import dataclass
from typing import List

from src.utils import load_data
from src.utils import print_result


@dataclass
class Command:
    direction: str
    steps: int

    @staticmethod
    def from_line(line: str) -> Command:
        split_line = line.split()
        return Command(split_line[0], int(split_line[1]))


def calculate_movement(commands: List[Command], task_one: bool) -> int:
    depth, depthv2, horizontal, aim = 0, 0, 0, 0
    for command in commands:
        match command:
            case Command(direction="forward", steps=steps):
                horizontal += steps
                depthv2 += aim * steps
            case Command(direction="down", steps=steps):
                depth += steps
                aim += steps
            case Command(direction="up", steps=steps):
                depth -= steps
                aim -= steps
    return (horizontal * depth) if task_one else (horizontal * depthv2)


if __name__ == "__main__":
    example_commands = [Command.from_line(line) for line in load_data(True)]
    commands = [Command.from_line(line) for line in load_data()]

    assert calculate_movement(example_commands, True) == 150
    print_result(1, calculate_movement(commands, True))

    assert calculate_movement(example_commands, False) == 900
    print_result(2, calculate_movement(commands, False))
