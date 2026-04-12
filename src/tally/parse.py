from re import match

from tally.query import (
    Expression,
    SumDice,
    Comparator,
    Comparison,
    MinDice,
    ComparableExpression,
    Dice,
    MaxDice,
    Modifier,
    SumExpression,
)


class ParseError(RuntimeError): ...


def parse_dice(number: str, sides: str, code: str) -> ComparableExpression:
    dice = Dice(int(number), int(sides))

    match code:
        case "d":
            return SumDice(dice)
        case "max":
            return MaxDice(dice)
        case "min":
            return MinDice(dice)
        case _:
            raise ParseError(f'Can\'t parse "{code}"')


def parse_modifier(sign: str, value: str) -> Modifier:
    match sign:
        case "+":
            factor = 1
        case "-":
            factor = -1
        case _:
            raise ParseError(f'Can\'t parse "{sign}"')

    return Modifier(factor * int(value))


def parse_query(input: str) -> Expression:
    m = match(
        r"^\s*(\d+)\s*(d|max|min)\s*(\d+)\s*(([+-])\s*(\d+))?\s*"
        r"((==|<|>|<=|>=)\s*(\d+)\s*(d|max|min)\s*(\d+)\s*(([+-])\s*(\d+))?\s*)?$",
        input,
    )

    if m is None:
        raise ParseError(f'Can\'t parse "{input}"')

    lhs = parse_dice(m.group(1), m.group(3), m.group(2))

    if m.group(4):
        lhs = SumExpression(lhs, parse_modifier(m.group(5), m.group(6)))

    if m.group(7):
        match m.group(8):
            case "==":
                comparator = Comparator.EQ
            case "<":
                comparator = Comparator.LT
            case ">":
                comparator = Comparator.GT
            case "<=":
                comparator = Comparator.LE
            case ">=":
                comparator = Comparator.GE
            case _:
                raise ParseError(f'Can\'t parse "{m.group(5)}"')

        rhs = parse_dice(m.group(9), m.group(11), m.group(10))

        if m.group(14):
            rhs = SumExpression(rhs, parse_modifier(m.group(13), m.group(14)))

        return Comparison(lhs, rhs, comparator)

    else:
        return lhs
