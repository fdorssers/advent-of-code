import math

from utils import load_data
from utils import print_result


def parse(data: list[str]) -> list[tuple[int, int]]:
    times = map(int, data[0].split()[1:])
    distances = map(int, data[1].split()[1:])
    return list(zip(times, distances))


def parse2(data: list[str]) -> tuple[int, int]:
    time = int("".join(data[0].split()[1:]))
    distance = int("".join(data[1].split()[1:]))
    return time, distance


def find_options(time: int, distance: int) -> int:
    return len([i for i in range(time) if (time - i) * i > distance])


def task01(data: list[tuple[int, int]]) -> int:
    return math.prod(find_options(*race) for race in data)


def task02(data: tuple[int, int]) -> int:
    return find_options(*data)


if __name__ == "__main__":
    example_data = load_data(True)
    data = load_data()

    assert task01(parse(example_data)) == 288
    print_result(1, task01(parse(data)))

    assert task02(parse2(example_data)) == 71503
    print_result(2, task02(parse2(data)))
