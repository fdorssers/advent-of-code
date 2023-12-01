import re
import string

from utils import load_data
from utils import print_result

NUM_WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
NUMS = dict(zip(NUM_WORDS, list(string.digits)[1:]))
VALS = list(NUMS.keys()) + list(string.digits)


def task1(lines: list[str]) -> int:
    int_lines = [[val for val in line if val.isdigit()] for line in lines]
    return sum(int(line[0] + line[-1]) for line in int_lines)


def join_first_and_last(results: dict[int, str]) -> int:
    return int(results[min(results.keys())] + results[max(results.keys())])


def task2(lines: list[str]) -> int:
    return sum(
        [
            join_first_and_last(
                {m.start(): NUMS.get(val, val) for val in VALS for m in re.finditer(val, line)}
            )
            for line in lines
        ]
    )


if __name__ == "__main__":
    example_data = load_data(True)
    data = load_data()

    assert task1(example_data) == 142
    print_result(1, task1(data))

    example_data_2 = load_data(True, 2)

    assert task2(example_data_2) == 281
    print_result(2, task2(data))
