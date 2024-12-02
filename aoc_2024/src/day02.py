from utils import load_data
from utils import print_result


def parse(data: list[str]) -> list[list[int]]:
    return [list(map(int, line.split())) for line in data]


def is_safe(line: list[int]) -> bool:
    diffs = set(a - b for a, b in zip(line, line[1:]))
    return diffs.issubset({1, 2, 3}) or diffs.issubset({-1, -2, -3})


def task01(data: list[list[int]]) -> int:
    return sum(is_safe(line) for line in data)


def task02(data: list[list[int]]) -> int:
    return sum(any(is_safe(l[:i] + l[i + 1 :]) for i in range(len(data) - 1)) for l in data)


if __name__ == "__main__":
    example_data = parse(load_data(True))
    data = parse(load_data())

    assert task01(example_data) == 2
    print_result(1, task01(data))

    assert task02(example_data) == 4
    print_result(2, task02(data))
