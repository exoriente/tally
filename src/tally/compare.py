from collections.abc import Mapping, Callable
from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class ComparisonDistribution:
    wins: int
    losses: int


def compare_sums(
    lhs: Mapping[int, int], rhs: Mapping[int, int], operator: Callable[[int, int], bool]
) -> ComparisonDistribution:
    wins = 0
    losses = 0

    for (r1, c1), (r2, c2) in product(lhs.items(), rhs.items()):
        if operator(r1, r2):
            wins += c1 * c2
        else:
            losses += c1 * c2

    return ComparisonDistribution(wins, losses)
