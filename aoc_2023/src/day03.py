from utils import load_data
from utils import print_result


def is_adjacent(x: int, y: int, data: list[str]) -> bool:
    y_diff = (-1, 0, 1)
    x_diff = (-1, 0, 1)
    for x_d in x_diff:
        for y_d in y_diff:
            if (x_d == 0) and (y_d == 0):
                continue
            x_new = x + x_d
            y_new = y + y_d
            if (x_new < 0) or (y_new < 0):
                continue
            if (x_new >= len(data[y])) or (y_new >= len(data)):
                continue

            if y_d == 0:
                if not data[y_new][x_new].isdigit() and (data[y_new][x_new] != "."):
                    return True
            else:
                if data[y_new][x_new] != ".":
                    return True
    return False


def task01(data: list[str]) -> int:
    chars = []
    adjacent_chars = []
    for y, line in enumerate(data):
        cur_char = ""
        cur_char_adjacent = False
        for x, char in enumerate(line):
            if char.isdigit():
                cur_char += char
                cur_char_adjacent |= is_adjacent(x, y, data)
            else:
                if cur_char:
                    chars.append(int(cur_char))
                    if cur_char_adjacent:
                        adjacent_chars.append(int(cur_char))
                    cur_char = ""
                    cur_char_adjacent = False
        if cur_char:
            chars.append(int(cur_char))
            if cur_char_adjacent:
                adjacent_chars.append(int(cur_char))
    return sum(adjacent_chars)


def task02(data: list[list[dict[str, int]]]) -> int:
    return 0


if __name__ == "__main__":
    example_data = load_data(True)
    data = load_data()

    assert task01(example_data) == 4361
    print_result(1, task01(data))
    #
    # assert task02(example_data) == 2286
    # print_result(2, task02(data))
