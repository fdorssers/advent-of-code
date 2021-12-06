from typing import List

from utils import load_data
from utils import print_result


def determine_position(data: str, lchar: str, uchar: str, upper: int) -> int:
    lower = 0
    for char in data:
        diff = upper - lower
        if char == lchar:
            upper = upper - round(diff / 2)
        elif char == uchar:
            lower = lower + round(diff / 2)
    return lower if lchar else upper


def calculate_seat_ids(passes: List[str]) -> List[int]:
    seat_ids = []
    for p in passes:
        row = determine_position(p[:7], "F", "B", 128)
        col = determine_position(p[7:], "L", "R", 8)
        seat_ids.append(row * 8 + col)
    return seat_ids


def part1(passes: List[str]) -> int:
    return max(calculate_seat_ids(passes))


def part2(passes: List[str]) -> int:
    seat_ids = sorted(calculate_seat_ids(passes))
    for a, b in zip(seat_ids[1:], seat_ids[2:]):
        if b - a > 1:
            return a + 1
    raise ValueError("Found nothing")


if __name__ == "__main__":
    example_data = load_data(True)
    data = load_data(False)

    assert part1(example_data) == 820
    print_result(1, part1(data))

    print_result(2, part2(data))
