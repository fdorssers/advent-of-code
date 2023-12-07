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

    def type_no_joker(self) -> int:
        card_counts = Counter(self.hand)
        count_counter = Counter(card_counts.values())
        if (4 in count_counter) or (5 in count_counter):
            return max(count_counter) + 2
        if (3 in count_counter) and (2 in count_counter):
            return 5
        if 3 in count_counter:
            return 4
        if (2 in count_counter) and (count_counter[2] == 2):
            return 3
        if 2 in count_counter:
            return 2
        return 1

    def type_with_joker(self) -> int:
        card_counts = Counter(self.hand)
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

    @lru_cache
    def type(self) -> int:
        if self.joker_rule:
            return self.type_with_joker()
        else:
            return self.type_no_joker()

    def __lt__(self, other: HandAndBid) -> bool:
        if self.type() == other.type():
            for l, r in zip(self.hand, other.hand):
                if self.joker_rule:
                    l_v, r_v = JOKER_CARD_RANKINGS[l], JOKER_CARD_RANKINGS[r]
                    if l_v == r_v:
                        continue
                    return l_v < r_v
                else:
                    l_v, r_v = CARD_RANKINGS[l], CARD_RANKINGS[r]
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
