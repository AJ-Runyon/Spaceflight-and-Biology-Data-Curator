import os
import subprocess
import re
import json
import requests
import sys
import signal
from pathlib import Path
from urllib.parse import unquote
from db import verify_connection, get_connection_info


# Sets the location of the raw, transformed, and loaded data
RAW_DIR = Path("data/raw_missions")
CLEAN_DIR = Path("data/clean_missions")

# Sets the files for raw and clean mission index JSONs
INDEX_FILE = RAW_DIR / "all_missions_index.json"
CLEAN_INDEX_FILE = CLEAN_DIR / "clean_missions_index.json"

# Sets the API url for OSDR mission data
MISSIONS_INDEX_URL = "https://osdr.nasa.gov/geode-py/ws/api/missions"
# Sets the delay for API requests
# DELAY: float = 0.3


# For politeness
HEADERS = {
    "User-Agent": "Spaceflight-Biology-Data-Curator 0.0.1 (GitHub: AJ-Runyon)"
}

#TODO add logging function

def initialize_pipeline():
    """Starts up the ETL pipeline."""
    print("Starting OSDR ETL pipeline..")
    # TODO create and wire in extraction module.
    mission_api_urls = extract_master_list()
    print(mission_api_urls)
    # TODO create and wire in transom module.
    clean_file_path = transform_mission_index(mission_api_urls)
    print(clean_file_path)
    # TODO create and wire in the load module.

# Clears the terminal for a clean look
def clear_screen():
    """
    Clears the terminal screen.
    """
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

def extract_master_list(index_url: str = MISSIONS_INDEX_URL, output_path: Path = INDEX_FILE) -> Path:
    """
    Extracts a json of all the missions from OSDR with the API urls and their mission titles as messy data.

    :param index_url: The API URL for mission urls
    :param output_path: The path to save the json
    :return: The path of the saved the json
    """
    # Ensures the folder exists for the output.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Sends a GET request to the sever
    response = requests.get(index_url, headers=HEADERS, timeout=20)
    # For when the server returns a failure status code
    response.raise_for_status()
    # Stores the data as a json
    index_data = response.json()
    # print(index_data)
    # Attach the keys to the URL where the keys are the mission titles (uncleaned)
    missions_map = {}
    for entry in index_data.get("data", []):
        mission_url = entry.get("mission")
        if mission_url:
            # Extracts the mission title from the end of the URL (e.g., "STS-135" or "SpaceX-12")
            mission_title = mission_url.rstrip("/").split("/")[-1]
            missions_map[mission_title] = mission_url

    # Creates the output file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(missions_map, f, indent=2)
    return output_path

def transform_mission_index(input_path: Path = INDEX_FILE, output_path: Path = CLEAN_INDEX_FILE) -> Path:
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
                #  Checks the connection before running network or disk operations
                if not verify_connection():
                    print("Aborting program: database is unreachable.")
                    sys.exit(1)
                # Starts up the pipeline
                initialize_pipeline()
            elif user_input == "2":
                print("Database querying not implemented yet.")
            elif user_input == "3":
                print("Exiting...")
                running = False
                sys.exit(0)
            else:
                print("Invalid input. Please enter '1' or '2' or '3'.")

    except (KeyboardInterrupt, EOFError):
        clear_screen()
        print("Exiting...")



if __name__ == "__main__":
    main()