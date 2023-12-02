import math

from utils import load_data
from utils import print_result


def parse(data: list[str]) -> list[list[dict[str, int]]]:
    games = []
    for line in data:
        game, choices = line.split(":")
        hand_list = []
        for hand in choices.split(";"):
            hand_dict = {}
            for die in hand.split(","):
                split_die = die.strip().split(" ")
                hand_dict[split_die[-1]] = int(split_die[0])
            hand_list.append(hand_dict)
        games.append(hand_list)
    return games


def task01(data: list[list[dict[str, int]]]) -> int:
    total = {"red": 12, "green": 13, "blue": 14}
    return sum(
        [
            game_num
            for game_num, game in enumerate(data, 1)
            if all([count <= total[color] for hand in game for color, count in hand.items()])
        ]
    )


def task02(data: list[list[dict[str, int]]]) -> int:
    powers = []
    for game in data:
        color_count = {"red": 0, "blue": 0, "green": 0}
        for hand in game:
            for color, count in hand.items():
                color_count[color] = max(count, color_count[color])
        powers.append(math.prod(color_count.values()))
    return sum(powers)


if __name__ == "__main__":
    example_data = parse(load_data(True))
    data = parse(load_data())

    assert task01(example_data) == 8
    print_result(1, task01(data))

    assert task02(example_data) == 2286
    print_result(2, task02(data))
