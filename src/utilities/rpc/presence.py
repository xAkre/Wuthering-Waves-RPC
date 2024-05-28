from os.path import join
from time import time, sleep
from psutil import Process, NoSuchProcess, pids
from sqlite3 import Connection
from pypresence import Presence as PyPresence
from config import Config
from src.utilities.rpc import (
    get_database,
    get_player_region,
    get_player_union_level,
    get_game_version,
    DiscordAssets,
    Logger,
)


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

        # If the user want to access the database, get the database connection
        if self.config["database_access_preference"]:
            database_path = join(
                self.config["wuwa_install_location"],
                "Wuthering Waves Game/Client/Saved/LocalStorage/LocalStorage.db",
            )
            self.local_database = get_database(database_path)
        else:
            self.local_database = None

        self.presence = PyPresence(Config.APPLICATION_ID)

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

        region = get_player_region(self.local_database)
        union_level = get_player_union_level(self.local_database)
        game_version = get_game_version(self.local_database)

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
