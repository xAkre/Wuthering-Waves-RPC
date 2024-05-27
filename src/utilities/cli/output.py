from rich.console import Console


# The cli doesn't really look nice when everything is flush against the left side of the terminal,
# so I added this function to indent the text
def indent(*args: str, spaces: int = 4) -> str:
    """
    Indent the provided strings by the specified number of spaces

    :param args: The strings to indent
    :param spaces: The number of spaces to indent the strings by
    :return: One string with all the provided strings indented
    """
    output = ""

    for i, arg in enumerate(args):
        output += f"{(' ' * spaces)}{arg}"

        if i != len(args) - 1:
            output += "\n"

    return output


def print_divider(console: Console, text: str, style: str) -> None:
    """
    Print a section divider

    :param console: The console to use for output
    :param content: The text inside the divider
    :param style: The style of the divider
    """
    console.print("\n")
    console.rule(text, style=style)
    console.print("\n")
