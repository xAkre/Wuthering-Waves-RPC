from os import getenv, path
from json import dumps
from rich.console import Console
from src.utilities.cli import (
    indent,
    print_divider,
    fatal_error,
    get_database_access_preference,
    get_input,
    get_rich_presence_install_location,
    get_shortcut_preference,
    get_wuwa_install_location,
    get_startup_preference,
)

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
        console,
        "Wuthering Waves Install Location",
        lambda: get_wuwa_install_location(
            console, DEFAULT_RICH_PRESENCE_INSTALL_LOCATION
        ),
    ),
    "database_access_preference": get_input(
        console,
        "Database Access Preference",
        lambda: get_database_access_preference(console),
    ),
    "rich_presence_install_location": get_input(
        console,
        "Rich Presence Install Location",
        lambda: get_rich_presence_install_location(
            console, DEFAULT_RICH_PRESENCE_INSTALL_LOCATION
        ),
    ),
    "startup_preference": get_input(
        console,
        "Launch on Startup Preference",
        lambda: get_startup_preference(console),
    ),
    "shortcut_preference": get_input(
        console,
        "Create Shortcut Preference",
        lambda: get_shortcut_preference(console),
    ),
}

print_divider(console, "[green]Options Finalised[/green]", "green")

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

print_divider(console, "[green]Setup Completed[/green]", "green")

console.show_cursor(False)

# For some reason using console.input() here doesn't work, so I'm using input() instead
input(indent("Press Enter to exit..."))
exit(0)
