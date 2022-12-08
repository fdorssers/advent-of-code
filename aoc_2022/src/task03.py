import string
from pathlib import Path

from utils import print_result


def load_data(example: bool = False) -> list[str]:
    path = Path(__file__).parent.parent / "data" / f"task03{'_example' if example else ''}.txt"
    with open(path) as f:
        return f.read().strip().split("\n")


VALUES = {char: val for val, char in enumerate(string.ascii_lowercase + string.ascii_uppercase, 1)}


def task1(sacks: list[str]) -> int:
    sack_sum = 0
    for sack in sacks:
        middle = len(sack) // 2
        intersection = set(sack[:middle]) & set(sack[middle:])
        sack_sum += VALUES[next(iter(intersection))]
    return sack_sum


def task2(sacks: list[str]) -> int:
    return sum(
        VALUES[next(iter(set.intersection(*(set(s) for s in sacks[i : i + 3]))))]
        for i in range(0, len(sacks), 3)
    )


if __name__ == "__main__":
    example_data = load_data(True)
    data = load_data()

    assert task1(example_data) == 157
    print_result(1, task1(data))

    assert task2(example_data) == 70
    print_result(2, task2(data))
