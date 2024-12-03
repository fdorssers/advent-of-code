import re
from operator import mul

from utils import load_data
from utils import print_result


def parse(data: list[str]) -> str:
    return "".join(data)


pattern = re.compile(r"mul\(\d+,\d+\)")


def task01(data: str) -> int:
    total = 0
    matches = re.findall(pattern, data)
    total += sum(mul(*map(int, re.findall(r"\d+", match))) for match in matches)
    return total


pattern2 = re.compile(r"(mul\(\d+,\d+\))|(do\(\))|(don't\(\))")


def task02(data: str) -> int:
    total = 0
    enabled = True
    matches = re.findall(pattern2, data)
    for match in matches:
        if match[0] and enabled:
            total += mul(*map(int, re.findall(r"\d+", match[0])))
        elif match[1]:
            enabled = True
        elif match[2]:
            enabled = False
    return total


if __name__ == "__main__":
    example_data = parse(load_data(True))
    data = parse(load_data())

    assert task01(example_data) == 161
    print_result(1, task01(data))

    example_data_2 = parse(load_data(True, 2))
    assert task02(example_data_2) == 48
    print_result(2, task02(data))
