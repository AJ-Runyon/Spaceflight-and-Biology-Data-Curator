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

def inti_logger(log_message: str, filename: str | Path = "Program_log.json", level: str = "INFO", time_precision: str = "seconds",
):
    """
    Appends a structured log entry to a JSON file, creating the file if it does not exist.

    :param log_message: the message to log
    :param filename: the name or path of the json log file
    :param level: the logging level
    :param time_precision: the time precision to use. Defaults to 'seconds'.
    """
    file_path = Path(filename)

    # Get the current date and time in UTC ISO 8601 format
    now = datetime.now(timezone.utc)
    time_stamp = now.isoformat(timespec=time_precision)

    # Load existing entries if the file exists and contains valid JSON
    entries = []
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                loaded_data = json.load(file)
                if isinstance(loaded_data, list):
                    entries = loaded_data
        except json.JSONDecodeError:
            entries = []

    # Get the highest existing ID (defaults to 0 if the file is empty)
    highest_id = max((entry.get("id", 0) for entry in entries), default=0)

    # Increases the id value for later entries
    next_id = highest_id + 1

    # Format and append the new log entry
    new_entry = {
        "id": next_id,
        "time": time_stamp,
        "level": level,
        "message": log_message,
    }
    # Adds the log to the list
    entries.append(new_entry)

    # Ensure parent directories exist and write the full updated list
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Writes the entries to the log file
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(entries, file, indent=4, ensure_ascii=False)

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
