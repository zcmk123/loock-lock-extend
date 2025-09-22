"""Console script for loock_lock_extend."""

import typer
from rich.console import Console

from loock_lock_extend import utils

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for loock_lock_extend."""
    console.print("Replace this message by putting your code into "
               "loock_lock_extend.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    utils.do_something_useful()


if __name__ == "__main__":
    app()
