from time import time, sleep
from psutil import Process, NoSuchProcess, pids
from sqlite3 import Connection
from pypresence import Presence as PyPresence
from config import Config
from src.database import (
    get_database,
    get_player_region,
    get_player_union_level,
    get_game_version,
)
from src.logger import Logger


class Presence:
    logger: Logger
    local_database: Connection
    """
    Local Wuthering Waves database connection. The database is a sqlite database and 
    is stored inside the Wuthering Waves game folder at 
    "{Game Folder}/Wuthering Waves Game/Client/Saved/LocalStorage"
    """
    presence: PyPresence

    def __init__(self) -> None:
        self.logger = Logger()
        self.local_database = get_database()
        self.presence = PyPresence(Config.APPLICATION_ID)

    def start(self) -> None:
        """
        Start the RPC
        """
        try:
            self.logger.clear()

            while not self.wuwa_process_exists():
                self.logger.info("Wuthering Waves is not running, waiting...")
                sleep(15)

            self.logger.info("Wuthering Waves is running, starting RPC...")
            self.start = time()
            self.presence.connect()
            self.presence.update(start=self.start)
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

        self.logger.info("Wuthering Waves has closed, closing RPC...")
        self.presence.close()

    def update(self) -> None:
        """
        Update RPC presence
        """
        self.logger.info("Updating RPC presence...")
        region = get_player_region(self.local_database)
        union_level = get_player_union_level(self.local_database)
        game_version = get_game_version(self.local_database)

        self.presence.update(
            start=self.start,
            details=f"Union Level {union_level}",
            state=f"Region: {region}",
            large_image=Config.Assets.LARGE_IMAGE,
            large_text="Wuthering Waves",
            small_image=Config.Assets.SMALL_IMAGE,
            # For some reason quotes are automatically added around the game version, and i don't want that
            small_text=f"Version: {game_version}".replace('"', ""),
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
