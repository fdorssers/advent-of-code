from collections import Counter
from collections import defaultdict
from itertools import groupby

from utils import load_data
from utils import print_result


def parse_data(lines: list[str]) -> tuple[str, defaultdict[str, str]]:
    template_group, rules_group = [
        list(group) for key, group in groupby(lines, lambda x: bool(x)) if key
    ]
    rule_dict = {rule[0]: rule[1] for rule in [r.split(" -> ") for r in rules_group]}
    return template_group[0], defaultdict(lambda: "", rule_dict)


def part(template: str, rules: defaultdict[str, str], steps: int) -> int:
    for _ in range(steps):
        template = "".join(
            [f"{a}{rules[a+b]}" for a, b in zip(template, template[1:])] + [template[-1]]
        )
    counts = Counter(template)
    return max(counts.values()) - min(counts.values())


if __name__ == "__main__":
    example_template, example_rules = parse_data(load_data(True))
    template, rules = parse_data(load_data(False))

    assert part(example_template, example_rules, 10) == 1588
    print_result(1, part(template, rules, 10))

    assert part(example_template, example_rules, 40) == 2188189693529
    print_result(1, part(template, rules, 40))
