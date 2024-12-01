from collections import Counter

from utils import load_data
from utils import print_result


def parse(data: list[str]) -> tuple[list[int], list[int]]:
    l1, l2 = [], []
    for line in data:
        split = line.split()
        l1.append(int(split[0]))
        l2.append(int(split[1]))
    return l1, l2


def task01(data: tuple[list[int], list[int]]) -> int:
    return sum(abs(comb[0] - comb[1]) for comb in zip(sorted(data[0]), sorted(data[1])))


def task02(data: tuple[list[int], list[int]]) -> int:
    multi = Counter(data[1])
    return sum(val * multi[val] for val in data[0])


if __name__ == "__main__":
    example_data = parse(load_data(True))
    data = parse(load_data())

    assert task01(example_data) == 11
    print_result(1, task01(data))

    assert task02(example_data) == 31
    print_result(2, task02(data))
