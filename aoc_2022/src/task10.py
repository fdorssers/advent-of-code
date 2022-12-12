from dataclasses import dataclass
from typing import Optional

from utils import load_data
from utils import print_result


@dataclass
class Op:
    instruction: str
    value: Optional[int]


def parse_data(lines: list[str]) -> list[Op]:
    ops = []
    for l in lines:
        l_split = l.split()
        ops.append(Op(l_split[0], int(l_split[1]) if len(l_split) > 1 else None))
    return ops


class System:
    def __init__(self) -> None:
        self._current = 1
        self._cycle_num = 1
        self._snapshots: dict[int, int] = {}
        self._operations: dict[int, int] = {}

    def cycle(self, op: Op) -> None:
        self._log_state()
        if op.instruction == "noop":
            self._cycle_num += 1
            return

        self._cycle_num += 1
        self._log_state()
        self._cycle_num += 1
        self._current += op.value

    def _log_state(self) -> None:
        if self._cycle_num > 0 and (self._cycle_num == 20 or (self._cycle_num - 20) % 40 == 0):
            self._snapshots[self._cycle_num] = self._current

    @property
    def output(self) -> int:
        return sum(k * v for k, v in self._snapshots.items())


def part1(ops: list[Op]) -> int:
    system = System()
    for op in ops:
        system.cycle(op)
    return system.output


def part2(ops: list[Op]) -> int:
    # return sum([1 for pair in pairs if pair[0] & pair[1]])
    pass


if __name__ == "__main__":
    example_data = parse_data(load_data(True))
    data = parse_data(load_data(False))

    assert part1(example_data) == 13140
    print_result(1, part1(data))
    #
    # assert part2(example_data) == 4
    # print_result(2, part2(data))
