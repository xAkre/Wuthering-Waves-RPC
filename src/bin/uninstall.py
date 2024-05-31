import sys
import subprocess
import os
import tempfile
from shutil import rmtree
from win32com.client import Dispatch
from os.path import exists, join, abspath, dirname, normcase, normpath, expanduser
from json import loads
from rich.console import Console
from src.utilities.cli import fatal_error, indent, print_divider
from config import Config

console = Console()

config_path = join(abspath(dirname(sys.executable)), "config/config.json")

if not exists(config_path):
    fatal_error(
        console,
        indent(f"Config file does not exist. It should be located at {config_path}"),
    )

with open(config_path, "r") as f:
    config = loads(f.read())
    if normpath(normcase(config["rich_presence_install_location"])) != normpath(
        normcase(abspath(dirname(sys.executable)))
    ):
        fatal_error(
            console,
            indent(
                "The rich presence install location in the config file does not match the actual install location. Please update the config file, or setup the RPC again"
            ),
        )


def remove_startup_task(console: Console):
    """
    Remove the startup task that was created during installation

    :param console: The console to use for input and output
    """
    try:
        with console.status(indent("Removing the startup task..."), spinner="dots"):
            delete_task_command = [
                "schtasks",
                "/delete",
                "/tn",
                "Wuthering Waves RPC",
                "/f",
            ]
            subprocess.run(
                delete_task_command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            console.print(indent("Startup task removed."), style="green")
    except:
        console.print(
            indent(
                "Failed to remove the startup task.",
                "Please remove it manually via the Task Manager application",
            ),
            style="red",
        )


def get_shortcut_target_path(shortcut_path: str) -> str:
    """
    Get the target path of a Windows shortcut.

    :param shortcut_path: The path to the shortcut (.lnk) file.
    :return: The target path that the shortcut points to.
    """
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    return shortcut.TargetPath


def find_shortcuts_pointing_to_exe(exe_path: str) -> list[str]:
    """
    Find all shortcuts that point to a specified executable.
    This function searches the user's desktop and the Start Menu.

    :param executable_path: The path to the executable
    :return: A list of shortcut paths that point to the specified executable
    """
    paths_to_search = [
        join(
            os.getenv("APPDATA"),
            "Microsoft/Windows/Start Menu/Programs",
        ),
        expanduser("~/Desktop"),
    ]

    shortcuts_pointing_to_exe = []

    for path in paths_to_search:
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".lnk"):
                    shortcut_path = join(root, file)
                    try:
                        if get_shortcut_target_path(shortcut_path) == exe_path:
                            shortcuts_pointing_to_exe.append(shortcut_path)
                    except Exception as e:
                        console.print(
                            indent(f"Error reading shortcut {shortcut_path}: {e}"),
                            style="yellow",
                        )

    return shortcuts_pointing_to_exe


def remove_shortcuts(console: Console, exe_path: str):
    """
    Remove shortcuts that point to a specified executable

    :param console: The console to use for input and output
    :param exe_path: The path to the executable
    """
    shortcuts = find_shortcuts_pointing_to_exe(exe_path)
    if not shortcuts:
        console.print(
            indent("No shortcuts pointing to the executable were found."),
            style="yellow",
        )
        return

    console.print(
        indent(f"Found {len(shortcuts)} shortcuts pointing to the executable:"),
        style="yellow",
    )
    for shortcut in shortcuts:
        console.print(indent(shortcut), style="yellow")

    for shortcut in shortcuts:
        try:
            os.remove(shortcut)
            console.print(indent(f"Removed shortcut {shortcut}"), style="green")
        except Exception as e:
            console.print(
                indent(f"Failed to remove shortcut {shortcut}: {e}"), style="red"
            )


def delete_program_folder(console: Console):
    """
    Delete the program folder

    :param console: The console to use for input and output
    """
    try:
        for root, _, files in os.walk(abspath(dirname(sys.executable))):
            for file in files:
                if normcase(normpath(join(root, file))) == normcase(
                    normpath(sys.executable)
                ):
                    continue
                with console.status(indent(f"Removing {file}..."), spinner="dots"):
                    os.remove(join(root, file))
                    console.print(indent(f"File {file} removed"), style="green")

        uninstall_exe_path = abspath(sys.executable)

        console.input(indent("Press Enter to finalize the uninstallation"))

        batch_script = f"""
        @echo off
        timeout 2
        rmdir /s /q "{dirname(uninstall_exe_path)}"
        if errorlevel 1 (
            echo "Failed to remove the program folder ({dirname(uninstall_exe_path)}). Please remove it manually. You may now close this window"
        ) else (
            echo "{dirname(uninstall_exe_path)} was removed. Uninstallation complete. You may now close this window"
        )
        """

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".bat", mode="w"
        ) as temp_script:
            temp_script.write(batch_script)
            temp_script_path = temp_script.name

        subprocess.Popen(["cmd", "/k", "start", "/wait", temp_script_path])
        sys.exit(0)
    except Exception as e:
        fatal_error(
            console,
            indent(
                "Failed to remove the program folder",
            ),
            e,
        )


print_divider(console, "Wuthering Waves Rich Presence Uninstaller", "white")
console.input(indent("Press Enter to uninstall the Wuthering Waves Rich Presence..."))

try:
    if config["startup_preference"]:
        print_divider(
            console,
            "[green]Removing Wuthering Waves RPC from Windows Task Scheduler[/green]",
            "green",
        )
        remove_startup_task(console)

    print_divider(
        console,
        "[green]Removing shortcuts pointing to the main executable[/green]",
        "green",
    )
    console.print(
        indent(
            "Note that this only searches for shortcuts on your Desktop and in the Start Menu.",
            "If you have shortcuts in other locations, you will need to remove them manually",
        ),
        style="yellow",
    )
    exe_path = join(abspath(dirname(sys.executable)), Config.MAIN_EXECUTABLE_NAME)
    remove_shortcuts(console, exe_path)
    print_divider(
        console,
        "[green]Removing shortcuts pointing to the uninstaller[/green]",
        "green",
    )
    uninstall_exe_path = abspath(sys.executable)
    remove_shortcuts(console, uninstall_exe_path)
    print_divider(console, "[green]Removing the program folder[/green]", "green")
    delete_program_folder(console)
    print_divider(console, "[green]Uninstallation complete[/green]", "green")
    input(indent("Press Enter to exit..."))
except Exception as e:
    fatal_error(
        console,
        indent(
            "An error occurred during uninstallation",
        ),
        e,
    )
