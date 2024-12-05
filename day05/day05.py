from performance_utils.performance_utils import measure_performance

with open("day05/in05.txt") as in05:
    data = in05.read()


def get_rulesets(rules):
    rulesets = dict()

    for rule in rules.split():
        before, after = rule.split("|")

        if before not in rulesets:
            rulesets[before] = set()

        rulesets[before].add(after)

    return rulesets


def part1(data):
    rules, updates = data.split("\n\n")

    rulesets = get_rulesets(rules)

    out = 0
    for pages in updates.split():
        pages = pages.split(",")
        for idx, page in enumerate(pages):
            if len(rulesets.get(page, set()) & set(pages[:idx])) > 0:
                break
        else:
            out += int(pages[len(pages) // 2])

    return out


def part2(data):
    rules, updates = data.split("\n\n")

    rulesets = get_rulesets(rules)

    out = 0
    for pages in updates.split():
        pages = pages.split(",")

        fixed_pages = pages[::]
        for idx, page in enumerate(pages):
            if (diff := len(rulesets.get(page, set()) & set(pages[:idx]))) > 0:
                fixed_pages.insert(idx - diff, fixed_pages.pop(idx))

        if pages != fixed_pages:
            out += int(fixed_pages[len(fixed_pages) // 2])

    return out


measure_performance("part 1", part1, data)
measure_performance("part 2", part2, data)
