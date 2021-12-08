from dataclasses import dataclass

from utils import load_data
from utils import print_result

UNIQUE_LENGTH_DIGITS = {2: 1, 3: 7, 4: 4, 7: 8}


@dataclass
class Line:
    input_patterns: list[frozenset[str]]
    output_patterns: list[frozenset[str]]

    @property
    def all_patterns(self) -> list[frozenset[str]]:
        return self.input_patterns + self.output_patterns


def parse_line(line: str) -> Line:
    split_line = line.split("|")
    return Line(
        [frozenset(pattern) for pattern in split_line[0].split()],
        [frozenset(pattern) for pattern in split_line[1].split()],
    )


def create_mapping(line: Line) -> dict[int, frozenset[str]]:
    mapping = {}
    unknown_patterns = set(line.all_patterns)

    for pattern in [p for p in unknown_patterns if len(p) in UNIQUE_LENGTH_DIGITS]:
        mapping[UNIQUE_LENGTH_DIGITS[len(pattern)]] = pattern

    for pattern in [p for p in unknown_patterns if len(p) == 6]:
        if len(mapping[7] & pattern) == 2:
            mapping[6] = pattern
        elif len(mapping[4] & pattern) == 3:
            mapping[0] = pattern
        else:
            mapping[9] = pattern

    for pattern in [p for p in unknown_patterns if len(p) == 5]:
        if mapping[1].issubset(pattern):
            mapping[3] = pattern
        elif len(mapping[4] & pattern) == 2:
            mapping[2] = pattern
        else:
            mapping[5] = pattern

    return mapping


def part1(lines: list[Line]) -> int:
    return sum(
        1 for line in lines for pattern in line.output_patterns if len(pattern) in {2, 3, 4, 7}
    )


def part2(lines: list[Line]) -> int:
    total = 0
    for line in lines:
        mapping = create_mapping(line)
        inverse_mapping = {v: k for k, v in mapping.items()}
        total += int("".join(str(inverse_mapping[p]) for p in line.output_patterns))
    return total


if __name__ == "__main__":
    example_data = [parse_line(val) for val in load_data(True)]
    data = [parse_line(val) for val in load_data(False)]

    print(example_data)

    assert part1(example_data) == 26
    print_result(1, part1(data))

    assert part2(example_data) == 61229
    print_result(2, part2(data))
