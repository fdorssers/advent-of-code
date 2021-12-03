import numpy as np

from src.utils import load_data, print_result


def part1(array: np.array) -> int:
    most_common = (array.sum(axis=0) / array.shape[0]).round()
    least_common = 1 - most_common
    gamma = int("".join(most_common.astype(int).astype(str)), 2)
    epsilon = int("".join(least_common.astype(int).astype(str)), 2)
    return gamma * epsilon


def _mask_helper(column: np.array, mask: np.array, is_scrubber: bool) -> np.array:
    if mask.sum() <= 1:
        return mask
    # Need a small delta so numpy actually rounds 0.5 up to 1.
    delta = 0.0000001
    column_masked = column[mask]
    mask_value = ((column_masked.sum() / column_masked.shape[0]) + delta).round().astype(int)
    if is_scrubber:
        mask_value = 1 - mask_value
    return mask & (column == mask_value)


def part2(array: np.array) -> int:
    gen_mask = np.full(array.shape[0], True)
    scrub_mask = np.full(array.shape[0], True)
    for column in array.T:
        gen_mask = _mask_helper(column, gen_mask, False)
        scrub_mask = _mask_helper(column, scrub_mask, True)
    generator_rating = int("".join(array[gen_mask].flatten().astype(str)), 2)
    scrubber_rating = int("".join(array[scrub_mask].flatten().astype(str)), 2)
    return generator_rating * scrubber_rating


if __name__ == "__main__":
    example_data = np.array([[int(char) for char in line] for line in load_data(True)])
    data = np.array([[int(char) for char in line] for line in load_data(False)])

    assert part1(example_data) == 198
    print_result(1, part1(data))

    assert part2(example_data) == 230
    print_result(2, part2(data))
