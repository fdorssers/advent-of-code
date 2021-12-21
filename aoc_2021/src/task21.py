from itertools import cycle
from typing import Iterator

from utils import load_data
from utils import print_result


def parse_positions(lines: list[str]) -> tuple[int, int]:
    return int(lines[0][-1]), int(lines[1][-1])


def roll3(die: Iterator[int]) -> int:
    return sum([next(die), next(die), next(die)])


def update(position: int, roll: int) -> int:
    return (position + roll) - (((position + roll) - 1) // 10) * 10


def part(positions: tuple[int, int]) -> int:
    pos_dict = {0: positions[0], 1: positions[1]}
    score_dict = {0: 0, 1: 0}
    die = cycle(range(1, 101))
    for rolls, player in enumerate(cycle([0, 1])):
        pos_dict[player] = update(pos_dict[player], roll3(die))
        score_dict[player] += pos_dict[player]
        if score_dict[player] >= 1000:
            return min(score_dict.values()) * (rolls + 1) * 3
    raise ValueError("Unexpected break from loop")


if __name__ == "__main__":
    example_positions = parse_positions(load_data(True))
    actual_positions = parse_positions(load_data(False))

    assert part(example_positions) == 739785
    print_result(1, part(actual_positions))

    # assert part(example_algo_inp, example_image_inp, 50) == 3351
    # print_result(1, part(algo_inp, image_inp, 50))
