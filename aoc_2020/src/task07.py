from collections import deque

from utils import load_data
from utils import print_result


def parse_bags(line: str) -> tuple[str, dict[str, int]]:
    outer, inner = line.split(" contain ")
    outer_bag = outer[:-5]
    inner_bags = {}
    for ib in inner.split(", "):
        if ib.startswith("no "):
            continue
        num, descriptor, color, _ = ib.split(" ")
        inner_bags[f"{descriptor} {color}"] = int(num)
    return outer_bag, inner_bags


def parse_data(lines: list[str]) -> dict[str, dict[str, int]]:
    bags = {}
    for line in lines:
        outer, inner = parse_bags(line)
        bags[outer] = inner
    return bags


def part1(bags: dict[str, dict[str, int]]) -> int:
    d = deque(["shiny gold"])
    num_colors = 0
    seen = set()
    while d:
        current_color = d.popleft()
        for outer_bag, inner_bags in bags.items():
            if current_color in inner_bags.keys():
                if outer_bag in seen:
                    continue
                seen.add(outer_bag)
                d.append(outer_bag)
                num_colors += 1
    return num_colors


def part2(bags: dict[str, dict[str, int]]) -> int:
    bag_count = 0
    d = deque([("shiny gold", 1)])
    while d:
        outer_bag, outer_count = d.popleft()
        for inner_bag, inner_count in bags[outer_bag].items():
            d.append((inner_bag, inner_count * outer_count))
            bag_count += inner_count * outer_count
    return bag_count


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    data = parse_data(load_data(False))

    assert part1(example_data) == 4
    print_result(1, part1(data))

    assert part2(example_data) == 32
    print_result(2, part2(data))
