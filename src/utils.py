import inspect
from pathlib import Path

PROJECT_DIR = Path(__file__).parents[1]
DATA_DIR = PROJECT_DIR / "data"


def load_data(example: bool = False):
    """
    Load either the actual or the example data for a specific day. Note that the day/task number is
    automatically detected based on the calling stack.

    :param example:
    :return:
    """
    task_id = _get_task_number_from_stack()
    with open(DATA_DIR / f"task{task_id:02d}{'_example' if example else ''}.txt") as f:
        return f.read().splitlines()


def _get_task_number_from_stack() -> int:
    """
    Retrieve the task number from the calling file.

    :return:
    """
    return int(inspect.stack()[2].filename[-5:-3])


def print_result(part: int, result: int):
    """
    Pretty print the result.

    :param part:
    :param result:
    :return:
    """
    print(f"The result for task {_get_task_number_from_stack()} part {part} is: {result}")
