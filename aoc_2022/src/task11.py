from collections import defaultdict
from copy import deepcopy
from typing import Optional

import numpy as np
from more_itertools import chunked

from utils import load_data
from utils import print_result


class Monkey:
    def __init__(
        self,
        items: list[int],
        operation: str,
        test_value: int,
        throw_to: dict[bool, int],
    ):
        self._items = items
        self._operation = operation
        self._test_value = test_value
        self._throw_to = throw_to
        self._inspect_count = 0

    def process_items(self, cap: Optional[int] = None) -> dict[int, list[int]]:
        throws: dict[int, list[int]] = defaultdict(list)
        for item in self._items:
            self._inspect_count += 1
            worry = eval(self._operation, {"old": item})
            if not cap:
                worry = worry // 3
            else:
                worry = worry % cap
            throws[self._throw_to[(worry % self._test_value) == 0]].append(worry)
        self._items = []
        return throws

    def give_items(self, items: list[int]) -> None:
        self._items.extend(items)

    @property
    def test_value(self) -> int:
        return self._test_value

    @property
    def inspect_count(self) -> int:
        return self._inspect_count


def parse_data(lines: list[str]) -> dict[int, Monkey]:
    return {
        int(chunk[0].strip().split()[1][:-1]): Monkey(
            items=[int(v.strip()) for v in chunk[1].strip().split(":")[1].split(",")],
            operation=chunk[2].split(":")[1].split("=")[1].strip(),
            test_value=int(chunk[3].split("by")[1].strip()),
            throw_to={
                True: int(chunk[4].split("monkey")[1].strip()),
                False: int(chunk[5].split("monkey")[1].strip()),
            },
        )
        for chunk in chunked(lines, 7)
    }


def part(monkeys: dict[int, Monkey], p1: bool = True) -> int:
    cap = None if p1 else np.prod(list(m.test_value for _, m in monkeys.items()))
    rounds = 20 if p1 else 10_000
    for _ in range(rounds):
        for _, monkey in monkeys.items():
            throws = monkey.process_items(cap)
            for monkey_num, items in throws.items():
                monkeys[monkey_num].give_items(items)
    return int(np.prod(sorted([m.inspect_count for _, m in monkeys.items()], reverse=True)[:2]))


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    data = parse_data(load_data(False))

    assert part(deepcopy(example_data)) == 10605
    print_result(1, part(deepcopy(data)))

    assert part(deepcopy(example_data), p1=False) == 2713310158
    print_result(2, deepcopy(part(data, p1=False)))
