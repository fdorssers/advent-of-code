from __future__ import annotations

from collections import Counter
from collections import defaultdict
from typing import Dict

from utils import load_data
from utils import print_result


def count_fishes(fishes: Dict[int, int], days: int) -> int:
    for _ in range(days):
        new_dict = defaultdict(lambda: 0)
        for new_day in range(0, 9):
            if new_day == 8:
                new_dict[new_day] = fishes[0]
            elif new_day == 6:
                new_dict[new_day] = fishes[7] + fishes[0]
            else:
                new_dict[new_day] = fishes[new_day + 1]
        fishes = new_dict
    return sum(fishes.values())


if __name__ == "__main__":
    example_data = defaultdict(lambda: 0, Counter(map(int, load_data(True)[0].split(","))))
    data = defaultdict(lambda: 0, Counter(map(int, load_data(False)[0].split(","))))

    assert count_fishes(example_data.copy(), 80) == 5934
    print_result(1, count_fishes(data.copy(), 80))

    assert count_fishes(example_data.copy(), 256) == 26984457539
    print_result(1, count_fishes(data.copy(), 256))
