import re
from operator import mul
from typing import Iterator

from utils import load_data
from utils import print_result


def parse(data: list[str]) -> str:
    return "".join(data)


patterns = re.compile(r"(mul\(\d+,\d+\))|(do\(\))|(don't\(\))")


def get_multiplications(data: str, task1: bool) -> Iterator[int]:
    enabled = True
    for match in re.findall(patterns, data):
        if match[0] and (enabled or task1):
            yield mul(*map(int, re.findall(r"\d+", match[0])))
        elif match[1]:
            enabled = True
        elif match[2]:
            enabled = False


def task(data: str, task1: bool) -> int:
    return sum(get_multiplications(data, task1))


if __name__ == "__main__":
    example_data = parse(load_data(True))
    data = parse(load_data())

    assert task(example_data, True) == 161
    print_result(1, task(data, True))

    example_data_2 = parse(load_data(True, 2))
    assert task(example_data_2, False) == 48
    print_result(2, task(data, False))
