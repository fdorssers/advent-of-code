from collections import Counter
from collections import defaultdict
from dataclasses import dataclass
from itertools import product

from utils import load_data
from utils import print_result


@dataclass
class Step:
    turn: str
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    @property
    def cubes(self) -> dict[tuple[int, int, int], str]:
        return {
            coords: self.turn
            for coords in product(
                range(self.x[0], self.x[1] + 1),
                range(self.y[0], self.y[1] + 1),
                range(self.z[0], self.z[1] + 1),
            )
        }


def parse_values(val: str) -> tuple[int, int]:
    values = val.split("=")[1]
    xyz_strs = values.split("..")
    return max(int(xyz_strs[0]), -50), min(int(xyz_strs[1]), 50)


def parse_data(lines: list[str]) -> list[Step]:
    steps = []
    for line in lines:
        split_line = line.split()
        x, y, z = split_line[1].split(",")
        steps.append(Step(split_line[0], parse_values(x), parse_values(y), parse_values(z)))
    return steps


def part1(steps: list[Step]) -> int:
    cubes: dict[tuple[int, int, int], str] = defaultdict(lambda: "off")
    for step in steps:
        cubes |= step.cubes
    return Counter(cubes.values())["on"]


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    actual_data = parse_data(load_data(False))

    assert part1(example_data) == 590784
    print_result(1, part1(actual_data))

    # assert part(example_algo_inp, example_image_inp, 50) == 3351
    # print_result(1, part(algo_inp, image_inp, 50))
