import numpy as np

from utils import load_data
from utils import print_result


def parse(data: list[str]) -> list[list[int]]:
    return [list(map(int, line.split())) for line in data]


def process_history(history: list[int]) -> int:
    histories = [history]
    while True:
        new_step = list(np.diff(histories[-1]))
        histories.append(new_step)
        if not any(new_step):
            break
    to_add = 0
    for hist in histories[::-1]:
        to_add = hist[-1] + to_add
    return to_add


def task01(data: list[list[int]]) -> int:
    return sum(process_history(history) for history in data)


def task02(data: list[list[int]]) -> int:
    reversed_data = [history[::-1] for history in data]
    return sum(process_history(history) for history in reversed_data)


if __name__ == "__main__":
    example_data = parse(load_data(True))
    data = parse(load_data())

    assert task01(example_data) == 114
    print_result(1, task01(data))

    assert task02(example_data) == 2
    print_result(2, task02(data))
