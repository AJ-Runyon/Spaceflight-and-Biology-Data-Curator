import re
import json
import requests
import sys
from pathlib import Path
from urllib.parse import unquote
from db import verify_connection
from utilities import clear_screen
import config
from pipeline import extract_master_list

#TODO add logging function

def initialize_pipeline():
    """Starts up the ETL pipeline."""
    clear_screen()
    print("Starting ETL pipeline..")
    mission_api_urls = extract_master_list()
    # TODO create and wire in transform module.
    clean_file_path = transform_mission_index(mission_api_urls)
    print(clean_file_path)
    # TODO create and wire in the load module.


def transform_mission_index(input_path: Path = config.INDEX_FILE, output_path: Path = config.CLEAN_INDEX_FILE) -> Path:
    """
    Reads the raw mission index JSON, decodes URL-encoded characters,
    normalizes whitespace in mission titles, and saves the cleaned JSON.

    :param input_path: The path to the raw mission index JSON
    :param output_path: The path to save the cleaned JSON
    :return: The path of the saved the cleaned JSON
    """
    # Ensure the clean directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Read the raw JSON data from the file
    with open(input_path, "r", encoding="utf-8") as f:
        raw_missions = json.load(f)

    cleaned_missions = {}
    for raw_title, url in raw_missions.items():
        # Decodes the URL encoding on the string key
        decoded = unquote(raw_title)
        # Replaces any underscores or multiple spaces with a single clean space
        cleaned_title = re.sub(r"[_\s]+", " ", decoded).strip()
        # sets the key name
        cleaned_missions[cleaned_title] = url

    # Save the cleaned dictionary to the clean index file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_missions, f, indent=2)

    return output_path

def main():
    running = True

    try:
        while running:
            print(
                "What would you like to do?:\n\n  1. Initialize the ETL Pipeline\n  2. Query the Database\n  3. exit\n\n")
            user_input = input("Enter your choice: >").strip().lower()
            if user_input == "1":
                clear_screen()
                #  Checks the connection before running network or disk operations
                if not verify_connection():
                    print("Aborting program: database is unreachable.")
                    sys.exit(1)
                # Starts up the pipeline
                initialize_pipeline()
            elif user_input == "2":
                clear_screen()
                print("Database querying not implemented yet.")
            elif user_input == "3":
                clear_screen()
                print("Exiting...")
                running = False
                sys.exit(0)
            else:
                clear_screen()
                print("Invalid input. Please enter '1' or '2' or '3'.")

    except (KeyboardInterrupt, EOFError):
        clear_screen()
        print("Exiting...")



if __name__ == "__main__":
    main()