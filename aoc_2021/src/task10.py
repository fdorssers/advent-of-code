from collections import deque
from functools import reduce
from typing import Optional

from utils import load_data
from utils import print_result

CLOSING_BRACKETS = {")": "(", "]": "[", "}": "{", ">": "<"}
INV_CLOSING_BRACKETS = {v: k for k, v in CLOSING_BRACKETS.items()}


def detect_corruption(line: str) -> Optional[str]:
    bracket_queue: deque[str] = deque()
    for char in line:
        if char in CLOSING_BRACKETS:
            if not CLOSING_BRACKETS[char] == bracket_queue.pop():
                return char
        else:
            bracket_queue.append(char)
    return None


def part1(lines: list[str]) -> int:
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    return sum(points[corruption] for line in lines if (corruption := detect_corruption(line)))


def create_unclosed_list(line: str) -> list[str]:
    bracket_queue: deque[str] = deque()
    for char in line:
        if char in CLOSING_BRACKETS:
            bracket_queue.pop()
        else:
            bracket_queue.append(char)
    return list(bracket_queue)


def autocomplete(line: str) -> list[str]:
    return [INV_CLOSING_BRACKETS[char] for char in create_unclosed_list(line)[::-1]]


def calculate_score(closing_brackets: list[str]) -> int:
    points = {")": 1, "]": 2, "}": 3, ">": 4}
    return reduce(lambda a, b: a * 5 + points[b], closing_brackets, 0)


def part2(lines: list[str]) -> int:
    relevant_lines = [line for line in lines if not detect_corruption(line)]
    scores = sorted([calculate_score(autocomplete(line)) for line in relevant_lines])
    return scores[round(len(scores) / 2)]


if __name__ == "__main__":
    example_data = load_data(True)
    data = load_data(False)

    assert part1(example_data) == 26397
    print_result(1, part1(data))

    assert part2(example_data) == 288957
    print_result(2, part2(data))
