import re
from collections import defaultdict

from utils import load_data
from utils import print_result


def parse(data: list[str]) -> list[tuple[set[int], set[int]]]:
    cards = []
    for line in data:
        split_line = line.split(": ")[-1].split(" | ")
        cards.append(
            (
                {int(card) for card in re.findall(r"\d+", split_line[0])},
                {int(card) for card in re.findall(r"\d+", split_line[1])},
            )
        )
    return cards


def task01(cards: list[tuple[set[int], set[int]]]) -> int:
    return sum(int(2 ** (len(card[0] & card[1]) - 1)) for card in cards)


def task02(cards: list[tuple[set[int], set[int]]]) -> int:
    card_values = {i + 1: len(card[0] & card[1]) for i, card in enumerate(cards)}
    total_cards = len(cards)
    card_counts = [{i: 1 for i in range(1, total_cards + 1)}]
    while True:
        new_card_counts: dict[int, int] = defaultdict(int)
        for card_number, count in card_counts[-1].items():
            for new_card_number in range(
                card_number + 1, min(card_number + card_values[card_number] + 1, total_cards + 1)
            ):
                if new_card_number > total_cards:
                    continue
                new_card_counts[new_card_number] += count
        if not new_card_counts:
            break
        card_counts.append(new_card_counts)
    return sum(sum(cw.values()) for cw in card_counts)


if __name__ == "__main__":
    example_data = parse(load_data(True))
    data = parse(load_data())

    assert task01(example_data) == 13
    print_result(1, task01(data))

    assert task02(example_data) == 30
    print_result(2, task02(data))
