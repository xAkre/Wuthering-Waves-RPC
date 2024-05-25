from config import Config
from sqlite3 import Connection, connect
from json import loads
from src.logger import Logger


def get_database() -> Connection:
    """
    Get a connection to the local Wuthering Waves database
    """
    logger = Logger()

    try:
        return connect(Config.LOCAL_DATABASE_PATH)
    except Exception as e:
        logger.error(f"An error occurred while connecting to the local database: {e}")


def get_player_region(connection: Connection) -> str:
    """
    Get the player's region from the local database

    :param connection: The connection to the local database
    :return: The player's region as a string or "Unknown" if an error occurred
    """
    logger = Logger()

    try:
        cursor = connection.cursor()
        result = cursor.execute(
            "SELECT * FROM LocalStorage WHERE key = ?", ("SdkLevelData",)
        ).fetchone()
        value = loads(result[1])
        content = value.get("Content")
        region = content[len(content) - 1][1][0].get("Region")
        return region if region else "Unknown"
    except Exception as e:
        logger.error(f"An error occurred while fetching the user's region: {e}")
        return "Unknown"


def get_player_union_level(connection: Connection) -> str:
    """
    Get the player's union level from the local database

    :param connection: The connection to the local database
    :return: The player's union level as a string or "Unknown" if an error occurred
    """
    logger = Logger()

    try:
        sdk_game_data = _get_sdk_level_data(connection)
        return sdk_game_data.get("Level") if sdk_game_data.get("Level") else "Unknown"
    except Exception as e:
        logger.error(f"An error occurred while fetching the user's union level: {e}")
        return "Unknown"


def get_game_version(connection: Connection) -> str:
    """
    Get the game version from the local database

    :param connection: The connection to the local database
    :return: The game version as a string or "Unknown" if an error occurred
    """
    logger = Logger()

    try:
        cursor = connection.cursor()
        result = cursor.execute(
            "SELECT * FROM LocalStorage WHERE key = ?", ("PatchVersion",)
        ).fetchone()
        version = result[1]
        return version if version else "Unknown"
    except Exception as e:
        logger.error(f"An error occurred while fetching the game version: {e}")
        return "Unknown"


def _get_sdk_level_data(connection: Connection) -> dict:
    """
    Get the player's sdk level data from the local database. The level data seems
    to be stored as follows:

    {
        "___MetaType___":"___Map___",
        "Content": [
            ["535414272", [
                {
                    "Region": "Europe",
                    "Level": 4
                }
            ]],
            ["536678859", [
                {
                    "Region": "Europe",
                    "Level": 3
                }
            ]],
            ["536789175", [
                {
                    "Region": "Europe",
                    "Level": 22
                }]
            ]
        ]
    }

    Can't say i know why there are multiple entries here, or whether the content
    key would be be a single array when there is only one entry. I'm just going to
    assume that the data is stored as an array of arrays, and that the last entry
    is the most recent data, as that seems to be the case for me

    :param connection: The connection to the local database
    :return: The player's sdk level data or None if an error occurred
    """
    logger = Logger()

    try:
        cursor = connection.cursor()
        result = cursor.execute(
            "SELECT * FROM LocalStorage WHERE key = ?", ("SdkLevelData",)
        ).fetchone()
        value = loads(result[1])
        content = value.get("Content")
        data = content[len(content) - 1][1][0]
        return data
    except Exception as e:
        logger.error(f"An error occurred while fetching the user's level data: {e}")
        return None
