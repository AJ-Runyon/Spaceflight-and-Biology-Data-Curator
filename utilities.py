"""
    Utilities.py - Stores the helper functions used in the project.
"""
import os
import subprocess
from pathlib import Path

def clear_screen():
    """
    Clears the terminal screen  for a clean look.
    """
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

def inti_logger():
    """
        Initializes a logger function for the program.
    """
    # Generates an entry id
    log_entry_id: int = 0

    # Capture compute & reproducibility provenance once at startup
    # Ensure output directory exists and safely across parallel workers
    #TODO ^

    pass

def verify_directory(path: str | Path) -> bool:
    """
    Verifies that the specified directory exists and if it doesn't it creates one.
    :param path: the directory address to verify
    :return: A log message indicating whether or not a directory was created.
    """
    log_message: str = "Verifying that the specified directory exists."
    dir_path: Path = Path(path)
    if not dir_path.is_dir():
        log_message = "The specified directory did not exist. Creating it."
        dir_path.mkdir(parents=True, exist_ok=True)
    if dir_path.exists():
        log_message = "The specified directory already exists."
    return log_message

def psql_connection_test():
    pass

def psql_connection():
    pass

def create_table(psql_conn):
    pass

def insert_members(psql_conn, member):
    pass
