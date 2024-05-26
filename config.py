from os.path import join
from os import getenv


class Config:
    APPLICATION_ID = "1243855663210303488"
    WUWA_PROCESS_NAME = "Wuthering Waves.exe"
    LOCAL_DATABASE_PATH = "C:\\Wuthering Waves\\Wuthering Waves Game\\Client\\Saved\\LocalStorage\\LocalStorage.db"
    LOCAL_APP_DATA_PATH = join(getenv("LOCALAPPDATA"), "WutheringWavesRPC")
    """
    This is the default path to the database. I would like to make this configurable somehow
    """
