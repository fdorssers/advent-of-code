from more_itertools import sliding_window as sw

from utils import load_data
from utils import print_result


def part(signal: str, p_size: int) -> int:
    return next(i + p_size for i, win in enumerate(sw(signal, p_size)) if len(set(win)) == p_size)


if __name__ == "__main__":
    example_data = load_data(True)[0]
    data = load_data(False)[0]

    assert part(example_data, 4) == 7
    print_result(1, part(data, 4))

    assert part(example_data, 14) == 19
    print_result(2, part(data, 14))
