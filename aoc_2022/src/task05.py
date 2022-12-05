import copy
import re
from collections import defaultdict
from typing import NamedTuple

from utils import load_data
from utils import print_result


Step = NamedTuple("Step", [("move_", int), ("from_", int), ("to_", int)])


def parse_data(
    lines: list[str],
) -> tuple[dict[int, list[str]], list[Step]]:
    file_split_index = lines.index("")
    box_lines = lines[:file_split_index]
    step_lines = lines[file_split_index + 1 :]

    stack: dict[int, list[str]] = defaultdict(list)
    for line in box_lines[:-1][::-1]:
        for col_num, col_ind in enumerate(range(1, len(line), 4), 1):
            if char := line[col_ind].strip():
                stack[col_num].append(char)
    parsed_steps = [Step(*[int(val) for val in re.findall(r"\d+", line)]) for line in step_lines]
    return stack, parsed_steps


def part1(stack: dict[int, list[str]], steps: list[Step]) -> str:
    for step in steps:
        to_move = stack[step.from_][-step.move_ :]
        stack[step.from_] = stack[step.from_][: -step.move_]
        stack[step.to_] = stack[step.to_] + to_move[::-1]
    return "".join(v[-1] for k, v in stack.items())


def part2(stack: dict[int, list[str]], steps: list[Step]) -> str:
    for step in steps:
        to_move = stack[step.from_][-step.move_ :]
        stack[step.from_] = stack[step.from_][: -step.move_]
        stack[step.to_] = stack[step.to_] + to_move
    return "".join(v[-1] for k, v in stack.items())


if __name__ == "__main__":
    example_stack, example_steps = parse_data(load_data(True))
    stack, steps = parse_data(load_data(False))

    assert part1(copy.deepcopy(example_stack), example_steps) == "CMZ"
    print_result(1, part1(copy.deepcopy(stack), steps))

    assert part2(copy.deepcopy(example_stack), example_steps) == "MCD"
    print_result(1, part2(copy.deepcopy(stack), steps))
