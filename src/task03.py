from typing import List

import numpy as np

from src.utils import load_data, print_result


def task01(array: np.array) -> int:
    most_common = (array.sum(axis=0) / array.shape[0]).round()
    least_common = 1 - most_common
    gamma = int("".join(most_common.astype(int).astype(str)), 2)
    epsilon = int("".join(least_common.astype(int).astype(str)), 2)
    return gamma * epsilon


if __name__ == "__main__":
    example_data = np.array([[int(char) for char in line] for line in load_data(True)])
    data = np.array([[int(char) for char in line] for line in load_data(False)])

    assert task01(example_data) == 198
    print_result(1, task01(data))

    # assert task01(example_data) == 900
    # print_result(2, task01(data))
