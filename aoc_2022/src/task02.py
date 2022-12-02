from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import cast

from utils import print_result


class Hand(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @staticmethod
    def parse(val: str) -> Hand:
        if val in {"A", "X"}:
            return Hand.ROCK
        elif val in {"B", "Y"}:
            return Hand.PAPER
        elif val in {"C", "Z"}:
            return Hand.SCISSORS
        else:
            raise ValueError(f'Unknown value "{val}"')


def load_task(example: bool = False) -> list[tuple[Hand, Hand]]:
    path = Path(__file__).parent.parent / "data" / f"task02{'_example' if example else ''}.txt"
    with open(path) as f:
        data = f.read().strip().split("\n")
        return cast(
            list[tuple[Hand, Hand]], [tuple(Hand.parse(r) for r in row.split()) for row in data]
        )


WINS = {Hand.ROCK: Hand.SCISSORS, Hand.PAPER: Hand.ROCK, Hand.SCISSORS: Hand.PAPER}
LOSES = {b: a for a, b in WINS.items()}


def task1(matches: list[tuple[Hand, Hand]]) -> int:
    sum_own_hand = 0
    sum_wins = 0
    for match in matches:
        sum_own_hand += match[1].value
        if match[1] == match[0]:
            sum_wins += 3
        elif WINS[match[1]] == match[0]:
            sum_wins += 6
    return sum_own_hand + sum_wins


def task2(matches: list[tuple[Hand, Hand]]) -> int:
    sum_own_hand = 0
    sum_wins = 0
    for match in matches:
        if match[1] == Hand.ROCK:  # lose
            sum_own_hand += WINS[match[0]].value
        elif match[1] == Hand.PAPER:  # draw
            sum_wins += 3
            sum_own_hand += match[0].value
        else:  # win
            sum_wins += 6
            sum_own_hand += LOSES[match[0]].value
    return sum_own_hand + sum_wins


if __name__ == "__main__":
    example_data = load_task(True)
    data = load_task()

    assert task1(example_data) == 15
    print_result(1, task1(data))

    assert task2(example_data) == 12
    print_result(2, task2(data))
