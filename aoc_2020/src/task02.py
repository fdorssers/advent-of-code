from dataclasses import dataclass
from typing import Callable
from typing import List
from typing import Tuple

from utils import load_data
from utils import print_result


@dataclass
class PasswordRule:
    num1: int
    num2: int
    char: str


def is_valid_p1(rule: PasswordRule, password: str) -> bool:
    return rule.num1 <= password.count(rule.char) <= rule.num2


def is_valid_p2(rule: PasswordRule, password: str) -> bool:
    return (password[rule.num1 - 1] == rule.char) != (password[rule.num2 - 1] == rule.char)


def part(
    items: List[Tuple[PasswordRule, str]], predicate: Callable[[PasswordRule, str], bool]
) -> int:
    return sum([1 for pwr, pw in items if predicate(pwr, pw)])


def parse_line(line: str) -> Tuple[PasswordRule, str]:
    split_line = line.split(": ")
    password = split_line[1]
    lims, char = split_line[0].split(" ")
    num1, num2 = lims.split("-")
    return PasswordRule(int(num1), int(num2), char), password


if __name__ == "__main__":
    example_data = [parse_line(val) for val in load_data(True)]
    data = [parse_line(val) for val in load_data(False)]

    assert part(example_data, is_valid_p1) == 2
    print_result(1, part(data, is_valid_p1))

    assert part(example_data, is_valid_p2) == 1
    print_result(2, part(data, is_valid_p2))
