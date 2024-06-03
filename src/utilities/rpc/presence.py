import os
import re
from sqlite3 import Connection
from time import sleep, time

from psutil import NoSuchProcess, Process, pids
from pypresence import Presence as PyPresence

from config import Config
from src.utilities.rpc import (DiscordAssets, Logger, get_database,
                               get_game_version, get_player_region,
                               get_player_union_level)


class Presence:
    logger: Logger
    local_database: Connection | None
    """
    Local Wuthering Waves database connection. The database is a sqlite database and 
    is stored inside the Wuthering Waves game folder at 
    "{Game Folder}/Wuthering Waves Game/Client/Saved/LocalStorage"
    """
    presence: PyPresence

    def __init__(self, config: dict) -> None:
        self.config = config
        self.logger = Logger()

        self.database_directory = os.path.join(
            self.config["wuwa_install_location"],
            "Wuthering Waves Game/Client/Saved/LocalStorage"
        )

        # If the user wants to access the database, get the database connection
        if self.config["database_access_preference"]:
            local_storage = self.get_last_modified_file(self.database_directory)
            self.logger.info(f"Found last modified LocalStorage file: {local_storage}")
            if local_storage:
                database_path = os.path.join(self.database_directory, local_storage)
                self.local_database = get_database(database_path)
            else:
                self.local_database = None
        else:
            self.local_database = None

        self.presence = PyPresence(Config.APPLICATION_ID)

    def get_last_modified_file(self, directory):
        """
        Returns the name of the last modified file with a '.db' extension
        in the specified directory.
        Args:
            directory (str): The directory to search for the last modified file.
        Returns:
            str: The name of the last modified file, or None if no matching file is found.
        """
        pattern = re.compile(r'.*\.db$')
        latest_mtime = -1
        latest_file = None

        self.logger.info(f"Looking for the last modified LocalStorage file in {directory}")
        for file in os.listdir(directory):
            if pattern.match(file):
                file_path = os.path.join(directory, file)
                mtime = os.path.getmtime(file_path)
                if mtime > latest_mtime:
                    latest_mtime = mtime
                    latest_file = file
        return latest_file

    def start(self) -> None:
        """
        Start the RPC
        """
        try:
            self.logger.clear()

            while True:
                try:
                    self.presence.connect()
                    break
                except Exception as e:
                    self.logger.info(
                        f"Discord could not be found installed and running on this machine"
                    )
                    sleep(15)

            while not self.wuwa_process_exists():
                self.logger.info("Wuthering Waves is not running, waiting...")
                sleep(15)

            self.logger.info("Wuthering Waves and Discord are running, starting RPC...")
            self.start_time = time()
            self.presence.update(start=self.start_time)
            self.rpc_loop()
        except Exception as e:
            self.logger.error(f"An uncaught error occured: {e}")

    def rpc_loop(self) -> None:
        """
        Loop to keep the RPC running
        """
        # Loop while Wuthering Waves process is running
        while self.wuwa_process_exists():
            self.update()
            sleep(15)

        if self.config["keep_running_preference"]:
            self.presence.close()
            while not self.wuwa_process_exists():
                self.logger.info(
                    "Wuthering waves has closed, waiting for it to start again..."
                )
                sleep(30)
            self.start()

        self.logger.info("Wuthering Waves has closed, closing RPC...")
        self.presence.close()

    def update(self) -> None:
        """
        Update RPC presence
        """
        self.logger.info("Updating RPC presence...")

        # Check for the last modified database file
        local_storage = self.get_last_modified_file(self.database_directory)
        self.logger.info(f"Found last modified LocalStorage file: {local_storage}")
        if local_storage:
            database_path = os.path.join(self.database_directory, local_storage)
            try:
                self.local_database = get_database(database_path)
            except self.local_database.Error as e:
                self.logger.error(f"Failed to connect to database: {e}")
                self.local_database = None

        # Add a button to the RPC to promote the Rich Presence if the user wants to
        buttons = (
            [
                {
                    "label": "Want a status like this?",
                    "url": "https://github.com/xAkre/Wuthering-Waves-RPC",
                }
            ]
            if self.config["promote_preference"]
            else None
        )

        # Update the RPC with only basic information if the user doesn't want to access the database
        if self.local_database is None:
            self.presence.update(
                start=self.start_time,
                details="Exploring SOL-III",
                large_image=DiscordAssets.LARGE_IMAGE,
                large_text="Wuthering Waves",
                buttons=buttons,
            )
            return

        try:
            region = get_player_region(self.local_database)
            union_level = get_player_union_level(self.local_database)
            game_version = get_game_version(self.local_database)
        except self.local_database.Error as e:
            self.logger.error(f"Failed to retrieve game data: {e}")
            region = "Unknown"
            union_level = "Unknown"
            game_version = "Unknown"

        self.presence.update(
            start=self.start_time,
            details=f"Union Level {union_level}",
            state=f"Region: {region}",
            large_image=DiscordAssets.LARGE_IMAGE,
            large_text="Wuthering Waves",
            small_image=DiscordAssets.SMALL_IMAGE,
            # For some reason quotes are automatically added around the game version, and i don't want that
            small_text=f"Version: {game_version}".replace('"', ""),
            buttons=buttons,
        )

    def wuwa_process_exists(self) -> bool:
        """
        Check whether the Wuthering Waves process is running

        :return: True if the process is running, False otherwise
        """
        for pid in pids():
            try:
                if Process(pid).name() == Config.WUWA_PROCESS_NAME:
                    return True
            except NoSuchProcess:
                pass

        return False
