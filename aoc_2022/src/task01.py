from pathlib import Path

from utils import print_result


def load_task(example: bool = False) -> list[list[int]]:
    path = Path(__file__).parent.parent / "data" / f"task01{'_example' if example else ''}.txt"
    with open(path) as f:
        data = f.read().split("\n\n")
        return [[int(val) for val in elf.split("\n") if val] for elf in data if elf]


def task1(elves: list[list[int]]) -> int:
    return max(sum(elf) for elf in elves)


def task2(elves: list[list[int]]) -> int:
    return sum(sorted([sum(elf) for elf in elves], reverse=True)[:3])


if __name__ == "__main__":
    example_data = load_task(True)
    data = load_task()

    assert task1(example_data) == 24000
    print_result(1, task1(data))

    assert task2(example_data) == 45000
    print_result(1, task2(data))
