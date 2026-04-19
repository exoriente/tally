from collections.abc import Collection
from operator import itemgetter


def to_blocks(part: float, width: int) -> str:
    eights = round(8 * width * part)

    base = "█" * int(eights // 8)

    match eights % 8:
        case 1:
            last = "▏"
        case 2:
            last = "▎"
        case 3:
            last = "▍"
        case 4:
            last = "▌"
        case 5:
            last = "▋"
        case 6:
            last = "▊"
        case 7:
            last = "▉"
        case _:
            last = ""

    return base + last


def render_sum_probabilities(probabilities: Collection[tuple[object, float]]) -> str:
    text = ""

    highest = max(map(itemgetter(1), probabilities))

    for result, prob in sorted(probabilities):
        text += f"{result:>4}: {prob:>7.2%} " + to_blocks(prob / highest, 20) + "\n"

    return text


def render_average(average: float) -> str:
    return f"On average: {average}"


def render_comparison_probabilities(wins: int, losses: int) -> str:
    total = wins + losses

    text = f"Win:   {wins / total:>7.2%} " + to_blocks(wins / total, 20) + "\n"
    text += f"Loose: {losses / total:>7.2%} " + to_blocks(losses / total, 20) + "\n"

    return text
