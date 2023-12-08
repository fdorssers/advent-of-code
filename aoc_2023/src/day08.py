import math
from collections import defaultdict

from utils import load_data
from utils import print_result


def parse(data: list[str]) -> tuple[list[str], dict[str, dict[str, str]]]:
    element_map = {}
    for line in data[2:]:
        from_, to = line.split(" = ")
        l_r = to[1:-1].split(",")
        element_map[from_.strip()] = {"L": l_r[0].strip(), "R": l_r[1].strip()}
    return list(data[0]), element_map


def task01(instructions: list[str], element_map: dict[str, dict[str, str]]) -> int:
    current = "AAA"
    steps = 0
    while True:
        for instruction in instructions:
            current = element_map[current][instruction]
            steps += 1
        if current == "ZZZ":
            break
    return steps


def determine_distances(
    instructions: list[str], element_map: dict[str, dict[str, str]]
) -> dict[str, int]:
    starting_positions = [el for el in element_map if el.endswith("A")]
    distances: dict[str, int] = defaultdict(int)
    for starting_position in starting_positions:
        current = starting_position
        while True:
            for instruction in instructions:
                current = element_map[current][instruction]
                distances[starting_position] += 1
            if current.endswith("Z"):
                break
    return distances


def task02(instructions: list[str], element_map: dict[str, dict[str, str]]) -> int:
    distances = determine_distances(instructions, element_map)
    return math.lcm(*distances.values())


if __name__ == "__main__":
    example_data = load_data(True)
    data = load_data()

    assert task01(*parse(example_data)) == 2
    print_result(1, task01(*parse(data)))

    example_data_2 = load_data(True, 2)

    assert task02(*parse(example_data_2)) == 6
    print_result(2, task02(*parse(data)))
