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


def init_structures(
    template: str, rules: defaultdict[str, str]
) -> tuple[defaultdict[str, int], defaultdict[str, int], defaultdict[str, list[str]]]:
    two_letter_counts = defaultdict(
        lambda: 0, Counter(["".join(t) for t in zip(template, template[1:])])
    )
    single_letter_counts = defaultdict(lambda: 0, Counter(template))
    rule_dict = defaultdict(list, {k: [f"{k[0]}{v}", f"{v}{k[1]}"] for k, v in rules.items()})
    return single_letter_counts, two_letter_counts, rule_dict


def part(template: str, rules: defaultdict[str, str], steps: int) -> int:
    single_letter_counts, two_letter_counts, rule_dict = init_structures(template, rules)
    for _ in range(steps):
        new_two_letter_counts: defaultdict[str, int] = defaultdict(lambda: 0)
        for two_letter_word, two_letter_word_occurrences in two_letter_counts.items():
            single_letter_counts[rules[two_letter_word]] += two_letter_word_occurrences
            for new_two_letter_word in rule_dict[two_letter_word]:
                new_two_letter_counts[new_two_letter_word] += two_letter_word_occurrences
        two_letter_counts = new_two_letter_counts
    return max(single_letter_counts.values()) - min(single_letter_counts.values())


if __name__ == "__main__":
    example_template, example_rules = parse_data(load_data(True))
    template, rules = parse_data(load_data(False))

    assert part(example_template, example_rules, 10) == 1588
    print_result(1, part(template, rules, 10))

    assert part(example_template, example_rules, 40) == 2188189693529
    print_result(1, part(template, rules, 40))
