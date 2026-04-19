from typer import Typer, echo, Argument, Option

from tally.parse import parse_query

app = Typer()


@app.command()
def main(
    combination: str = Argument("3d6", help="The dice you want to tally"),
    cumulative: bool = Option(
        False, "-c", "--cumulative", help="Show cumulative graph"
    ),
) -> None:
    expr = parse_query(combination)
    echo(expr.render(cumulative=cumulative))


if __name__ == "__main__":
    app(["1d6>1d6"])
