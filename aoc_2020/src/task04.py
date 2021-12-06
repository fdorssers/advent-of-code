import string
from functools import partial
from itertools import groupby
from typing import Callable
from typing import Dict
from typing import List

from utils import load_data
from utils import print_result


def parse(line: str) -> Dict[str, str]:
    return {k: v for k, v in [part.split(":") for part in line.split()]}


def part1(passports: List[Dict[str, str]]) -> int:
    required_elements = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    valid = [passport for passport in passports if required_elements.issubset(passport.keys())]
    return len(valid)


def valid_height(hgt: str) -> bool:
    height = hgt[:-2]
    if hgt.endswith("cm"):
        return int_between(height, 150, 193)
    elif hgt.endswith("in"):
        return int_between(height, 59, 76)
    else:
        return False


def int_between(val: str, lower: int, upper: int) -> bool:
    return lower <= int(val) <= upper


def int_between_partial(lower: int, upper: int) -> Callable[[str], bool]:
    return partial(int_between, lower=lower, upper=upper)


def valid_color(val: str) -> bool:
    return val in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def valid_pid(val: str) -> bool:
    return len(val) == 9 and val.isdigit()


def valid_hcl(val: str) -> bool:
    return val.startswith("#") and all(c in string.hexdigits for c in val[1:])


RULES = {
    "byr": int_between_partial(1920, 2002),
    "iyr": int_between_partial(2010, 2020),
    "eyr": int_between_partial(2020, 2030),
    "hgt": valid_height,
    "hcl": valid_hcl,
    "ecl": valid_color,
    "pid": valid_pid,
}


def part2(passports: List[Dict[str, str]]) -> int:
    acceptable = []
    for passport in passports:
        for key, rule in RULES.items():
            if key not in passport:
                break
            if not rule(passport[key]):
                break
        else:
            acceptable.append(passport)
    return len(acceptable)


if __name__ == "__main__":
    tmp = load_data(True)
    example_data = [
        parse(" ".join(v)) for k, v in groupby(load_data(True), key=lambda l: bool(l)) if k
    ]
    data = [parse(" ".join(v)) for k, v in groupby(load_data(False), key=lambda l: bool(l)) if k]

    assert part1(example_data) == 10
    print_result(1, part1(data))

    assert part2(example_data) == 6
    print_result(2, part2(data))
