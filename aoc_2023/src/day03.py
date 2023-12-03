import math
from collections import defaultdict

from utils import load_data
from utils import print_result


def is_adjacent(x: int, y: int, data: list[str]) -> bool:
    y_diff = (-1, 0, 1)
    x_diff = (-1, 0, 1)
    for x_d in x_diff:
        for y_d in y_diff:
            if (x_d == 0) and (y_d == 0):
                continue
            x_new = x + x_d
            y_new = y + y_d
            if (x_new < 0) or (y_new < 0):
                continue
            if (x_new >= len(data[y])) or (y_new >= len(data)):
                continue

            if y_d == 0:
                if not data[y_new][x_new].isdigit() and (data[y_new][x_new] != "."):
                    return True
            else:
                if data[y_new][x_new] != ".":
                    return True
    return False


def is_adjacent_to_star(x: int, y: int, data: list[str]) -> set[tuple[int, int]]:
    gear_coords = set()
    y_diff = (-1, 0, 1)
    x_diff = (-1, 0, 1)
    for x_d in x_diff:
        for y_d in y_diff:
            if x_d == 0 and y_d == 0:
                continue
            x_new = x + x_d
            y_new = y + y_d
            if (x_new < 0) or (y_new < 0):
                continue
            if (x_new >= len(data[y])) or (y_new >= len(data)):
                continue

            if data[y_new][x_new] == "*":
                gear_coords.add((x_new, y_new))

    return gear_coords


def task(data: list[str], task: int) -> int:
    chars = []
    adjacent_chars = []

    gears: dict[tuple[int, int], list[int]] = defaultdict(list)

    for y, line in enumerate(data):
        cur_char = ""
        cur_char_adjacent = False

        cur_gear_coords = set()

        for x, char in enumerate(line):
            if char.isdigit():
                cur_char += char
                cur_char_adjacent |= is_adjacent(x, y, data)
                cur_gear_coords.update(is_adjacent_to_star(x, y, data))
            else:
                if cur_char:
                    chars.append(int(cur_char))
                    if cur_char_adjacent:
                        adjacent_chars.append(int(cur_char))
                        for cgc in cur_gear_coords:
                            gears[cgc] += [int(cur_char)]
                    cur_char = ""
                    cur_char_adjacent = False
                    cur_gear_coords = set()
        if cur_char:
            chars.append(int(cur_char))
            if cur_char_adjacent:
                adjacent_chars.append(int(cur_char))
                for cgc in cur_gear_coords:
                    gears[cgc] += [int(cur_char)]
    gear_ratios = []
    for gear, nums in gears.items():
        if len(nums) > 1:
            gear_ratios.append(math.prod(nums))
    return sum(adjacent_chars) if task == 1 else sum(gear_ratios)


if __name__ == "__main__":
    example_data = load_data(True)
    data = load_data()

    assert task(example_data, 1) == 4361
    print_result(1, task(data, 1))

    assert task(example_data, 2) == 467835
    print_result(2, task(data, 2))
