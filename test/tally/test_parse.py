from tally.parse import parse_query
from tally.query import Comparison, SumDice, Dice, Comparator, SumExpression, Modifier


def test_parse() -> None:
    assert parse_query("4d4 >= 2d12") == Comparison(
        lhs=SumDice(Dice(4, 4)),
        rhs=SumDice(Dice(2, 12)),
        comparator=Comparator.GE
    )

    assert parse_query("4d4 >= 2d12 + 2") == Comparison(
        lhs=SumDice(Dice(4, 4)),
        rhs=SumExpression(
         lhs=   SumDice(Dice(2, 12)),
            rhs=Modifier(2)
        ),
        comparator=Comparator.GE
    )