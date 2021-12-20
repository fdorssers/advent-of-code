import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from utils import load_data
from utils import print_result


def parse_input(lines: list[str]) -> tuple[str, np.array]:
    algo = "".join(["0" if c == "." else "1" for c in lines[0]])
    image = np.array([[0 if c == "." else 1 for c in line] for line in lines[2:]])
    return algo, image


BINARY_MAPPING = (2 ** np.arange(8, -1, -1)).reshape(3, 3)


def to_number(array: np.array, algorithm: str) -> int:
    return int(algorithm[(array * BINARY_MAPPING).sum()])


def enhance(algo: str, image: np.array, lit: bool) -> tuple[np.array, bool]:
    padded_image = np.pad(image, pad_width=2, mode="constant", constant_values=int(lit))
    new_image = np.zeros_like(padded_image)[:-2, :-2]
    for i, row in enumerate(sliding_window_view(padded_image, (3, 3))):
        for j, col in enumerate(row):
            new_image[i, j] = to_number(col, algo)
    return new_image, not lit


def part(algo: str, image: np.array, times: int) -> int:
    lit = False
    for _ in range(times):
        image, lit = enhance(algo, image, lit)
    return int(image.sum())


if __name__ == "__main__":
    example_algo_inp, example_image_inp = parse_input(load_data(True))
    algo_inp, image_inp = parse_input(load_data(False))

    # assert part(example_algo_inp, example_image_inp, 2) == 35
    print_result(1, part(algo_inp, image_inp, 2))

    # assert part(example_algo_inp, example_image_inp, 50) == 3351
    print_result(1, part(algo_inp, image_inp, 50))
