"""
    Utilities.py - Stores the helper functions used in the project.
"""
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone
import json

def clear_screen():
    """
    Clears the terminal screen  for a clean look.
    """
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

def inti_logger(log_message: str,  filename: str = "Program_log.json", level="INFO", time_precision: str = "seconds"):
    """
        Initializes a logger function for the program. Outputs a log entry within a json file.

        :param log_message: the message to log
        :param filename: the name of the json log file
        :param level: the logging level
        :param time_precision: the time precision to use. Defaults to 'seconds'.
    """
    # Get the current date and time in  ISO 8601: YYYY-MM-DDTHH:mm:ss
    now = datetime.now(timezone.utc)

    # controls the time stamp precision in the log entry
    time_precision = time_precision

    # sets time stamp
    time_stamp = now.isoformat(timespec=time_precision)

    # Reads the number of existing entries
    with open(filename, "r", encoding="utf-8") as file:
        entries = json.load(file)

    # Get the highest existing ID (defaults to 0 if the file is empty)
    highest_id = max((entry["id"] for entry in entries), default=0)

    # increase the entry number for the log file
    next_id = highest_id + 1

    # Formats the log entry
    testing_entry = {
        "id": next_id,
        "time": time_stamp,
        "level": level,
        "message": log_message,
    }

    # writes the log message to the file
    with open(filename, "a", encoding="utf-8") as file:
        json.dump(testing_entry, file, indent=4)

def verify_directory(path: str | Path) -> str:
    """
    Verifies that the specified directory exists and if it doesn't it creates one.
    :param path: the directory address to verify
    :return: A log message indicating regardless whether a directory was created.
    """
    log_message: str = "Verifying that the specified directory exists."
    dir_path: Path = Path(path)
    if not dir_path.is_dir():
        log_message = "The specified directory did not exist. Created it."
        dir_path.mkdir(parents=True, exist_ok=True)
    if dir_path.exists():
        log_message = "The specified directory already existed."
    return log_message

def verify_file():

    pass

def psql_connection_test():
    pass

def psql_connection():
    pass

def create_table(psql_conn):
    pass

def insert_members(psql_conn, member):
    pass
