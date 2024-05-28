from os import path, listdir, makedirs
from shutil import rmtree
from rich.console import Console
from src.utilities.cli import indent, print_divider, fatal_error


def get_boolean_input(console: Console, prompt: str) -> bool:
    """
    Get a boolean input from the user

    :param console: The console to use for input and output
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


def get_wuwa_install_location(console: Console, default_location: str) -> str:
    """
    Get the Wuthering Waves install location from the user

    :param console: The console to use for input and output
    :param default_location: The default install location
    :return: The Wuthering Waves install location
    """
    while True:
        wuwa_install_location = console.input(
            indent(
                f"Where is Wuthering Waves installed?",
                f'Leave blank for the default location ("{default_location}"): ',
            )
        ).strip()

        if wuwa_install_location == "":
            return default_location

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


def get_database_access_preference(console: Console) -> bool:
    """
    Get the user's preference for accessing the game's local database

    :param console: The console to use for input and output
    :return: The user's preference for accessing the game's local database
    """
    return get_boolean_input(
        console,
        indent(
            "Would you like the rich presence to get data from the game's local database?",
            "Without this selected, union level and region data will not be displayed.",
            "[red]If you choose yes, I am not responsible for any issues and/or bans that may arise.[/red] (Y/N): ",
        ),
    )


def get_rich_presence_install_location(console: Console, default_location: str) -> str:
    """
    Get the rich presence install location from the user

    :param console: The console to use for input and output
    :param default_location: The default install location
    :return: The rich presence install location
    """
    while True:
        rich_presence_install_location = console.input(
            indent(
                "Where would you like the rich presence to be installed?",
                f'Leave blank for the default location ("{default_location}"): ',
            )
        ).strip()

        if rich_presence_install_location == "":
            rich_presence_install_location = default_location

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
                console,
                indent(
                    "That folder is not empty. Would you like to clear it? (Y/N): ",
                ),
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
                        console,
                        indent(
                            f"An error occurred while clearing the folder:",
                        ),
                        e,
                    )
        else:
            if rich_presence_install_location == default_location:
                with console.status(indent("Creating the folder..."), spinner="dots"):
                    makedirs(rich_presence_install_location)
                    console.print(indent("Folder created."), style="green")

                return rich_presence_install_location

            while True:
                if get_boolean_input(
                    console,
                    indent(
                        "That folder does not exist. Would you like to create it? (Y/N): ",
                    ),
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
                            console,
                            indent(
                                f"An error occurred while creating the folder",
                            ),
                            e,
                        )
                else:
                    break


def get_startup_preference(console: Console) -> bool:
    """
    Get the user's preference for starting the rich presence on system startup

    :param console: The console to use for input and output
    :return: The user's preference for starting the rich presence on system startup
    """
    return get_boolean_input(
        console,
        indent(
            "Would you like to start the rich presence on system startup? (Y/N): ",
        ),
    )


def get_shortcut_preference(console: Console) -> bool:
    """
    Get the user's preference for creating a desktop shortcut

    :param console: The console to use for input and output
    :return: The user's preference for creating a desktop shortcut
    """
    return get_boolean_input(
        console,
        indent(
            "Would you like to create a desktop shortcut for the rich presence? (Y/N): ",
        ),
    )


def get_promote_preference(console: Console) -> bool:
    """
    Get the user's preference for promoting the rich presence on Discord

    :param console: The console to use for input and output
    :return: The user's preference for promoting the rich presence on Discord
    """
    return get_boolean_input(
        console,
        indent(
            "Would you like to help promote the rich presence on Discord?",
            "This will add a button to the rich presence that links to the GitHub repository. (Y/N): ",
        ),
    )


def get_keep_running_preference(console: Console) -> bool:
    """
    Get the user's preference for keeping the rich presence running after Wuthering Waves is closed

    :param console: The console to use for input and output
    :return: The user's preference for keeping the rich presence running in the background
    """
    return get_boolean_input(
        console,
        indent(
            "Would you like to keep the rich presence running in the background?",
            "This will keep the rich presence running after Wuthering Waves is closed,",
            "and it will wait for the next launch (Y/N): ",
        ),
    )


def get_input(console, divider_text, callback) -> any:
    """
    Get input from the user using the provided callback

    :param console: The console to use for displaying the divider
    :param divider_text: The text to display in the divider
    :param callback: The callback to call to get the input
    """
    print_divider(console, divider_text, "white")
    return callback()
