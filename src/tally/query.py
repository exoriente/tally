from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum, auto

from tally.compare import compare_sums, ComparisonDistribution
from tally.probabilities import probabilities, accumulate_ge
from tally.render import (
    render_sum_probabilities,
    render_comparison_probabilities,
    render_average,
)
from tally.int_distribution import IntDistribution, create_int_distribution


class Comparator(Enum):
    EQ = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()


INT_OPERATOR = {
    Comparator.EQ: int.__eq__,
    Comparator.LE: int.__le__,
    Comparator.GE: int.__ge__,
    Comparator.LT: int.__lt__,
    Comparator.GT: int.__gt__,
}


def accumulate_if(
    cumulative: bool, distribution: Mapping[int, int]
) -> Mapping[int, int]:
    return accumulate_ge(distribution) if cumulative else distribution


@dataclass(frozen=True)
class Expression(ABC):
    @abstractmethod
    def render(self, cumulative: bool) -> str: ...


@dataclass(frozen=True)
class ComparableExpression(Expression, ABC):
    @abstractmethod
    def compute(self) -> IntDistribution: ...

    def render(self, cumulative: bool) -> str:
        base = self.compute()

        probs = probabilities(accumulate_if(cumulative, base.d), cumulative)
        average = base.average()

        return render_sum_probabilities(probs.items()) + render_average(average)


@dataclass(frozen=True)
class Dice:
    number: int
    sides: int


@dataclass(frozen=True)
class SumDice(ComparableExpression):
    dice: Dice

    def compute(self) -> IntDistribution:
        return create_int_distribution(self.dice.number, self.dice.sides, int.__add__)


@dataclass(frozen=True)
class Modifier(ComparableExpression):
    constant: int

    def compute(self) -> IntDistribution:
        return IntDistribution.constant(self.constant)


@dataclass(frozen=True)
class MaxDice(ComparableExpression):
    dice: Dice

    def compute(self) -> IntDistribution:
        return create_int_distribution(self.dice.number, self.dice.sides, max)


@dataclass(frozen=True)
class MinDice(ComparableExpression):
    dice: Dice

    def compute(self) -> IntDistribution:
        return create_int_distribution(self.dice.number, self.dice.sides, min)


@dataclass(frozen=True)
class SumExpression(ComparableExpression):
    lhs: ComparableExpression
    rhs: ComparableExpression

    def compute(self) -> IntDistribution:
        return self.lhs.compute() + self.rhs.compute()


@dataclass(frozen=True)
class Comparison(Expression):
    lhs: ComparableExpression
    rhs: ComparableExpression
    comparator: Comparator

    def compute(self) -> ComparisonDistribution:
        return compare_sums(
            self.lhs.compute().d,
            self.rhs.compute().d,
            INT_OPERATOR[self.comparator],
        )

    def render(self, cumulative: bool) -> str:
        result = self.compute()
        return render_comparison_probabilities(result.wins, result.losses)
