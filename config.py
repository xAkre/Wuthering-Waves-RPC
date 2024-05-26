from os.path import join
from os import getenv


class Config:
    MAIN_EXECUTABLE_NAME = "Wuthering Waves RPC.exe"
    APPLICATION_ID = "1243855663210303488"
    WUWA_PROCESS_NAME = "Wuthering Waves.exe"
    LOCAL_DATABASE_PATH = "C:\\Wuthering Waves\\Wuthering Waves Game\\Client\\Saved\\LocalStorage\\LocalStorage.db"
    """
    This is the default path to the database. I would like to make this configurable somehow
    """
    LOCAL_APP_DATA_PATH = join(getenv("LOCALAPPDATA"), "Wuthering Waves RPC")
