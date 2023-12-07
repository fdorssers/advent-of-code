from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache

from utils import load_data
from utils import print_result

CARD_RANKINGS = {c: r for r, c in enumerate("23456789TJQKA")}
JOKER_CARD_RANKINGS = {c: r for r, c in enumerate("J23456789TQKA")}


@dataclass(frozen=True)
class HandAndBid:
    hand: str
    bid: int
    joker_rule: bool

    @staticmethod
    def parse(line: str, joker_rule: bool) -> HandAndBid:
        split = line.split()
        return HandAndBid(split[0], int(split[-1]), joker_rule)

    @lru_cache
    def type(self) -> int:
        card_counts = Counter(self.hand)
        joker_count = 0
        if self.joker_rule:
            joker_count = card_counts["J"]
            del card_counts["J"]
        count_counter = Counter(card_counts.values())
        if (joker_count == 5) or (max(count_counter) + joker_count == 5):
            return 7
        if max(count_counter) + joker_count == 4:
            return 6
        if sum(sorted(card_counts.values(), reverse=True)[:2]) + joker_count == 5:
            return 5
        if max(count_counter) + joker_count == 3:
            return 4
        if sum(sorted(card_counts.values(), reverse=True)[:2]) + joker_count == 4:
            return 3
        if max(count_counter) + joker_count == 2:
            return 2
        return 1

    def __lt__(self, other: HandAndBid) -> bool:
        card_ranking = JOKER_CARD_RANKINGS if self.joker_rule else CARD_RANKINGS
        if self.type() == other.type():
            for l, r in zip(self.hand, other.hand):
                l_v, r_v = card_ranking[l], card_ranking[r]
                if l_v == r_v:
                    continue
                return l_v < r_v
        return self.type() < other.type()


def parse(data: list[str], joker_rule: bool) -> list[HandAndBid]:
    return [HandAndBid.parse(line, joker_rule) for line in data]


def task01(hands: list[HandAndBid]) -> int:
    return sum([rank * hand.bid for rank, hand in enumerate(sorted(hands), 1)])


def task02(hands: list[HandAndBid]) -> int:
    return sum([rank * hand.bid for rank, hand in enumerate(sorted(hands), 1)])


if __name__ == "__main__":
    example_data = load_data(True)
    data = load_data()

    assert task01(parse(example_data, False)) == 6440
    print_result(1, task01(parse(data, False)))

    assert task02(parse(example_data, True)) == 5905
    print_result(2, task02(parse(data, True)))
