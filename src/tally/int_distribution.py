from collections.abc import Mapping, Reversible, Callable
from dataclasses import dataclass
from functools import cache
from itertools import product, starmap
from typing import KeysView


def first_and_last[T](keys: KeysView[T]) -> tuple[T, T]:
    assert isinstance(keys, Reversible)
    return next(iter(keys)), next(reversed(keys))


@dataclass(frozen=True)
class IntDistribution:
    d: Mapping[int, int]

    @staticmethod
    def constant(c: int) -> IntDistribution:
        return IntDistribution({c: 1})

    @staticmethod
    def of_die(sides: int) -> IntDistribution:
        return IntDistribution({s: 1 for s in range(1, sides + 1)})

    def commutative_combine(
        self, other: IntDistribution, operator: Callable[[int, int], int]
    ) -> IntDistribution:
        f1, l1 = first_and_last(self.d.keys())
        f2, l2 = first_and_last(other.d.keys())

        d = {x: 0 for x in range(operator(f1, f2), operator(l1, l2) + 1)}

        for (s1, r1), (s2, r2) in product(self.d.items(), other.d.items()):
            d[operator(s1, s2)] += r1 * r2

        return IntDistribution(d)

    def __add__(self, other: IntDistribution) -> IntDistribution:
        return self.commutative_combine(other, int.__add__)

    def average(self) -> float:
        return sum(starmap(int.__mul__, self.d.items())) / sum(self.d.values())


@cache
def create_int_distribution(
    number: int, sides: int, operator: Callable[[int, int], int]
) -> IntDistribution:
    if number == 1:
        return IntDistribution.of_die(sides)
    elif number % 2 == 0:
        half = create_int_distribution(number // 2, sides, operator)
        return half.commutative_combine(half, operator)
    else:
        halfish = create_int_distribution((number - 1) // 2, sides, operator)
        one = create_int_distribution(1, sides, operator)
        return halfish.commutative_combine(halfish, operator).commutative_combine(
            one, operator
        )
