import re
import string

from utils import load_data
from utils import print_result

WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
NUM_DICT = dict(zip(string.digits, string.digits))
ALL_DICT = NUM_DICT | dict(zip(WORDS, string.digits[1:]))


def join_first_and_last(results: dict[int, str]) -> int:
    return int(results[min(results.keys())] + results[max(results.keys())])


def task(lines: list[str], dct: dict[str, str]) -> int:
    return sum(
        [
            join_first_and_last(
                {m.start(): dct[val] for val in dct.keys() for m in re.finditer(val, line)}
            )
            for line in lines
        ]
    )


if __name__ == "__main__":
    example_data = load_data(True)
    data = load_data()

    assert task(example_data, NUM_DICT) == 142
    print_result(1, task(data, NUM_DICT))

    example_data_2 = load_data(True, 2)

    assert task(example_data_2, ALL_DICT) == 281
    print_result(2, task(data, ALL_DICT))
