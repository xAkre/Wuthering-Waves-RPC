from rich.console import Console
from src.utilities.cli import indent, print_divider


def fatal_error(
    console: Console, message: str, exception: Exception | None = None
) -> None:
    """
    Display a fatal error message and exit the program

    :param console: The console to use for output
    :param message: The fatal error message to display
    """
    print_divider(console, "[red]An Error Occurred[/red]", "red")
    console.print(message, style="red")

    if exception is not None:
        console.print_exception(show_locals=True)

    console.show_cursor(False)
    # For some reason using console.input() here doesn't work, so I'm using input() instead
    input(indent("Press Enter to exit..."))
    exit(1)
