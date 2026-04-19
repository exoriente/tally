from collections.abc import Mapping
from itertools import product


def probabilities(
    distribution: Mapping[int, int], cumulative: bool
) -> Mapping[int, float]:
    if cumulative:
        total = max(distribution.values())
    else:
        total = sum(distribution.values())

    return {k: v / total for k, v in distribution.items()} or {0: 1.0}


def accumulate_ge(distribution: Mapping[int, int]) -> Mapping[int, int]:
    result = {k: 0 for k in distribution.keys()}

    for r, (v, c) in product(result.keys(), distribution.items()):
        if v >= r:
            result[r] += c

    return result
