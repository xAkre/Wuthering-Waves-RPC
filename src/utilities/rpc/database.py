from sqlite3 import Connection, connect
from json import loads
from src.utilities.rpc import Logger


def get_database(path: str) -> Connection:
    """
    Get a connection to the local Wuthering Waves database
    """
    logger = Logger()

    try:
        return connect(path)
    except Exception as e:
        logger.error(f"An error occurred while connecting to the local database: {e}")


def get_player_region(connection: Connection, kuro_games_uid: str) -> str:
    """
    Get the player's region from the local database

    :param connection: The connection to the local database
    :param kuro_games_uid: The player's Kuro Games UID
    :return: The player's region as a string or "Unknown" if an error occurred
    """
    logger = Logger()

    try:
        sdk_game_data = _get_sdk_level_data(connection, kuro_games_uid)
        return sdk_game_data.get("Region") if sdk_game_data.get("Region") else "Unknown"
    except Exception as e:
        logger.error(f"An error occurred while fetching the user's region: {e}")
        return "Unknown"


def get_player_union_level(connection: Connection, kuro_games_uid: str) -> str:
    """
    Get the player's union level from the local database

    :param connection: The connection to the local database
    :param kuro_games_uid: The player's Kuro Games UID
    :return: The player's union level as a string or "Unknown" if an error occurred
    """
    logger = Logger()

    try:
        sdk_game_data = _get_sdk_level_data(connection, kuro_games_uid)
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


def _get_sdk_level_data(connection: Connection, kuro_games_uid: str) -> dict:
    """
    Get the player's sdk level data from the local database. The level data is
    stored as follows:

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

    Where the first value in the array is the player's Kuro Games UID and the second
    is the player's level data

    :param connection: The connection to the local database
    :param kuro_games_uid: The player's Kuro Games UID
    :return: The player's sdk level data or None if an error occurred or the Kuro Games UID is not found
    """
    logger = Logger()

    try:
        cursor = connection.cursor()
        result = cursor.execute(
            "SELECT * FROM LocalStorage WHERE key = ?", ("SdkLevelData",)
        ).fetchone()
        value = loads(result[1])
        content = value.get("Content")

        for entry in content:
            if entry[0] == kuro_games_uid:
                data = entry[1][0]
                return data

        return None
    except Exception as e:
        logger.error(f"An error occurred while fetching the user's level data: {e}")
        return None
