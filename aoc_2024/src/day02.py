from utils import load_data
from utils import print_result


def parse(data: list[str]) -> list[list[int]]:
    return [list(map(int, line.split())) for line in data]


def is_safe(line: list[int]) -> bool:
    diffs = [a - b for a, b in zip(line, line[1:])]
    if not (all(diff > 0 for diff in diffs) or all(diff < 0 for diff in diffs)):
        return False
    return all(0 <= abs(val) <= 3 for val in diffs)


def task01(data: list[list[int]]) -> int:
    return sum([is_safe(line) for line in data])


def task02(data: list[list[int]]) -> int:
    return sum(
        any(is_safe(line[:num] + line[num + 1 :]) for num in range(len(data) - 1)) for line in data
    )


if __name__ == "__main__":
    example_data = parse(load_data(True))
    data = parse(load_data())

    assert task01(example_data) == 2
    print_result(1, task01(data))

    assert task02(example_data) == 4
    print_result(2, task02(data))
