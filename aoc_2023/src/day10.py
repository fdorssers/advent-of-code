import numpy as np

from utils import load_data
from utils import print_result

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRECTION_MAP: dict[str, list[tuple[int, int]]] = {
    "|": [UP, DOWN],
    "-": [LEFT, RIGHT],
    "L": [UP, RIGHT],
    "J": [LEFT, UP],
    "7": [LEFT, DOWN],
    "F": [RIGHT, DOWN],
    "S": [UP, DOWN, LEFT, RIGHT],
    ".": [],
}


def parse(data: list[str]) -> np.array:
    return np.array([list(line) for line in data])


def find_starting_pos(tiles: np.array) -> tuple[int, int]:
    loc = np.where(tiles == "S")
    return int(loc[0][0]), int(loc[1][0])


def add(pos1: tuple[int, int], pos2: tuple[int, int]) -> tuple[int, int]:
    return pos1[0] + pos2[0], pos1[1] + pos2[1]


def is_outside_of_bounds(pos: tuple[int, int], tiles: np.array) -> bool:
    max_size = tiles.shape[0]
    return not ((0 <= pos[0] < max_size) and (0 <= pos[1] < max_size))


def get_possible_directions_from_start(
    pos: tuple[int, int], tiles: np.array
) -> list[tuple[int, int]]:
    new_positions = []
    for direction, options in [
        (UP, {"|", "7", "S"}),
        (DOWN, {"|", "J", "L"}),
        (LEFT, {"-", "L", "F"}),
        (RIGHT, {"-", "J", "7"}),
    ]:
        new_pos = add(pos, direction)
        if is_outside_of_bounds(new_pos, tiles):
            continue
        if tiles[new_pos] in options:
            new_positions.append(new_pos)
    return new_positions


def get_possible_directions(pos: tuple[int, int], tiles: np.array) -> list[tuple[int, int]]:
    if tiles[pos] == "S":
        return get_possible_directions_from_start(pos, tiles)

    new_positions = []
    for direction in DIRECTION_MAP[tiles[pos]]:
        new_pos = add(pos, direction)
        if is_outside_of_bounds(new_pos, tiles):
            continue
        new_positions.append(new_pos)
    return new_positions


def task01(tiles: np.array) -> int:
    distance_map = np.zeros_like(tiles, dtype=int)
    starting_pos = find_starting_pos(tiles)
    current_distance = 0
    current_positions = [starting_pos]
    while True:
        new_current_positions = []
        current_distance += 1
        for current_position in current_positions:
            new_positions = get_possible_directions(current_position, tiles)
            for new_pos in new_positions:
                if distance_map[new_pos] > 0:
                    continue
                if new_pos == starting_pos:
                    continue
                distance_map[new_pos] = current_distance
                new_current_positions.append(new_pos)
        current_positions = new_current_positions
        if not current_positions:
            break
    return int(distance_map.max())


def task02(tiles: np.array) -> int:
    return 0


if __name__ == "__main__":
    example_data = parse(load_data(True))
    data = parse(load_data())

    assert task01(example_data) == 8
    print_result(1, task01(data))

    assert task02(example_data) == 2
    print_result(2, task02(data))
