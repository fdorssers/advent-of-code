from dataclasses import dataclass

from utils import load_data
from utils import print_result


@dataclass
class Command:
    direction: str
    steps: int


def tadd(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return (t1[0] + t2[0], t1[1] + t2[1])


def tsub(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return (t1[0] - t2[0], t1[1] - t2[1])


DIRECTIONS = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}


class State:
    head: tuple[int, int] = (0, 0)
    tail: tuple[int, int] = (0, 0)
    visited: set[tuple[int, int]] = {(0, 0)}

    def move(self, command: Command) -> None:
        print(command)
        for steps in range(command.steps):
            self.update(command.direction)
            self.visited.add(self.tail)

    def update(self, direction: str) -> None:
        match direction:
            case "U":
                self.head = tadd(self.head, (0, 1))
            case "D":
                self.head = tadd(self.head, (0, -1))
            case "L":
                self.head = tadd(self.head, (-1, 0))
            case "R":
                self.head = tadd(self.head, (1, 0))
            case _:
                raise ValueError(f"Unknown direction: {direction}")
        self.tail = tadd(self.tail, self.tail_step(self.head, self.tail))
        # print(f"New locations: {self.head}, {self.tail}")

    @staticmethod
    def tail_step(h: tuple[int, int], t: tuple[int, int]) -> tuple[int, int]:
        diff = tsub(t, h)
        # print(f"Diff: {diff}")
        # h = (5,5), t=(4,3) -> diff = (-1,-2)
        # if (-1 <= diff[0] <= 1) and (-1 <= diff[1] <= 1):
        #     # Do nothing, we're close enough
        #     return 0,0
        if (-1 <= diff[0] <= 1) and (diff[1] == -2):
            # Move a step up and to the middle
            return -diff[0], 1
        elif (-1 <= diff[0] <= 1) and (diff[1] == 2):
            # Move a step down
            return -diff[0], -1
        elif (diff[0] == -2) and (-1 <= diff[1] <= 1):
            # Move a step right
            return 1, -diff[1]
        elif (diff[0] == 2) and (-1 <= diff[1] <= 1):
            # Move a step left
            return -1, -diff[1]
        elif (diff[0] == 2) and (diff[1] == 2):
            return -1, -1
        elif (diff[0] == -2) and (diff[1] == 2):
            return 1, -1
        elif (diff[0] == 2) and (diff[1] == -2):
            return -1, 1
        elif (diff[0] == -2) and (diff[1] == -2):
            return 1, 1
        else:
            print(f"Default: {diff}")
            return 0, 0
            # Need to move diagonally


def parse_data(lines: list[str]) -> list[Command]:
    return [Command(line.split()[0], int(line.split()[1])) for line in lines]


def part1(commands: list[Command]) -> int:
    board = State()
    for command in commands:
        board.move(command)
    print(board.visited)
    return len(board.visited)


def part2(pairs: list[tuple[set[int], set[int]]]) -> int:
    # return sum([1 for pair in pairs if pair[0] & pair[1]])
    return 0


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    data = parse_data(load_data(False))

    # 6193 Too high

    assert part1(example_data) == 13
    print_result(1, part1(data))
    #
    # assert part2(example_data) == 4
    # print_result(2, part2(data))
