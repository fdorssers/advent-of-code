from typing import List

from more_itertools import sliding_window as window

from utils import load_data
from utils import print_result


def increase_count(values: List[int], win_size: int = 1) -> int:
    return sum([w2 > w1 for w1, w2 in window([sum(win) for win in window(values, win_size)], 2)])


if __name__ == "__main__":
    example_data = [int(val) for val in load_data(True)]
    data = [int(val) for val in load_data()]

    assert increase_count(example_data) == 7
    print_result(1, increase_count(data))

    assert increase_count(example_data, win_size=3) == 5
    print_result(2, increase_count(data, win_size=3))
