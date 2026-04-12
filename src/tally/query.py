from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto

from tally.compare import compare_sums, ComparisonDistribution
from tally.probabilities import probabilities, accumulate_ge
from tally.render import render_sum_probabilities, render_comparison_probabilities
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


@dataclass(frozen=True)
class Expression(ABC):
    @abstractmethod
    def render(self) -> str: ...


@dataclass(frozen=True)
class ComparableExpression(Expression, ABC):
    @abstractmethod
    def compute(self) -> IntDistribution: ...


@dataclass(frozen=True)
class Dice:
    number: int
    sides: int


@dataclass(frozen=True)
class SumDice(ComparableExpression):
    dice: Dice

    def compute(self) -> IntDistribution:
        return create_int_distribution(self.dice.number, self.dice.sides, int.__add__)

    def render(self) -> str:
        return render_sum_probabilities(
            probabilities(accumulate_ge(self.compute().d)).items()
        )


@dataclass(frozen=True)
class Modifier(ComparableExpression):
    constant: int

    def compute(self) -> IntDistribution:
        return IntDistribution.constant(self.constant)

    def render(self) -> str:
        return render_sum_probabilities(
            probabilities(accumulate_ge(self.compute().d)).items()
        )


@dataclass(frozen=True)
class MaxDice(ComparableExpression):
    dice: Dice

    def compute(self) -> IntDistribution:
        return create_int_distribution(self.dice.number, self.dice.sides, max)

    def render(self) -> str:
        return render_sum_probabilities(
            probabilities(accumulate_ge(self.compute().d)).items()
        )


@dataclass(frozen=True)
class MinDice(ComparableExpression):
    dice: Dice

    def compute(self) -> IntDistribution:
        return create_int_distribution(self.dice.number, self.dice.sides, min)

    def render(self) -> str:
        return render_sum_probabilities(probabilities(self.compute().d).items())


@dataclass(frozen=True)
class SumExpression(ComparableExpression):
    lhs: ComparableExpression
    rhs: ComparableExpression

    def compute(self) -> IntDistribution:
        return self.lhs.compute() + self.rhs.compute()

    def render(self) -> str:
        return render_sum_probabilities(probabilities(self.compute().d).items())


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

    def render(self) -> str:
        result = self.compute()
        return render_comparison_probabilities(result.wins, result.losses)
