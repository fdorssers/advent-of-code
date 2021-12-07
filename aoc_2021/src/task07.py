from typing import Callable

import numpy as np

from utils import load_data
from utils import print_result


def cheapest_fuel(crabs: np.array, crab_cost: Callable[[np.array, int], int]) -> int:
    fuel_costs = {i: crab_cost(crabs, i) for i in range(crabs.min(), crabs.max() + 1)}
    return min(fuel_costs.values())


def p1_calc(crabs: np.array, target: int) -> int:
    return int(np.abs(crabs - target).sum())


def p2_calc(crabs: np.array, target: int) -> int:
    steps = np.abs(crabs - target)
    return int((1 / 2 * (steps * (steps + 1))).sum())


if __name__ == "__main__":
    example_data = np.array(list(map(int, load_data(True)[0].split(","))))
    data = np.array(list(map(int, load_data(False)[0].split(","))))

    assert cheapest_fuel(example_data, p1_calc) == 37
    print_result(1, cheapest_fuel(data, p1_calc))

    assert cheapest_fuel(example_data, p2_calc) == 168
    print_result(1, cheapest_fuel(data, p2_calc))
