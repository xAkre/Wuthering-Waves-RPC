from os import getenv, makedirs
from os.path import join
from datetime import datetime
from config import Config


class Logger:
    """
    Handles application logging
    """

    log_file_path: str

    def __init__(
        self,
        log_folder: str = Config.LOCAL_APP_DATA_PATH,
    ):
        """
        Create a new logger instance

        :param log_file_path: The path to the log file
        """
        makedirs(log_folder, exist_ok=True)
        self.log_folder = log_folder
        self.log_file_path = join(log_folder, "log.txt")

    def error(self, message: str):
        """
        Log an error message
        """
        self.write("ERROR", message)
        print(f"ERROR: {message}")

    def warning(self, message: str):
        """
        Log a warning message
        """
        self.write("WARNING", message)
        print(f"WARNING: {message}")

    def info(self, message: str):
        """
        Log an info message
        """
        self.write("INFO", message)
        print(f"INFO: {message}")

    def write(self, type: str, message: str):
        """
        Write a message to the log file
        """
        with open(self.log_file_path, "a") as log_file:
            log_file.write(f"[{type}] [{datetime.now()}] {message}\n")

    def clear(self):
        """
        Clear the log file of all content
        """
        open(self.log_file_path, "w").close()
