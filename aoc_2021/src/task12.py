from collections import Counter
from collections import defaultdict

from utils import load_data
from utils import print_result


def parse_data(lines: list[str]) -> defaultdict[str, list[str]]:
    connections = defaultdict(list)
    for k, v in [line.split("-") for line in lines]:
        connections[k].append(v)
        connections[v].append(k)
    return connections


def is_small_visited_cave(cave: str, path: list[str]) -> bool:
    return cave.islower() and (cave in path)


def depth_first_search(path: list[str], connections: dict[str, list[str]]) -> int:
    if path[-1] == "end":
        return 1
    paths = 0
    for cave in connections[path[-1]]:
        if is_small_visited_cave(cave, path):
            continue
        paths += depth_first_search(path + [cave], connections)
    return paths


def part1(connections: defaultdict[str, list[str]]) -> int:
    return depth_first_search(["start"], connections)


def has_double_visits(path: list[str]) -> bool:
    return any(k.islower() and v == 2 for k, v in Counter(path).items())


def depth_first_search_repeating(path: list[str], connections: dict[str, list[str]]) -> int:
    if path[-1] == "end":
        return 1
    paths = 0
    for cave in connections[path[-1]]:
        if cave == "start":
            continue
        if has_double_visits(path) and is_small_visited_cave(cave, path):
            continue
        paths += depth_first_search_repeating(path + [cave], connections)
    return paths


def part2(connections: defaultdict[str, list[str]]) -> int:
    return depth_first_search_repeating(["start"], connections)


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    data = parse_data(load_data(False))

    assert part1(example_data) == 10
    print_result(1, part1(data))

    assert part2(example_data.copy()) == 36
    print_result(2, part2(data.copy()))
