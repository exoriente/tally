from collections.abc import Mapping

from pytest import fixture

from tally.compare import compare_sums, ComparisonDistribution
from tally.int_distribution import IntDistribution, create_int_distribution


@fixture
def die1d2() -> Mapping[int, int]:
    return IntDistribution.of_die(2).d


def test_compare_1d2_le_1d2(die1d2: Mapping[int, int]) -> None:
    assert compare_sums(die1d2, die1d2, int.__le__) == ComparisonDistribution(
        wins=3, losses=1
    )


def test_compare_max_2d3() -> None:
    assert create_int_distribution(2, 3, max) == IntDistribution(
        d={
            1: 1,
            2: 3,
            3: 5,
        }
    )
