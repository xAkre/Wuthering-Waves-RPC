from os import getenv, path, listdir, makedirs
from shutil import rmtree
from time import sleep
from json import dumps
from rich.console import Console

console = Console()

DEFAULT_WUWA_INSTALL_LOCATION = r"C:\Wuthering Waves"
DEFAULT_RICH_PRESENCE_INSTALL_LOCATION = (
    rf"{getenv('LOCALAPPDATA')}\Wuthering Waves RPC"
)
LARGE_DIVIDER = r"""
      .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.-.   .-.   
     / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / \ \ / / 
    `-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'   `-`-'      
"""


# Utility functions


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


def print_divider(text: str, style: str) -> None:
    """
    Print a section divider

    :param content: The text inside the divider
    :param style: The style of the divider
    """
    console.print("\n")
    console.rule(text, style=style)
    console.print("\n")


def get_boolean_input(prompt: str) -> bool:
    """
    Get a boolean input from the user

    :param prompt: The prompt to display to the user
    :return: The boolean input from the user
    """
    while True:
        user_input = console.input(prompt).strip().lower()

        if user_input in ["y", "yes"]:
            return True
        elif user_input in ["n", "no"]:
            return False
        else:
            console.print(
                indent("\n", "Please enter 'Y' for yes or 'N' for no.", "\n"),
                style="red",
            )


def fatal_error(message: str) -> None:
    """
    Display a fatal error message and exit the program

    :param message: The fatal error message to display
    """
    print_divider("[red]An Error Occurred[/red]", "red")
    console.print(message, style="red")
    console.show_cursor(False)
    # For some reason using console.input() here doesn't work, so I'm using input() instead
    input(indent("Press Enter to exit..."))
    exit(1)


def get_wuwa_install_location() -> str:
    """
    Get the Wuthering Waves install location from the user

    :return: The Wuthering Waves install location
    """
    while True:
        wuwa_install_location = console.input(
            indent(
                f"Where is Wuthering Waves installed?",
                f'Leave blank for the default location ("{DEFAULT_WUWA_INSTALL_LOCATION}"): ',
            )
        ).strip()

        if wuwa_install_location == "":
            return DEFAULT_WUWA_INSTALL_LOCATION

        if path.exists(wuwa_install_location):
            if not path.isdir(wuwa_install_location):
                console.print(
                    indent(
                        "That path is not a folder. Please enter a valid folder.",
                    ),
                    style="red",
                )
                continue

            return wuwa_install_location

        console.print(
            indent(
                "That path does not exist. Please enter a valid path.",
            ),
            style="red",
        )


def get_database_access_preference() -> bool:
    """
    Get the user's preference for accessing the game's local database

    :return: The user's preference for accessing the game's local database
    """
    return get_boolean_input(
        indent(
            "Would you like the rich presence to get data from the game's local database?",
            "Without this selected, union level and region data will not be displayed.",
            "[red]If you choose yes, I am not responsible for any issues and/or bans that may arise.[/red] (Y/N): ",
        )
    )


def get_rich_presence_install_location() -> str:
    """
    Get the rich presence install location from the user

    :return: The rich presence install location
    """
    while True:
        rich_presence_install_location = console.input(
            indent(
                "Where would you like the rich presence to be installed?",
                f'Leave blank for the default location ("{DEFAULT_RICH_PRESENCE_INSTALL_LOCATION}"): ',
            )
        ).strip()

        if rich_presence_install_location == "":
            rich_presence_install_location = DEFAULT_RICH_PRESENCE_INSTALL_LOCATION

        if path.exists(rich_presence_install_location):
            if not path.isdir(rich_presence_install_location):
                console.print(
                    indent(
                        "That path is a file. Please enter a valid folder.",
                    ),
                    style="red",
                )
                continue

            if len(listdir(rich_presence_install_location)) == 0:
                return rich_presence_install_location

            if get_boolean_input(
                indent(
                    "That folder is not empty. Would you like to clear it? (Y/N): ",
                )
            ):
                try:
                    with console.status(
                        indent("Clearing the folder..."), spinner="dots"
                    ):
                        rmtree(rich_presence_install_location)
                        makedirs(rich_presence_install_location)
                        console.print(indent("Folder cleared."), style="green")

                    return rich_presence_install_location
                except Exception as e:
                    fatal_error(
                        indent(
                            f"An error occurred while clearing the folder: {e}",
                        )
                    )
        else:
            if rich_presence_install_location == DEFAULT_RICH_PRESENCE_INSTALL_LOCATION:
                with console.status(indent("Creating the folder..."), spinner="dots"):
                    makedirs(rich_presence_install_location)
                    console.print(indent("Folder created."), style="green")

                return rich_presence_install_location

            while True:
                if get_boolean_input(
                    indent(
                        "That folder does not exist. Would you like to create it? (Y/N): ",
                    )
                ):
                    try:
                        with console.status(
                            indent("Creating the folder..."), spinner="dots"
                        ):
                            makedirs(rich_presence_install_location)
                            console.print(indent("Folder created."), style="green")

                        return rich_presence_install_location
                    except Exception as e:
                        fatal_error(
                            indent(
                                f"An error occurred while creating the folder: {e}",
                            )
                        )
                else:
                    break

        console.print(
            indent("That path does not exist. Please enter a valid path."),
            style="red",
        )


def get_startup_preference() -> bool:
    """
    Get the user's preference for starting the rich presence on system startup

    :return: The user's preference for starting the rich presence on system startup
    """
    return get_boolean_input(
        indent(
            "Would you like to start the rich presence on system startup? (Y/N): ",
        )
    )


def get_shortcut_preference() -> bool:
    """
    Get the user's preference for creating a desktop shortcut

    :return: The user's preference for creating a desktop shortcut
    """
    return get_boolean_input(
        indent(
            "Would you like to create a desktop shortcut for the rich presence? (Y/N): ",
        )
    )


def get_input(divider_text, callback):
    """
    Get input from the user using the provided callback

    :param divider_text: The text to display in the divider
    :param callback: The callback to call to get the input
    """
    print_divider(divider_text, "white")
    return callback()


# Main setup script


console.print(
    "\n\n",
    LARGE_DIVIDER,
    r"""                                                                                                      
        __        __     _   _               _             
        \ \      / /   _| |_| |__   ___ _ __(_)_ __   __ _ 
         \ \ /\ / / | | | __| '_ \ / _ \ '__| | '_ \ / _` |
          \ V  V /| |_| | |_| | | |  __/ |  | | | | | (_| |
           \_/\_/  \__,_|\__|_| |_|\___|_|  |_|_| |_|\__, |
        __        __                     ____  ____  |___/ 
        \ \      / /_ ___   _____  ___  |  _ \|  _ \ / ___|
         \ \ /\ / / _` \ \ / / _ \/ __| | |_) | |_) | |    
          \ V  V / (_| |\ V /  __/\__ \ |  _ <|  __/| |___ 
           \_/\_/ \__,_| \_/ \___||___/ |_| \_\_|    \____|                                        
    """,
    LARGE_DIVIDER,
    indent(
        "\n\n",
        "[blue]Thank you for choosing to use Wuthering Waves Discord Rich Presence![/blue]",
        "Source code for this program can be found at https://github.com/xAkre/Wuthering-Waves-RPC",
        "A star would be appreciated if you found this program useful!",
        "Please follow the instructions below to set up the program.",
        "[red]Please note that this program is not affiliated with Wuthering Waves or its developers.[/red]",
    ),
    highlight=False,
)

config = {
    "wuwa_install_location": get_input(
        "Wuthering Waves Install Location", get_wuwa_install_location
    ),
    "database_access_preference": get_input(
        "Database Access Preference", get_database_access_preference
    ),
    "rich_presence_install_location": get_input(
        "Rich Presence Install Location", get_rich_presence_install_location
    ),
    "startup_preference": get_input(
        "Launch on Startup Preference", get_startup_preference
    ),
    "shortcut_preference": get_input(
        "Create Shortcut Preference", get_shortcut_preference
    ),
}

print_divider("[green]Options Finalised[/green]", "green")

# Write the config to a file
with console.status("Writing the configuration to a file...", spinner="dots"):
    try:
        with open(
            path.join(config["rich_presence_install_location"], "config.json"), "w"
        ) as f:
            f.write(dumps(config, indent=4))

        console.print(indent("Configuration written to file."), style="green")
    except Exception as e:
        fatal_error(
            indent(f"An error occurred while writing the config to a file: {e}")
        )

print_divider("[green]Setup Completed[/green]", "green")

console.show_cursor(False)

# For some reason using console.input() here doesn't work, so I'm using input() instead
input(indent("Press Enter to exit..."))
exit(0)
